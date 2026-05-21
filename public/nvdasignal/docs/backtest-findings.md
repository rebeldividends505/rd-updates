# Backtest Findings — Memory-Cycle Short Signals (two cycles)

*Companion to `backtest_engine.py`, `memory_cycle_data.csv`, and the per-cycle charts. Now spans TWO downturns: 2018–19 and 2021–24. Data is monthly; MU revenue/gross-margin anchors and all turning-point DATES are real (Micron 8-Ks, TrendForce); DRAM indices are normalized shapes and MU stock levels are approximate monthly closes. Overwrite the pricing columns in the CSV with real TrendForce series to harden it.*

---

## The finding that repeats across both cycles

**The stock leads the earnings by ~4–6 months — in both downturns, at both the top and the bottom.** Waiting for the income statement to confirm the turn was structurally too late every time.

| Metric | 2018–19 | 2021–24 |
|---|---|---|
| DRAM price peak | Jun 2018 | Aug 2021 |
| **MU stock peak** | May 2018 | Jan 2022 |
| **MU stock trough** | Dec 2018 | Oct 2022 |
| Revenue peak | Oct 2018 | Jul 2022 |
| Revenue trough | May 2019 | Feb 2023 |
| Price → stock-peak lead | **−1 mo** (stock anticipated) | **+5 mo** (price led) |
| Stock → revenue-peak lead | **+5 mo** | **+6 mo** |
| Stock → revenue-trough lead | **+5 mo** | **+4 mo** |

## Entry timing — P&L on the short (exit at the stock trough)

| Entry rule | 2018–19 | 2021–24 |
|---|---|---|
| Stock breaks down −15% from peak | **+30%** | **+37%** |
| DRAM price −10% from peak | +18% | **+37%** |
| Wait for first revenue decline (print) | +18% | +18% |
| Wait for first margin decline (print) | +18% | +18% |

In both cycles, acting on the **stock's technical breakdown** captured the most — and waiting for the earnings print left a third to two-thirds of the move on the table.

## What changed vs. the single-cycle read (and why it matters)

1. **"Stock leads earnings" is robust** — it held in two independent cycles, so it's a real structural feature of how memory equities discount the cycle, not a one-off.
2. **The price→stock lead is regime-dependent.** In 2021–24 DRAM price clearly led the stock by ~5 months. In 2018–19 the stock topped *first* (the price plateaued into Q3-2018 while the stock had already rolled in May, partly on the broad Q4-2018 macro selloff). **Implication: don't trade price alone as the trigger — pair the pricing roll with the stock's own technical breakdown.** The −15%-from-peak stock signal was the best single entry in *both* cycles.
3. **Magnitude varies — size to the regime.** 2018–19 was mild (margin troughed ~+27%, stayed profitable). 2022–23 was savage (margin went to −31%). Same shape, very different depth.
4. **Capitulation = the bottom, not an entry.** The Nov-2022 wafer-start cut and the late-2019 price-decline *deceleration* both marked lows. When management capitulates on supply, you're covering, not initiating.

## Honest caveats

- The month-over-month cross-correlation came back ~0 with low r in both cycles — expected, because a smooth normalized index has no real high-frequency texture. The **turning-point leads are the meaningful measure here.** Real TrendForce *spot* prices (which genuinely move week to week and lead contract) would make the cross-correlation informative — that's the single biggest upgrade.
- Turning-point dates and MU fundamentals are real; the price indices and inter-anchor stock levels are reconstructed for shape. Treat the leads as directionally solid (±1 month), not decimal-precise.

## To harden / extend (drop-in ready)

The engine reads `memory_cycle_data.csv`. To improve it:
1. **Overwrite `dram_spot` and `dram_contract`** with real TrendForce series (and `mu_stock` with real monthly closes). Re-run — no code changes needed.
2. **Add a third cycle** ("2025-26") as the current up-cycle rolls, to test the framework live.
3. Add `hyperscaler_capex` as a column to test the NVDA demand lead directly against NVDA stock.
4. Layer in realistic borrow cost + a stop in the P&L to model the "right but early" risk with position sizing.

Run: `python backtest_engine.py memory_cycle_data.csv`
