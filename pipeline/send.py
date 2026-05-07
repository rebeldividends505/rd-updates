#!/usr/bin/env python3
"""
RD Daily — Brevo email + SimpleTexting SMS delivery.

Usage:
  python3 send.py --date YYYY-MM-DD --test      # sends to Jason only (morning preview)
  python3 send.py --date YYYY-MM-DD --test-all  # sends to Jason + Ryan + Dean (after Jason approves)
  python3 send.py --date YYYY-MM-DD --live      # sends to full lists (after go-live)

Reads outputs/<date>/email.html and outputs/<date>/sms.txt.
The sms.txt file format is:
    SUBJECT: <subject line>

    SMS: <sms body, may span multiple lines>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Load .env from repo root (never committed; holds API keys)
_ENV_PATH = Path(__file__).parent.parent / ".env"
if _ENV_PATH.exists():
    for _line in _ENV_PATH.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

REPO_DIR = Path(__file__).resolve().parent.parent

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
SIMPLETEXTING_API_KEY = os.environ.get("SIMPLETEXTING_API_KEY", "")
SIMPLETEXTING_LIST_ID = os.environ.get("SIMPLETEXTING_LIST_ID", "")

# Brevo lists — see instructions/brand-config.md
BREVO_EMAIL_LIST = 4          # RD Investors - Email (full list)
BREVO_INVESTOR_LIST = 5       # RD Investors - SMS (full list)
BREVO_TEST_LIST = 6           # internal QA list

# Test recipients
# --test      = Jason only (morning auto-run, before Jason approves)
# --test-all  = all 3 (after Jason approves the content, before go-live)
TEST_JASON_ONLY = [{"email": "jasonjamescox85@gmail.com", "phone": "5055956003", "name": "Jason"}]
TEST_CONTACTS_ALL = [
    {"email": "jasonjamescox85@gmail.com", "phone": "5055956003", "name": "Jason"},
    {"email": "ryan@rebeldividends.com",   "phone": "5052808236", "name": "Ryan"},
    {"email": "dean@rebeldividends.com",   "phone": "5053227515", "name": "Dean"},
]
TEST_EMAIL = TEST_JASON_ONLY[0]["email"]
TEST_PHONE = TEST_JASON_ONLY[0]["phone"]

SENDER_EMAIL = "support@rebeldividends.com"
SENDER_NAME = "Rebel Dividends"


def load_output(date_str: str) -> dict[str, str]:
    """Read the generated files for a given date."""
    output_dir = REPO_DIR / "outputs" / date_str
    if not output_dir.is_dir():
        return {}
    out: dict[str, str] = {}
    for fname in ("email.html", "sms.txt", "deploy-notes.md"):
        path = output_dir / fname
        if path.exists():
            key = fname.replace(".", "_").replace("-", "_")
            out[key] = path.read_text(encoding="utf-8")
    return out


def parse_subject(sms_txt: str) -> Optional[str]:
    """Pull `SUBJECT: ...` from the first non-blank line of sms.txt."""
    for line in sms_txt.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        if upper.startswith("SUBJECT:"):
            return stripped.split(":", 1)[1].strip()
        if upper.startswith("SUBJECT"):
            return stripped[len("SUBJECT"):].lstrip(": ").strip()
        # First non-blank line wasn't a subject — give up.
        break
    return None


def parse_sms_body(sms_txt: str) -> str:
    """Extract the SMS body — everything after the `SMS:` marker."""
    lines = sms_txt.splitlines()
    body: list[str] = []
    in_sms = False
    for line in lines:
        stripped = line.strip()
        if not in_sms:
            upper = stripped.upper()
            if upper.startswith("SMS:") or upper == "SMS":
                in_sms = True
                rest = stripped.split(":", 1)[1].strip() if ":" in stripped else ""
                if rest:
                    body.append(rest)
            continue
        if stripped:
            body.append(stripped)
    return " ".join(body).strip()


def get_subject(output: dict[str, str]) -> str:
    parsed = parse_subject(output.get("sms_txt", ""))
    if parsed:
        return parsed
    return f"Rebel Dividends Update — {datetime.now().strftime('%B %d, %Y')}"


def send_email_brevo(
    subject: str,
    html_body: str,
    *,
    to_email: Optional[str] = None,
    list_ids: Optional[list[int]] = None,
    test: bool = True,
) -> bool:
    """Test = transactional one-off to a single address. Live = campaign."""
    if not BREVO_API_KEY:
        print("[WARN] BREVO_API_KEY not set — skipping email send")
        return False
    headers = {"api-key": BREVO_API_KEY, "Content-Type": "application/json"}

    if test and to_email:
        endpoint = "https://api.brevo.com/v3/smtp/email"
        payload = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "to": [{"email": to_email}],
            "subject": subject,
            "htmlContent": html_body,
        }
    else:
        endpoint = "https://api.brevo.com/v3/emailCampaigns"
        payload = {
            "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
            "name": f"RD Daily — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "subject": subject,
            "htmlContent": html_body,
            "recipients": {"listIds": list_ids or [BREVO_EMAIL_LIST]},
        }

    resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    print(f"Brevo: {resp.status_code} {resp.text[:200]}")
    return resp.status_code < 300


def send_sms_simpletexting(
    message: str,
    *,
    phone: Optional[str] = None,
    list_id: Optional[str] = None,
    test: bool = True,
) -> bool:
    if not SIMPLETEXTING_API_KEY:
        print("[WARN] SIMPLETEXTING_API_KEY not set — skipping SMS send")
        return False
    headers = {
        "Authorization": f"Bearer {SIMPLETEXTING_API_KEY}",
        "Content-Type": "application/json",
    }

    if test and phone:
        endpoint = "https://app2.simpletexting.com/v2/api/messages"
        payload = {"text": message, "contactPhone": phone}
    else:
        endpoint = "https://app2.simpletexting.com/v2/api/campaigns"
        payload = {"text": message, "listId": list_id or SIMPLETEXTING_LIST_ID}

    resp = requests.post(endpoint, json=payload, headers=headers, timeout=30)
    print(f"SimpleTexting: {resp.status_code} {resp.text[:200]}")
    return resp.status_code < 300


def main() -> int:
    parser = argparse.ArgumentParser(description="RD daily email + SMS sender")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--test", action="store_true", help="send to Jason only (morning preview)")
    parser.add_argument("--test-all", action="store_true", help="send to Jason + Ryan + Dean (after Jason approves)")
    parser.add_argument("--live", action="store_true", help="send to full lists")
    parser.add_argument(
        "--list",
        choices=("email", "investor"),
        default="email",
        help="Which Brevo list to target on --live (default: email)",
    )
    args = parser.parse_args()

    if not (args.test or getattr(args, 'test_all', False) or args.live):
        print("[ERROR] must pass --test, --test-all, or --live")
        return 2
    if args.test and args.live:
        print("[ERROR] --test and --live are mutually exclusive")
        return 2

    output = load_output(args.date)
    if not output:
        print(f"[ERROR] no output found for {args.date}")
        return 1

    subject = get_subject(output)
    email_html = output.get("email_html", "")
    sms_body = parse_sms_body(output.get("sms_txt", ""))

    if not email_html:
        print(f"[ERROR] outputs/{args.date}/email.html is missing or empty")
        return 1

    print(f"--- {'TEST' if args.test else 'LIVE'} SEND ({args.date}) ---")
    print(f"Subject: {subject}")
    print(f"SMS preview: {(sms_body or '<empty>')[:140]}")

    if args.test:
        recipients = TEST_JASON_ONLY
        print(f"--- TEST SEND — Jason only ---")
        for contact in recipients:
            print(f"  → {contact['name']} ({contact['email']} / {contact['phone']})")
            send_email_brevo(subject, email_html, to_email=contact["email"], test=True)
            if sms_body:
                send_sms_simpletexting(sms_body, phone=contact["phone"], test=True)
            else:
                print(f"[INFO] no SMS body — skipping SMS for {contact['name']}")
        return 0

    if getattr(args, 'test_all', False):
        print(f"--- TEST-ALL SEND — Jason + Ryan + Dean ---")
        for contact in TEST_CONTACTS_ALL:
            print(f"  → {contact['name']} ({contact['email']} / {contact['phone']})")
            send_email_brevo(subject, email_html, to_email=contact["email"], test=True)
            if sms_body:
                send_sms_simpletexting(sms_body, phone=contact["phone"], test=True)
            else:
                print(f"[INFO] no SMS body — skipping SMS for {contact['name']}")
        return 0

    list_id = BREVO_EMAIL_LIST if args.list == "email" else BREVO_INVESTOR_LIST
    send_email_brevo(subject, email_html, list_ids=[list_id], test=False)
    if sms_body:
        send_sms_simpletexting(sms_body, list_id=SIMPLETEXTING_LIST_ID, test=False)
    print("Live send complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
