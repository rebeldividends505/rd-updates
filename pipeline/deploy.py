#!/usr/bin/env python3
"""
RD Bot — daily web deploy.

Stages the day's elementor.html into public/daily/<dateslug>.html and
updates the constants at the top of src/app/page.tsx so the home page shows
today's numbers. Then commits + pushes (Vercel picks up the rest).

Usage:
  python3 pipeline/deploy.py --date 2026-05-07 --file outputs/2026-05-07/elementor.html
  python3 pipeline/deploy.py --date 2026-05-07 --file ... --dry-run
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

REPO_DIR = Path(__file__).resolve().parent.parent
DAILY_DIR = REPO_DIR / "public" / "daily"
PAGE_TSX = REPO_DIR / "src" / "app" / "page.tsx"
DOMAIN = "updates.rebeldividends.com"


def date_slug(dt: datetime) -> str:
    """e.g. 2026-05-06 -> 'may6'."""
    try:
        return dt.strftime("%b%-d").lower()
    except ValueError:
        # Windows / strict-libc fallback
        return f"{dt.strftime('%b').lower()}{dt.day}"


def parse_deploy_notes(notes_path: Path) -> dict[str, str]:
    """Extract the key numbers from a deploy-notes.md file.

    Looks for lines like:
        - HYPE: $43.00
        - Share price: $0.001750
        - Day %: +1.0%
        - Day theme: replay
        - Headline: Your RD Update for Wednesday
    Returns whatever it finds; missing keys just stay absent.
    """
    if not notes_path.exists():
        return {}
    text = notes_path.read_text(encoding="utf-8")
    patterns = {
        "hype_price": r"HYPE[^$\n:]*[:\-]\s*\$?([\d.]+)",
        "share_price": r"(?:RD\s*)?[Ss]hare\s*price[^$\n:]*[:\-]\s*\$?([\d.]+)",
        "day_pct": r"[Dd]ay\s*%[^:\n]*[:\-]\s*([+\-]?\d+\.?\d*%?)",
        "day_theme": r"[Dd]ay\s*theme[^:\n]*[:\-]\s*(\w+)",
        "headline": r"[Hh]eadline[^:\n]*[:\-]\s*(.+)",
    }
    out: dict[str, str] = {}
    for key, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            out[key] = m.group(1).strip()
    return out


def update_page_tsx(
    dt: datetime,
    *,
    hype_price: Optional[str],
    share_price: Optional[str],
    day_pct: Optional[str],
    day_theme: Optional[str],
    headline: Optional[str],
    dry_run: bool = False,
) -> bool:
    """Patch the leading constants of src/app/page.tsx in place."""
    if not PAGE_TSX.exists():
        print(f"[WARN] {PAGE_TSX} not found — skipping page.tsx update")
        return False

    src = PAGE_TSX.read_text(encoding="utf-8")
    original = src

    update_date = dt.strftime("%A, %B %-d, %Y")
    src = re.sub(
        r'const UPDATE_DATE = "[^"]*";',
        f'const UPDATE_DATE = "{update_date}";',
        src,
        count=1,
    )
    if hype_price:
        src = re.sub(
            r"const HYPE_PRICE = [\d.]+;",
            f"const HYPE_PRICE = {float(hype_price):.2f};",
            src,
            count=1,
        )
    if share_price:
        src = re.sub(
            r'const RD_SHARE_PRICE = "[^"]*";',
            f'const RD_SHARE_PRICE = "{float(share_price):.5f}";',
            src,
            count=1,
        )
    if day_pct:
        pct = day_pct if day_pct.endswith("%") else f"{day_pct}%"
        src = re.sub(
            r'const RD_DAY_CHANGE = "[^"]*";',
            f'const RD_DAY_CHANGE = "{pct}";',
            src,
            count=1,
        )
    if day_theme:
        src = re.sub(
            r'const DAY_THEME = "[^"]*";',
            f'const DAY_THEME = "{day_theme}";',
            src,
            count=1,
        )

    if src == original:
        print("    page.tsx: no changes")
        return False

    if dry_run:
        print("[DRY RUN] would patch src/app/page.tsx constants")
        return True

    PAGE_TSX.write_text(src, encoding="utf-8")
    print("    page.tsx: constants updated")
    return True


def deploy_web(date_str: str, html_src_path: Optional[str], *, dry_run: bool = False):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    slug = date_slug(dt)
    dst_path = DAILY_DIR / f"{slug}.html"
    DAILY_DIR.mkdir(parents=True, exist_ok=True)

    if html_src_path:
        src = Path(html_src_path)
        if not src.exists():
            print(f"[ERROR] source file not found: {src}")
            return False
        if dry_run:
            print(f"[DRY RUN] would copy {src} -> public/daily/{slug}.html")
        else:
            shutil.copy(src, dst_path)
            print(f"    staged: public/daily/{slug}.html")

    # Update page.tsx from the day's deploy notes (best-effort)
    notes_path = REPO_DIR / "outputs" / date_str / "deploy-notes.md"
    notes = parse_deploy_notes(notes_path)
    update_page_tsx(
        dt,
        hype_price=notes.get("hype_price"),
        share_price=notes.get("share_price"),
        day_pct=notes.get("day_pct"),
        day_theme=notes.get("day_theme"),
        headline=notes.get("headline"),
        dry_run=dry_run,
    )

    if dry_run:
        print(f"[DRY RUN] would push -> Vercel auto-deploy")
        print(f"[DRY RUN] URL: https://{DOMAIN}/daily/{slug}.html")
        return True

    for cmd in (
        ["git", "add", "public/", "src/", "outputs/"],
        ["git", "commit", "-m", f"Daily update — {date_str}"],
        ["git", "push", "origin", "main"],
    ):
        result = subprocess.run(cmd, cwd=REPO_DIR, capture_output=True, text=True)
        combined = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            if "nothing to commit" in combined:
                print("    (nothing to commit, skipping push)")
                return f"https://{DOMAIN}/daily/{slug}.html"
            print(f"[ERROR] {' '.join(cmd)}:\n  {combined[:400]}")
            return False
        print(f"    {' '.join(cmd[:2])} ok")

    url = f"https://{DOMAIN}/daily/{slug}.html"
    print(f"\nPushed. Live in ~60s. {url}")
    return url


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy RD daily update to web")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--file",
        default=None,
        help="Path to elementor.html (optional; defaults to outputs/<date>/elementor.html)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    src = args.file
    if not src:
        guess = REPO_DIR / "outputs" / args.date / "elementor.html"
        src = str(guess) if guess.exists() else None

    result = deploy_web(args.date, src, dry_run=args.dry_run)
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
