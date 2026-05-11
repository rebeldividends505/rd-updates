# Deploy Notes — Monday, May 11, 2026

## Today's numbers

| Field            | Value           |
|------------------|-----------------|
| Share price      | $0.00171        |
| Day %            | -4.7% (red)     |
| HYPE price       | $41.33          |
| Week number      | 107 (this Mon)  |
| Dividend per share | $0.00002      |
| Chart URL        | https://www.rebeldividends.com/wp-content/uploads/2026/05/reinvestor-chart-may11.png |

## One-sentence hook

Week 107 dividend just paid; HYPE at $41 keeps RD shares ~31% below the $60 September ATH — exactly the discount window Dean has been telling clients to add into.

## Dean talking points

1. **Week 107 streak intact.** Today's payout is the 107th consecutive Monday dividend since the April 2024 pivot. 2026 distributions remain Return of Capital under IRC §301(c)(2) — no federal income tax on what hit accounts today. Consult your CPA on basis impact.
2. **Discount window, not a problem.** Share price down 4.7% overnight on macro noise (fresh trade-policy headlines, BTC sitting at $96K). HYPE held above $41 through it. Anything below $60 is a buying window. Reinvesters buying the dip today get the most new shares.
3. **Tomorrow's webinar (3:30 PM ET).** Live walk-through of where we are: macro setup, buyback flywheel still running, path back to $60 and the $150 / $350-$500 longer-range targets. Replay goes up after, but live is where the Q&A happens.

## What changed vs last week

- HYPE down to $41.33 from ~$44 a week ago. Share price followed (was $0.00184 last Wed; now $0.00171).
- Week 107 paid this morning (week 106 was last Monday).
- Macro tape: BTC holding the $96K range, broader market under trade-policy pressure. HYPE outperforming the broader risk basket relatively.

## Anything unusual

- `instructions/current-week.md` was not updated this Monday before the run — it still shows week 106 and the week-of 2026-05-04. I incremented the week count to 107 based on the brand-config rule ("increments by 1 every Monday") and the May 5 Tuesday template confirming week 106 was paid 2026-05-04. Jason should refresh `current-week.md` before next week's run.
- Prices JSON `week_number` field was `null` (pipeline did not pass an override).
- Tuesday package generated alongside this Monday run (per format-guide), stored as `tuesday-email.html`, `tuesday-elementor.html`, `tuesday-sms.txt` in this directory.
