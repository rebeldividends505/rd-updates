# AI Short-Signal System

A tiered, editable dashboard for tracking **when downside-risk conditions align** across the AI semiconductor / memory / storage complex — plus a CSV-driven historical **backtest** that shows which signals actually lead price.

Built as a dependency-free static site: deploy anywhere, no build step.

> **Educational research framework — not investment advice.** A "SHORT SETUP CONFIRMING" reading is a prompt to investigate, never a signal to trade.

---

## What's inside

```
ai-short-signal-system/
  index.html              # the dashboard (open in a browser, or host)
  css/styles.css          # terminal aesthetic + webinar mode
  js/data.js              # ← THE CONFIG: macro layer + 10 tickers + signals (edit this)
  js/app.js               # rendering, scoring, persistence, export/import, live hook
  data/live.sample.json   # automation hook schema (rename to live.json to activate)
  backtest/               # the lead-lag backtest (Python, runs standalone)
    backtest_engine.py
    build_seed_csv.py
    memory_cycle_data.csv # ← edit/replace with real TrendForce + price data
    cycle_2018_19.png / cycle_2021_24.png / leadlag_summary.csv
  docs/
    framework.md          # the core short-signal methodology (deep)
    backtest-findings.md   # what the two-cycle backtest showed
    DEPLOY.md             # how to host, test, and auto-update (for OpenClaw)
    DATA-PROVENANCE.md    # what's verified vs feed-provided, and refresh cadence
    CHANGELOG.md
```

## Run it

- **Quickest:** open `index.html` in a browser. Everything works except the optional `live.json` auto-refresh (browsers block local file fetches).
- **Proper (and for the automation hook):** serve over http —
  `cd ai-short-signal-system && python3 -m http.server 8080` → visit `http://localhost:8080`.

State persists in the browser via `localStorage`. Use **export/import** to move a saved state between machines or snapshot it for a webinar.

## The model in one paragraph

Two short *archetypes* dominate. **Cyclical-peak** names (MU, SNDK, WDC, STX) are shorted on the **pricing roll** — spot turns, contract momentum stalls, margins crack — and the backtest shows price/technicals lead the earnings by ~4–6 months. **Secular-growth** names (NVDA, AVGO, AMD) are shorted on a **demand + margin + multiple** unwind, where hyperscaler capex is the master variable. Two more archetypes round it out: **parabolic momentum** small-caps (AEHR, CIEN) where order-flow and froth dominate, and **turnaround/foundry** (INTC) which is execution-driven. Every name also carries a universal **froth** layer (YTD extension, distance above the 200-day average, **equity issuance into strength**, price-vs-target, short interest, post-earnings reaction).

## Scoring

Each signal contributes `status × weight` to a 0–100 **short-readiness** score (intact 0, watch 0.5, short 1; weights 1–3, Tier-1 = 3; `na` excluded). A reading only reaches **"SHORT SETUP CONFIRMING"** at ≥60/100 **and** at least one **Tier-1** trigger firing — so froth alone can't confirm a short; an actual driver (pricing/demand) has to roll. This gate is deliberate: it's what separates "expensive" from "topping."

## Extend it

- **Add a ticker:** copy an entry in `js/data.js → TICKERS`, set its `archetype` (must exist in `ARCHETYPE_ORDER`), and add signals. Froth signals auto-attach.
- **Add a signal:** push an object to a ticker's `signals[]` or to `MACRO`.
- **Add a backtest cycle:** append rows to `backtest/memory_cycle_data.csv` with a new `cycle` label and re-run the engine.

See `docs/DEPLOY.md` for hosting + the auto-update hook, and `docs/DATA-PROVENANCE.md` for what to refresh and how often.
