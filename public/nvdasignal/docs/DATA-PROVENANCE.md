# DATA PROVENANCE & REFRESH

Every seed reading carries a provenance badge in the UI. This file records what was
independently verified as of **2026-05-20**, what came from the input feed (verify
before citing publicly), and how often each thing should be refreshed.

## Provenance legend
- **verified (v)** — independently web-verified on/around 2026-05-20.
- **filing (r)** — from a company SEC filing (8-K/10-Q).
- **feed·verify (u)** — provided by your data feed/AI summary; treat as approximate, verify before a webinar.
- **illustrative (n)** — normalized/placeholder for shape (mainly backtest indices).

## Verified figures (2026-05-20)
| Item | Value | Note |
|---|---|---|
| SanDisk (SNDK) YTD | ≈ **+509%** | multiple sources; fwd P/E ~7x on FY27 (peak-cycle trap); GM 78.4%; $3.17B follow-on |
| Aehr (AEHR) YTD | ≈ **+379%** | revenue **−27% YoY** while stock tripled — divergence; ATM equity agreement (Apr 8); $41M order |
| Western Digital (WDC) YTD | ≈ **+152–169%** | record ~46% GM; HDDs sold out 2026; mean target ~3% above price; divested SanDisk stake |
| Seagate (STX) YTD | ≈ **+135%** | targets being raised (Rosenblatt $750); +65% in April alone |
| NVDA Q1 FY27 | rev $81.6B (+85%), DC $75.2B (+92%), GM 74.9%, $18.6B invested/qtr | from release/10-Q |
| Hyperscaler capex 2026 | ≈ **$725B**, +77% YoY; 3 of 4 raised | Meta −9% on its raise |
| DRAM contract | +90–95% Q1 → +58–63% Q2 (decelerating); PC DRAM slowed April | TrendForce |

## Feed-provided — VERIFY before public use
| Item | As given | Action |
|---|---|---|
| Micron (MU) YTD | ≈ +130–170% | confirm exact YTD; 12-mo return was ~+290% |
| Intel (INTC) YTD | ≈ +150% ("doubled") | **verify** — turnaround move, figure uncertain |
| Broadcom (AVGO) YTD | ≈ +18–20% | confirm |
| Ciena (CIEN) YTD | ≈ "doubled" | confirm exact |
| AMD YTD | unknown | **fill in** |
| All `na` macro fields (book-to-bill, real rate, credit, ISM, VIX, breadth) | — | populate from your feeds |

## Refresh cadence
- **Weekly:** DRAM/NAND **spot** prices; YTD %, distance-from-200dma, short interest per name; SEC EDGAR scan for new ATM/secondary filings (the "issuance" signal).
- **Monthly:** DRAM/NAND **contract** prices; SEMI book-to-bill; WSTS sales; ISM; analyst-target vs price.
- **Quarterly (around prints):** gross-margin direction, inventory days, data-center sequential growth, capex revisions, post-earnings reaction.
- **Continuous-ish:** real rates, credit spreads, DXY, VIX (cheap to pull daily).

Keep an `asof` date visible on screen during webinars; stale memory-pricing data is the
fastest way to lose credibility with a numbers-literate audience.
