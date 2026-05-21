#!/usr/bin/env python3
"""
alert_engine.py — AI Short-Signal alert engine (Tier 2, Module A)
==================================================================
Computes composite scores, diffs against last run, fires Telegram
alerts for meaningful changes, saves new state snapshot.

Usage:
  python3 alert_engine.py            # normal run
  python3 alert_engine.py --dry-run  # print alerts, don't send
  python3 alert_engine.py --force    # send even if no changes (testing)
  python3 alert_engine.py --ticker MU
"""
import json, sys, subprocess, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from signal_loader import load_model, apply_live, build_state, verdict, TICKERS as ALL_TICKERS

STATE_DIR  = HERE / "state"
LAST_STATE = STATE_DIR / "last_state.json"
DASHBOARD  = "updates.rebeldividends.com/nvdasignal"

TELEGRAM_JASON    = "511154657"
TELEGRAM_RD_GROUP = "-5275068164"

DRY   = "--dry-run" in sys.argv
FORCE = "--force" in sys.argv
ONLY  = None
if "--ticker" in sys.argv:
    idx = sys.argv.index("--ticker")
    ONLY = sys.argv[idx + 1].upper() if idx + 1 < len(sys.argv) else None

def log(*a):
    import datetime as _dt
    print(f"[{_dt.datetime.now():%H:%M:%S}]", *a)

# ---------------------------------------------------------------------------
def send_telegram(target, message):
    if DRY:
        print(f"\n  → [DRY-RUN] Telegram {target}:\n  {message}\n")
        return True
    cmd = ["openclaw", "message", "send",
           "--channel", "telegram",
           "--target", target,
           "--message", message]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if r.returncode != 0:
            log(f"Telegram send failed (target {target}): {r.stderr.strip()}")
            return False
        return True
    except Exception as e:
        log(f"Telegram send error: {e}")
        return False

# ---------------------------------------------------------------------------
def detect_changes(cur, prev):
    """Compare current vs previous state, return list of alert dicts."""
    alerts = []
    syms = [ONLY] if ONLY else list(cur["tickers"].keys())

    for sym in syms:
        ct = cur["tickers"].get(sym)
        if not ct:
            continue
        pt = prev.get("tickers", {}).get(sym, {})

        cur_score   = ct["score"]
        prev_score  = pt.get("score", cur_score)
        delta       = cur_score - prev_score
        cur_verdict = ct["verdict"]
        prev_verdict = pt.get("verdict", cur_verdict)

        # Index prev tier1 by signal id
        prev_t1 = {s["id"]: s for s in pt.get("tier1_signals", [])}
        cur_t1  = {s["id"]: s for s in ct.get("tier1_signals", [])}

        # Find Tier-1 signals that newly flipped to "short"
        new_t1_shorts = []
        for sid, cs in cur_t1.items():
            ps = prev_t1.get(sid, {})
            if cs["status"] == "short" and ps.get("status", "na") != "short":
                new_t1_shorts.append((cs["name"], ps.get("status", "unknown")))

        newly_confirming = (
            cur_verdict == "SHORT SETUP CONFIRMING"
            and prev_verdict != "SHORT SETUP CONFIRMING"
        )

        crossed_threshold = prev_score < 60 <= cur_score

        if newly_confirming:
            t1_names = ", ".join(s["name"] for s in ct["tier1_signals"] if s["status"] == "short")
            alerts.append({
                "type": "confirming", "sym": sym, "score": cur_score,
                "msg": (
                    f"🚨 {sym} SHORT SETUP CONFIRMING: Score {cur_score}/100. "
                    f"Tier-1 triggers: {t1_names or 'see dashboard'}. "
                    f"Check dashboard: {DASHBOARD}"
                ),
            })
        else:
            for sig_name, was_status in new_t1_shorts:
                alerts.append({
                    "type": "tier1_flip", "sym": sym, "score": cur_score,
                    "msg": (
                        f"⚠️ {sym} Tier-1 signal flipped SHORT: {sig_name} "
                        f"(was {was_status.upper()}). "
                        f"Composite: {cur_score}/100. "
                        + ("NOT confirming yet — more Tier-1 needed." if cur_verdict != "SHORT SETUP CONFIRMING"
                           else f"CONFIRMING. Check: {DASHBOARD}")
                    ),
                })

            if crossed_threshold and not new_t1_shorts:
                alerts.append({
                    "type": "threshold", "sym": sym, "score": cur_score,
                    "msg": (
                        f"📈 {sym} crossed 60 threshold: Score {cur_score}/100 (was {prev_score}). "
                        f"Verdict: {cur_verdict}. "
                        + (f"Tier-1 trigger needed to confirm." if cur_verdict != "SHORT SETUP CONFIRMING"
                           else f"Check: {DASHBOARD}")
                    ),
                })
            elif abs(delta) >= 10 and not new_t1_shorts:
                arrow = "▲" if delta > 0 else "▼"
                alerts.append({
                    "type": "movement", "sym": sym, "score": cur_score, "delta": delta,
                    "msg": (
                        f"📊 {sym} score moved {arrow}{abs(delta):.0f}pts → {cur_score}/100. "
                        f"Verdict: {cur_verdict}."
                    ),
                })

    return alerts

# ---------------------------------------------------------------------------
def build_daily_summary(cur):
    """Build daily scorecard message for RD group chat."""
    today = cur.get("asof", dt.date.today().isoformat())
    lines = [f"📊 AI SHORT SIGNAL DAILY — {today}", ""]

    # Sort tickers by score descending
    sorted_t = sorted(cur["tickers"].items(), key=lambda x: x[1]["score"], reverse=True)

    emoji_map = {
        "SHORT SETUP CONFIRMING": "🚨",
        "WATCH — building": "⚠️",
        "EARLY WATCH": "👁",
        "NO SHORT SIGNAL": "✅",
    }
    lines.append("SCORECARD:")
    for sym, t in sorted_t:
        em = emoji_map.get(t["verdict"], "—")
        lines.append(f"  {sym:<6} {t['score']:>3}/100  {em} {t['verdict']}")

    lines.append("")
    lines.append(f"MACRO REGIME: {cur['macro_score']}/100")

    # Confirming setups
    confirming = [sym for sym, t in cur["tickers"].items()
                  if t["verdict"] == "SHORT SETUP CONFIRMING"]
    if confirming:
        lines.append("")
        lines.append(f"🚨 CONFIRMING: {', '.join(confirming)}")
        lines.append(f"   Dashboard: {DASHBOARD}")
    else:
        lines.append("")
        lines.append("No confirming setups today.")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    log("Loading signal model...")
    model = load_model()
    apply_live(model)
    cur = build_state(model)

    prev = {}
    if LAST_STATE.exists():
        try:
            prev = json.loads(LAST_STATE.read_text())
        except Exception:
            prev = {}

    alerts = detect_changes(cur, prev)

    if not alerts and not FORCE:
        log(f"No alert triggers detected for {ONLY or 'all tickers'}.")
    else:
        if alerts:
            log(f"{len(alerts)} alert(s) to send.")
        else:
            log("--force: sending daily summary only.")

        for a in alerts:
            log(f"  [{a['type']}] {a['sym']}: {a['msg'][:80]}...")
            send_telegram(TELEGRAM_JASON, a["msg"])

    # Daily summary always goes to the RD group
    summary = build_daily_summary(cur)
    if DRY:
        print("\n--- DAILY SUMMARY (RD Group) ---")
        print(summary)
        print("--- END SUMMARY ---\n")
    else:
        send_telegram(TELEGRAM_RD_GROUP, summary)

    # Persist state
    if not DRY:
        LAST_STATE.write_text(json.dumps(cur, indent=2))
        log(f"State saved → {LAST_STATE}")
    else:
        log("[DRY-RUN] State NOT saved.")

    # Print score table to stdout
    print("\nCurrent scores:")
    for sym, t in sorted(cur["tickers"].items(), key=lambda x: x[1]["score"], reverse=True):
        print(f"  {sym:<6} {t['score']:>3}/100  {t['verdict']}")
    print(f"  MACRO  {cur['macro_score']:>3}/100")

if __name__ == "__main__":
    main()
