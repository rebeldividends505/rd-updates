<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# Repo purpose — Rebel Dividends daily pipeline

This repo is two things at once:

1. The **Next.js site** that powers https://updates.rebeldividends.com (the
   public daily update page).
2. The **source of truth** for the daily content pipeline — instructions,
   templates, generated outputs, and the orchestrator scripts that turn live
   market data into the day's email/SMS/web update.

A cron job on the production box fires `pipeline/generate_daily.sh` at 7:31 AM
MST every weekday. The orchestrator pulls `main`, fetches prices, runs Claude
Code to generate the day's content, deploys the web copy, commits, and sends a
test message to Jason for approval before any live broadcast.

## Directory layout

| Path                          | Purpose                                        |
|-------------------------------|------------------------------------------------|
| `instructions/`               | Brand config, format guide, current-week file. Read these before generating. |
| `templates/examples/`         | Hand-written reference outputs for each day. Study before writing. |
| `pipeline/`                   | Orchestration scripts (generate, fetch, deploy, send, approval). |
| `outputs/<YYYY-MM-DD>/`       | Generated artifacts per day (email.html, elementor.html, sms.txt, deploy-notes.md, claude-summary.txt). |
| `public/daily/<slug>.html`    | Static-served daily update for the web (Vercel). |
| `src/app/page.tsx`            | Home page; constants at top are patched by `pipeline/deploy.py`. |

## Pipeline flow (per weekday)

```
cron 7:31 AM MST
  → pipeline/generate_daily.sh
       1. git pull
       2. pipeline/research_fetch.py  → /tmp/rd_prices_<date>.json
            • gog sheets read P23:P24 (and Tuesday cells on Mondays)
            • CoinGecko HYPE price (Yahoo fallback)
       3. (skip Sat/Sun)
       4. (Tue): reuse Monday's outputs/<monday>/ — do NOT regenerate
       5. claude --print --add-dir .   ← reads instructions/, writes outputs/<date>/
       6. pipeline/deploy.py
            • copies elementor.html → public/daily/<slug>.html
            • patches constants in src/app/page.tsx from deploy-notes.md
            • git add, commit, push  (Vercel auto-deploys ~60s later)
       7. Post SMS preview + web URL to Jason's Telegram group for review
       8. pipeline/approval_listen.py waits for Jason's chat approval
       9. (after 'approve') pipeline/send.py --test → email + SMS to Jason, Ryan, Dean
      10. pipeline/approval_listen.py waits for 'go live'
      11. (after 'go live') pipeline/send.py --live → full Brevo/SimpleTexting lists

## Test contacts (as of May 7, 2026)
| Name  | Email                     | Phone       |
|-------|---------------------------|-------------|
| Jason | jasonjamescox85@gmail.com | 5055956003  |
| Ryan  | ryan@rebeldividends.com   | 5052808236  |
| Dean  | dean@rebeldividends.com   | 5053227515  |
```

## Day cadence

| Day | Output                                             |
|-----|----------------------------------------------------|
| MON | Standard daily update + the Tuesday webinar package built ahead |
| TUE | (no generation — reuses Monday's Tuesday package)  |
| WED | Replay recap                                       |
| THU | HYPE technical hook + replay/macro CTA             |
| FRI | Either /forward/ promo (mode A) or macro tease (mode B) — set in current-week.md |
| SAT | no send                                            |
| SUN | no send                                            |

## Conventions for AI agents working in this repo

- **Always read `instructions/brand-config.md`, `instructions/format-guide.md`,
  and `instructions/current-week.md` before writing any daily output.** The
  brand facts and format rules are non-negotiable.
- **Study `templates/examples/` for the matching day** before writing the
  email or elementor HTML. The hand-tuned templates are the gold standard.
- **Never invent prices or numbers.** Read them from the prices JSON the
  orchestrator passes in, or from `outputs/<date>/deploy-notes.md`.
- **Never put secrets in any committed file.** All secrets come from
  `os.environ` (see `.env.example`).
- **Author is always Jason Cox.** Dean Gallagher (505-322-7515) is the
  closer / contact box, never the byline.
- **Do not generate a Tuesday package on a Tuesday** — it was built Monday.
- `.env*` is gitignored; copy `.env.example` to `.env` for local development.
