# automation/ — live data fetcher

Generates `../data/live.json` so the dashboard auto-refreshes without code edits.
Built to run on an OpenClaw / cron schedule. Free data sources only.

## What it does
- **yfinance** → for each ticker: YTD %, distance above the 200-day average, short
  interest, and price-vs-mean-analyst-target. Maps each to a `short / watch / intact`
  status using `thresholds.json`.
- **SEC EDGAR** → scans the last N days of filings for equity-issuance forms
  (424B/S-3/ATM). A recent one flips the `issuance` signal to `short` — the
  "company is selling stock into strength" top-tell. Uses the bundled, verified
  `cik_map.json` (so it doesn't depend on SEC's rate-limited ticker file).

## What it does NOT auto-update (by design)
- **Tier-1 drivers** (DRAM/NAND/HBM pricing, gross-margin direction, data-center
  growth, capex revisions) — these come from TrendForce / earnings, not a free API.
  That's intentional: it keeps the system from ever showing a "confirmed short" off
  froth alone. Wire your pricing feed into `fetch_memory_pricing()` in `update_signals.py`.

## Run it
```bash
pip install yfinance requests          # one time
python3 update_signals.py              # writes ../data/live.json
python3 update_signals.py --dry-run    # print only
python3 update_signals.py --only MU,SNDK,AEHR
```

## Schedule it (OpenClaw / cron)
```cron
# weekdays 7:30am MT — refresh froth + issuance, then (if hosted) redeploy
30 7 * * 1-5  cd /path/to/ai-short-signal-system/automation && /usr/bin/python3 update_signals.py >> fetch.log 2>&1
```
If the site is static-hosted, writing `../data/live.json` is enough — the dashboard
picks it up on next load. If on Vercel/Netlify, trigger a redeploy after the write.

## Tune it
Edit `thresholds.json` — e.g. raise the `ytd.short` cutoff, change the issuance
look-back window, or add forms. Each ticker signal id (for `live.json` keys) can be
listed with:
```bash
node -e "const d=require('../js/data.js'); for(const[s,t]of Object.entries(d.TICKERS)){t.signals.forEach(x=>console.log(s+':'+x.id,'=',x.name));}"
```

## Files
- `update_signals.py` — the fetcher
- `thresholds.json` — status-mapping config
- `cik_map.json` — bundled, SEC-verified ticker→CIK map (10 names)

> Educational research tooling — not investment advice.
