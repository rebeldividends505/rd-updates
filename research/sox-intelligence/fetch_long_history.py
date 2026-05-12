#!/usr/bin/env python3
"""Fetch 2020-2026 weekly OHLCV for SOX universe via Polygon.

Writes JSON per ticker into weekly_prices_long/. Skips files that already
exist with > 200 weeks. Sleeps between requests to be polite.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import requests

POLYGON = os.environ["POLYGON_API_KEY"]
ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "weekly_prices_long"
OUT_DIR.mkdir(parents=True, exist_ok=True)

START = "2020-01-01"
END = "2026-05-11"

TICKERS = [
    "NVDA", "AMD", "AVGO", "TXN", "QCOM",
    "INTC", "MU", "AMAT", "LRCX", "KLAC",
    "ADI", "MRVL", "NXPI", "ON", "MCHP",
    "TSM", "ARM", "SMCI", "MPWR", "ENTG",
    "SWKS", "QRVO", "TER", "WOLF", "ACLS",
    "SLAB", "CRUS", "RMBS", "SITM",
    "SOXL", "SOXX", "QQQ", "SPY",
]


def fetch_weekly(ticker: str) -> dict | None:
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/week/{START}/{END}"
    params = {"apiKey": POLYGON, "limit": 5000, "adjusted": "true"}
    r = requests.get(url, params=params, timeout=30)
    if r.status_code != 200:
        print(f"  HTTP {r.status_code}: {r.text[:200]}")
        return None
    js = r.json()
    if not js.get("results"):
        print(f"  No results")
        return None
    return js


def main():
    ok, fail = 0, []
    for t in TICKERS:
        path = OUT_DIR / f"{t}.json"
        if path.exists():
            try:
                cached = json.loads(path.read_text())
                if cached.get("resultsCount", 0) > 250:
                    print(f"✓ {t} (cached, {cached['resultsCount']} weeks)")
                    ok += 1
                    continue
            except Exception:
                pass
        js = fetch_weekly(t)
        if js is None:
            fail.append(t)
            print(f"✗ {t}")
            continue
        path.write_text(json.dumps(js))
        print(f"✓ {t}: {js.get('resultsCount', 0)} weeks")
        ok += 1
        time.sleep(0.25)
    print(f"\nDone. {ok} ok, {len(fail)} failed: {fail}")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
