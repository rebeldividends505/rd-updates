#!/usr/bin/env python3
"""
RD Daily — research fetch.

Pulls today's price + day% from the RD Track Record sheet (via gog) and the
HYPE spot price from CoinGecko (Yahoo Finance fallback). Emits a single JSON
object on stdout for the rest of the pipeline to consume.

On Mondays, also fetches the Tuesday-package data cells (B1, K1, M26, M29,
M30, I20). Other days `tuesday_data` is null.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Optional

SHEET_ID = "1g4N5EEctfd_cu_PPA3FGb8cHxF5OgVOR2qs0b63z82A"
COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=hyperliquid&vs_currencies=usd"
)


def _gog_read(cell_range: str) -> list:
    """Run `gog sheets read SHEET_ID RANGE -j` and return parsed JSON.

    Raises RuntimeError on failure so the caller decides how to handle it.
    """
    cmd = ["gog", "sheets", "read", SHEET_ID, cell_range, "-j"]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if proc.returncode != 0:
        raise RuntimeError(
            f"gog sheets read {cell_range} failed: {proc.stderr.strip()}"
        )
    try:
        data = json.loads(proc.stdout)
        # gog returns {"range": "...", "values": [[...], ...]} — extract values
        if isinstance(data, dict) and "values" in data:
            return data["values"]
        return data
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"gog sheets read {cell_range} returned non-JSON: {exc}"
        )


def _flatten(rows: list) -> list[str]:
    """Flatten gog's nested-list JSON output to a flat list of strings."""
    out: list[str] = []
    for row in rows or []:
        if isinstance(row, list):
            for cell in row:
                out.append("" if cell is None else str(cell))
        else:
            out.append("" if row is None else str(row))
    return out


def _format_share_price(raw: str) -> str:
    """Normalize the P23 value to exactly 5 decimals (no leading $)."""
    cleaned = re.sub(r"[^0-9.\-]", "", raw)
    if not cleaned:
        return "0.00000"
    return f"{float(cleaned):.5f}"


def _format_day_pct(raw: str) -> str:
    """Normalize P24 to one decimal with sign, e.g. '+1.0' or '-3.7'."""
    cleaned = raw.strip().replace("%", "")
    if not cleaned:
        return "+0.0"
    val = float(cleaned)
    # Sheet sometimes returns 0.0107 (fractional) instead of 1.07.
    if -1.0 < val < 1.0 and val != 0:
        val = val * 100
    return f"{val:+.1f}"


def fetch_share_price() -> tuple[str, str]:
    """Fetch P23 (share price) and P24 (day %) from the sheet."""
    rows = _gog_read("P23:P24")
    flat = _flatten(rows)
    if len(flat) < 2:
        raise RuntimeError(f"Expected 2 cells from P23:P24, got {flat!r}")
    return _format_share_price(flat[0]), _format_day_pct(flat[1])


def fetch_hype_price() -> str:
    """Fetch HYPE spot price (USD), 2 decimals. Tries CoinGecko then Yahoo."""
    try:
        import urllib.request

        with urllib.request.urlopen(COINGECKO_URL, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        price = float(data["hyperliquid"]["usd"])
        return f"{price:.2f}"
    except Exception as exc:  # noqa: BLE001 — fallback path
        print(f"[research_fetch] CoinGecko failed: {exc}", file=sys.stderr)

    try:
        import yfinance  # type: ignore

        ticker = yfinance.Ticker("HYPE-USD")
        hist = ticker.history(period="1d")
        if hist.empty:
            raise RuntimeError("yfinance returned empty history")
        price = float(hist["Close"].iloc[-1])
        return f"{price:.2f}"
    except Exception as exc:  # noqa: BLE001 — surface to caller
        raise RuntimeError(f"HYPE price unavailable: {exc}")


def fetch_tuesday_data() -> Optional[dict]:
    """Fetch the six Track Record cells used for the Tuesday package."""
    cells = {
        "portfolio_value": "B1",
        "total_shares": "K1",
        "dividend_amount": "M26",
        "week_return": "M29",
        "dividend_roi": "M30",
        "cash_balance": "I20",
    }
    out: dict[str, str] = {}
    for label, ref in cells.items():
        try:
            rows = _gog_read(ref)
            flat = _flatten(rows)
            out[label] = flat[0] if flat else ""
        except RuntimeError as exc:
            print(
                f"[research_fetch] tuesday cell {ref} failed: {exc}",
                file=sys.stderr,
            )
            out[label] = ""
    return out


def read_week_number() -> Optional[int]:
    """Best-effort read of the week number from instructions/current-week.md."""
    try:
        from pathlib import Path

        path = (
            Path(__file__).resolve().parent.parent
            / "instructions"
            / "current-week.md"
        )
        text = path.read_text(encoding="utf-8")
        m = re.search(
            r"week number.*?:\s*(\d+)", text, flags=re.IGNORECASE
        )
        if m:
            return int(m.group(1))
    except Exception as exc:  # noqa: BLE001
        print(f"[research_fetch] week number read failed: {exc}", file=sys.stderr)
    return None


def main() -> int:
    now = datetime.now(timezone.utc).astimezone()
    today = now.date()
    day_of_week = now.strftime("%A")

    try:
        share_price, day_pct = fetch_share_price()
    except RuntimeError as exc:
        print(f"[research_fetch] FATAL: {exc}", file=sys.stderr)
        return 1

    try:
        hype_price = fetch_hype_price()
    except RuntimeError as exc:
        print(f"[research_fetch] FATAL: {exc}", file=sys.stderr)
        return 1

    tuesday_data = fetch_tuesday_data() if day_of_week == "Monday" else None

    payload = {
        "date": today.isoformat(),
        "day_of_week": day_of_week,
        "share_price": share_price,
        "day_pct": day_pct,
        "hype_price": hype_price,
        "week_number": read_week_number(),
        "tuesday_data": tuesday_data,
        "fetched_at": now.replace(microsecond=0).isoformat(),
    }

    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
