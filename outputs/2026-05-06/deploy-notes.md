# RD Wed-May06 — Deploy Notes

## Today's numbers

- **RD share price:** $0.00184
- **Day over day:** +1.1%
- **HYPE:** $43.25
- **Week #:** 106 consecutive weekly dividends
- **Date slug:** may6
- **Chart:** https://www.rebeldividends.com/wp-content/uploads/2026/05/reinvestor-chart-may6.png

## Hook (one sentence)

Wednesday recap: HYPE at $43.25, clean follow-through above the late-January breakout — and a $60 retest puts shares ~39% higher from here. Yesterday's webinar replay still live.

## What changed vs. template

- Hand-tuned template (`templates/examples/wednesday-email-may06.html`) was built around HYPE $44.40 / day +1.07%. Live numbers are HYPE **$43.25** / day **+1.1%** — math updated accordingly:
  - "roughly 35% from here" → **"roughly 39% from here"** (($60 − $43.25) / $43.25 ≈ 38.7%).
  - "+1.07%" → **"+1.1%"** (per format guide, 1 decimal place).
- Chart URL uses the no-leading-zero convention (`may6.png`) per the user-provided URL and the brand-config rule.
- Share price unchanged from template ($0.00184).
- All disclaimer / Dean / footer copy verbatim.

## Dean talking points

- RD shares **$0.00184**, up **1.1%** overnight; HYPE **$43.25**.
- The clean technical setup is intact: higher highs, higher lows, holding above the late-January breakout.
- $60 = HYPE's **September 2025 ATH** — already-proven price. From $43.25 that's **~39% upside** for shares (1:1 spot, no leverage).
- $100K at the April 2024 pivot is now ~**$280K (Reinvestor)** vs **$198K (Collector)** — Reinvestor advantage ≈ $82K and widens weekly.
- **106 consecutive weekly dividends**; every 2026 distribution Return of Capital under IRC §301(c)(2) (consult CPA).
- CTA: webinar replay → rebeldividends.com/startwebinar/

## Anything unusual?

- `instructions/current-week.md` still has placeholders for webinar live link, Tuesday hook, Friday/Thursday modes. Wednesday copy is the recap pattern and references "yesterday's webinar" generically, so no field was needed today — but Friday/Thursday will need real values.
- GBRAIN context returned no results for today; copy is fully built from price feed + template, no breaking-news weave.
