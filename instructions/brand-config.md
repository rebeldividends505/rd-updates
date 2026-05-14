# Rebel Dividends — Brand Config

This file is the single source of truth for all brand facts, copy rules, contact
info, and disclaimers. Read it before generating any daily output.

## Company

- **Legal name:** Rebel Dividends Corporation
- **Marketing name:** Rebel Dividends
- **Domain:** https://rebeldividends.com
- **Updates site:** https://updates.rebeldividends.com
- **Investor portal:** https://portal.rebeldividends.com
- **Sender email:** support@rebeldividends.com
- **Sender name (in mail clients):** Rebel Dividends
- **Author of all daily content:** Jason Cox (sole author — never list anyone
  else as author).

## Closer / CTA contact

- **Name:** Dean Gallagher
- **Phone:** 505-322-7515
- **Standard close box:** "Questions? Reply to this email or call Dean at
  505-322-7515 and he'll take care of you."
- Dean is the closer, not the author. Never reference Dean as the writer of the
  update.

## Underlying asset

- **Ticker:** HYPE (Hyperliquid)
- **Strategy:** Unleveraged, spot HYPE only. Pivoted from a leveraged ETH
  strategy in **April 2024**.
- The RD share price tracks HYPE 1:1 (spot, unleveraged) — when HYPE moves, the
  share price moves with it.

## Share price

- **Formula (reference only — read from the sheet, do not recalculate):**
  `RD_SHARE = 0.001776 × (HYPE_current / 39.41)`
- **Source of truth:** Google Sheet cell P23 (current share price) and P24
  (day %). The pipeline always reads these values rather than calculating.

## Dividends

- **Cadence:** Weekly, paid every Monday.
- **Per-share amount:** $0.00002 per share, per week.
- **Consecutive weekly dividend streak:** **106+** (increments by 1 every
  Monday — see `instructions/current-week.md` for the canonical current count).
- **2026 tax treatment:** All 2026 distributions classified as Return of
  Capital under **IRC §301(c)(2)** — tax-free in 2026. Always note "consult
  your CPA" when discussing tax treatment.

## Performance benchmarks (since April 2024 pivot)

Use these reference numbers when illustrating "$100K invested at the pivot":

- **Reinvestor (DRIP):** ~$277K (+177%)
- **Collector (cash dividends):** ~$196K (+96%)
- The Reinvestor advantage over the Collector is the recurring talking point —
  it widens every week as dividends compound.

## Webinar

- **Cadence:** Tuesdays at 3:30 PM ET (live).
- **Replay URL:** https://www.rebeldividends.com/startwebinar/
- The replay URL stays the same week-to-week; the embedded video changes.

## Key landing pages

- **/forward/:** https://rebeldividends.com/forward/ — "How HYPE hits $150 in
  12 months." Used by Friday-A (forward promo) emails.
- **/macro/:** https://rebeldividends.com/macro/ — Macro thesis page. Used by
  Thursday default and Friday macro-tease editorials.

## Image assets

- **WordPress media URL format:**
  `https://www.rebeldividends.com/wp-content/uploads/YYYY/MM/<filename>.png`
- **Daily Reinvestor chart filename pattern:** `reinvestor-chart-MMDD.png` —
  e.g. `reinvestor-chart-may06.png` for 2026-05-06.
- Use lowercase three-letter month + **two-digit day with leading zero**:
  `may06`, `may16`, `jun03` — this matches the actual WordPress uploads on the server.
  `may6` (no leading zero) returns 404 — always use two digits for the day.

## Distribution lists (VERIFIED May 7, 2026 — DO NOT CHANGE WITHOUT VERIFICATION)

### Brevo (email + SMS)

- **List ID 4** — RD Investors - Email — FULL broadcast email list.
- **List ID 5** — RD Investors - SMS — FULL broadcast SMS list.
- **List ID 6** — RD TEST - Email (internal QA only).
- **List ID 7** — RD TEST - SMS (internal QA only).
- Lists 14 and 15 **DO NOT EXIST** — do not use.

### SimpleTexting (SMS fallback)

- API Key env var: `SIMPLETEXTING_API_KEY`
- Live list ID: `656def0f0d113f14b617af55` (also via `SIMPLETEXTING_LIST_ID` env var)
- Account phone: 5615896099

### Test recipients (ALL 3 must receive test before any full send)

| Name  | Email                     | Phone      |
|-------|---------------------------|------------|
| Jason | jasonjamescox85@gmail.com | 5055956003 |
| Ryan  | ryan@rebeldividends.com   | 5052808236 |
| Dean  | dean@rebeldividends.com   | 5053227515 |

## Required disclaimer (always include verbatim in email footer)

> Past performance does not guarantee future results. Forward-looking
> projections are hypothetical. Crypto markets are highly volatile. This is not
> financial advice. Fund experienced significant losses during prior leveraged
> ETH strategy (2022–2024). All performance data reflects results only since
> the April 2024 pivot to unleveraged, spot HYPE strategy. Fee: 20% management
> fee on all dividends.

The Wednesday/Thursday/Friday templates already split this into three short
paragraphs (Disclaimer, Tax Treatment, Fee Structure). Either format is
acceptable as long as every clause above is present.

## Voice and tone

- Plain, confident, slightly contrarian. No hype words ("moonshot", "rocket",
  "to the moon") even when the asset is named HYPE.
- Numbers carry the argument. Lead with the price, then the math, then the
  thesis.
- One CTA per email (except Friday macro-tease, which has none).
- Never invent specifics — if a number isn't in the prices JSON or the sheet
  cells listed in `format-guide.md`, don't include it.

## Content Strategy Rules (HARDCODED — May 7, 2026 — DO NOT OVERRIDE)

### The Core Thesis
- BTC and HYPE are **extremely undervalued** relative to macro forces — coiled to pop
- $60 = HYPE's September 2025 ATH — already been there, just getting back
- **Anything below $60 is a buying opportunity. Full stop.**
- 106+ consecutive weekly dividends, all tax-free under IRC §301(c)(2)
- Reinvestors up ~177% since April 2024 pivot ($100K → $277K)

### The Macro Argument (use every day)
- BTC has decoupled from global M2 money supply — when M2 catches up, BTC explodes
- Hyperliquid: #1 decentralized perp exchange, ~70% market share, $180B+ monthly volume
- $1.3B HYPE bought back and burned (4.17% of supply); 97% of protocol fees go to token holders
- 388M HYPE tokens in community rewards wallet (untouched) — last airdrop took HYPE $4→$35 in 23 days
- Hyperliquid removed "points program ended" from their documentation — signals something coming

### Writing Rules (confirmed by Jason)
1. Write for **investors**, not traders — simple, powerful language
2. **NO technical analysis** — no support/resistance/RSI/chart patterns/holding levels
3. Focus on **BTC + macro fundamentals** — NOT Coinbase/Solana/Ethereum comparisons
4. On red stock days: use SOXL/AI overbought angle — rotate profits into RD
5. Always reiterate Tuesday's macro thesis in every other day's content
6. **Push Dean CTA hard**: "Call Dean: 505-322-7515" — Dean closes, Dean is the CTA
7. Author = Jason Cox always. Dean = closer/CTA box only, never mentioned as author.

### Content Angle by Market Condition
- **HYPE up:** Momentum building, thesis playing out, great time to add or switch to reinvesting
- **HYPE down:** Discount window, below $60 = opportunity, coiled to pop
- **Stocks red (SOXL/AI down):** Rotate stock profits into RD — AI at 35-45x earnings, overbought
- **Every day:** $60 target, 106+ consecutive dividends, call Dean 505-322-7515

### SMS Formula (LOCKED — May 14, 2026)
1. **Always start with `Rebel Dividends:` — NOT `RD:`** — then share price + day %: `Rebel Dividends: $0.00179 (-2.8%).`
2. **One brief thesis blurb** — the day's angle (macro, rotation, undervalued)
3. **Page link:** `updates.rebeldividends.com` — always include
4. **Call Dean: 505-322-7515** — every SMS, no exceptions
5. **Reply STOP to opt out** — always last
- Do NOT lead with dividend count
- 2 segments (320 chars) is acceptable
- Example: `Rebel Dividends: $0.00179 (-2.8%). Stocks most overbought in history. HYPE 40% from ATH. Rotate now: updates.rebeldividends.com. Call Dean: 505-322-7515. Reply STOP to opt out.`
