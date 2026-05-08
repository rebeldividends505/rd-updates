# RD Fri-May08 — Deploy Notes (Friday-A /forward/ promo)

## Today's numbers

- **RD share price:** $0.00179
- **Day over day:** -2.8% (RED #c41e3a)
- **HYPE:** $42.44
- **Week #:** 106 consecutive weekly dividends
- **Date slug:** may8 (per orchestrator-supplied URL — see chart caveat below)
- **Chart URL (used verbatim):** https://www.rebeldividends.com/wp-content/uploads/2026/05/reinvestor-chart-may8.png

## Hook (one sentence)

HYPE at $42.44 needs ~3.5x to hit $150 — and because RD holds spot HYPE 1:1 unleveraged, your share moves from $0.00179 today to $0.00676 at the target, a +278% return. Read the full /forward/ scenario before the market prices it in.

## Subject + CTA

- **Subject:** HYPE at $42.44 → $150 = +278% from your share *(47 chars, under 60)*
- **CTA:** READ THE $150 HYPE SCENARIO → https://www.rebeldividends.com/forward/ (green button, locked to `forward` per current-week.md)

## The $150 math

- HYPE today: **$42.44**
- HYPE multiplier needed to reach $150: **3.534x**
- Share at $150 (per share-price formula 0.001776 × HYPE/39.41): **$0.00676**
- Return from today's $0.00179: **+277.7% → "+278%"**

## Dean talking points

- **The math is dead simple:** HYPE 3.5x to hit $150. Spot, unleveraged, 1:1. Share goes from $0.00179 to $0.00676 — that's +278%, no derivative tricks, no leverage decay.
- **Why $150 isn't a fantasy:** $1.3B in HYPE already bought and burned (4.17% of supply gone), 97% of protocol fees flow to token holders, ~70% perp DEX market share, $180B+ monthly volume. Real revenue, real buyback flywheel — not a meme.
- **The discount window:** Anything below $60 is the September 2025 ATH coming back at a discount. Today's red day (-2.8%) is the pitch, not the problem.
- **The streak:** **106 consecutive weekly dividends** through every red day since April 2024. Reinvestors up ~177% ($100K → ~$277K). 2026 distributions = Return of Capital under IRC §301(c)(2), tax-free this year (consult CPA).
- **The ask:** Today is the day to (1) add to RD on the dip, or (2) flip dividends to reinvest. Dean handles either in 5 minutes at 505-322-7515.

## What changed vs. yesterday (Thu-May07)

- **Format:** Switched from Thursday's "AI rotation" hook to **Friday-A /forward/ promo** per current-week.md (`Friday mode: forward`).
- **Subject:** Anchored on the $150 thesis math with today's HYPE price as the anchor.
- **CTA:** Green button → /forward/ (Friday-A pattern), replacing Thursday's /startwebinar/ button.
- **Headline link:** H2 wraps an `<a>` to /forward/ (matches `friday-forward.html` template).
- **Chart link:** Chart image is wrapped in a /forward/ anchor (Friday-A pattern from template).
- **SMS:** Rewritten to lead with share price + $150 math + /forward/ link. 178 chars, well under 320.

## Anything unusual / flags for Jason

- **Chart URL caveat:** The orchestrator passed `reinvestor-chart-may8.png` (no leading zero). Brand-config explicitly says single-digit-day filenames return 404 (`may6`, `may7` both 404'd in prior days; Thursday fell back to `may06`). The user prompt's "Use the chart URL above verbatim" overrode brand-config here, so the URL is shipped as-is. **If the may8 asset was not actually uploaded to WordPress this morning, replace with `reinvestor-chart-may06.png` before live send.**
- **Red day framed as the pitch:** -2.8% is leveraged into the discount-window angle rather than papered over.
- **No webinar mention:** Friday-A is a pure /forward/ promo; no /startwebinar/ link, no replay nudge — keeps the single CTA discipline.
- **Author byline:** None in the rendered email body (matches the `friday-forward.html` reference); Jason Cox is implicit per brand config.
