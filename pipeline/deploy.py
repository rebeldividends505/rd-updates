#!/usr/bin/env python3
"""
RD Bot — daily web deploy.

Writes public/daily/latest.json so the Next.js home redirect points at the
latest update, then commits + pushes (Vercel rebuilds the static routes).
The actual day's content is rendered by src/app/daily/[slug]/page.tsx, which
reads outputs/<YYYY-MM-DD>/email.html at build time.

Usage:
  python3 pipeline/deploy.py --date 2026-05-07
  python3 pipeline/deploy.py --date 2026-05-07 --dry-run
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent.parent
DAILY_DIR = REPO_DIR / "public" / "daily"
LATEST_JSON = DAILY_DIR / "latest.json"
DOMAIN = "updates.rebeldividends.com"


def write_latest_json(date_str: str, *, dry_run: bool = False) -> bool:
    payload = {"date": date_str, "slug": date_str}
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2) + "\n"
    if dry_run:
        print(f"[DRY RUN] would write {LATEST_JSON.relative_to(REPO_DIR)}: {payload}")
        return True
    LATEST_JSON.write_text(serialized, encoding="utf-8")
    print(f"    wrote {LATEST_JSON.relative_to(REPO_DIR)} -> {payload}")
    return True


def deploy_web(date_str: str, *, dry_run: bool = False):
    # Validate date format up front.
    datetime.strptime(date_str, "%Y-%m-%d")

    output_dir = REPO_DIR / "outputs" / date_str
    if not (output_dir / "email.html").exists():
        print(f"[ERROR] {output_dir/'email.html'} not found — nothing to deploy")
        return False

    write_latest_json(date_str, dry_run=dry_run)

    url = f"https://{DOMAIN}/daily/{date_str}"
    home = f"https://{DOMAIN}"

    if dry_run:
        print(f"[DRY RUN] would push -> Vercel auto-deploy")
        print(f"[DRY RUN] URL: {url}")
        print(f"[DRY RUN] Home redirects to: {url}")
        return url

    for cmd in (
        ["git", "add", "public/", "outputs/"],
        ["git", "commit", "-m", f"Daily update — {date_str}"],
        ["git", "push", "origin", "main"],
    ):
        result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
        combined = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            if "nothing to commit" in combined:
                print("    (nothing to commit, skipping push)")
                return url
            print(f"[ERROR] {' '.join(cmd)}:\n  {combined[:400]}")
            return False
        print(f"    {' '.join(cmd[:2])} ok")

    print(f"\nPushed. Live in ~60s.")
    print(f"  Day URL: {url}")
    print(f"  Home (redirects to latest): {home}")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy RD daily update to web")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--file",
        default=None,
        help="(deprecated) ignored — content is now rendered from outputs/<date>/email.html by Next.js",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.file:
        print("[NOTE] --file is deprecated and ignored; content comes from outputs/<date>/email.html")

    result = deploy_web(args.date, dry_run=args.dry_run)
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
