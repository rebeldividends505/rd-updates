#!/usr/bin/env python3
"""
update_signals.py  —  live-data fetcher for the AI Short-Signal System
=======================================================================
Pulls market data + SEC issuance filings, maps them to signal statuses, and
writes ../data/live.json (the file the dashboard reads on load).

Designed to run on an OpenClaw / cron schedule. Free data sources only:
  * yfinance  -> price, YTD %, distance above 200-day avg, short interest,
                 analyst target-vs-price
  * SEC EDGAR -> recent equity-issuance filings (424B/S-3/ATM) per ticker
A clearly-marked hook (fetch_memory_pricing) is left for your TrendForce feed.

USAGE:
  python3 update_signals.py            # fetch + write ../data/live.json
  python3 update_signals.py --dry-run  # print what it would write, no file
  python3 update_signals.py --only MU,SNDK

Status semantics (SHORT tracker): more froth = more "short".
Thresholds live in thresholds.json (edit freely).
"""
import json, sys, os, time, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "data" / "live.json"
CFG = json.loads((HERE / "thresholds.json").read_text())
UA = {"User-Agent": CFG.get("sec_user_agent", "ShortSignalSystem research contact@example.com")}

# tickers we can auto-refresh (froth signals). Memory/macro pricing = manual/feed.
TICKERS = ["MU", "SNDK", "WDC", "STX", "NVDA", "AVGO", "AMD", "AEHR", "CIEN", "INTC"]

DRY = "--dry-run" in sys.argv
if "--only" in sys.argv:
    TICKERS = sys.argv[sys.argv.index("--only") + 1].split(",")

def log(*a): print(f"[{dt.datetime.now():%H:%M:%S}]", *a)

# ----------------------------------------------------------------------
def band(value, t_short, t_watch, higher_is_short=True):
    if value is None: return None
    if higher_is_short:
        if value >= t_short: return "short"
        if value >= t_watch: return "watch"
        return "intact"
    else:
        if value <= t_short: return "short"
        if value <= t_watch: return "watch"
        return "intact"

def market_signals(sym):
    """Return {signalId: {reading, status}} for the froth layer from yfinance."""
    import yfinance as yf
    out = {}
    try:
        tk = yf.Ticker(sym)
        hist = tk.history(period="1y", auto_adjust=True)
        if hist.empty:
            log(f"  {sym}: no history"); return out
        price = float(hist["Close"].iloc[-1])
        # YTD
        ystart = hist[hist.index >= f"{dt.date.today().year}-01-01"]
        if len(ystart):
            base = float(ystart["Close"].iloc[0])
            ytd = (price / base - 1) * 100
            out["ytd"] = {"reading": f"{ytd:+.0f}% YTD (auto)",
                          "status": band(ytd, CFG["ytd"]["short"], CFG["ytd"]["watch"])}
        # distance above 200-day MA
        if len(hist) >= 200:
            ma200 = float(hist["Close"].rolling(200).mean().iloc[-1])
            dist = (price / ma200 - 1) * 100
            out["ma200"] = {"reading": f"{dist:+.0f}% vs 200-day avg (auto)",
                            "status": band(dist, CFG["ma200_pct"]["short"], CFG["ma200_pct"]["watch"])}
        # short interest + analyst target (best-effort; info can be sparse)
        info = {}
        try: info = tk.get_info()
        except Exception: pass
        sip = info.get("shortPercentOfFloat")
        if sip is not None:
            sipct = sip * 100
            out["si"] = {"reading": f"SI {sipct:.1f}% of float — squeeze risk (auto)",
                         "status": "watch" if sipct >= CFG["short_interest_pct"]["watch"] else "intact"}
        tgt = info.get("targetMeanPrice")
        if tgt:
            gap = (price / tgt - 1) * 100  # +ve = price above mean target
            out["target"] = {"reading": f"price {gap:+.0f}% vs mean target ${tgt:.0f} (auto)",
                             "status": band(gap, CFG["target_gap"]["short"], CFG["target_gap"]["watch"])}
        log(f"  {sym}: {', '.join(out.keys()) or 'none'}")
    except Exception as e:
        log(f"  {sym}: market fetch error: {e}")
    return out

# ----------------------------------------------------------------------
_CIK = None
def cik_map():
    """Prefer the bundled verified map; fall back to the live SEC ticker file."""
    global _CIK
    if _CIK is None:
        bundled = HERE / "cik_map.json"
        if bundled.exists():
            _CIK = json.loads(bundled.read_text())
        else:
            _CIK = {}
        # try to enrich from live file (non-fatal if rate-limited)
        try:
            import requests
            r = requests.get("https://www.sec.gov/files/company_tickers.json", headers=UA, timeout=20)
            if r.headers.get("content-type", "").startswith("application/json"):
                for v in r.json().values():
                    _CIK.setdefault(v["ticker"], str(v["cik_str"]).zfill(10))
        except Exception:
            pass
    return _CIK

def issuance_signal(sym):
    """Scan recent SEC filings for equity-issuance forms -> 'issuance' status."""
    import requests
    try:
        cik = cik_map().get(sym)
        if not cik: return None
        r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=UA, timeout=20)
        recent = r.json().get("filings", {}).get("recent", {})
        forms = recent.get("form", []); dates = recent.get("filingDate", [])
        cutoff = dt.date.today() - dt.timedelta(days=CFG["issuance_lookback_days"])
        hits = []
        for f, d in zip(forms, dates):
            try: fd = dt.date.fromisoformat(d)
            except Exception: continue
            if fd >= cutoff and any(f.startswith(x) for x in CFG["issuance_forms"]):
                hits.append((f, d))
        time.sleep(0.2)  # be polite to EDGAR
        if hits:
            f, d = hits[0]
            return {"reading": f"{f} filed {d} (equity issuance near highs)", "status": "short"}
        return {"reading": "No recent issuance filings (auto)", "status": "intact"}
    except Exception as e:
        log(f"  {sym}: EDGAR error: {e}"); return None

# ----------------------------------------------------------------------
def fetch_memory_pricing():
    """HOOK: wire your TrendForce / contract-price feed here.
    Return a dict of MACRO overrides, e.g.:
        {"dram_spot": {"reading": "...", "status": "watch"}, ...}
    Return {} to leave macro pricing at its seeded values."""
    return {}

# ----------------------------------------------------------------------
def main():
    log(f"Refreshing {len(TICKERS)} tickers  (dry_run={DRY})")
    readings = {}
    for sym in TICKERS:
        for sid, val in market_signals(sym).items():
            if val and val.get("status"): readings[f"{sym}:{sid}"] = val
        iss = issuance_signal(sym)
        if iss: readings[f"{sym}:issuance"] = iss
    for mid, val in fetch_memory_pricing().items():
        readings[f"MACRO:{mid}"] = val

    payload = {"asof": dt.date.today().isoformat(), "readings": readings,
               "_generated_by": "update_signals.py"}
    if DRY:
        print(json.dumps(payload, indent=2)); return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    log(f"Wrote {OUT}  ({len(readings)} signal overrides)")

if __name__ == "__main__":
    main()
