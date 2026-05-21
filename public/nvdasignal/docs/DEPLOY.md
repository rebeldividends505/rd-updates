# DEPLOY — hosting, testing, and auto-updating

Audience: whoever wires this onto the site (OpenClaw / Ryan).

## 1. Host it (pick one)

It's a static site — no build, no Node server required at runtime.

- **Subfolder on the existing site:** drop the whole `ai-short-signal-system/` folder under your web root (e.g. `/tools/signals/`). Done.
- **Vercel / Netlify:** drag-drop the folder, or `vercel deploy` / `netlify deploy --dir=ai-short-signal-system`. No framework preset needed (it's static).
- **S3 / Cloudflare Pages:** upload the folder, set `index.html` as the entry.
- **Local check first:** `cd ai-short-signal-system && python3 -m http.server 8080` → `http://localhost:8080`.

> Serve over **http(s)**, not `file://`, so the `live.json` auto-refresh and import/export behave consistently.

## 2. Test checklist (do this after every deploy)

- [ ] Page loads; macro panel + ticker nav + a ticker detail all render.
- [ ] Click a status chip → it cycles `— → INTACT → WATCH → SHORT`, the score and gauge update.
- [ ] Edit a reading → reload the page → the edit persists (localStorage).
- [ ] `export` downloads a JSON; `import` restores it.
- [ ] Toggle `webinar` → fonts scale up cleanly for screen-share.
- [ ] Mobile width: macro grid collapses to one column.
- [ ] (If using the hook) `data/live.json` values appear on load with their new status.

Quick integrity test of the data config (Node):
```bash
node -e "const d=require('./js/data.js');
  let n=0; Object.values(d.TICKERS).forEach(t=>n+=t.signals.length);
  console.log('tickers',Object.keys(d.TICKERS).length,'signals',n,'macro',d.MACRO.length);"
```

## 3. Auto-update hook (the important part)

The app fetches `data/live.json` on load (cache-busted). If present, it overrides the
seeded `reading` and `status` of any signal — so automation can refresh the fast-moving
numbers **without touching code**.

**Schema** (`data/live.sample.json` is a working template):
```json
{
  "asof": "2026-05-20",
  "readings": {
    "MACRO:dram_spot": { "reading": "Spot -2% w/w", "status": "watch" },
    "MU:0":   { "reading": "Contract guide flat QoQ", "status": "watch" },
    "SNDK:0": { "reading": "NAND +12% (decel)", "status": "watch" }
  }
}
```
- Key format: `MACRO:<id>` or `<SYMBOL>:<signalId>`. Signal ids are **stable** (survive reordering); run the map command below to list them. A numeric 0-based index also works as a fallback.
- Only include fields you want to overwrite. Omitted signals keep their seed.
- `status` must be one of `na | intact | watch | short`.

**Suggested OpenClaw job** (pseudocode for a Mac Mini cron):
```
weekly/daily:
  pull DRAM/NAND spot + contract (TrendForce or your feed)
  pull YTD %, 200dma distance, short interest for each ticker (your market data)
  scan SEC EDGAR for new 424B/ATM filings  -> set the "issuance" froth signal
  map each value -> status via your thresholds (e.g. contract MoM<=0 => "watch")
  write data/live.json
  redeploy (or just overwrite the file if hosted statically)
```

A signal index map for `live.json` keys: run
`node -e "const d=require('./js/data.js'); for(const [s,t] of Object.entries(d.TICKERS)){t.signals.forEach(x=>console.log(s+':'+x.id,'=',x.name));}"`

## 4. Backtest (separate, Python)

```bash
cd backtest
python3 backtest_engine.py memory_cycle_data.csv   # regenerates charts + summary
```
Replace the `dram_spot`/`dram_contract`/`mu_stock` columns in the CSV with real series and
re-run to harden the lead-lag numbers. Add a `cycle` = "2025-26" row block to track the
current up-cycle live.

## 5. Webinar workflow

1. Refresh `live.json` (or hand-edit readings) the morning of.
2. Open the dashboard, toggle **webinar** mode.
3. Walk the macro regime gauge → then the ticker nav (scores tell the story at a glance) →
   drill into 2–3 names. The backtest charts in `backtest/` are your "why this matters" slide.
4. Keep the disclaimer visible.
