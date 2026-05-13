# VISUAL INVENTORY — Tuesday May 19 Package (v2)
## 30 charts: 15 hero number cards + 15 analytical/comparison/explainer

This is the canonical chart checklist. Build these and check them off. The master prompt references each by filename.

---

## A. HERO NUMBER CARDS (build first — they're fast and high-impact)

All 800×800 PNG, square format, dark background (#0a0a0a), white giant number, short orange (#ff6600) or green (#0a7c42) phrase, small "Rebel Dividends · May 19, 2026" watermark in bottom-right corner. Use a strong sans-serif (Helvetica/Arial bold 280pt for the number).

| # | Filename | Big Number | Subtitle | Color |
|---|---|---|---|---|
| 1 | `hero-2-6-trillion.png` | **$2.6T** | "S&P call notional traded May 7 — all-time record. The gamma trap is loaded." | Orange |
| 2 | `hero-177-billion.png` | **$177B** | "Levered ETF AUM — all-time high. $8B forced flow per 1% move." | Orange |
| 3 | `hero-108-weeks.png` | **108** | "Consecutive weekly dividends paid. Through every drawdown." | Green |
| 4 | `hero-share-price.png` | **$0.00165** | "Your RD share — cheapest since Q4 2024." | Green |
| 5 | `hero-gold-ath.png` | **$4,685** | "Gold ATH May 6. Now -8%. The rotation already started." | Orange |
| 6 | `hero-silver-ytd.png` | **+21.9%** | "Silver YTD. Profits worth protecting." | Orange |
| 7 | `hero-powell-out.png` | **MAY 15** | "Powell exits Friday. 8-year era ends 3 days before our webinar." | Orange |
| 8 | `hero-warsh-in.png` | **WARSH** | "First openly pro-Bitcoin Fed Chair: 'Bitcoin is the new gold for people under 40.'" | Green |
| 9 | `hero-thyp-etf.png` | **THYP** | "First-ever spot HYPE ETF — Nasdaq May 12 — with staking yield." | Green |
| 10 | `hero-bull-bear-green.png` | **GREEN** | "BTC bull-bear cycle indicator turned green May 12 — first time since March 2023." | Green |
| 11 | `hero-saylor-buying.png` | **$62B** | "Strategy's Bitcoin treasury. Saylor disclosed the engine this week." | Green |
| 12 | `hero-dividends-paid.png` | **$20.6M+** | "Cumulative dividends RD has paid out since 2022. Real cash to real shareholders." | Green |
| 13 | `hero-reinvestor-return.png` | **+165%** | "Reinvestor return since April 2024 pivot. Compounding works." | Green |
| 14 | `hero-hype-target.png` | **$150** | "HYPE target = $0.00609 RD share = +269% from $0.00165." | Green |
| 15 | `hero-six-days.png` | **6 DAYS** | "Five catalysts converged in six days. This is the window." | Orange |

**Design tip for Claude Code:** matplotlib with `ax.text()` is fine. For the giant number use `fontsize=280, fontweight='bold', color='white'`. For the subtitle use `fontsize=22, color='#ff6600'` or `'#0a7c42'`. Save with `bbox_inches='tight', facecolor='#0a0a0a', dpi=150`.

Optional: if Claude Code has Pillow/PIL access, generate via PIL for sharper text rendering — but matplotlib is acceptable.

---

## B. THE MASTER REINVESTOR CHART (highest priority — same chart format as last week)

| # | Filename | What It Shows |
|---|---|---|
| 16 | `reinvestor-chart-may19.png` | Collector $X vs Reinvestor $Y since pivot, monthly. Use `gen_chart_apr16.py` adapted. Update Apr 2026 close = Tuesday's share price. Title: "Your $100K Since April 2024 Pivot — Week 108 \| May 19, 2026" |

---

## C. COMPARISON CHARTS (the analytical core)

| # | Filename | What It Shows | Notes |
|---|---|---|---|
| 17 | `ytd-comparison-may19.png` | Horizontal bar chart: RD Reinvestor, RD Collector, SPY, QQQ, NVDA, MU, BTC, GLD, SLV, XLE YTD returns | RD bars highlighted green/orange; everything else grey; sort by return descending |
| 18 | `best-investment-comparison.png` | **THE PITCH CHART** — comparison table image with columns: Asset \| Forward 12mo \| Income \| Risk \| Track Record | RD row visually distinct (green background, bold). 10 rows including Cash, Bonds, S&P, Gold, Silver, Energy, SOXL, Raw BTC, Raw HYPE, **RD** |
| 19 | `safety-comparison.png` | Twin chart: SOXL price chart + RD share + dividend bars overlay | Shows SOXL volatility/decay vs RD's smoother ride with weekly dividend bars below |
| 20 | `btc-vs-rd-since-pivot.png` | Both BTC and RD share normalized to 100 at April 2024 pivot | Same chart from last week, refreshed |
| 21 | `gold-from-ath.png` | GLD/XAU 12-month line chart with ATH May 6 marked, current -X% off | Annotate the May 6 peak with date label |
| 22 | `hype-target-ladder-may19.png` | Step/waterfall chart: HYPE $40→$60→$90→$150→$180→$360 with RD share at each step | Use Tuesday's actual share + HYPE values |
| 23 | `108-week-dividend-streak.png` | 108 green bars, all same height, one per week, x-axis = week 1 through week 108 | Title: "108 Consecutive Weekly Dividends Paid" |
| 24 | `rotation-trade-table.png` | Table image: Asset \| YTD \| Why It Worked \| Why It May Soften | 6 rows: Gold, Silver, Energy, Semis, Bitcoin, HYPE — BTC/HYPE rows highlighted |
| 25 | `warsh-fed-timeline.png` | Horizontal timeline: Apr 29 → May 12 → May 13-14 → May 15 (Powell out) → May 19 (TUESDAY) | Each milestone as a dot with label below |

---

## D. EXPLAINER CHARTS (the mechanical pieces)

| # | Filename | What It Shows | Notes |
|---|---|---|---|
| 26 | `gamma-trap-explainer.png` | 4-panel feedback loop diagram | Panel 1: Retail buys OTM calls. Panel 2: Dealers hedge by buying underlying. Panel 3: Levered ETFs forced-buy on up days. Panel 4: Loop repeats. Bottom red banner: McElligott reversal trigger quote |
| 27 | `levered-etf-aum-growth.png` | Bar chart: Levered ETF total AUM 2018→2026, ending at $177B (100%ile) | Highlight 2026 bar in orange |
| 28 | `sp-call-volume-record.png` | Daily S&P call notional 2024-2026 with May 7 spike marked at $2.6T | Annotate with "+all-time high" callout |
| 29 | `forward-macro-5-pillars.png` | **NEW MACRO FRAMEWORK** — 5 themes as gears/columns/pillars | 1. Gold→BTC rotation 2. M2/Debt 3. AI Agents 4. Tech Revolution 5. **Gamma Reversal + Fed Regime Change (NEW)** |
| 30 | `catalyst-calendar-2026.png` | Horizontal timeline of forward catalyst dates | May 15 (Powell out) → May 19 (Tuesday) → June 17-18 FOMC → Sept 17-18 FOMC → Dec 16-17 FOMC → Q4 BTC ATH retest → Q1 27 HYPE $90 → H1 27 HYPE $150 |

---

## E. OPTIONAL ADD-ONS (if time permits — push toward 35 total visuals)

| Filename | What It Shows |
|---|---|
| `hyperliquid-q1-fees.png` | Hyperliquid Q1 protocol fees breakdown + buyback amounts |
| `gold-silver-ratio-2026.png` | Gold/silver ratio time series 2024-2026 |
| `btc-etf-flows-recent.png` | Spot BTC ETF cumulative inflows recent 4 weeks |
| `purr-q1-earnings.png` | Hyperliquid Strategies $152.5M Q1 net profit breakdown |
| `hype-12month-chart.png` | HYPE 1-year price chart with key levels ($59.31 ATH, $40 current, $20.53 cycle low) marked |
| `dividend-streak-with-drawdowns.png` | 108 dividend bars overlaid with HYPE drawdown chart — visually shows dividends paid even during -56% drawdown |

---

## F. CHART STYLING GUIDELINES (consistency across all visuals)

- **Background**: white #ffffff for analytical charts, dark #0a0a0a for hero cards
- **Primary colors**: RD orange #ff6600, RD green #0a7c42, neutral grey #888888
- **Bullish bars/lines**: green #0a7c42 (or #4ade80 for lighter)
- **Bearish bars/lines**: red #c41e3a
- **Highlight color**: orange #ff6600
- **Font**: Helvetica/Arial sans-serif, bold for titles/numbers, regular for body
- **Title**: 16pt bold, dark grey #1a1a1a
- **Subtitle**: 12pt regular, grey #555555
- **Axis labels**: 10pt, grey #666666
- **Watermark**: 8pt, grey #999999, bottom-right "Rebel Dividends · May 19, 2026"
- **Image dimensions**:
  - Hero cards: 800×800 PNG
  - Analytical charts: 1200×600 or 1200×800 PNG
  - Wide timelines: 1400×400 PNG
  - Tables/comparison: 1200×800 PNG
- **DPI**: 150 minimum for retina display
- **Save**: `bbox_inches='tight'` to avoid white border, `facecolor` matches background

---

## G. BUILD ORDER (most important first, in case time runs short)

**Must-have (Tier 1):**
1. `reinvestor-chart-may19.png` — the master trust anchor
2. `best-investment-comparison.png` — THE pitch chart, the new section that justifies the show
3. `ytd-comparison-may19.png` — the standard opener
4. `hype-target-ladder-may19.png` — the action math
5. `gamma-trap-explainer.png` — the mechanical centerpiece
6. `warsh-fed-timeline.png` — the urgency anchor
7. `108-week-dividend-streak.png` — the safety anchor
8. `hero-share-price.png` — the lead number ($0.00165)
9. `hero-108-weeks.png` — the safety hero
10. `hero-2-6-trillion.png` — the gamma hero

**Should-have (Tier 2):**
11-20. The remaining hero cards (#1, 5-9, 11-15) — these are fast to build, lots of impact

**Nice-to-have (Tier 3):**
21-30. Forward macro 5-pillar diagram, catalyst calendar, safety comparison, gold-from-ATH, sp-call-volume, levered-etf-AUM, rotation table, BTC vs RD, optional add-ons

If time-constrained, ship Tier 1 + Tier 2 (20 visuals). The Tier 3 visuals can be added to the Elementor page post-launch.
