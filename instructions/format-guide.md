# RD Daily — Format Guide

Day-by-day rules for the daily update package. Read this with
`brand-config.md` and `current-week.md` before generating output.

## Day cadence (what gets sent)

| Day  | Type                          | Approx length   | Notes                                       |
|------|-------------------------------|-----------------|---------------------------------------------|
| MON  | Daily update                  | ~80 lines HTML  | **Same format as Wed/Thu/Fri** — use wednesday-email-may06.html as reference. Was previously done by hand; now automated. |
| TUE  | **Webinar package**           | 774+ lines      | Built **Monday** alongside Monday's own daily send. NEVER generated on Tuesday itself. This is the ONLY day with a different format. |
| WED  | Replay recap                  | ~80 lines HTML  | Subject leads with replay                   |
| THU  | Market hook + replay          | ~89 lines HTML  | Lead with HYPE technical angle              |
| FRI-A| /forward/ promo               | ~81 lines HTML  | $150 thesis math, green CTA → /forward/     |
| FRI-B| Macro Tease                   | ~80 lines HTML  | Pure editorial — **NO CTA buttons, no URLs** except Dean box |
| SAT  | NO send                       | —               |                                             |
| SUN  | NO send                       | —               |                                             |

Friday mode (A vs B) is set in `current-week.md` each week.

## Data sources per day

- **MON / WED / THU / FRI-A / FRI-B:** Use **P23** (share price) and **P24**
  (day %) only. HYPE price comes from CoinGecko (with Yahoo fallback).
- **TUE (built Monday):** P23 + P24 + the Track Record sheet cells below.

### Tuesday extra cells (Track Record sheet)

| Cell | Meaning                  | Example          |
|------|--------------------------|------------------|
| B1   | Portfolio value          | $14,133,827.19   |
| K1   | Total shares outstanding | 7,831,760,849    |
| M26  | Dividend per share       | 0.00002          |
| M29  | Week-over-week return    | -3.89%           |
| M30  | Dividend ROI %           | 1.18%            |
| I20  | Cash balance             | $772,265.04      |

## Price formatting (NON-NEGOTIABLE)

- **RD share price:** exactly **5 decimal places** — `$0.00175` is **wrong**;
  write `$0.001750`. Always lead with `$`.
- **HYPE price:** exactly **2 decimal places** — `$40.85`, never `$40.8` or
  `$40.853`.
- **Day %:** exactly **1 decimal place with sign** — `+2.0%`, `-4.8%`,
  `+0.0%` for flat.
- **Day % color in HTML:**
  - green `#4ade80` for positive
  - red   `#c41e3a` for negative
  - gray  `#888888` for flat (0.0%)

## HTML email structure (MON / WED / THU / FRI-A / FRI-B)

All non-Tuesday emails follow this skeleton, in order:

1. **Header bar** — "Rebel Dividends" left, date + RD share price + day % right.
2. **H2 headline** — day-specific hook (see day rules below).
3. **Narrative paragraphs** — 3–5 short paragraphs.
4. **CTA button** — day-specific. **Friday-B (macro tease) has NO button.**
5. **Reinvestor chart image** — sourced from
   `https://www.rebeldividends.com/wp-content/uploads/YYYY/MM/reinvestor-chart-MMDD.png`
   where MMDD is the lowercase month + day (e.g. `may6`, `may16`).
6. **Dean contact box** — verbatim from `brand-config.md`.
7. **Footer disclaimer** — full required disclaimer (see `brand-config.md`).

The Tuesday package is its own beast — see "Tuesday package" section below.

## Day-by-day rules

### MON — Daily update

- **Subject line pattern:** `Your RD update for Monday — <hook>.`
- Use P23 + P24 only. Frame the week ahead. Mention the Tuesday webinar at
  3:30 PM ET (link to `/startwebinar/`).
- CTA button: green, → `/startwebinar/`.

### TUE — Webinar day (BUILT MONDAY, never on Tuesday)

When today is **Monday**, also produce the Tuesday package alongside Monday's
update. When today is **Tuesday**, the orchestrator reuses Monday's
`outputs/<monday>/` directory; do not regenerate.

The Tuesday package is the full production package: 774+ lines of HTML, dark
stats dashboard, 14+ charts, full macro thesis, all the Track Record cells
(B1, K1, M26, M29, M30, I20). Study
`templates/examples/tuesday-icontact-may05.html` and the matching
`tuesday-elementor-may05.html` for the exact structure.

### WED — Replay recap

- **Subject line pattern (pick one):**
  - `Your RD update for Wednesday — and where we go from here.`
  - `Missed <Tuesday topic>? Replay is live.`
- Lead with the prior day's webinar topic (from `current-week.md`).
- CTA: green, → `/startwebinar/` (Watch the Webinar Replay →).

### THU — Market hook + replay

- **Subject line pattern:** `HYPE <state> at $<price> — <hook>. Replay still live.`
- **Lead with the HYPE technical angle.** First paragraph is always the price
  read.
- **CTA default:**
  - During webinar week (replay still relevant): `/startwebinar/`.
  - Otherwise: `/macro/`.
  - The week's choice is locked in `current-week.md` → "Thursday CTA".

### FRI-A — /forward/ promo

- **Subject line pattern:** `How HYPE hits $150 in 12 months.`
- Body shows the $150 thesis math (HYPE 1:1 spot exposure, what $100K becomes
  at HYPE $60 / $100 / $150, the buyback flywheel).
- CTA: **green** button, → `/forward/`.

### FRI-B — Macro Tease

- Pure editorial — no urls, no CTA buttons. The **only** anchor URL allowed
  outside the disclaimer footer is implicit (Dean box uses a tel: link only,
  no web URL).
- No "click here", no "watch the replay", no "read more". The subject line
  should be a hook on the macro story; the body should be 3–4 paragraphs of
  pure editorial. End with the Dean box and disclaimer.

## Output files (every send day)

The pipeline writes these into `outputs/YYYY-MM-DD/`:

1. **email.html** — iContact / Brevo email body. Full HTML email skeleton.
2. **elementor.html** — web version for the Elementor widget on
   updates.rebeldividends.com. Same content adapted for the web context (drop
   the email-specific table boilerplate, keep it as a clean HTML fragment).
3. **sms.txt** — first line is `SUBJECT: <subject line>`, then a blank line,
   then `SMS:` followed by the SMS body.
4. **deploy-notes.md** — short markdown briefing for Jason / Dean. Include:
   - Today's HYPE price, share price, day %.
   - Week number (consecutive dividends).
   - The day's hook in one sentence.
   - 2–3 Dean talking points.
   - Anything unusual about today's data.
5. **claude-summary.txt** — one-paragraph summary of what was generated and
   why, written by Claude Code at the end of the run.

## SMS body rules

- Keep under 320 characters (two-segment SMS max).
- Lead with the share price + day % + HYPE.
- One clear CTA URL on Mon/Wed/Thu/Fri-A. **None** on Fri-B.
- No emojis unless explicitly requested.
- Always end with the dean line: `Reply STOP to opt out.`

## Subject line rules

- 60 characters or less.
- No clickbait, no all-caps, no emojis.
- Always include either the day name or the hook noun (HYPE, replay, $150,
  etc.) so the recipient knows the cadence at a glance.
