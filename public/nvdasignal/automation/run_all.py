#!/usr/bin/env python3
"""
run_all.py — Master runner for the AI Short-Signal daily pipeline (Module C)
=============================================================================
Runs the full sequence:
  1. update_signals.py  — fetch fresh market data → live.json
  2. snapshot.py        — log state to score_history.csv + snapshots/
  3. alert_engine.py    — diff vs last run, send Telegram alerts

Usage:
  python3 run_all.py            # full run
  python3 run_all.py --dry-run  # dry-run passed to each stage
"""
import sys, subprocess, datetime as dt
from pathlib import Path

HERE    = Path(__file__).resolve().parent
PYTHON  = sys.executable
DRY     = "--dry-run" in sys.argv

STEPS = [
    ("update_signals", HERE / "update_signals.py"),
    ("snapshot",       HERE / "snapshot.py"),
    ("alert_engine",   HERE / "alert_engine.py"),
]

def log(*a):
    print(f"[{dt.datetime.now():%H:%M:%S}]", *a, flush=True)

def run_step(label, script_path):
    cmd = [PYTHON, str(script_path)]
    if DRY:
        cmd.append("--dry-run")
    log(f"{'='*60}")
    log(f"STEP: {label}")
    log(f"{'='*60}")
    r = subprocess.run(cmd, cwd=str(HERE))
    if r.returncode != 0:
        log(f"ERROR: {label} exited {r.returncode} — aborting pipeline.")
        sys.exit(r.returncode)
    log(f"OK: {label} completed.")
    print()

def main():
    log(f"AI Short-Signal daily pipeline — {dt.date.today()} {'(DRY RUN)' if DRY else ''}")
    print()
    for label, script in STEPS:
        run_step(label, script)
    log("Pipeline complete.")

if __name__ == "__main__":
    main()
