#!/usr/bin/env python3
"""
Mega Thesis Research — runs all Perplexity searches concurrently,
plus FRED + Polygon data pulls. Saves everything to JSON for synthesis.

Output files (all in this directory):
  - perplexity_results.json   — all Perplexity sonar-pro responses keyed by search slug
  - fred_data.json            — current readings on consumer health series
  - polygon_perf.json         — % change since BTC peak (Sep 28 2025) for AI stocks + BTC
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

OUT_DIR = Path(__file__).parent
PERPLEXITY_KEY = os.environ["PERPLEXITY_API_KEY"]
POLYGON_KEY = os.environ["POLYGON_API_KEY"]
FRED_KEY = os.environ["FRED_API_KEY"]

# ----------------------------------------------------------------------
# Perplexity searches — debate, leading indicators, Trump/China
# ----------------------------------------------------------------------

SEARCHES: dict[str, str] = {
    "debate_bear": (
        "What are the most reliable leading indicators that Google, Meta, Microsoft, Amazon AI revenue growth "
        "is about to slow in 2026? Historical examples of when earnings disappointed AI/cloud stocks and what "
        "happened next? What indicators predicted the 2022 tech selloff before it happened? Cite specific "
        "metrics and timing."
    ),
    "debate_bull": (
        "Why might Google, Meta, Amazon, Microsoft continue to grow revenue despite a US consumer slowdown in "
        "2026? What is the evidence that enterprise AI adoption is accelerating enough to offset consumer "
        "weakness? Historical examples where AI/cloud stocks kept growing despite consumer slowdown? Cite "
        "specific channel checks, surveys, and earnings commentary from Q1 2026."
    ),
    "indicator_google_ads": (
        "Google advertising revenue leading indicators 6 months ahead — what tracks it best? DoubleClick "
        "impressions, Google Trends search query volume, ComScore digital ad spend, real-time digital ad "
        "platform data. What is the current 2026 reading on each and what level historically signals a "
        "Google ad revenue slowdown? Cite IAB, eMarketer, Magna Global 2026."
    ),
    "indicator_meta_ads": (
        "Meta Facebook advertising revenue leading indicators 2026 — CPM trends, ad load rates, DAU/MAU "
        "growth, time-spent metrics, Reels monetization. What are the best 3-6 month leading indicators for "
        "Meta ad revenue and what are they showing in Q1-Q2 2026? Compare to the 2022 Snap ad warning that "
        "preceded Meta's miss."
    ),
    "indicator_msft_azure": (
        "Microsoft Azure consumption growth rate Q3 FY2026 (Mar 2026 quarter) — accelerating or "
        "decelerating? What did Satya Nadella and Amy Hood say on the most recent earnings call about Azure "
        "AI growth? What are Gartner, Forrester, IDC, and channel checks (RBC, Morgan Stanley CIO survey) "
        "showing about enterprise cloud spending 2026? Cite specific growth rate numbers."
    ),
    "indicator_aws": (
        "Amazon AWS revenue growth Q1 2026 results and Q2 2026 guidance — any signs of deceleration vs "
        "Azure or Google Cloud? Enterprise cloud spending surveys (Flexera State of the Cloud 2026, Morgan "
        "Stanley CIO survey, Goldman Sachs CIO survey) showing AWS-specific trends. What is the AWS "
        "operating margin trajectory and what does it imply about AI economics?"
    ),
    "indicator_nvda_dc": (
        "NVIDIA data center revenue Q1 FY2027 (April 2026 quarter) results, guidance, and commentary on "
        "H100, H200, B200 and Blackwell Ultra demand. Any signs of order pushouts or slowdowns from "
        "hyperscalers? What did Colette Kress say about Q2 guidance? Channel checks on lead times and "
        "pricing power in Q2 2026. Cite specific dollar numbers and growth rates."
    ),
    "indicator_consumer_lag": (
        "When US consumer spending slows, how long historically before it hits corporate advertising "
        "budgets and Google/Meta revenue growth? Specific lag time between Conference Board Consumer "
        "Confidence decline and digital ad revenue growth slowdown in 2008, 2020, and 2022. What is the "
        "transmission mechanism and approximate quarters of lag?"
    ),
    "trump_xi_summit": (
        "Trump-Xi summit May 13-15 2026 Beijing — expected outcomes, technology concessions, rare earth "
        "agreement, semiconductor export restrictions. How would various outcomes (deal vs no-deal vs "
        "escalation) affect Nvidia, AMD, Applied Materials, Lam Research, Microsoft and Apple stocks? "
        "Cite specific analyst forecasts and current market expectations as of May 2026."
    ),
    "trump_tariff_history": (
        "Trump historical pattern of aggressive tariffs when S&P 500 is at all-time highs — what happened "
        "in December 2018 when S&P was near record highs and Trump escalated China tariffs? Day-by-day "
        "timeline of tariff escalation versus market reaction. When did Trump back off and why? Also cover "
        "April 2025 tariff episode if relevant — how long did the selloff last and what triggered the "
        "reversal?"
    ),
    "trump_chip_restrictions": (
        "If Trump restricts AI chip exports to China in 2026 — revenue impact on Nvidia, Applied Materials, "
        "Lam Research, KLA, Advantest, ASML. What percentage of each company's revenue is China exposed? "
        "What did the October 2023 and 2024 export controls do to these names and how quickly did they "
        "recover? Cite specific percentages and dates."
    ),
}


def perplexity_call(slug: str, query: str) -> dict:
    """Single Perplexity sonar-pro call. Returns dict ready to dump to JSON."""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a top-tier sell-side macro/equity research analyst. Cite specific numbers, "
                    "dates, and sources. Use 2026 data where possible. Be precise — no hedging. If a "
                    "datapoint is unverified, say so explicitly."
                ),
            },
            {"role": "user", "content": query},
        ],
        "temperature": 0.2,
        "max_tokens": 1500,
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=180)
        r.raise_for_status()
        data = r.json()
        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations") or data.get("search_results") or []
        return {"slug": slug, "query": query, "answer": content, "citations": citations}
    except Exception as e:
        return {"slug": slug, "query": query, "error": str(e)}


def run_perplexity_searches() -> dict:
    print(f"[perplexity] launching {len(SEARCHES)} concurrent sonar-pro queries...", flush=True)
    results: dict = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(perplexity_call, slug, q): slug for slug, q in SEARCHES.items()}
        for fut in as_completed(futures):
            slug = futures[fut]
            res = fut.result()
            results[slug] = res
            status = "ERR" if "error" in res else "OK"
            print(f"  [{status}] {slug}", flush=True)
    return results


# ----------------------------------------------------------------------
# FRED — consumer health series
# ----------------------------------------------------------------------

FRED_SERIES = {
    "consumer_confidence_umich": "UMCSENT",
    "credit_card_delinquency_pct": "DRCCLACBS",
    "personal_savings_rate_pct": "PSAVERT",
    "nonfarm_payrolls_thousands": "PAYEMS",
    "core_pce_index": "PCEPILFE",
    "real_gdp_growth_qoq_saar": "A191RL1Q225SBEA",
    "retail_sales_yoy_pct": "RSAFS",
    "unemployment_rate": "UNRATE",
    "initial_claims": "ICSA",
}


def fred_series(series_id: str, start: str = "2022-01-01") -> list[dict]:
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_KEY,
        "file_type": "json",
        "observation_start": start,
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    obs = r.json().get("observations", [])
    return [
        {"date": o["date"], "value": float(o["value"])}
        for o in obs
        if o.get("value") not in (".", None, "")
    ]


def fetch_fred() -> dict:
    print("[fred] pulling series...", flush=True)
    out = {}
    for name, sid in FRED_SERIES.items():
        try:
            series = fred_series(sid)
            if not series:
                out[name] = {"series_id": sid, "error": "empty"}
                continue
            latest = series[-1]
            # Find ~6 months ago for trend.
            six_m = series[-7] if len(series) > 7 else series[0]
            yr_ago = series[-13] if len(series) > 13 else series[0]
            out[name] = {
                "series_id": sid,
                "latest_date": latest["date"],
                "latest_value": latest["value"],
                "six_months_ago": six_m,
                "year_ago": yr_ago,
                "n_obs": len(series),
            }
            print(f"  {name}: {latest['value']} as of {latest['date']}", flush=True)
        except Exception as e:
            out[name] = {"series_id": sid, "error": str(e)}
            print(f"  ERR {name}: {e}", flush=True)
    return out


# ----------------------------------------------------------------------
# Polygon — performance since BTC peak Sep 28 2025
# ----------------------------------------------------------------------

AI_STOCKS = ["NVDA", "MSFT", "GOOGL", "META", "AMZN", "AMD", "PLTR", "AVGO", "SOXL", "MSTR"]


def polygon_close_window(ticker: str, start: str, end: str) -> dict | None:
    """Get closing prices in a date window. Returns first and last close."""
    is_crypto = ticker.startswith("X:")
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}"
        f"?adjusted=true&sort=asc&apiKey={POLYGON_KEY}"
    )
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return {"error": f"HTTP {r.status_code}: {r.text[:120]}"}
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None
    first = results[0]
    last = results[-1]
    return {
        "first_date": time.strftime("%Y-%m-%d", time.gmtime(first["t"] / 1000)),
        "first_close": first["c"],
        "last_date": time.strftime("%Y-%m-%d", time.gmtime(last["t"] / 1000)),
        "last_close": last["c"],
        "n_bars": len(results),
    }


def fetch_polygon_perf() -> dict:
    print("[polygon] pulling perf vs BTC peak Sep 28 2025...", flush=True)
    out = {}
    for ticker in AI_STOCKS + ["X:BTCUSD"]:
        start_win = polygon_close_window(ticker, "2025-09-25", "2025-10-03")
        end_win = polygon_close_window(ticker, "2026-05-04", "2026-05-12")
        if not start_win or not end_win or "error" in (start_win or {}) or "error" in (end_win or {}):
            out[ticker] = {"start": start_win, "end": end_win, "error": "incomplete data"}
            print(f"  ERR {ticker}: {start_win} / {end_win}", flush=True)
            continue
        start_px = start_win["first_close"]
        end_px = end_win["last_close"]
        change = (end_px / start_px - 1) * 100
        out[ticker] = {
            "start_date": start_win["first_date"],
            "start_price": start_px,
            "end_date": end_win["last_date"],
            "end_price": end_px,
            "change_pct": round(change, 2),
        }
        print(f"  {ticker}: {change:+.1f}% (since {start_win['first_date']})", flush=True)
        time.sleep(0.15)  # Polygon free tier rate limit cushion
    return out


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Run all three sources concurrently as well.
    with ThreadPoolExecutor(max_workers=3) as pool:
        f_perp = pool.submit(run_perplexity_searches)
        f_fred = pool.submit(fetch_fred)
        f_poly = pool.submit(fetch_polygon_perf)

        perp = f_perp.result()
        fred = f_fred.result()
        poly = f_poly.result()

    (OUT_DIR / "perplexity_results.json").write_text(json.dumps(perp, indent=2))
    (OUT_DIR / "fred_data.json").write_text(json.dumps(fred, indent=2))
    (OUT_DIR / "polygon_perf.json").write_text(json.dumps(poly, indent=2))

    print(f"\n[done] wrote {len(perp)} perplexity, {len(fred)} fred, {len(poly)} polygon entries", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
