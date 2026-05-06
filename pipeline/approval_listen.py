#!/usr/bin/env python3
"""
RD Daily — approval listener (stub).

Polls for Jason's approval of the day's test send. Once Jason approves, this
script will trigger the live send by invoking `send.py --live`.

For now it just prints the manual instructions — full Telegram/OpenClaw
integration comes later. The contract that downstream code can rely on:

  - Exit 0 + write `outputs/<date>/approved.flag` once approved.
  - Exit non-zero on timeout or rejection.

Usage:
  python3 pipeline/approval_listen.py --date YYYY-MM-DD [--timeout 3600]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent

INSTRUCTIONS = """
=== RD daily approval pending ===
Date: {date}
Test email sent to: jasonjamescox85@gmail.com
Test SMS sent to:   5055956003

Review the test message, then approve manually with one of:

  # Approve and trigger live send:
  touch outputs/{date}/approved.flag
  python3 pipeline/send.py --date {date} --live

  # Reject (no live send):
  touch outputs/{date}/rejected.flag

This listener will poll every {interval}s for up to {timeout}s.
Telegram/OpenClaw approval integration is TODO.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="RD daily approval poller")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--timeout",
        type=int,
        default=3600,
        help="Seconds to wait for approval before giving up (default: 3600)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=15,
        help="Seconds between polls (default: 15)",
    )
    args = parser.parse_args()

    output_dir = REPO_DIR / "outputs" / args.date
    if not output_dir.is_dir():
        print(f"[ERROR] no outputs directory at {output_dir}")
        return 1

    approved = output_dir / "approved.flag"
    rejected = output_dir / "rejected.flag"

    print(
        INSTRUCTIONS.format(
            date=args.date,
            interval=args.interval,
            timeout=args.timeout,
        )
    )

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        if approved.exists():
            print(f"[approval] approved at {approved}")
            return 0
        if rejected.exists():
            print(f"[approval] rejected at {rejected}")
            return 2
        time.sleep(args.interval)

    print(f"[approval] timed out after {args.timeout}s — no decision")
    return 3


if __name__ == "__main__":
    sys.exit(main())
