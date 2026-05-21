#!/usr/bin/env python3
"""
snapshot.py — Daily state snapshot logger (Tier 2, Module B)
=============================================================
Reads live.json, computes all composite scores, appends a row to
state/score_history.csv, and saves a full JSON snapshot.

Usage:
  python3 snapshot.py            # log today's snapshot
  python3 snapshot.py --dry-run  # print without writing
"""
import json, sys, csv, datetime as dt
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from signal_loader import load_model, apply_live, build_state, TICKERS as ALL_TICKERS

STATE_DIR      = HERE / "state"
SNAPSHOTS_DIR  = STATE_DIR / "snapshots"
HISTORY_CSV    = STATE_DIR / "score_history.csv"

DRY = "--dry-run" in sys.argv

CSV_COLS = (
    ["date"]
    + [f"{sym}_score" for sym in ALL_TICKERS]
    + ["macro_score", "confirming_tickers"]
)

def log(*a):
    import datetime as _dt
    print(f"[{_dt.datetime.now():%H:%M:%S}]", *a)

def main():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    log("Loading signal model...")
    model = load_model()
    apply_live(model)
    state = build_state(model)

    today = dt.date.today().isoformat()
    confirming = [
        sym for sym, t in state["tickers"].items()
        if t["verdict"] == "SHORT SETUP CONFIRMING"
    ]

    # Build CSV row
    row = {"date": today, "macro_score": state["macro_score"],
           "confirming_tickers": ";".join(confirming) if confirming else ""}
    for sym in ALL_TICKERS:
        row[f"{sym}_score"] = state["tickers"].get(sym, {}).get("score", "")

    if DRY:
        print("\n[DRY-RUN] Would append to score_history.csv:")
        print("  " + ", ".join(f"{k}={v}" for k, v in row.items()))
        snap_path = SNAPSHOTS_DIR / f"{today}.json"
        print(f"[DRY-RUN] Would save snapshot → {snap_path}")
    else:
        # Append to CSV (write header if new file)
        write_header = not HISTORY_CSV.exists()
        with open(HISTORY_CSV, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLS)
            if write_header:
                w.writeheader()
            w.writerow(row)
        log(f"Appended row to {HISTORY_CSV}")

        # Full JSON snapshot
        snap_path = SNAPSHOTS_DIR / f"{today}.json"
        snap_path.write_text(json.dumps(state, indent=2))
        log(f"Saved snapshot → {snap_path}")

    # Print summary table
    print(f"\nSnapshot — {today}")
    print(f"{'Ticker':<8} {'Score':>6}  Verdict")
    print("-" * 50)
    for sym in ALL_TICKERS:
        t = state["tickers"].get(sym, {})
        print(f"  {sym:<6} {t.get('score', '?'):>5}/100  {t.get('verdict', '?')}")
    print(f"  {'MACRO':<6} {state['macro_score']:>5}/100")
    if confirming:
        print(f"\n🚨 CONFIRMING: {', '.join(confirming)}")
    else:
        print("\nNo confirming setups.")

if __name__ == "__main__":
    main()
