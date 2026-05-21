# CHANGELOG

## v4 — 2026-05-20 — "complex-wide" expansion + deployable package
**Added**
- Full static web app (no build step): macro/cycle regime layer + 10 tickers across 4 short-thesis archetypes (cyclical-peak memory/storage, secular-growth GPU/ASIC, parabolic momentum, turnaround/foundry).
- Universal **froth & exhaustion** signal layer on every name (YTD extension, distance-above-200dma, **equity-issuance-into-strength**, price-vs-target, short interest/squeeze, post-earnings reaction).
- Weighted **short-readiness composite** (0–100) with a Tier-1 gate for "SHORT SETUP CONFIRMING."
- Persistence (localStorage), JSON **export/import**, **webinar mode**, on-screen status + provenance legend.
- **Auto-update hook**: app reads `data/live.json` to let automation refresh readings without code changes.
- Backtest extended to **two cycles** (2018-19 + 2021-24), CSV-driven engine, per-cycle charts + cross-cycle comparison.
- Docs: README, DEPLOY (with OpenClaw job sketch), DATA-PROVENANCE (verified vs feed), framework, backtest-findings.

**Audit-pass fixes**
- Backtest peak-detection corrected to "high **before** the trough," so a later recovery exceeding the prior peak is no longer misread as the cycle top (was mis-flagging Jun-2024 as the 2021-24 peak).
- Removed a degenerate P&L scenario whose entry post-dated the exit.
- Verified the top YTD movers (SNDK 509%, AEHR 379%, WDC ~160%, STX ~135%) rather than ingesting feed numbers blindly; flagged the unverified ones (INTC, AMD) in DATA-PROVENANCE.
- Data-integrity validator added (Node) — all signals have valid status/weight/source/trigger; 6 froth signals per ticker confirmed.

**Known limitations**
- Several macro fields ship as `na` (book-to-bill, real rate, credit, ISM, VIX, breadth) — populate from feeds.
- Backtest price indices are normalized shapes; turning points & MU fundamentals are real. Drop in real TrendForce series to harden.
- INTC/AMD/CIEN YTD figures need verification before public/webinar use.

## v3 — earlier — single-cycle backtest + NVDA/MU-only tracker (superseded)
