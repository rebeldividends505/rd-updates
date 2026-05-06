#!/usr/bin/env python3
"""
RD Bot — Daily Update Web Deploy
Usage: python3 deploy.py --date YYYY-MM-DD --file /path/to/daily_update.html
       python3 deploy.py --date 2026-05-07 --file /path/to/daily_update.html --dry-run
"""
import subprocess, shutil, os, argparse
from datetime import datetime

SITE_DIR = os.path.dirname(os.path.abspath(__file__))
DOMAIN   = 'updates.rebeldividends.com'

def deploy_web(date_str, html_src_path, dry_run=False):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    # e.g. "may6" from "2026-05-06"
    date_slug = dt.strftime('%b%-d').lower()
    daily_dir = f'{SITE_DIR}/public/daily'
    dst_path  = f'{daily_dir}/{date_slug}.html'

    os.makedirs(daily_dir, exist_ok=True)

    if html_src_path and not os.path.exists(html_src_path):
        print(f'[ERROR] Source file not found: {html_src_path}')
        return False

    if dry_run:
        print(f'[DRY RUN] Would copy {html_src_path} → /public/daily/{date_slug}.html')
        print(f'[DRY RUN] Would push to GitHub → Vercel auto-deploy (~60s)')
        print(f'[DRY RUN] URL: https://{DOMAIN}/daily/{date_slug}.html')
        return True

    if html_src_path:
        shutil.copy(html_src_path, dst_path)
        print(f'✅ Staged: /public/daily/{date_slug}.html')

    for cmd in [
        ['git', 'add', '.'],
        ['git', 'commit', '-m', f'Daily update — {date_str}'],
        ['git', 'push', 'origin', 'main'],
    ]:
        result = subprocess.run(cmd, cwd=SITE_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            if 'nothing to commit' in result.stdout or 'nothing to commit' in result.stderr:
                print(f'  (nothing to commit, skipping)')
                continue
            print(f'[ERROR] {" ".join(cmd)}:\n  {result.stderr[:300]}')
            return False
        print(f'  {" ".join(cmd[:2])} ✅')

    url = f'https://{DOMAIN}/daily/{date_slug}.html'
    print(f'\n🚀 Pushed! Live in ~60s')
    print(f'   Preview URL: {url}')
    return url

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deploy RD daily update to web')
    parser.add_argument('--date', required=True, help='YYYY-MM-DD')
    parser.add_argument('--file', default=None, help='Path to daily HTML file (optional)')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    deploy_web(args.date, args.file, dry_run=args.dry_run)
