#!/usr/bin/env python3
"""
Generate the Early Warning Dashboard chart — 6 indicators we monitor daily
for signs that the dealer-gamma suppression regime is breaking.

Dark theme. Title/footer match the rest of the May 19 webinar build.

Usage:
    python3 pipeline/gen_early_warning_chart.py \
        --date 2026-05-19 \
        --output outputs/2026-05-19/charts/early-warning-dashboard.png

Optional --readings expects a JSON string overriding the placeholder GREEN
default values:
    --readings '{"VIX":17.2,"SKEW":138,"SMH_50DMA":"above","PUTCALL":0.78,"LEV_ETF_FLOWS":"inflows","HYG_OAS":310}'

If --readings is omitted, all 6 dots render GREEN as the pre-Tuesday placeholder.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Brand palette
BG = "#0a0a0a"
PANEL = "#171717"
ORANGE = "#ff6600"
WHITE = "#ffffff"
MUTED = "#94a3b8"
GREEN = "#0a7c42"
YELLOW = "#f59e0b"
RED = "#c41e3a"


@dataclass
class Indicator:
    name: str
    threshold: str
    current: str
    status: str  # "green" | "yellow" | "red" | "grey"


def _status_color(status: str) -> str:
    return {
        "green": GREEN,
        "yellow": YELLOW,
        "red": RED,
        "grey": MUTED,
    }.get(status, MUTED)


def build_indicators(readings: dict | None) -> list[Indicator]:
    """Build the 6 indicators. If readings is None, all default to GREEN placeholder."""
    rows: list[Indicator] = []

    # 1. VIX
    vix = (readings or {}).get("VIX")
    if vix is None:
        rows.append(Indicator("VIX (1-month)", "Above 18", "TBD", "green"))
    else:
        try:
            v = float(vix)
            status = "red" if v >= 18 else "yellow" if v >= 14.4 else "green"
            rows.append(Indicator("VIX (1-month)", "Above 18", f"{v:.1f}", status))
        except (TypeError, ValueError):
            rows.append(Indicator("VIX (1-month)", "Above 18", "TBD", "grey"))

    # 2. SKEW
    skew = (readings or {}).get("SKEW")
    if skew is None:
        rows.append(Indicator("CBOE SKEW Index", "Above 150", "TBD", "green"))
    else:
        try:
            s = float(skew)
            status = "red" if s >= 150 else "yellow" if s >= 120 else "green"
            rows.append(Indicator("CBOE SKEW Index", "Above 150", f"{s:.0f}", status))
        except (TypeError, ValueError):
            rows.append(Indicator("CBOE SKEW Index", "Above 150", "TBD", "grey"))

    # 3. SMH 50-day MA
    smh = (readings or {}).get("SMH_50DMA")
    if smh is None:
        rows.append(Indicator("SMH 50-day MA", "Break below", "Above", "green"))
    else:
        s = str(smh).lower()
        if s in ("below", "broken"):
            rows.append(Indicator("SMH 50-day MA", "Break below", "Below", "red"))
        elif s in ("test", "testing", "near"):
            rows.append(Indicator("SMH 50-day MA", "Break below", "Testing", "yellow"))
        else:
            rows.append(Indicator("SMH 50-day MA", "Break below", "Above", "green"))

    # 4. Put/Call ratio
    pc = (readings or {}).get("PUTCALL")
    if pc is None:
        rows.append(Indicator("Put/Call Ratio (CBOE)", "Above 1.0", "TBD", "green"))
    else:
        try:
            p = float(pc)
            status = "red" if p >= 1.0 else "yellow" if p >= 0.8 else "green"
            rows.append(Indicator("Put/Call Ratio (CBOE)", "Above 1.0", f"{p:.2f}", status))
        except (TypeError, ValueError):
            rows.append(Indicator("Put/Call Ratio (CBOE)", "Above 1.0", "TBD", "grey"))

    # 5. Levered ETF flows
    flows = (readings or {}).get("LEV_ETF_FLOWS")
    if flows is None:
        rows.append(Indicator("Levered ETF Outflows", "SOXL/TQQQ redemptions", "Inflows", "green"))
    else:
        f = str(flows).lower()
        if f in ("outflows", "redemptions"):
            rows.append(Indicator("Levered ETF Outflows", "SOXL/TQQQ redemptions", "Outflows", "red"))
        elif f in ("mixed", "flat"):
            rows.append(Indicator("Levered ETF Outflows", "SOXL/TQQQ redemptions", "Mixed", "yellow"))
        else:
            rows.append(Indicator("Levered ETF Outflows", "SOXL/TQQQ redemptions", "Inflows", "green"))

    # 6. HY credit spreads
    hyg = (readings or {}).get("HYG_OAS")
    if hyg is None:
        rows.append(Indicator("HY Credit Spreads (OAS)", "Above 350 bps", "TBD", "green"))
    else:
        try:
            h = float(hyg)
            status = "red" if h >= 350 else "yellow" if h >= 280 else "green"
            rows.append(Indicator("HY Credit Spreads (OAS)", "Above 350 bps", f"{h:.0f} bps", status))
        except (TypeError, ValueError):
            rows.append(Indicator("HY Credit Spreads (OAS)", "Above 350 bps", "TBD", "grey"))

    return rows


def draw_chart(indicators: list[Indicator], run_date: datetime, out_paths: list[str]):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": MUTED,
        "axes.labelcolor": WHITE,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": WHITE,
    })

    # 1280 x 720 at 160 dpi -> 8 x 4.5 inches
    fig = plt.figure(figsize=(8, 4.5), dpi=160)
    fig.patch.set_facecolor(BG)

    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_facecolor(BG)
    ax.axis("off")

    # Title + subtitle
    ax.text(0.04, 0.92, "Early Warning Dashboard",
            fontsize=20, fontweight="bold", color=WHITE, va="center")
    ax.text(0.04, 0.86, "Tracking the Gamma Trap",
            fontsize=12, color=ORANGE, va="center", fontweight="bold")
    ax.text(0.96, 0.92, f"As of {run_date.strftime('%b %d, %Y')}",
            fontsize=10, color=MUTED, va="center", ha="right")

    # Column headers
    header_y = 0.78
    ax.text(0.06, header_y, "INDICATOR", fontsize=9, color=ORANGE,
            fontweight="bold", va="center")
    ax.text(0.46, header_y, "THRESHOLD", fontsize=9, color=ORANGE,
            fontweight="bold", va="center")
    ax.text(0.76, header_y, "CURRENT", fontsize=9, color=ORANGE,
            fontweight="bold", va="center")

    # Header underline
    ax.add_patch(mpatches.Rectangle((0.04, header_y - 0.025), 0.92, 0.002,
                                     facecolor=ORANGE, edgecolor="none"))

    # 6 indicator rows
    row_top = 0.72
    row_h = 0.085
    for i, ind in enumerate(indicators):
        y = row_top - i * row_h

        # Alternating row band
        if i % 2 == 0:
            ax.add_patch(mpatches.Rectangle((0.04, y - row_h / 2 + 0.005),
                                             0.92, row_h - 0.01,
                                             facecolor=PANEL, edgecolor="none",
                                             alpha=0.6))

        # Indicator name
        ax.text(0.06, y, ind.name, fontsize=11, color=WHITE,
                fontweight="bold", va="center")
        # Threshold
        ax.text(0.46, y, ind.threshold, fontsize=10, color=MUTED, va="center")
        # Current reading
        ax.text(0.76, y, ind.current, fontsize=11, color=WHITE,
                fontweight="bold", va="center")

        # Status dot
        dot_color = _status_color(ind.status)
        circle = mpatches.Circle((0.92, y), 0.018,
                                  facecolor=dot_color, edgecolor=WHITE, lw=1.2)
        ax.add_patch(circle)

    # Legend (status dot key) at the bottom
    legend_y = 0.13
    ax.text(0.04, legend_y + 0.04, "STATUS KEY", fontsize=8, color=ORANGE,
            fontweight="bold", va="center")
    legend_items = [
        ("Below threshold", GREEN),
        ("Within 20% of threshold", YELLOW),
        ("At or above threshold", RED),
    ]
    lx = 0.04
    for label, color in legend_items:
        ax.add_patch(mpatches.Circle((lx + 0.01, legend_y), 0.011,
                                      facecolor=color, edgecolor=WHITE, lw=0.8))
        ax.text(lx + 0.028, legend_y, label, fontsize=9, color=WHITE, va="center")
        lx += 0.27

    # Footer
    ax.text(0.04, 0.04, "Updated daily through June 17. — Rebel Dividends",
            fontsize=9, color=MUTED, va="center", style="italic")
    ax.text(0.96, 0.04, "rebeldividends.com",
            fontsize=9, color=MUTED, va="center", ha="right", alpha=0.8)

    for out in out_paths:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, facecolor=BG, dpi=160, bbox_inches="tight")
        print(f"wrote {out}")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True, help="run date YYYY-MM-DD")
    p.add_argument("--output", required=True,
                   help="primary output path (e.g., outputs/2026-05-19/charts/early-warning-dashboard.png)")
    p.add_argument("--also-copy-to", action="append", default=[],
                   help="additional output path (repeatable)")
    p.add_argument("--readings",
                   help='Optional JSON dict of current readings. If omitted, all dots render GREEN as placeholder.')
    args = p.parse_args()

    run_date = datetime.strptime(args.date, "%Y-%m-%d")
    readings = json.loads(args.readings) if args.readings else None

    indicators = build_indicators(readings)

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def resolve(path: str) -> str:
        return path if os.path.isabs(path) else os.path.join(repo_root, path)

    out_paths = [resolve(args.output)] + [resolve(p) for p in args.also_copy_to]
    draw_chart(indicators, run_date, out_paths)


if __name__ == "__main__":
    main()
