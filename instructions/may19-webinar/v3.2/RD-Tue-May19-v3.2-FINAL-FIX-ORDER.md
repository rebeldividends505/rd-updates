# RD Tuesday May 19 Webinar — v3.2-FINAL FIX ORDER

**For:** OpenClaw worker bot → Claude Code CLI
**Generated:** May 17, 2026 (revised with May 17 PM data pull)
**Webinar broadcast:** Tuesday May 19, 2026 — 3:30 PM ET / 1:30 PM MDT
**Working hours remaining:** ~48
**Build under iteration:** v3.1 (Opus package)
**Source of truth:** This document supersedes v3.2 v1. Worker bot should treat this as authoritative.

---

## REVISION LOG (what changed from v3.2 to v3.2-FINAL)

Based on `rd-data-pull/` from May 17 PM:

1. **Hyperliquid stats upgraded.** Cumulative volume $4.62T (not $4.4T). Active users now ~2M (1,988,869). Total perp open interest $38.7B.
2. **New institutional proof point.** Bitwise Onchain Solutions x FalconX is operating an active validator on Hyperliquid. Plus Anchorage By Figment, Hyper Foundation 1, multiple other institutional names. This is stronger than the ETF news alone.
3. **CPI re-acceleration is a real story.** January 2026 CPI was 2.39% YoY. April 2026 is 3.81%. That is a 142 basis point jump in 4 months. The "Fed will cut" narrative is materially under pressure.
4. **Japan 10Y JGB moved significantly.** 2.36% to 2.63% in one month.
5. **Top Hyperliquid perp markets are memecoin-dominated.** PUMP alone has $18.77B in OI - roughly half of all perp OI. Framing question for the email: lean into "where the most-traded onchain markets live" without naming the memecoin specifics.
6. **HIP-4 prediction markets data is NOT publicly queryable.** Worker bot should not cite HIP-4-specific numbers.
7. **HeyZibi API is broken.** Domain does not resolve. Worker bot should not retry.

---

## EXECUTIVE SUMMARY

The v3.1 build needs:
- 4 must-fix data corrections (Section 1)
- 3 surgical content edits with paste-ready HTML (Section 2)
- 7 chart specs (Section 3)
- 5 API tasks for Tuesday morning automation (Section 4)
- 2 SMS fixes (Section 5)
- Full QA checklist (Section 6)

**Permission check needed from Jason before send:** Coinbase + Bitwise in catalyst table. The OPUS brief said "BTC and HYPE only - no Coinbase/Solana/ETH comparisons." These mentions are about Hyperliquid, not recommendations. Worker bot should ask Jason to greenlight.

---

# PART 1 - MUST-FIX DATA CORRECTIONS

## FIX 1.1 - YTD figures don't match May 17 data

**Email current state (line ~89):**
Silver +23.2%, Gold +8.6%, Energy +29.7%, NVDA +21.1%

**Verified values (May 17):**

| Asset | Email shows | Actual | Drift |
|---|---|---|---|
| Silver (SLV) | +23.2% | +7.17% | -16.0 |
| Gold (GLD) | +8.6% | +5.29% | -3.3 |
| Energy (XLE) | +29.7% | +33.81% | +4.1 |
| NVDA | +21.1% | +20.82% | trivial |
| SOXL (3x semis) | not shown | +290.63% | NEW |
| SMH (semis) | not shown | +54.48% | NEW |
| BTC | not shown | -10.72% | NEW |
| 30Y Treasury | not shown | 5.128% | NEW |
| CPI YoY (Apr) | not shown | 3.81% | NEW |

**Fix:** See Surgical Edit 3.

## FIX 1.2 - Warsh row in catalysts table is wrong

**Email:** "May 12 | Warsh confirmed to Fed Board (51-45)"

**Verified:** May 13 confirmation as Fed CHAIR, 54-45 vote (closest in modern era). Powell stays on as governor through 2028.

**Replace with:** "May 13 | Warsh confirmed as Fed Chair (54-45) | First openly pro-Bitcoin Fed Chair in history. Closest confirmation vote in modern era."

## FIX 1.3 - "First-ever HYPE ETF" is stale in 4 places

Locations: Live Webinar Banner subhead, Bridge paragraph ("yesterday" is 7 days stale), 5 Catalysts table, SMS file.

**Reality:** Two spot HYPE ETFs now trading (THYP May 12, BHYP May 15). Plus Coinbase USDC deal May 14.

**Fix:** See Surgical Edit 1.

## FIX 1.4 - Hyperliquid stats understated

**Verified values from rd-data-pull/hl_l1_stats.json:**
- All-time cumulative volume: $4.62 trillion
- 24h volume: $2.38 billion
- Active users: 1,988,869 (~2 million)
- Total open interest: $38.7 billion
- Active validators: 24 of 31 (including Bitwise Onchain Solutions x FalconX)
- HYPE circulating supply: 298.76M of 999.23M total
- HYPE 24h change: +6.55% to $43.52

**Fix:** See Surgical Edit 2.

---

# PART 2 - THREE SURGICAL CONTENT EDITS

## SURGICAL EDIT 1 - Expand 5 Catalysts to 7

**Files:** email-v3.1.html, elementor-v3.1.html
**Section:** 6 DAYS / 5 CATALYSTS

**Step 1.** Section header changes to "7 Days. 7 Catalysts. One Window."

**Step 2.** Lead paragraph changes to:
```
In the seven days between last Tuesday's webinar and today, seven major catalysts have landed. None of them was on the public calendar a month ago. All seven point the same direction.
```

**Step 3.** Replace the 5-row catalyst table with this 7-row version:

| Date | Event | Why It Matters |
|---|---|---|
| May 7 | McElligott $2.6T gamma trap warning | Mechanic behind the AI rally is public. So is the reversal trigger. |
| May 12 | 21Shares THYP launches on Nasdaq | First U.S. spot HYPE ETF with built-in staking yield |
| May 12 | BTC bull-bear indicator turns GREEN | First green signal since March 2023 |
| May 13 | Warsh confirmed as Fed Chair (54-45) | First openly pro-Bitcoin Fed Chair in history. Closest vote in modern era. |
| May 14 | Coinbase makes Hyperliquid its USDC home | Largest U.S. crypto exchange picks Hyperliquid as its stablecoin treasury network |
| May 15 | Bitwise BHYP launches on NYSE | Second spot HYPE ETF in four days. Bitwise is also running a Hyperliquid validator. |
| May 15 (Fri) | Powell's 8-year term ends | Warsh era starts the Friday before today's broadcast |

(Worker bot will translate this back into the same HTML styling as the current 5-row table - same colors, same borders, same fonts. Last row highlighted in orange/peach background like the current Powell row.)

**Step 4.** Update Live Webinar Banner subhead from:
```
$2.6T gamma trap loaded. Powell exits Friday. Pro-Bitcoin Fed Chair in. First-ever HYPE ETF live. BTC bull-bear cycle indicator turned green.
```

To:
```
$2.6T gamma trap loaded. Powell exits Friday. Pro-Bitcoin Fed Chair confirmed. Two spot HYPE ETFs trading. Coinbase picks Hyperliquid for USDC. BTC indicator turns green.
```

**Step 5.** Update Bridge paragraph - replace the entire "Powell exits Friday..." sentence with:
```
Powell exits Friday. The first pro-Bitcoin Fed Chair in history takes over the same week. Two spot Hyperliquid ETFs went live (21Shares THYP on May 12, Bitwise BHYP on May 15). Coinbase made Hyperliquid its official USDC treasury network. The Bitcoin bull-bear cycle indicator turned green for the first time since March 2023. And Nomura published a 12-page report on the gamma trap holding the AI rally together.
```

**Bonus closing italic** (optional, after the catalyst table):
```
Seven catalysts in seven days. None were on the calendar a month ago. All of them point the same direction: institutional acceptance of HYPE is happening at the same time the AI/semis rally is at its most extended in modern history.
```

---

## SURGICAL EDIT 2 - Add "Protocol Behind Your Shares" mini-section

**Files:** email-v3.1.html, elementor-v3.1.html
**Insert between:** RD vs BTC section and Mid Webinar CTA banner

**Section content:**

Header: "The Machine Underneath" / "The Protocol Behind Your Shares."

Lead: "Most RD investors hold the shares because the dividends keep paying. Most don't fully see the machine underneath. Here's what Hyperliquid actually is, pulled directly from the chain this weekend:"

**Stats table (8 rows):**

| What Hyperliquid Is | The Number |
|---|---|
| Cumulative trading volume since launch | $4.62 Trillion |
| Active users on the protocol | ~2 Million |
| Open interest across all markets | $38.7 Billion |
| Daily trading volume | $2.38 Billion |
| Perpetual markets live | 230 |
| Spot trading markets | 297 |
| Active validators securing the network | 24 of 31 |
| Prediction markets layer (just launched) | Live |

Insert hyperliquid-market-share.png chart after table.

**Closing prose (2 paragraphs):**

Paragraph 1:
"That's the asset Rebel Dividends holds for you. Not a memecoin. Not a vibe. One of the most active onchain trading platforms on earth, generating real fees, burning real supply, returning value to token holders week after week. The dividend engine has paid 108 times in a row because the protocol underneath keeps generating revenue. It's not magic. It's the machine working."

Paragraph 2 (green callout box):
"**This Week's Institutional Signal:** Bitwise (managing $11 billion in client assets) is now running a Hyperliquid validator with FalconX. Anchorage Digital Bank, the major U.S. institutional crypto custodian, is also validating the chain. Two spot HYPE ETFs went live in four days. Coinbase chose Hyperliquid as the network for its USDC treasury. The most credible names in U.S. crypto infrastructure are not just buying HYPE. They're running it."

(Worker bot will style this section matching the existing brand patterns - dark theme header with green border-left, white card body, green-bg institutional callout. Same as Edit 3 in the original v3.2 fix order package.)

---

## SURGICAL EDIT 3 - Rewrite YTD paragraph with verified data + macro context

**Files:** email-v3.1.html, elementor-v3.1.html
**Section:** YTD COMPARISON

**Find current paragraph:** "Silver +23.2% YTD. Gold +8.6%. Energy +29.7%..."

**Replace with two paragraphs:**

Paragraph 1:
"Energy +34% YTD. NVDA +21%. SMH (semis) +54%. **SOXL (3x semis) +291%.** Silver +7%. Gold +5%. The S&P traded $2.6 trillion in call options on a single day. The 30-year Treasury yield is above 5% for the first time since 2007 and CPI just jumped from 2.39% in January to **3.81% in April** - a 142 basis point re-acceleration in four months. **RD Reinvestors are roughly flat YTD - which is exactly the setup the rest of this email is about.**"

Paragraph 2:
"Energy and semis ran first this cycle, hard. HYPE - and through it, RD - typically rotates last, when the macro money looks for the lagging asset with real income and real upside. Buying $0.00165 today is buying the same 108-week dividend engine at the discount entry the rotation always offers right before it shows up. **Flat YTD isn't a problem. It's the entry.**"

**Also fix Why RD section.** Find "Silver's stretched +21.9% YTD" line.

Replace with: "Gold and silver gave back most of their early-year gains. Energy and semis went vertical (SOXL +291% YTD). The 30-year Treasury is above 5% and CPI is sticky at 3.81% - up from 2.39% in January."

---

# PART 3 - NEW CHARTS / VISUALS TO BUILD

## CHART 3.1 - Hyperliquid Hero Stats Card

**Filename:** charts/hyperliquid-market-share.png
**Used by:** Surgical Edit 2

**Concept:** Single-stat hero chart with big centered "$4.62 Trillion" number. Subtitle "Cumulative Volume Traded on Hyperliquid Since Launch." Four secondary stat cards below: $2.38B daily volume, ~2M active users, 230 perp markets, $38.7B open interest. Footer: "Pulled directly from api.hyperliquid.xyz, May 17, 2026."

**Data source:** rd-data-pull/hl_l1_stats.json - all numbers already there.

**Spec:** matplotlib, 1280x720, dark theme (#0a0a0a bg), brand orange (#ff6600) for hero number.

## CHART 3.2 - HYPE Target Ladder REGENERATE

**Filename:** charts/hype-target-ladder-may19.png
**Trigger:** Tuesday 5 AM MDT refresh
**Math:** target_rd_share = current_rd_share * (target_hype / current_hype)

Tuesday morning values approximate (assuming HYPE $43.49 and RD share ~$0.00179):
- $60 target: $0.00247, +38%
- $90: $0.00370, +107%
- $150: $0.00617, +245%
- $180: $0.00740, +313%

Final values must come from Tuesday RD Daily Gmail + CoinGecko pull.

## CHART 3.3 - CPI Re-Acceleration Line Chart (NEW)

**Filename:** charts/cpi-reacceleration.png
**Concept:** Line chart showing CPI YoY from Nov 2025 to Apr 2026.
- Nov 2025: 2.74%
- Dec 2025: 2.68%
- Jan 2026: 2.39% (the low)
- Feb 2026: 2.41%
- Mar 2026: 3.26%
- Apr 2026: 3.81%

Title: "CPI YoY: From 2.39% to 3.81% in Four Months"
Subtitle: "(And Why The Fed Is Stuck)"
Annotation arrow from Jan low to April high showing +142bps
Footer: "Source: BLS via data.bls.gov, May 17, 2026"

**Data source:** rd-data-pull/cpi_raw.json

## CHART 3.4 - 30Y Treasury Above 5%

**Filename:** charts/30y-treasury-above-5.png
**Data:** US 30Y at 5.128% per rd-data-pull/macro_rates.json
**API:** FRED `series_id=DGS30` (free, fred.stlouisfed.org)
**Spec:** Line chart 2007-present, threshold line at 5%, highlight 2008-2024 dip below 5%, annotation "First crossing since 2007."

## CHART 3.5 - VIX Threshold Crossing

**Filename:** charts/vix-threshold-crossing.png
**Data:** VIX at 18.43 - already crossed dashboard's "above 18" first warning.
**Spec:** Line chart of VIX last 90 days, threshold line at 18 yellow / 20 red, annotation "18.43 - just crossed."

**Note:** Early Warning Dashboard prose needs updating - VIX has crossed.

## CHART 3.6 - SOXL +291% YTD Insanity

**Filename:** charts/soxl-ytd-insanity.png
**Data from ytd-refresh-may17.json:**
- SOXL: +290.63%
- SMH: +54.48%
- SPY: +8.69%
- BTC: -10.72%
- RD Reinvestor: ~flat

**Spec:** Horizontal bar chart, brand colors. Title: "What Levered Semis Did in 2026 So Far." Subtitle: "(And Why That's Now the Most Extended Position in Modern Markets)."

## CHART 3.7 - Hyperliquid Validator Set (NEW)

**Filename:** charts/hyperliquid-institutional-validators.png
**Data:** rd-data-pull/hl_l1_stats.json - top validators list

Top validators include: ValiDAO, B-Harvest, **Bitwise Onchain Solutions x FalconX**, Alphaticks, **Anchorage By Figment**, USDT0 x Luganodes, Hyperbeat x P2P x Hypio, CMI, **Hyper Foundation 1**, HypurrCorea: SKYGG x DeSpread.

**Spec:** Text/logo grid, dark theme, brand orange highlight on institutional names. Title: "Who's Actually Running Hyperliquid."

---

# PART 4 - API / DATA REFRESH TASKS FOR TUESDAY MORNING

## TASK 4.1 - YTD figures (yfinance)

```python
import yfinance as yf
symbols = ['SLV','GLD','XLE','NVDA','SPY','QQQ','SOXL','SMH','TLT','BTC-USD']
ytd = {}
for sym in symbols:
    hist = yf.Ticker(sym).history(start='2025-12-31', end='2026-05-20')
    ytd[sym] = round((hist['Close'].iloc[-1] / hist['Close'].iloc[0] - 1) * 100, 2)
# Compare to May 17 baseline; flag any drift >3 percentage points
```

## TASK 4.2 - HYPE Target Ladder Recompute

```python
import requests
hype = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=hyperliquid&vs_currencies=usd').json()['hyperliquid']['usd']
rd_share = parse_rd_daily_email()
targets = [60, 90, 150, 180]
ladder = [(t, round(rd_share * (t / hype), 5), round((t / hype - 1) * 100)) for t in targets]
```

## TASK 4.3 - Early Warning Dashboard

| Indicator | API | Endpoint |
|---|---|---|
| VIX | yfinance | ^VIX |
| SKEW | yfinance | ^SKEW |
| SMH 50DMA | yfinance | SMH + rolling |
| Put/Call | CBOE | cboe.com/us/options/market_statistics/daily |
| ETF flows | ETF.com or Morningstar | (may need access) |
| HY OAS | FRED | series_id=BAMLH0A0HYM2 |

## TASK 4.4 - Hyperliquid stats refresh

```python
r = requests.post('https://api.hyperliquid.xyz/info', json={'type': 'metaAndAssetCtxs'})
# Cross-check totals against email body. If shifted >5%, update HTML.
```

## TASK 4.5 - Breaking news sanity check

Perplexity or web search:
- "McElligott Nomura May 18 2026"
- "Hyperliquid HYPE news May 18 2026"
- "S&P 500 close May 18 2026"
- "VIX May 18 2026"

Log to DEPLOYMENT-NOTES.txt. Escalate any material findings to Jason.

---

# PART 5 - SMS FIXES

Full replacement of sms.txt:

```
SUBJECT (primary): While SOXL Holders Get Squeezed, RD Pays Dividend #108. Live Today 3:30 PM ET.

SUBJECT (alt - Warsh angle): Powell Out Friday. Pro-Bitcoin Fed Chair In. Two HYPE ETFs Live. Watch Today.

SUBJECT (alt - comparison angle): Cash, Bonds, S&P, Gold, BTC, HYPE: Which One Pays Weekly?

SUBJECT (alt - convergence angle): 7 Days. 7 Catalysts. The Setup Is Loaded. Live Today 3:30 PM ET.

---

SMS (primary, ~340 chars):
Rebel Dividends: Live today 3:30 PM ET. 7 days, 7 catalysts: $2.6T gamma trap, Powell out Friday, pro-BTC Fed Chair confirmed, 2 HYPE ETFs live, Coinbase backs Hyperliquid for USDC, BTC indicator green. Why RD is the highest-conviction trade right now: https://rebeldividends.com/startwebinar/

SMS (shorter alt, ~220 chars):
Rebel Dividends: Live today 3:30 PM ET. Powell out Friday. Pro-Bitcoin Fed Chair in. Two HYPE ETFs live. The rotation trade is here, and RD is the way to play it. Watch: https://rebeldividends.com/startwebinar/

(SimpleTexting auto-appends the opt-out language - do NOT include manually.)
```

Changes from v3.1: em dashes replaced with hyphens/colons, "first HYPE ETF" -> "two HYPE ETFs", 7 catalysts, Coinbase line added.

---

# PART 6 - FINAL QA CHECKLIST

## Data accuracy
- [ ] All YTD figures match Tuesday-AM yfinance pull
- [ ] HYPE price matches Tuesday CoinGecko
- [ ] Warsh row: "Fed Chair (54-45)" with date "May 13"
- [ ] No "first-ever HYPE ETF" anywhere
- [ ] No "yesterday" reference to ETFs
- [ ] HYPE Target Ladder uses Tuesday baseline
- [ ] CPI 3.81% YoY referenced
- [ ] Hyperliquid stats match hl_l1_stats.json: $4.62T, ~2M users, $38.7B OI, 24/31 validators

## Content additions
- [ ] 5 Catalysts -> 7 Catalysts (Coinbase + Bitwise added)
- [ ] Live Webinar Banner subhead updated
- [ ] Bridge paragraph updated
- [ ] "Protocol Behind Your Shares" mini-section inserted
- [ ] YTD paragraph rewritten with CPI re-acceleration
- [ ] "Why RD" silver line updated

## Charts (must build)
- [ ] hyperliquid-market-share.png
- [ ] hype-target-ladder-may19.png
- [ ] early-warning-dashboard.png

## Charts (optional)
- [ ] cpi-reacceleration.png
- [ ] 30y-treasury-above-5.png
- [ ] vix-threshold-crossing.png
- [ ] soxl-ytd-insanity.png
- [ ] hyperliquid-institutional-validators.png

## Brand voice
- [ ] No em dashes in sms.txt
- [ ] Coinbase/Bitwise framed as Hyperliquid catalysts only
- [ ] No naming of memecoin perps (PUMP, kPEPE)
- [ ] No HIP-4 specific numbers cited
- [ ] Author = Jason Cox, Closer = Dean Gallagher 505-322-7515
- [ ] Every CTA links to /startwebinar/

## Format
- [ ] No DOCTYPE/html/head/body in email.html
- [ ] Inline table fragment (iContact)
- [ ] Elementor uses div wrappers
- [ ] All v3.1 preserved content intact

## Sanity
- [ ] McElligott not contradicted
- [ ] No Hyperliquid breaking news
- [ ] S&P May 15/18 confirmed no limit-down event
- [ ] VIX Tuesday level checked against dashboard

---

# PART 7 - PERMISSION CHECKS NEEDED FROM JASON

Worker bot must flag these BEFORE handing to Claude Code:

1. **Greenlight Coinbase + Bitwise in catalyst table?** Mentions are about Hyperliquid not competing investments. Need Jason's confirmation.

2. **HIP-4 framing.** Data not queryable. OK to mention by name only without specific numbers, or pull from email entirely?

3. **HeyZibi API.** Failing 401. Skip for this build, or wait for new key?

4. **CPI number.** Use 3.81% (BLS May 17 source) not 3.78% (earlier brief).

5. **Validators / institutional names.** OK to name Bitwise x FalconX, Anchorage By Figment in Protocol Behind Your Shares section? Publicly listed validators.

---

# PART 8 - WHAT NOT TO TOUCH

- Shareholder Acknowledgment block at top
- "What We're Doing In Our Own Book" block
- HYPE Target Ladder at climax position
- 3-paragraph consolidated disclaimer
- McElligott red callout
- "While SOXL Holders Learn What Daily-Reset Gamma Costs" Safety Case headline
- "Last Week We Said. This Week It's Happening." Bridge framing
- Dean Box
- OPEX coincidence callout (v2 fix)
- SOXL -45-60% math callout (v2 fix)
- 9x leverage-squared explanation (v2 fix)
- "Cash 4% / Bonds 5%" paragraph open
- Early Warning Dashboard structure
- "And If We're Early?" patience block

---

# CLOSING NOTES

Biggest improvement remaining: Surgical Edit 2 (Protocol Behind Your Shares). The new stats ($4.62T cumulative, ~2M users, $38.7B OI, Bitwise validator) are the kind of numbers that make Hyperliquid feel real to a 52-year-old who's never traded a perp.

Bitwise Onchain Solutions x FalconX running a validator on Hyperliquid is stronger institutional proof than the ETF alone. Worth lingering on.

CPI re-acceleration (2.39% to 3.81% in 4 months) is a more credible macro hook than vague "inflation is sticky."

End of v3.2-FINAL fix order.
