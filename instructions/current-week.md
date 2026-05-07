# Current Week

Jason updates this file every **Monday morning** before the pipeline runs.
The generator reads it for the live webinar link, the Tuesday hook, and the
Friday/Thursday mode toggles.

Convert relative dates from this file into the absolute MMDD slug used in
image filenames before generating output.

---

- **Week number (consecutive weekly dividends):** 106
- **Week starts (Monday):** 2026-05-04
- **Webinar live link:** https://www.rebeldividends.com/startwebinar/
  *(Tuesday 3:30 PM ET stream URL; falls back to /startwebinar/ replay after
  the live ends.)*
- **Tuesday hook / topic:** Week 106 dividend confirmed — 106 consecutive weeks of uninterrupted income
  *(One-line headline of the Tuesday webinar — used by Wed/Thu recap copy.)*
- **Friday mode:** forward
  *(`forward` = Friday-A /forward/ promo. `macro-tease` = Friday-B pure
  editorial, no CTA.)*
- **Thursday CTA:** startwebinar
  *(Locks the Thursday CTA target. Default = `startwebinar` during webinar
  week, `macro` otherwise.)*
- **Breaking news / current events to weave in:** HYPE holding above $42 despite broader market pressure; macro uncertainty from trade policy; BTC holding $96K range
  *(Anything in the macro tape that should be referenced in this week's
  copy: HYPE catalyst, regulatory news, ETH/BTC moves, etc.)*

---

## Update protocol

1. On Monday before 7:00 AM MST, fill in the four PLACEHOLDER fields.
2. Commit + push so the pipeline picks it up.
3. The pipeline runs at 7:31 AM MST and reads this file every day.

If a field is left as `[PLACEHOLDER ...]` when the generator runs, the
generator will fail loudly — that is intentional. Do not paper over a missing
value.
