# RD Tuesday May 19 Webinar — COMPREHENSIVE ITERATION BRIEF (v2 → v3)

**For:** OpenClaw orchestrator + Claude Code CLI
**Generated:** May 13, 2026
**Webinar live:** Tuesday May 19, 2026 — 3:30 PM ET / 1:30 PM MDT
**Working days remaining:** 6 (May 13 PM through May 19 AM)
**Build under iteration:** `outputs/2026-05-19/` (v2 PostFixes — all 9 prior fixes verified in place)

---

## PROJECT CONTEXT

The May 19 webinar package has cleared two passes:
1. **PreBuild** — initial structure, 30 charts, 5 new middle sections inserted
2. **PostFixes (v2)** — 9 specific fixes applied: OPEX coincidence callout, SOXL -45-60% math, 9x leverage-squared, Early Warning Dashboard, SMS subject swap, +169% consistency, disclaimer addendum

**Current state is a B+.** Analytical content is strong. Tone discipline holds. Charts render correctly. Disclaimers responsibly attribute McElligott.

**The gap to A** is audience empathy. The build currently optimizes for *explaining the setup* but doesn't fully optimize for *the existing shareholder reading it Tuesday morning*. This brief closes that gap and stacks additional research, automation, and companion content to make this the strongest package the brand has ever shipped.

**The 6 days we have:**
- May 13 PM — this brief, kick off research delegations
- May 14 — research returns + audit fixes applied (v3 build)
- May 15 — companion content draft (web deep-dive, Wed/Thu/Fri follow-ups), data pipeline build
- May 16 (Sat) — buffer / Jason review
- May 17 (Sun) — buffer / Jason review
- May 18 — final polish, dry run, send tests
- May 19 — Tuesday morning data refresh, deploy, broadcast live

---

# PART 1 — CRITICAL AUDIENCE AUDIT FIXES

These are the seven gaps an existing shareholder reading the email Tuesday morning would feel. Ranked by impact on their experience.

## FIX 1 — Add shareholder acknowledgment block at the top

**Severity:** HIGH
**File:** `email.html` AND `elementor.html`
**Why:** The current opening jumps from stats panel straight to webinar pitch. A shareholder reading this just got paid dividend #108. That's the most important fact in the entire email and it's not surfaced as a personal payoff. They should feel rewarded for being here BEFORE we ask them to watch a webinar.

**Where to insert:** Immediately AFTER the `<!-- ==================== HEADER STATS ==================== -->` block, BEFORE the `<!-- ==================== LIVE WEBINAR BANNER ==================== -->` block.

**Insert this:**

```html
<!-- ==================== SHAREHOLDER ACKNOWLEDGMENT ==================== -->
<tr><td bgcolor="#0a0a0a" style="background-color:#0a0a0a;padding:22px 24px;border-bottom:1px solid #1f2937;">
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="padding:0;">
<div style="font-size:11px;letter-spacing:3px;color:#0a7c42;font-weight:700;text-transform:uppercase;margin-bottom:8px;">Before We Get To The Macro</div>
<div style="font-size:20px;font-weight:700;color:#ffffff;line-height:1.35;margin-bottom:10px;">You Just Collected Dividend #108. For The 108th Time In A Row.</div>
<div style="font-size:15px;line-height:1.7;color:#cbd5e1;">Through a 32% HYPE pullback. Through a Fed regime change. Through what Nomura just called the largest gamma squeeze in S&amp;P options history. <strong style="color:#4ade80;">The dividend engine kept paying.</strong> Every single week, without fail, since the April 2024 pivot. That's not a coincidence &mdash; that's the structure working as designed. The rest of this email is about what comes next. Before we get to it: thank you for being a shareholder.</div>
</td></tr>
</table>
</td></tr>
```

**Elementor version:** same content, replace `<tr><td>` with `<div>` and adjust padding to match flexbox structure.

---

## FIX 2 — Drop the "safest, highest-upside trio" framing

**Severity:** HIGH
**File:** `email.html` AND `elementor.html`
**Section:** Bridge ("Last Week We Said. This Week It's Happening.")
**Why:** Two problems with current copy:
1. "Safest" is too close to "guaranteed" — tone-discipline red flag
2. Recommending BTC + HYPE + RD as a "trio" undermines the rest of the email which argues RD is the *best* vehicle for HYPE exposure

**Where to edit:** Find this current line:
```
Today's broadcast walks through all five &mdash; and then makes the case for why Rebel Dividends, Bitcoin, and Hyperliquid are the safest, highest-upside trio in the market right now.
```

**Replace with:**
```
Today's broadcast walks through all five &mdash; and then makes the case for why Rebel Dividends is the highest-conviction setup we've seen since the April 2024 pivot. Spot HYPE exposure, weekly dividend income, audited entity-level structure, and an entry at $0.00165 going into the most catalyst-dense five-week window of the cycle.
```

---

## FIX 3 — Add "What We're Doing In Our Own Book" block

**Severity:** HIGH
**File:** `email.html` AND `elementor.html`
**Why:** The brand voice list specifically calls for transparency on positioning. The current email tells readers about the setup but never tells them what Jason/the team is actually DOING. Sophisticated investors want this — it's the single most credibility-building piece you can add.

**Where to insert:** New section between the Safety Case and Early Warning Dashboard sections.

**Insert this:**

```html
<!-- ==================== WHAT WE'RE DOING IN OUR BOOK ==================== -->
<tr><td bgcolor="#ffffff" style="background-color:#ffffff;padding:30px 24px 8px 24px;">
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:16px;">
<tr><td bgcolor="#0a7c42" style="background-color:#0a7c42;padding:14px 18px;border-left:6px solid #4ade80;">
<div style="font-size:11px;letter-spacing:2px;color:#a7f3d0;font-weight:700;text-transform:uppercase;margin-bottom:4px;">Full Transparency</div>
<div style="font-size:22px;font-weight:700;color:#ffffff;line-height:1.3;">What We're Doing In Our Own Book This Week.</div>
</td></tr>
</table>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:14px;">Because nothing in this email is theoretical for us &mdash; we're shareholders too &mdash; here's how we're positioning into the five-week window:</div>

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;border:1px solid #e0e0e0;margin-bottom:14px;">
<tr style="background:#0a0a0a;">
<td style="padding:10px;border:1px solid #333;font-size:13px;color:#ff6600;font-weight:700;width:30%;">Action</td>
<td style="padding:10px;border:1px solid #333;font-size:13px;color:#ff6600;font-weight:700;">Details</td>
</tr>
<tr>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;font-weight:700;background:#f0fff4;">Not selling any RD</td>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;">Spot exposure stays. Dividends keep compounding through whatever happens.</td>
</tr>
<tr style="background:#f8f8f8;">
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;font-weight:700;">Added at $0.00163 last week</td>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;">Cheapest entry since Q4 2024. Sized as a standard add, not a swing.</td>
</tr>
<tr>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;font-weight:700;">Watching $0.00148 for aggressive adds</td>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;">If HYPE retests $35-37 zone, that's where we deploy meaningful capital.</td>
</tr>
<tr style="background:#f8f8f8;">
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;font-weight:700;">Reinvest setting: ON</td>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;">Compounding through the volatility is the whole edge. Don't break it.</td>
</tr>
<tr>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;font-weight:700;background:#fff8f3;">Trimming if needed: SOXL, TQQQ, levered tech</td>
<td style="padding:10px;border:1px solid #e0e0e0;font-size:13px;">Not advice for yours. If you hold these, the math in the Safety Case section applies.</td>
</tr>
</table>

<div style="font-size:14px;line-height:1.65;color:#475569;background:#f8f8f8;border-left:4px solid #cbd5e1;padding:12px 14px;margin-bottom:18px;font-style:italic;">This is how we're playing it. Not advice for your portfolio &mdash; your tax situation, risk tolerance, and timeline are different from ours. But you asked what we're doing, and we're telling you.</div>
</td></tr>
```

**Note:** The specific entry prices ($0.00163, $0.00148) need verification with Jason before final ship. These are illustrative. Substitute his actual positions if different.

---

## FIX 4 — Move HYPE Target Ladder to climax position

**Severity:** HIGH (biggest structural change)
**File:** `email.html` AND `elementor.html`
**Why:** Currently the HYPE Target Ladder sits at position 5 (between RD vs BTC and the mid-CTA), before the gamma trap thesis is even built. The payoff arrives before the setup. Readers see the upside math before they understand why it would happen — which dampens the impact.

**Restructure to this section order:**

1. Header stats (existing)
2. **NEW: Shareholder acknowledgment block** (Fix 1 — dark, between stats and webinar banner)
3. Live Webinar Banner (existing)
4. Bridge: "Last Week We Said. This Week It's Happening." (existing, with Fix 2 edit)
5. YTD Comparison (existing)
6. RD vs BTC Since Pivot (existing)
7. ~~HYPE Target Ladder~~ ← REMOVE FROM HERE
8. Mid Webinar CTA (existing orange banner)
9. 6 Days / 5 Catalysts urgency block (existing)
10. What Changed This Week — Gamma Trap (existing, with OPEX callout from v2)
11. Why RD Is The Best Investment (existing)
12. The Safety Case — SOXL vs RD (existing, with -45-60% callout from v2)
13. **NEW: What We're Doing In Our Own Book** (Fix 3)
14. Early Warning Dashboard (existing v2 addition)
15. Forward Macro Framework + Catalyst Calendar (existing)
16. **MOVED HERE: HYPE Target Ladder** — now the climax
17. Performance Stats (existing)
18. CTAs (existing)
19. Dean Box (existing)
20. Disclaimer (existing, with Fix 5 consolidation below)

**Mechanical change:** Cut the entire HYPE Target Ladder section (the `<!-- ==================== REINVESTOR ADVANTAGE TABLE ==================== -->` block, currently at lines ~73-86 in email.html, including the table AND the chart) and paste it AFTER the Forward Macro Framework section (after the catalyst calendar image), BEFORE the Performance Stats section.

**Also update the section header at the new location.** The current header reads:
```
<div style="...">HYPE Target Ladder</div>
<div style="...">What Each Side Gets at Each HYPE Level</div>
```

Replace with:
```html
<div style="font-size:11px;letter-spacing:2px;color:#ff6600;font-weight:700;text-transform:uppercase;margin-bottom:8px;">The Math At The End Of The Setup</div>
<div style="font-size:22px;font-weight:700;color:#000000;line-height:1.3;margin-bottom:14px;">If The Rotation Plays Out: What Your RD Position Becomes At Each HYPE Level.</div>
```

This framing positions the ladder as the *consequence* of everything they just read, not a standalone teaser.

---

## FIX 5 — Consolidate disclaimer paragraphs (5 → 3)

**Severity:** MEDIUM
**File:** `email.html` AND `elementor.html`
**Why:** Five separate disclaimer paragraphs read as defensive. Each is reasonable individually; together they signal anxiety. The three forward-looking analytical carve-outs (McElligott, comparison table, early warning) can be merged into one with no loss of legal protection.

**Find these three existing paragraphs:**
1. `<strong>McElligott / Nomura attribution.</strong>`
2. `<strong>Comparison-table carve-out.</strong>`
3. `<strong>Early warning indicators carve-out.</strong>`

**Replace all three with this single consolidated paragraph:**

```html
<p style="margin:0 0 10px 0;"><strong>Forward-looking analysis disclosure.</strong> This email contains analysis of macroeconomic conditions, derivatives flows, levered ETF mechanics, asset class comparisons, and market indicators. Specific references include: Nomura Securities research from Charlie McElligott (May 7, 2026 ZeroHedge report) on gamma exposure, dealer hedging, and levered ETF rebalance mechanics &mdash; Rebel Dividends does not have direct access to Nomura's proprietary research; the "Nasdaq limit-down" and "SMH -15% to -20% single session" scenarios are McElligott's stated analysis, not predictions by Rebel Dividends Corporation. Asset class comparisons (cash, bonds, equities, gold, silver, energy, crypto, levered products) are illustrative and reflect Rebel Dividends Corporation's views, not recommendations for any individual investor. The six market indicators in the "What We're Watching" section are publicly observable signals; a signal crossing a threshold does not guarantee any specific outcome. Any decision to sell, trim, rotate, or add any portfolio position depends on your tax situation, risk tolerance, and timeline. Consult your advisor before acting on anything in this email.</p>
```

Keep the existing **Performance disclosure** and **Fee & tax structure** paragraphs as separate. Final disclaimer count: 3 paragraphs (down from 5).

---

## FIX 6 — Soften Early Warning Dashboard "flashing red yet" assumption

**Severity:** MEDIUM (Tuesday-morning risk)
**File:** `email.html` AND `elementor.html`
**Section:** Early Warning Dashboard
**Why:** Current copy: *"None of them is flashing red yet — but the window when they could starts Friday."* If Tuesday morning one IS flashing yellow or red, this copy is wrong. We don't yet know Tuesday's readings.

**Find:**
```
These are the indicators that flip first when dealer gamma starts to unwind. We're tracking them every morning. None of them is flashing red yet &mdash; but the window when they could starts Friday and runs through the first Warsh FOMC (June 17). When two or more turn yellow, the rotation accelerates.
```

**Replace with:**
```
These are the indicators that flip first when dealer gamma starts to unwind. We're tracking them every morning. Tuesday's current readings are shown above &mdash; by the time you watch the webinar, two of them may already have moved. The window when they could turn yellow or red starts Friday and runs through the first Warsh FOMC on June 17. When two or more turn yellow, the rotation accelerates.
```

---

## FIX 7 — Cut victory-lap "you'll know we flagged them on May 19" line

**Severity:** LOW (brand voice)
**File:** `email.html` AND `elementor.html`
**Section:** Early Warning Dashboard footer
**Why:** *"When you see them, you'll know what they mean — and you'll know we flagged them on May 19."* This pre-loads a victory lap before anything has happened.

**Find:**
```
These are the canaries professional desks watch. Not predictions. Indicators. When you see them, you'll know what they mean &mdash; and you'll know we flagged them on May 19.
```

**Replace with:**
```
These are the canaries professional desks watch. Not predictions. Indicators. When you see them move, you'll know what they mean.
```

---

# PART 2 — RESEARCH DELEGATIONS

The audit fixes above are mechanical. These tasks deepen the analytical foundation by pulling fresh, cited, multi-source data. Each task is assigned to the AI/API best suited.

## 2A — Gemini Deep Research tasks

**Why Gemini Deep Research:** Long-context multi-source synthesis. Best for producing 5-10 page research briefs from 50+ source documents.

### Task G1 — Gamma trap historical precedents brief
**Output:** 4-6 page research brief titled `research/gamma-precedents-brief.md`
**Prompt to give Gemini:**
> Produce a research brief on the four most significant gamma-unwind episodes in U.S. equities since 2018: (1) February 2018 Volmageddon / XIV blowup, (2) March 2020 COVID-19 crash, (3) August 2024 yen carry unwind / VIX spike to 65, (4) any 2025 events. For each, provide: the precise trigger event with date and time, the speed of unwind (peak-to-trough hours), the underlying gamma positioning data (call notional, levered ETF AUM, dealer positioning at the time vs. May 2026 current), the specific assets that fell hardest with percentages, the Fed response timing, and the recovery arc. Include direct quotes from Charlie McElligott (Nomura), Marko Kolanovic (formerly JPM), and Brent Donnelly (Spectra Markets) describing each event. Cite all sources with URLs. End with a one-paragraph comparison framework: how does May 2026's positioning compare to each historical setup?

**Use:** Feeds Section 10 (gamma trap explainer) with a "historical pattern match" callout. Also valuable for webinar live talking points.
**Deadline:** May 14 EOD

### Task G2 — Hyperliquid Q1 2026 comprehensive financial deep-dive
**Output:** 6-8 page brief titled `research/hyperliquid-q1-deepdive.md`
**Prompt:**
> Compile every publicly available financial and operational metric for Hyperliquid from January 1, 2026 through April 30, 2026. Include: revenue (daily, weekly, monthly), trading volume (perpetual swaps, spot), active addresses, new wallet creations, buyback pace and total HYPE destroyed cumulatively (including HIP-3 expansion), market share vs. dYdX/GMX/Aevo/Drift, HIP-3 single-stock perp launch performance (NVDA, AMD, S&P perps), HIP-4 prediction market launches and volumes, validator economics and staking yields, treasury holdings, Hyperliquid Strategies (PURR) Q1 financial reports including net profit and HYPE position. Source from: hyperliquid.xyz official posts, Hyperliquid Foundation blog, on-chain explorers (Hyperscan), Dune Analytics dashboards, Token Terminal, Messari, Delphi Digital, Galaxy Digital reports. Cite all sources. End with: how does Hyperliquid's revenue per employee compare to Coinbase, Binance, dYdX, and the most profitable traditional tech companies?

**Use:** Powers a new "The Asset We Own" mini-section, plus Wed/Thu/Fri follow-up content.
**Deadline:** May 15 EOD

### Task G3 — Kevin Warsh public statement compendium
**Output:** 3-5 page brief titled `research/warsh-statement-compendium.md`
**Prompt:**
> Compile every public statement, speech, op-ed, podcast appearance, congressional testimony, and Fed-related publication by Kevin Warsh from his original Fed governorship (2006-2011) through his nomination and confirmation in 2026. Organize by theme: (1) inflation and price stability, (2) Bitcoin and digital assets, (3) monetary policy framework and "regime change," (4) Fed independence, (5) financial stability. For each, provide the exact quote, date, source URL, and context. Pay special attention to: every Bitcoin/crypto reference, every statement about lower interest rates, every comment about ending "telegraphing" of Fed decisions, every comment about Powell-era Fed policy. End with: a structured prediction of how a Warsh-led Fed would likely communicate differently than Powell, with direct supporting quotes.

**Use:** Section 8 (6 Days / 5 Catalysts) Warsh row, plus webinar talking points, plus Thursday /macro/ promo email.
**Deadline:** May 15 EOD

### Task G4 — Levered ETF graveyard / blowup history
**Output:** 2-3 page brief titled `research/levered-etf-graveyard.md`
**Prompt:**
> Compile a comprehensive list of every U.S.-listed leveraged ETF (2x or 3x in either direction) that has been delisted, reverse-split, or experienced a single-day drawdown greater than 30% since 2020. For each: ticker symbol, issuer, leverage factor, underlying index, date of event, peak AUM before event, what happened (delisted/reverse-split/just dropped), recovery (if any), and the specific market conditions that triggered it. Pay special attention to: UWT/DWT (oil, March 2020), DUST/JNUG (gold miners), JDST/JNUG (junior miners), LABD/LABU (biotech), and any 3x semis/tech products. Source from: SEC EDGAR, ETF.com archives, Direxion/ProShares investor relations, Bloomberg ETF research, etf-database.

**Use:** Adds credibility to Section 12 (Safety Case) — instead of theoretical SOXL math, show actual historical precedent.
**Deadline:** May 15 EOD

### Task G5 — McElligott full quote bank (last 90 days)
**Output:** 4-6 page brief titled `research/mcelligott-quote-bank.md`
**Prompt:**
> Compile every publicly available McElligott (Nomura) commentary, note, podcast appearance, Bloomberg interview, ZeroHedge citation, Heisenberg Report citation, and X/Twitter post from February 1, 2026 through May 13, 2026. Organize chronologically. For each: date, source URL, full direct quote, surrounding context, the specific data points referenced. Pay special attention to anything mentioning: gamma exposure, dealer positioning, levered ETF flows, call notional records, VIX dynamics, SKEW, "limit down" scenarios, the "$2.6 trillion" figure, "Pretty Damn Real Delta," Warsh nomination, Iran/Hormuz risks, CTA positioning, vol regime shifts. Flag any McElligott commentary that contradicts or modifies the May 7 ZeroHedge framing.

**Use:** Verifies our McElligott attribution is current and complete. May surface follow-up notes that strengthen or update the email's framing.
**Deadline:** May 14 EOD

---

## 2B — ChatGPT / Perplexity tasks

**Why Perplexity:** Real-time cited search with current-event awareness. Best for Tuesday morning data refreshes and verification of specific facts.
**Why ChatGPT:** Quick analytical work, code generation, alternative framings, second-opinion drafting.

### Task P1 — Tuesday morning data refresh script
**Run on:** Tuesday May 19, 5:00 AM MDT
**Tool:** Perplexity Pro or direct API calls
**Pulls needed:**
- VIX 1-month current level (CBOE)
- CBOE SKEW Index current level
- SMH price + 50-day moving average (status: above/below)
- CBOE equity put/call ratio (current day)
- SOXL + TQQQ 5-day net flows (ETF.com or Morningstar)
- HYG OAS or 10Y minus equivalent risk-free spread (FRED or Bloomberg)
- HYPE price (CoinGecko + Coinbase + CMC, average)
- BTC price (CoinGecko)
- Daily McElligott check: any new note from him in the last 48 hours

**Output:** `tuesday-morning-data-may19.json` with all values + status colors (green/yellow/red per dashboard logic).

**Use:** Auto-feeds the early warning dashboard chart regeneration + replaces all `<!-- PLACEHOLDER -->` values in email/elementor HTML.

### Task P2 — Saylor / Strategy disclosure verification + BTC ETF flows
**Tool:** Perplexity
**Prompt:**
> What has Michael Saylor / Strategy (formerly MicroStrategy) disclosed about Bitcoin treasury operations between May 1, 2026 and May 19, 2026? Include: latest total BTC holdings, recent purchase announcements with dates and average prices, the "Stretch credit engine" disclosure detail (May 12, 2026), any new product launches, public statements by Saylor on X/Twitter. Also: what have the U.S. spot Bitcoin ETFs (IBIT, FBTC, ARKB, BITB, etc.) shown in net flows for each trading day from May 1, 2026 through May 18, 2026? Source from CoinDesk, The Block, Farside Investors, BitcoinTreasuries.net, and Strategy investor relations.

**Output:** `research/saylor-btc-etf-update.md`
**Use:** Refreshes BTC indicator green callout + Saylor row in 6 Days / 5 Catalysts table.

### Task P3 — THYP ETF first-week performance
**Tool:** Perplexity
**Prompt:**
> What has 21Shares THYP (Hyperliquid spot ETF) shown in trading performance since its Nasdaq launch on May 12, 2026? Include: daily trading volume, AUM evolution, NAV vs HYPE spot price tracking, any institutional disclosures, news coverage from BeInCrypto, CoinDesk, ETF.com, Nasdaq Trader, and Bloomberg. Compare first-week performance to other recent crypto ETF launches (spot BTC ETFs in January 2024, spot ETH ETFs in 2024).

**Output:** `research/thyp-first-week.md`
**Use:** Powers a potential new "THYP Is Already Working" callout if data supports it, or holds the existing THYP row in 5 Catalysts table accurate.

### Task P4 — Alternative framings for "What We're Doing In Our Book" block
**Tool:** ChatGPT (or Claude Opus second-pass)
**Prompt:**
> I have a draft "What We're Doing In Our Own Book" block for an investor email (text below). The brand voice is: transparent, conversational, never hyped, no "we called the top" language, prefers "smart time to take profits" over "sell," prefers "what we're doing with our own book" over "you should do this." The audience is high-net-worth retail investors who own Rebel Dividends shares. Draft three alternative framings of this block, each with different tone/structure: (1) more conversational, less table-heavy, (2) more numeric/precise with exact share counts and dollar amounts, (3) more philosophical/educational about position sizing through volatility.

**Output:** `research/whats-in-our-book-alternates.md`
**Use:** Jason picks the best framing or merges elements. The current Fix 3 draft is the table-heavy version.

---

## 2C — Direct API pulls (for automation pipeline)

These should be added to `pipeline/tuesday_morning_refresh.py` as scheduled calls.

| API | Endpoint / Use | Data Returned |
|---|---|---|
| CoinGecko Pro | `/coins/hyperliquid` and `/coins/bitcoin` | Price, 24h change, market cap, volume |
| CoinMarketCap | `/cryptocurrency/quotes/latest?symbol=HYPE,BTC` | Backup price + ranking |
| CBOE Direct | `/v1/data/options/vix` and `/v1/data/options/skew` | VIX 1mo, VIX 3mo, SKEW |
| Alpha Vantage | `query?function=GLOBAL_QUOTE&symbol=SMH` | SMH price + 50DMA via separate technical indicator call |
| ETF.com (scrape) or Morningstar API | SOXL, TQQQ daily flow data | Net inflow/outflow |
| FRED | `series_id=BAMLH0A0HYM2` | HY OAS spread |
| Twitter/X API v2 | Search "from:zerohedge OR from:hkuppy" (McElligott RT account), last 24hr | McElligott new commentary check |
| Hyperscan / Dune | Hyperliquid on-chain metrics | Active addresses, volume, buyback pace |

**Build target:** `pipeline/tuesday_morning_refresh.py` with `--date YYYY-MM-DD` argument that:
1. Pulls all of the above
2. Writes `tuesday-morning-data-{date}.json`
3. Regenerates `early-warning-dashboard.png` with current readings
4. Regenerates `reinvestor-chart-{date}.png` with Tuesday's actual share price from RD Daily Gmail
5. Patches all `<!-- PLACEHOLDER -->` values in email.html and elementor.html
6. Outputs ready-to-deploy zip

**Deadline:** Script ready by May 16 EOD so we have buffer for testing.

---

# PART 3 — NEW CONTENT / CHART ADDITIONS

Based on the research returns, these are additions that would meaningfully strengthen the email if the data supports them. Build conditionally — i.e., only add if the research actually backs the claim.

## 3A — "Historical Pattern Match" callout in gamma trap section

**Trigger:** If Gemini G1 returns clear data comparing May 2026 positioning to Feb 2018 / March 2020 / August 2024 setups.

**New chart asset:** `charts/historical-gamma-precedents.png`
**Spec:** Side-by-side 4-panel comparison. Each panel: one historical event with date, trigger, peak-to-trough hours, max single-day drawdown, current S&P comparison row. Dark theme matching brand.

**Insert location:** Gamma trap section, AFTER the existing 2-image stack of `sp-call-volume-record.png` and `levered-etf-aum-growth.png`.

## 3B — "The Asset We Own" mini-section between RD vs BTC and the existing flow

**Trigger:** If Gemini G2 returns strong Hyperliquid Q1 financial data.

**Purpose:** Counter the implicit "but HYPE is risky" objection. Show that the underlying asset is one of the most profitable financial protocols ever built.

**Content:** Brief 2-3 paragraph section showing: Hyperliquid Q1 revenue, profit margin, market share growth, buyback pace, single-employee productivity stat. Anchored by one new chart: `charts/hyperliquid-vs-fintechs.png` showing revenue-per-employee comparison.

**Insert location:** After RD vs BTC Since Pivot section, before HYPE Target Ladder (in new climax position).

## 3C — "SOXL Graveyard" historical examples in Safety Case

**Trigger:** If Gemini G4 returns specific levered ETF blowup cases.

**Purpose:** Strengthen Safety Case with actual historical precedent, not just McElligott math.

**Content:** 3-row mini-table showing UWT/DWT (March 2020 oil), JDST (any major event), and one tech-adjacent example. Each row: ETF, leverage, what happened, peak AUM lost, recovery status.

**Insert location:** Safety Case, between the SOXL -45-60% callout and the existing 6-row comparison table.

## 3D — Hero card refresh for any data that's stale

If any of the existing 15 hero number cards have data that's outdated by Tuesday (e.g., HYPE price ladder hero, or "108 weeks" if a daily counter exists), regenerate them with Tuesday morning values.

---

# PART 4 — COMPANION CONTENT PRODUCTION

The email is the appetizer. These are the other deliverables for the full Tuesday-through-Friday content stack.

## 4A — Long-form web deep-dive: `/daily/2026-05-25`

**URL target:** `https://updates.rebeldividends.com/daily/2026-05-25`
**Length target:** 3,500-5,000 words
**Build target:** Vercel-hosted Next.js page

**Structure:**
1. Hero — full version of the email's opening, dark theme
2. Section: "What Just Happened — The Five-Catalyst Convergence" (longer version of 6 Days / 5 Catalysts)
3. Section: "The Gamma Trap Explained For Non-Quants" — 1,200 word primer with embedded historical precedents from Gemini G1
4. Section: "Why Warsh Matters" — 800 words from Gemini G3 + market reaction analysis
5. Section: "Hyperliquid Is The Asset" — 1,000 words from Gemini G2
6. Section: "Why We Built Rebel Dividends" — origin story, the pivot, why this structure is unique
7. Section: "What We're Doing With Our Own Book" — expanded version of the email block
8. Section: "What We're Watching" — Early Warning Dashboard with daily-refresh component
9. Section: "The Math At The End" — HYPE Target Ladder with interactive HYPE-price slider component (if engineering bandwidth)
10. Footer CTA: Watch the webinar, talk to Dean, full disclaimer

**Build by:** May 16 EOD (so it's live before the webinar Tuesday)

## 4B — Webinar live show talking points / script

**Output:** `webinar/may19-talking-points.md`
**Length:** 60-minute show structure with timing

**Structure (60 min):**
- 0:00-3:00 — Open. Welcome shareholders. Acknowledge dividend #108. Frame the week.
- 3:00-12:00 — The Five Catalysts: walk through each with chart pulls
- 12:00-25:00 — The Gamma Trap Explained: full McElligott walkthrough + historical precedents
- 25:00-32:00 — The Safety Case: SOXL math, levered ETF graveyard
- 32:00-40:00 — What We're Doing In Our Own Book: full transparency, Q&A teaser
- 40:00-48:00 — The Math: HYPE target ladder with HYPE-price slider live demo
- 48:00-55:00 — Forward Macro: 5 pillars + catalyst calendar
- 55:00-60:00 — Live Q&A intro + Dean handoff

**Include:**
- Anticipated Q&A topics with prepared answers (10-15)
- Backup slides for technical issues
- Specific quotes/data points to memorize
- Tone reminders (no "we called the top," etc.)

**Build by:** May 17 EOD

## 4C — Wed/Thu/Fri follow-up email packages

These reference Tuesday's webinar and extend the narrative.

### Wed May 20 — Webinar Replay Drive
- Subject ideas: "Replay: The 6 Charts That Show The Gamma Trap" / "If You Missed Yesterday's Show, This Is The 4-Minute Version"
- CTA: rebeldividends.com/startwebinar/
- Content: Brief recap of the 5 catalysts, embed 3-4 key charts from Tuesday, push to replay
- Length target: 60% of Tuesday's email length

### Thu May 21 — /macro/ Promo
- Subject ideas: "The Pro-Bitcoin Fed Chair Just Took Over. Here's The 5-Pillar Macro Framework." / "Warsh's First Week. The Macro Setup Goes Live."
- CTA: rebeldividends.com/macro/
- Content: Deep on the 5-pillar framework, lean on Gemini G3 Warsh research, anchor on Section 14 from Tuesday
- Length target: 50% of Tuesday's email length

### Fri May 22 — /forward/ $150 Math
- Subject ideas: "Weekend Math: $0.00165 To $0.00619 — Here's The Path" / "5 Hours Of Reading For The Weekend"
- CTA: rebeldividends.com/forward/
- Content: HYPE Target Ladder expanded with reasoning for each level, lean on Gemini G2 Hyperliquid Q1 data
- Length target: 50% of Tuesday's email length

**Build all three by:** May 16 EOD (so we're not scrambling during the week)

## 4D — SMS sequences

Already in the v2 build (sms.txt). For Wed/Thu/Fri:
- Wed: 2 SMS variants pushing webinar replay
- Thu: 2 SMS variants pushing /macro/
- Fri: 2 SMS variants pushing /forward/

**Build by:** May 17 EOD

---

# PART 5 — TUESDAY MORNING AUTOMATION

The goal: minimize human intervention on Tuesday morning. Jason wakes up, reviews, approves, and clicks send.

## 5A — Master refresh pipeline

**File:** `pipeline/tuesday_morning_refresh.py`
**Trigger:** Cron job at 5:00 AM MDT on May 19, 2026
**Steps:**
1. Pull RD Daily Gmail (5:30 AM expected delivery) — extract Share Price, Day-over-Day Return
2. Hit all APIs listed in Section 2C
3. Compute dashboard status (green/yellow/red) for each of 6 indicators
4. Regenerate `early-warning-dashboard.png` with current readings
5. Regenerate `reinvestor-chart-may19.png` with Tuesday share price
6. Regenerate `hype-target-ladder-may19.png` if HYPE moved >5% from $40 baseline
7. Patch all PLACEHOLDER values in `email.html` and `elementor.html`
8. Run sanity checks (all 15 items from DEPLOYMENT-NOTES.txt)
9. Zip the final package
10. Telegram to Jason at 6:30 AM MDT

## 5B — Telegram bot handoff

Existing OpenClaw → Telegram bot. Verify the zip handoff fires correctly on Tuesday morning. Test fire on Monday May 18 to confirm.

## 5C — Verification dry run on Monday May 18

Run the full Tuesday automation on Monday afternoon with Monday's data. Confirm:
- All APIs returning data
- All charts regenerating without errors
- HTML patches landing correctly
- Sanity checks passing
- Zip + Telegram firing

---

# PART 6 — TONE / BRAND DISCIPLINE REMINDERS

For Claude Code and all downstream content production. Re-paste these into every research delegation.

## DO use:
- "Smart time to take profits"
- "Add to RD on the dip"
- "What we're doing with our own book"
- "Nomura's McElligott sees the trigger as…"
- "The asymmetric setup"
- "Not advice for yours"
- "Our analysis"
- "Through every drawdown, the dividend engine kept paying"
- "108 consecutive weeks"
- "Spot exposure, no leverage, no daily reset"
- "The structure working as designed"

## DO NOT use:
- "We called the top"
- "Sell gold / sell silver / sell energy"
- "The crash is coming"
- "Guaranteed returns"
- "Safest investment"
- "Trust us"
- "Massive gains"
- "Don't miss this"
- Any phrasing that sounds like a hype merchant or victory lap
- Any "you'll thank us later" pre-loading

## Branded contacts:
- Author of all content: **Jason Cox**
- Closer/CTA only: **Dean Gallagher, 505-322-7515, dean@rebeldividends.com**
- Entity: Rebel Dividends Corporation

## Hard formatting rules:
- Email: inline table fragment, NO `<!DOCTYPE>` / `<html>` / `<head>` / `<body>` tags (iContact requirement)
- Elementor: same content in `<div>` wrappers, flexbox OK
- Day% color: green `#4ade80` positive, red `#c41e3a` negative
- Dean box: black 2px border on grey `#f8f8f8`, centered
- SimpleTexting auto-appends "Reply STOP" — never include manually
- Share price: ONLY source is the RD Daily Gmail. Never calculate. Never use API.

---

# PART 7 — 6-DAY TIMELINE

| Date | Tasks | Owner | Deliverable |
|---|---|---|---|
| **May 13 PM** (today) | Kick off all Gemini Deep Research tasks (G1-G5) | OpenClaw | 5 research jobs initiated |
| **May 13 PM** | Kick off Perplexity tasks P1 prep, P2, P3 | OpenClaw | 3 perp queries running |
| **May 13 PM** | Apply Audit Fixes 1-7 (this brief, Part 1) | Claude Code | v3 build |
| **May 14 AM** | Review v3 build | Jason + Claude Opus | Sign-off or revise |
| **May 14 PM** | Gemini G1, G5 returns; integrate findings into v3 if applicable | OpenClaw | v3.1 build |
| **May 14 PM** | Start Tuesday morning refresh script build | Claude Code | `tuesday_morning_refresh.py` skeleton |
| **May 15 AM** | Gemini G2, G3, G4 returns | OpenClaw | Research artifacts saved |
| **May 15 AM** | Build /daily/2026-05-25 long-form web page | Claude Code | Web page deployed staging |
| **May 15 PM** | Build refresh script API integrations | Claude Code | All APIs returning data |
| **May 15 PM** | Add Section 3A/B/C if research supports | Claude Code | v3.2 build with new charts |
| **May 16** | Build Wed/Thu/Fri follow-up email packages | Claude Code | 3 zipped packages |
| **May 16** | Buffer / Jason deep review | Jason | Comments + revisions queued |
| **May 17** | Build webinar talking points / script | Claude Code + Jason | `may19-talking-points.md` |
| **May 17** | Build SMS sequences for Wed/Thu/Fri | Claude Code | 3 SMS files |
| **May 18** | Final polish v3.3 | Claude Code | Production-ready package |
| **May 18** | Monday refresh dry-run | OpenClaw | Pipeline verified |
| **May 18 PM** | Send tests to Jason / Ryan / Dean | OpenClaw | 3 email tests, 3 SMS tests |
| **May 19 5:00 AM MDT** | Tuesday morning refresh fires | Cron + OpenClaw | Final zip |
| **May 19 6:30 AM MDT** | Telegram zip to Jason | OpenClaw | Jason approval |
| **May 19 9:00 AM MDT** | Ryan deploys email + elementor + SMS + web page | Ryan | Live |
| **May 19 3:30 PM ET / 1:30 PM MDT** | Webinar broadcast | Jason + Dean | Live show |
| **May 19 4:30 PM ET** | Webinar ends, replay activates | Jason + Ryan | Replay link live |

---

# PART 8 — FINAL QA / SANITY CHECKLIST (v3.3 PRE-SEND)

Run all of this before the May 18 PM test send. Each line must pass.

## Content
- [ ] Shareholder acknowledgment block present at top
- [ ] "Trio" framing removed; replaced with singular RD pitch
- [ ] "What We're Doing In Our Own Book" section present
- [ ] HYPE Target Ladder moved to climax position
- [ ] Disclaimers consolidated to 3 paragraphs (Forward-looking analysis + Performance + Fee & tax)
- [ ] Early Warning Dashboard preamble softened (no "flashing red yet" assumption)
- [ ] Victory-lap "you'll know we flagged them" line removed
- [ ] May 15 OPEX coincidence callout present (v2 carryover)
- [ ] SOXL -45 to -60% callout present (v2 carryover)
- [ ] 9x leverage-squared fact present (v2 carryover)
- [ ] Reinvestor return = +169% across all references

## Research-driven additions (conditional)
- [ ] Historical Gamma Precedents callout present (if G1 supports)
- [ ] Hyperliquid Q1 mini-section present (if G2 supports)
- [ ] Levered ETF graveyard table present (if G4 supports)
- [ ] Warsh expanded quote in 5 Catalysts row (if G3 surfaces strong quote)

## Brand voice scan
- [ ] No "we called the top" anywhere
- [ ] No "sell gold/silver/energy" anywhere
- [ ] No "guaranteed" / "guaranteed returns" anywhere
- [ ] No "trust us" / "don't miss this" anywhere
- [ ] "Smart time to take profits" or equivalent present where appropriate
- [ ] "Not advice for yours" present in What We're Doing block

## Format
- [ ] No `<!DOCTYPE>` / `<html>` / `<head>` / `<body>` in email.html
- [ ] Inline tables only in email.html
- [ ] Dean box: 2px black border on `#f8f8f8`, centered
- [ ] All Day% values: green `#4ade80` positive / red `#c41e3a` negative
- [ ] Webinar live time: 3:30 PM ET / 1:30 PM MDT
- [ ] Date: Tuesday May 19, 2026, Week 108

## Data
- [ ] Tuesday share price from RD Daily Gmail (replaces $0.00165 placeholder)
- [ ] Tuesday Day-over-Day Return populated (replaces "TBD")
- [ ] HYPE and BTC prices from Tuesday morning API pull
- [ ] All 6 dashboard readings populated (not "TBD")
- [ ] Dashboard chart regenerated with Tuesday values + correct color dots
- [ ] Reinvestor chart regenerated with Tuesday share price
- [ ] HYPE target ladder recomputed if HYPE moved >5%

## SMS / Subject
- [ ] Primary subject: "While SOXL Holders Get Squeezed, RD Pays Dividend #108. Live Today 3:30 PM ET."
- [ ] 3 alt subjects present
- [ ] SMS body under 320 chars (primary)
- [ ] No "Reply STOP" in SMS body

## URLs
- [ ] rebeldividends.com/startwebinar/ — verify resolves
- [ ] rebeldividends.com/macro/ — verify resolves
- [ ] rebeldividends.com/forward/ — verify resolves
- [ ] updates.rebeldividends.com/daily/2026-05-25 — verify deployed
- [ ] All chart image URLs return 200 OK

## Deliverables
- [ ] email.html (table fragment, no DOCTYPE)
- [ ] elementor.html (div wrappers)
- [ ] sms.txt
- [ ] charts/ folder (31+ PNGs depending on conditional additions)
- [ ] DEPLOYMENT-NOTES.txt with updated checklist
- [ ] Zip created with correct naming: `RD-Tue-May19-v3.3-FINAL.zip`
- [ ] Telegram fire to Jason successful

---

# APPENDIX — PASTE-READY SNIPPETS

All HTML snippets in this brief are formatted to match the existing build's styling conventions. Drop them directly into the file using the section markers (`<!-- ==================== SECTION NAME ==================== -->`) for location.

**Existing color tokens used:**
- Background dark: `#000000`, `#0a0a0a`
- Background light: `#ffffff`, `#f8f8f8`
- Accent green: `#0a7c42`, `#4ade80`, `#f0fff4`, `#a7f3d0`
- Accent orange: `#ff6600`, `#fff8f3`
- Accent red: `#c41e3a`, `#991b1b`, `#fef2f2`
- Text: `#1a1a1a`, `#475569`, `#cbd5e1`
- Border: `#e0e0e0`, `#333333`
- Divider: `#1f2937`, `#cbd5e1`

All callouts use the established pattern: `background: [tint] ; border-left: 4px solid [accent] ; padding: 14px 16px ;` for soft callouts, or solid `[dark]` with white text for strong callouts.

---

# CLOSING NOTES

This brief assumes OpenClaw can:
- Run Gemini Deep Research tasks (5 jobs)
- Run Perplexity queries (4+ tasks)
- Run ChatGPT/alternative LLM tasks (1 task)
- Hit 8+ external APIs for market data
- Run Python pipelines (matplotlib chart gen, HTML patching)
- Deploy to Vercel for the web page
- Trigger Telegram bot handoff

If any of these capabilities aren't yet wired up, the priority order is:
1. **Audit Fixes 1-7** (Part 1) — non-negotiable, do these first
2. **Tuesday Morning Refresh Pipeline** (Part 5) — second priority, removes manual work
3. **Gemini Deep Research G1, G3, G5** (Part 2A) — third priority, biggest analytical lift
4. **Long-form web deep-dive** (Part 4A) — fourth priority, extends the package
5. **Wed/Thu/Fri follow-up emails** (Part 4C) — fifth priority, completes the week
6. **Everything else** — nice-to-haves

If anything is unclear, ask Jason. If anything would meaningfully improve this brief or the build, propose it. Six days is a lot of time when the orchestration is good.

— End of comprehensive iteration brief —
