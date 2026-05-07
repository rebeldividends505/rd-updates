#!/bin/bash
# RD Daily — main orchestrator. Cron fires this at 7:31 AM MST.
# Pulls latest, fetches prices, runs Claude Code to generate the day's
# package, deploys to web, commits, and sends a test to Jason.
set -e

REPO_DIR="${REPO_DIR:-$HOME/rd-updates-site}"
DATE=$(date +%Y-%m-%d)
DAY=$(date +%A)
YEAR=$(date +%Y)
MONTH=$(date +%m)
OUTPUT_DIR="$REPO_DIR/outputs/$DATE"

echo "==> RD daily run — $DATE ($DAY)"

# Pull latest
cd "$REPO_DIR"
git pull origin main

# Fetch prices (always — the JSON is consumed by Claude prompt below)
PRICES_FILE="/tmp/rd_prices_$DATE.json"
python3 "$REPO_DIR/pipeline/research_fetch.py" > "$PRICES_FILE"
echo "==> Prices fetched:"
cat "$PRICES_FILE"

# Skip weekends entirely
if [[ "$DAY" == "Saturday" || "$DAY" == "Sunday" ]]; then
  echo "==> Weekend — no send. Exiting."
  exit 0
fi

# Tuesday: package was built Monday. Don't regenerate. Reuse Monday's outputs.
if [[ "$DAY" == "Tuesday" ]]; then
  echo "==> Tuesday: reusing Monday's outputs."
  MONDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)
  if [ -d "$REPO_DIR/outputs/$MONDAY" ]; then
    OUTPUT_DIR="$REPO_DIR/outputs/$MONDAY"
    DATE="$MONDAY"
    echo "    Using $OUTPUT_DIR"
  else
    echo "[ERROR] Tuesday run but no Monday output at $REPO_DIR/outputs/$MONDAY"
    exit 1
  fi
fi

mkdir -p "$OUTPUT_DIR"

# Query GBrain for additional context (optional — fail soft)
GBRAIN_CONTEXT=$(gbrain query "RD daily update format standards brand config current week" 2>/dev/null || echo "GBrain unavailable")

# Compute the WordPress chart URL slug for today (e.g. may6, may16)
DATE_SLUG=$(date -j -f %Y-%m-%d "$DATE" "+%b%-d" 2>/dev/null | tr '[:upper:]' '[:lower:]' \
  || date -d "$DATE" "+%b%-d" | tr '[:upper:]' '[:lower:]')

CHART_URL="https://www.rebeldividends.com/wp-content/uploads/$YEAR/$MONTH/reinvestor-chart-$DATE_SLUG.png"

# Skip generation on Tuesday — just deploy/send Monday's output
if [[ "$DAY" != "Tuesday" ]]; then
  PROMPT_FILE="/tmp/rd_daily_prompt_$DATE.txt"
  cat > "$PROMPT_FILE" <<EOF
Generate today's Rebel Dividends investor update package.

TODAY: $DAY, $DATE
PRICES: $(cat "$PRICES_FILE")
CHART URL FOR TODAY: $CHART_URL
GBRAIN CONTEXT: $GBRAIN_CONTEXT

Read these files carefully before writing anything:
- instructions/brand-config.md (brand facts, Dean CTA, disclaimer)
- instructions/format-guide.md (exact format rules per day)
- instructions/current-week.md (this week's webinar link and hook)
- templates/examples/ (study the correct day's template)

WRITE these output files to outputs/$DATE/:
1. email.html — Brevo/iContact email (follow the exact format for $DAY)
2. elementor.html — web version (same content, adapted for the Elementor widget)
3. sms.txt — SUBJECT line first, blank line, then SMS: body
4. deploy-notes.md — key numbers, what changed, Dean talking points

CRITICAL RULES:
- Share price: exactly 5 decimal places (e.g. \$0.001750)
- HYPE price: exactly 2 decimal places (e.g. \$40.85)
- Day%: 1 decimal place with sign (+1.0%, -3.7%)
- Day% color: green #4ade80, red #c41e3a, gray #888888
- Use the chart URL above verbatim
- Always include the Dean contact box and full footer disclaimer
- Author is Jason Cox — never mention Dean as author
- Do NOT generate a Tuesday package on Tuesday (use Monday's output)
- If today is Monday, also generate the Tuesday package for tomorrow into
  outputs/$DATE/tuesday-email.html, outputs/$DATE/tuesday-elementor.html,
  outputs/$DATE/tuesday-sms.txt

When done, write a brief summary to outputs/$DATE/claude-summary.txt
EOF

  echo "==> Running Claude Code generator..."
  cd "$REPO_DIR"  # Claude Code auto-reads files from cwd; no --add-dir needed
  claude --permission-mode bypassPermissions --print \
    "$(cat "$PROMPT_FILE")"
fi

# Deploy to web (copies elementor.html into public/daily/, updates page.tsx)
ELEMENTOR_FILE="$OUTPUT_DIR/elementor.html"
if [ -f "$ELEMENTOR_FILE" ]; then
  python3 "$REPO_DIR/pipeline/deploy.py" --date "$DATE" --file "$ELEMENTOR_FILE"
else
  echo "[WARN] No elementor.html at $ELEMENTOR_FILE — skipping deploy"
fi

# Commit outputs (deploy.py already pushes; this catches anything it missed)
cd "$REPO_DIR"
git add outputs/ src/ public/ || true
git commit -m "Daily output — $DATE ($DAY)" || echo "    (nothing extra to commit)"
git push origin main || echo "    (nothing to push)"

# Post preview to Jason in Telegram group chat BEFORE sending test
# Jason must approve here before test goes to Dean/Jason/Ryan
SMS_PREVIEW=$(python3 - <<PYEOF 2>/dev/null
import sys; sys.path.insert(0, '$REPO_DIR/pipeline')
from send import parse_sms_body, load_output
out = load_output('$DATE')
body = parse_sms_body(out.get('sms_txt', ''))
print(body[:300] if body else '(SMS body missing)')
PYEOF
)

WEB_URL="https://updates.rebeldividends.com"

PREVIEW_MSG="⏳ *$DAY $DATE content ready for review:*

*SMS Preview:*
$SMS_PREVIEW

*Web page:* $WEB_URL

Reply 'approve' to send test to Dean/Jason/Ryan
Reply 'edit: [text]' to revise
Reply 'go live' to send to full investor list after test"

openclaw message send \
  --channel telegram \
  --target '-5275068164' \
  --message "$PREVIEW_MSG" || echo "[WARN] Telegram preview failed — check openclaw"

echo "==> Preview posted to Telegram. Awaiting Jason's approval before test send."

# approval_listen.py watches for the approved.flag (set by the approval flow)
python3 "$REPO_DIR/pipeline/approval_listen.py" --date "$DATE" --wait-for-preview

echo "==> Approval received. Sending test to Jason only first..."
python3 "$REPO_DIR/pipeline/send.py" --date "$DATE" --test

echo "==> Test sent to Jason. Awaiting Jason's approval before sending to Ryan + Dean."
