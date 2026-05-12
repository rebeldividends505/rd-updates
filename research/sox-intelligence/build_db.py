"""
SOX Intelligence Database build job.

Pulls 24mo of weekly prices, earnings, ratios, and FRED macro series for every
SOX component plus SOXL/SOXX/QQQ/SPY benchmarks. Computes SOXL correlation and
leading-indicator analysis.

Run: python3 build_db.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


_load_env_file(Path(__file__).resolve().parents[2] / ".env")

FMP = os.environ["FMP_API_KEY"]
POLYGON = os.environ["POLYGON_API_KEY"]
FRED_KEY = os.environ["FRED_API_KEY"]

BASE = Path("/Users/rebeldividends/rd-updates-site/research/sox-intelligence")
BASE.mkdir(parents=True, exist_ok=True)

LOG_PATH = BASE / "build.log"


def log(msg: str) -> None:
    stamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line, flush=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


def get_json(url: str, timeout: int = 20, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return r.json(), 200
            if r.status_code in (429, 502, 503, 504) and attempt < retries:
                time.sleep(2 + attempt * 2)
                continue
            return None, r.status_code
        except requests.RequestException as e:
            if attempt < retries:
                time.sleep(2)
                continue
            log(f"  request error: {e}")
            return None, -1
    return None, -1


# ──────────────────────────────────────────────────────────────────────
# STEP 1: SOX components
# ──────────────────────────────────────────────────────────────────────
def fetch_sox_components() -> list[str]:
    log("STEP 1: SOX components")
    data, status = get_json(
        f"https://financialmodelingprep.com/api/v3/index-constituent/^SOX?apikey={FMP}"
    )
    if status == 200 and isinstance(data, list) and data:
        log(f"  FMP returned {len(data)} components")
        with open(BASE / "sox_components.json", "w") as f:
            json.dump(data, f, indent=2)
        return [c["symbol"] for c in data if c.get("symbol")]

    log(f"  FMP failed ({status}); using fallback list")
    tickers = [
        "NVDA", "AMD", "AVGO", "TXN", "QCOM", "INTC", "MU", "AMAT", "LRCX", "KLAC",
        "ADI", "MRVL", "NXPI", "ON", "MCHP", "TSM", "ARM", "SMCI", "MPWR", "ENTG",
        "SWKS", "QRVO", "TER", "COHU", "WOLF", "ACLS", "SLAB", "CRUS", "RMBS", "SITM",
    ]
    with open(BASE / "sox_components.json", "w") as f:
        json.dump([{"symbol": t, "source": "fallback"} for t in tickers], f, indent=2)
    return tickers


# ──────────────────────────────────────────────────────────────────────
# STEP 2: weekly prices via Polygon
# ──────────────────────────────────────────────────────────────────────
def fetch_weekly_prices(tickers: list[str], start: str, end: str) -> None:
    log(f"STEP 2: weekly prices {start} → {end}")
    prices_dir = BASE / "weekly_prices"
    prices_dir.mkdir(exist_ok=True)

    for t in tickers:
        out = prices_dir / f"{t}.json"
        url = (
            f"https://api.polygon.io/v2/aggs/ticker/{t}/range/1/week/{start}/{end}"
            f"?apiKey={POLYGON}&limit=200&adjusted=true"
        )
        data, status = get_json(url)
        if status == 200 and data and data.get("results"):
            with open(out, "w") as f:
                json.dump(data, f)
            log(f"  ✓ {t}: {len(data['results'])} weeks")
        else:
            log(f"  ✗ {t}: status={status}")
        time.sleep(0.2)


# ──────────────────────────────────────────────────────────────────────
# STEP 3: earnings + ratios via FMP
# ──────────────────────────────────────────────────────────────────────
def fetch_earnings(tickers: list[str]) -> None:
    log("STEP 3: earnings + ratios")
    earnings_dir = BASE / "earnings"
    earnings_dir.mkdir(exist_ok=True)

    endpoints = {
        "surprises": "earnings-surprises/{t}?apikey={k}&limit=12",
        "estimates": "analyst-estimates/{t}?apikey={k}&limit=8",
        "calendar":  "earning_calendar?symbol={t}&apikey={k}",
        "ratios":    "ratios/{t}?apikey={k}&limit=8",
    }

    for t in tickers:
        bundle: dict = {}
        for key, path in endpoints.items():
            url = "https://financialmodelingprep.com/api/v3/" + path.format(t=t, k=FMP)
            data, status = get_json(url, timeout=15)
            if status == 200 and data is not None:
                bundle[key] = data[:5] if key == "calendar" and isinstance(data, list) else data
            time.sleep(0.15)

        with open(earnings_dir / f"{t}.json", "w") as f:
            json.dump(bundle, f, indent=2)

        got = ",".join(k for k in bundle if bundle[k])
        log(f"  ✓ {t}: {got or 'no data'}")


# ──────────────────────────────────────────────────────────────────────
# STEP 4: FRED macro
# ──────────────────────────────────────────────────────────────────────
def fetch_macro(start: str) -> None:
    log("STEP 4: FRED macro")
    import fredapi
    fred = fredapi.Fred(api_key=FRED_KEY)
    macro_dir = BASE / "macro"
    macro_dir.mkdir(exist_ok=True)

    series = {
        "UMCSENT": "consumer_sentiment",
        "DRCCLACBS": "credit_card_delinquency",
        "PSAVERT": "personal_savings_rate",
        "PAYEMS": "nonfarm_payrolls",
        "PCEPILFE": "core_pce_inflation",
        "USREC": "recession_indicator",
        "DFF": "fed_funds_rate",
        "T10Y2Y": "yield_curve_10y_2y",
        "UNRATE": "unemployment_rate",
        "INDPRO": "industrial_production",
        "RSAFS": "retail_sales",            # RETAILSMSA is discontinued; RSAFS is current
        "TOTALSL": "consumer_credit",
        "CPIAUCSL": "cpi_all_items",
        "DCOILWTICO": "wti_crude_oil_price",
        "DEXJPUS": "usd_jpy_exchange",
        "BAMLH0A0HYM2": "high_yield_spread",
        "EFFR": "effective_fed_funds_rate",
    }

    out: dict = {}
    full_series: dict = {}
    for sid, name in series.items():
        try:
            s = fred.get_series(sid, observation_start=start).dropna()
            if len(s) == 0:
                log(f"  ✗ {name}: empty")
                continue
            latest = float(s.iloc[-1])
            six = float(s.iloc[-6]) if len(s) > 6 else None
            twelve = float(s.iloc[-12]) if len(s) > 12 else None
            trend_3m = "rising" if len(s) > 3 and latest > float(s.iloc[-3]) else "falling"
            out[name] = {
                "series_id": sid,
                "latest": latest,
                "latest_date": str(s.index[-1].date()),
                "6m_ago": six,
                "12m_ago": twelve,
                "trend_3m": trend_3m,
                "data_points": int(len(s)),
            }
            full_series[name] = {str(d.date()): float(v) for d, v in s.items()}
            log(f"  ✓ {name}: {latest:.4f} ({trend_3m})")
        except Exception as e:
            log(f"  ✗ {sid}: {e}")

    with open(macro_dir / "macro_summary.json", "w") as f:
        json.dump(out, f, indent=2)
    with open(macro_dir / "macro_series_full.json", "w") as f:
        json.dump(full_series, f)


# ──────────────────────────────────────────────────────────────────────
# STEP 5: SOXL signal analysis
# ──────────────────────────────────────────────────────────────────────
def load_weekly(t: str) -> pd.DataFrame | None:
    p = BASE / "weekly_prices" / f"{t}.json"
    if not p.exists():
        return None
    with open(p) as f:
        raw = json.load(f)
    if not raw.get("results"):
        return None
    df = pd.DataFrame(raw["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("date", inplace=True)
    df["return_1w"] = df["c"].pct_change()
    return df


def analyze(tickers: list[str]) -> None:
    log("STEP 5: SOXL signal analysis")
    analysis_dir = BASE / "analysis"
    analysis_dir.mkdir(exist_ok=True)

    soxl = load_weekly("SOXL")
    if soxl is None:
        log("  ✗ SOXL data missing — aborting analysis")
        return

    # Same-week correlations
    correlations: dict[str, float] = {}
    for t in tickers:
        df = load_weekly(t)
        if df is None:
            continue
        a = pd.concat([soxl["return_1w"], df["return_1w"]], axis=1, join="inner").dropna()
        a.columns = ["soxl", t]
        if len(a) < 10:
            continue
        correlations[t] = round(float(a["soxl"].corr(a[t])), 3)

    correlations_sorted = dict(sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True))
    log("  top same-week correlations:")
    for t, c in list(correlations_sorted.items())[:10]:
        log(f"    {t}: {c:+.3f}")

    # Leading indicator check: does last-week's component return predict this-week's SOXL?
    leading: dict[str, dict] = {}
    for t in tickers:
        df = load_weekly(t)
        if df is None:
            continue
        # df shifted +1 = this week's SOXL paired with last week's component return
        a = pd.concat(
            [soxl["return_1w"], df["return_1w"].shift(1)], axis=1, join="inner"
        ).dropna()
        a.columns = ["soxl_this", f"{t}_prev"]
        if len(a) < 10:
            continue
        lag = round(float(a["soxl_this"].corr(a[f"{t}_prev"])), 3)
        same = correlations.get(t, 0.0)
        leading[t] = {
            "same_week_corr": same,
            "lead_1wk_corr": lag,
            "leads_soxl": abs(lag) > abs(same) and abs(lag) > 0.1,
        }

    # SOXL momentum auto-prediction
    soxl_momentum: dict[str, float] = {}
    for period in [2, 4, 8, 13, 26]:
        soxl[f"mom_{period}w"] = soxl["c"].pct_change(period)
        a = pd.concat(
            [soxl[f"mom_{period}w"], soxl["return_1w"].shift(-1)], axis=1, join="inner"
        ).dropna()
        if len(a) < 10:
            continue
        pred = round(float(a.iloc[:, 0].corr(a.iloc[:, 1])), 3)
        soxl_momentum[f"{period}w_momentum_predicts_next"] = pred
        log(f"  SOXL {period}w momentum → next-week corr: {pred:+.3f}")

    # Macro context
    macro_summary = {}
    p = BASE / "macro" / "macro_summary.json"
    if p.exists():
        with open(p) as f:
            macro_summary = json.load(f)

    # Findings
    findings: list[str] = []
    top = list(correlations_sorted.items())[:5]
    if top:
        findings.append(
            f"Highest SOXL same-week correlation: {top[0][0]} ({top[0][1]:+.2f}); "
            f"top 5: {', '.join(f'{t} ({c:+.2f})' for t, c in top)}"
        )
    leaders = [(t, d["lead_1wk_corr"]) for t, d in leading.items() if d["leads_soxl"]]
    leaders.sort(key=lambda x: abs(x[1]), reverse=True)
    if leaders:
        findings.append(
            "Potential SOXL leading indicators (prior-week return predicts next): "
            + ", ".join(f"{t} ({c:+.2f})" for t, c in leaders[:5])
        )
    else:
        findings.append("No component shows a clean 1-week lead over SOXL — coincident moves dominate.")
    if soxl_momentum:
        best_mom = max(soxl_momentum.items(), key=lambda x: abs(x[1]))
        findings.append(
            f"SOXL momentum signal: {best_mom[0]} has strongest auto-correlation ({best_mom[1]:+.2f}); "
            f"{'momentum continuation' if best_mom[1] > 0 else 'mean-reversion'} regime."
        )
    if macro_summary:
        yc = macro_summary.get("yield_curve_10y_2y", {})
        hys = macro_summary.get("high_yield_spread", {})
        if yc:
            findings.append(
                f"Yield curve 10y-2y: {yc.get('latest')} ({yc.get('trend_3m')})"
            )
        if hys:
            findings.append(
                f"HY spread: {hys.get('latest')} ({hys.get('trend_3m')})"
            )

    analysis = {
        "generated_at": datetime.now().isoformat(),
        "tickers_analyzed": len(correlations),
        "soxl_component_correlations": correlations_sorted,
        "leading_indicators": leading,
        "soxl_momentum_autocorrelation": soxl_momentum,
        "key_findings": findings,
    }

    with open(analysis_dir / "soxl_signals.json", "w") as f:
        json.dump(analysis, f, indent=2)
    log(f"  wrote analysis with {len(findings)} findings")


# ──────────────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────────────
def main() -> None:
    LOG_PATH.unlink(missing_ok=True)
    log(f"=== SOX intel build start: {datetime.now().isoformat()} ===")

    start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")

    tickers = fetch_sox_components()
    benchmarks = ["SOXL", "SOXX", "QQQ", "SPY"]
    all_tickers = list(dict.fromkeys(tickers + benchmarks))
    log(f"Total tickers to process: {len(all_tickers)} ({len(tickers)} SOX + {len(benchmarks)} benchmarks)")

    fetch_weekly_prices(all_tickers, start_date, end_date)
    fetch_earnings(tickers)   # not the ETFs
    fetch_macro(start_date)
    analyze(tickers)

    log(f"=== SOX intel build done: {datetime.now().isoformat()} ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("interrupted by user")
        sys.exit(130)
