#!/usr/bin/env python3
"""
Generate the "$100K at the April 2024 Pivot" dark-theme chart.

Simulates Reinvestor vs Collector using weekly steps inside each month:
  - weekly_price interpolates linearly from monthly open -> close
  - weekly_div_per_share = monthly_div / weeks_in_month
  - Reinvestor: buys MORE shares each week using that week's dividend cash
  - Collector: shares fixed; cash piles up

Usage:
    python3 pipeline/gen_pivot_chart.py --date 2026-05-13 --price 0.00164 --monthly-div 0.00004

The last row of MONTHLY_DATA is treated as the "current/MTD" row and
its `close` and `monthly_div` are overridden by the CLI flags. To roll
forward to a new month, append a new dict to MONTHLY_DATA.

Outputs:
    public/charts/<YYYY-MM-DD>/reinvest-since-pivot-<mmmDD>.png
    public/charts/2026-05-12/reinvest-since-pivot-may12.png   (compat)
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from datetime import datetime, date

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

# ---------------------------------------------------------------------------
# Monthly data — appendable.  open/close = HYPE price at month open/close.
# monthly_div = total dividend per share for the month.
# weeks = simulation steps inside that month (4 normal, 2 for May 2026 MTD).
# ---------------------------------------------------------------------------
MONTHLY_DATA = [
    {"label": "Apr 2024", "year": 2024, "month":  4, "open": 0.00297, "close": 0.00269, "monthly_div": 0.00030, "weeks": 4},
    {"label": "May 2024", "year": 2024, "month":  5, "open": 0.00265, "close": 0.00353, "monthly_div": 0.00055, "weeks": 4},
    {"label": "Jun 2024", "year": 2024, "month":  6, "open": 0.00311, "close": 0.00225, "monthly_div": 0.00030, "weeks": 4},
    {"label": "Jul 2024", "year": 2024, "month":  7, "open": 0.00238, "close": 0.00234, "monthly_div": 0.00042, "weeks": 4},
    {"label": "Aug 2024", "year": 2024, "month":  8, "open": 0.00147, "close": 0.00175, "monthly_div": 0.00024, "weeks": 4},
    {"label": "Sep 2024", "year": 2024, "month":  9, "open": 0.00154, "close": 0.00153, "monthly_div": 0.00009, "weeks": 4},
    {"label": "Oct 2024", "year": 2024, "month": 10, "open": 0.00143, "close": 0.00237, "monthly_div": 0.00005, "weeks": 4},
    {"label": "Nov 2024", "year": 2024, "month": 11, "open": 0.00241, "close": 0.00275, "monthly_div": 0.00007, "weeks": 4},
    {"label": "Dec 2024", "year": 2024, "month": 12, "open": 0.00337, "close": 0.00337, "monthly_div": 0.00020, "weeks": 4},
    {"label": "Jan 2025", "year": 2025, "month":  1, "open": 0.00367, "close": 0.00302, "monthly_div": 0.00010, "weeks": 4},
    {"label": "Feb 2025", "year": 2025, "month":  2, "open": 0.00295, "close": 0.00286, "monthly_div": 0.00008, "weeks": 4},
    {"label": "Mar 2025", "year": 2025, "month":  3, "open": 0.00246, "close": 0.00182, "monthly_div": 0.00010, "weeks": 4},
    {"label": "Apr 2025", "year": 2025, "month":  4, "open": 0.00159, "close": 0.00223, "monthly_div": 0.00008, "weeks": 4},
    {"label": "May 2025", "year": 2025, "month":  5, "open": 0.00246, "close": 0.00408, "monthly_div": 0.00009, "weeks": 4},
    {"label": "Jun 2025", "year": 2025, "month":  6, "open": 0.00338, "close": 0.00353, "monthly_div": 0.00012, "weeks": 4},
    {"label": "Jul 2025", "year": 2025, "month":  7, "open": 0.00406, "close": 0.00364, "monthly_div": 0.00008, "weeks": 4},
    {"label": "Aug 2025", "year": 2025, "month":  8, "open": 0.00301, "close": 0.00387, "monthly_div": 0.00012, "weeks": 4},
    {"label": "Sep 2025", "year": 2025, "month":  9, "open": 0.00400, "close": 0.00352, "monthly_div": 0.00008, "weeks": 4},
    {"label": "Oct 2025", "year": 2025, "month": 10, "open": 0.00352, "close": 0.00318, "monthly_div": 0.00013, "weeks": 4},
    {"label": "Nov 2025", "year": 2025, "month": 11, "open": 0.00278, "close": 0.00191, "monthly_div": 0.00018, "weeks": 4},
    {"label": "Dec 2025", "year": 2025, "month": 12, "open": 0.00191, "close": 0.00174, "monthly_div": 0.00010, "weeks": 4},
    {"label": "Jan 2026", "year": 2026, "month":  1, "open": 0.00174, "close": 0.00131, "monthly_div": 0.00008, "weeks": 4},
    {"label": "Feb 2026", "year": 2026, "month":  2, "open": 0.00131, "close": 0.00143, "monthly_div": 0.00008, "weeks": 4},
    {"label": "Mar 2026", "year": 2026, "month":  3, "open": 0.00143, "close": 0.00180, "monthly_div": 0.00010, "weeks": 4},
    {"label": "Apr 2026", "year": 2026, "month":  4, "open": 0.00180, "close": 0.001691, "monthly_div": 0.00008, "weeks": 4},
    # last row = current MTD; close + monthly_div override-able via CLI
    {"label": "May 2026 MTD", "year": 2026, "month": 5, "open": 0.001691, "close": 0.00164, "monthly_div": 0.00004, "weeks": 2},
]

PIVOT_PRICE = 0.00297
INITIAL_CAPITAL = 100_000.0
INITIAL_SHARES = INITIAL_CAPITAL / PIVOT_PRICE  # 33,670,033.67

# First weekly dividend after the April 2024 pivot. Used to count
# consecutive weekly dividends from the run date.
FIRST_DIV_DATE = date(2024, 4, 22)


# ---------------------------------------------------------------------------
@dataclass
class MonthlyPoint:
    label: str
    end_date: date
    close: float
    monthly_div: float
    reinvestor_shares: float
    reinvestor_value: float
    collector_cash: float
    collector_value: float


def simulate(months: list[dict]) -> list[MonthlyPoint]:
    """Weekly-step simulation; returns one MonthlyPoint per month + a t=0 row."""
    points: list[MonthlyPoint] = []

    # t=0 anchor at pivot
    points.append(MonthlyPoint(
        label="Pivot",
        end_date=date(months[0]["year"], months[0]["month"], 1),
        close=PIVOT_PRICE,
        monthly_div=0.0,
        reinvestor_shares=INITIAL_SHARES,
        reinvestor_value=INITIAL_CAPITAL,
        collector_cash=0.0,
        collector_value=INITIAL_CAPITAL,
    ))

    reinvestor_shares = INITIAL_SHARES
    collector_cash = 0.0

    for m in months:
        weeks = int(m["weeks"])
        open_p = float(m["open"])
        close_p = float(m["close"])
        weekly_div = float(m["monthly_div"]) / weeks

        for w in range(1, weeks + 1):
            # linear interpolation from open -> close at end of each week
            frac = w / weeks
            weekly_price = open_p + (close_p - open_p) * frac

            # Reinvestor: collect div cash, buy more shares at weekly_price
            div_cash = reinvestor_shares * weekly_div
            new_shares = div_cash / weekly_price
            reinvestor_shares += new_shares

            # Collector: cash collected on FIXED initial share count
            collector_cash += INITIAL_SHARES * weekly_div

        reinvestor_value = reinvestor_shares * close_p
        collector_value = (INITIAL_SHARES * close_p) + collector_cash

        # end-of-month date (use day 28 for stability; MTD uses run date)
        eom = date(m["year"], m["month"], 28)

        points.append(MonthlyPoint(
            label=m["label"],
            end_date=eom,
            close=close_p,
            monthly_div=m["monthly_div"],
            reinvestor_shares=reinvestor_shares,
            reinvestor_value=reinvestor_value,
            collector_cash=collector_cash,
            collector_value=collector_value,
        ))

    return points


# ---------------------------------------------------------------------------
def draw_chart(points: list[MonthlyPoint], run_date: date, out_paths: list[str]):
    bg = "#0f172a"
    grid = "#1e293b"
    text = "#e2e8f0"
    muted = "#94a3b8"
    green = "#22c55e"
    orange = "#f97316"

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": muted,
        "axes.labelcolor": text,
        "xtick.color": muted,
        "ytick.color": muted,
        "text.color": text,
    })

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    dates = [p.end_date for p in points]
    reinv = [p.reinvestor_value for p in points]
    coll = [p.collector_value for p in points]

    # Replace last point's date with the run date so the "Today" marker sits where it should
    dates[-1] = run_date

    ax.plot(dates, reinv, color=green, lw=2.2, marker="o", ms=4.5, mfc=green, mec=green, zorder=3)
    ax.plot(dates, coll, color=orange, lw=2.2, marker="o", ms=4.5, mfc=orange, mec=orange, zorder=3)

    # $100K reference line
    ax.axhline(INITIAL_CAPITAL, color=muted, ls="--", lw=1, alpha=0.6, zorder=1)

    # Grid
    ax.grid(True, color=grid, lw=0.6, alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(grid)

    # Y axis formatting in $k
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1000:,.0f}k"))

    # X axis: ticks every ~3 months
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    fig.autofmt_xdate(rotation=0, ha="center")

    # ATH annotation (pick reinvestor peak after first month)
    body = points[1:]  # skip pivot anchor
    ath_idx = max(range(len(body)), key=lambda i: body[i].reinvestor_value)
    ath_pt = body[ath_idx]
    ath_coll = ath_pt.collector_value
    ath_text = (
        f"ATH {ath_pt.label}\n"
        f"Reinvestor ${ath_pt.reinvestor_value/1000:,.0f}k\n"
        f"Collector ${ath_coll/1000:,.0f}k"
    )
    ax.annotate(
        ath_text,
        xy=(ath_pt.end_date, ath_pt.reinvestor_value),
        xytext=(20, 18),
        textcoords="offset points",
        fontsize=8.5,
        color=text,
        bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec=green, lw=1),
        arrowprops=dict(arrowstyle="->", color=green, lw=1),
    )

    # Jan 2026 low annotation (find reinvestor min in 2026)
    candidates_2026 = [p for p in body if p.end_date.year == 2026 and p.end_date.month <= 4]
    if candidates_2026:
        low_pt = min(candidates_2026, key=lambda p: p.reinvestor_value)
        low_text = (
            f"{low_pt.label} low\n"
            f"Reinvestor ${low_pt.reinvestor_value/1000:,.0f}k\n"
            f"Collector ${low_pt.collector_value/1000:,.0f}k"
        )
        ax.annotate(
            low_text,
            xy=(low_pt.end_date, low_pt.reinvestor_value),
            xytext=(-130, -55),
            textcoords="offset points",
            fontsize=8.5,
            color=text,
            bbox=dict(boxstyle="round,pad=0.4", fc="#1e293b", ec=muted, lw=1),
            arrowprops=dict(arrowstyle="->", color=muted, lw=1),
        )

    # "Today" marker on endpoint
    today = points[-1]
    ax.plot([run_date], [today.reinvestor_value], "o", ms=9,
            mfc=green, mec="white", mew=1.3, zorder=5)
    ax.annotate(
        f"Today {run_date.strftime('%b %d')}",
        xy=(run_date, today.reinvestor_value),
        xytext=(-58, 14),
        textcoords="offset points",
        fontsize=9,
        color=text,
        fontweight="bold",
    )

    # $100K start label
    ax.annotate(
        "$100K start (April 2024 pivot)",
        xy=(dates[0], INITIAL_CAPITAL),
        xytext=(8, -16),
        textcoords="offset points",
        fontsize=8,
        color=muted,
    )

    # Legend (top-left box)
    reinv_pct = (today.reinvestor_value / INITIAL_CAPITAL - 1) * 100
    coll_pct = (today.collector_value / INITIAL_CAPITAL - 1) * 100
    legend_lines = [
        ("Reinvestor", f"${today.reinvestor_value/1000:,.0f}k", f"+{reinv_pct:.0f}%", green),
        ("Collector", f"${today.collector_value/1000:,.0f}k", f"+{coll_pct:.0f}%", orange),
    ]
    # Build legend manually
    ax.text(
        0.018, 0.965,
        "",
        transform=ax.transAxes,
    )
    legend_x = 0.020
    legend_y_top = 0.965
    legend_box = mpatches.FancyBboxPatch(
        (legend_x, legend_y_top - 0.13),
        0.30, 0.13,
        boxstyle="round,pad=0.012",
        transform=ax.transAxes,
        fc="#1e293b", ec=muted, lw=0.8, zorder=4,
    )
    ax.add_patch(legend_box)
    for i, (label, val, pct, color) in enumerate(legend_lines):
        y = legend_y_top - 0.04 - i * 0.05
        ax.text(legend_x + 0.012, y, "●", color=color,
                fontsize=12, transform=ax.transAxes, va="center", zorder=5)
        ax.text(legend_x + 0.040, y, label, color=text, fontsize=9.5,
                transform=ax.transAxes, va="center", zorder=5, fontweight="bold")
        ax.text(legend_x + 0.150, y, val, color=text, fontsize=9.5,
                transform=ax.transAxes, va="center", zorder=5)
        ax.text(legend_x + 0.230, y, pct, color=color, fontsize=9.5,
                transform=ax.transAxes, va="center", zorder=5, fontweight="bold")

    # Consecutive weekly dividends = calendar weeks since first weekly div
    div_weeks = max(1, (run_date - FIRST_DIV_DATE).days // 7 + 1)
    # Title + subtitle
    title_date = run_date.strftime("%B %d, %Y")
    fig.suptitle(
        f"$100K at the April 2024 Pivot — Through {title_date}",
        fontsize=15, color=text, fontweight="bold", x=0.02, ha="left", y=0.965,
    )
    ax.set_title(
        f"{div_weeks} consecutive weekly dividends",
        loc="left", fontsize=10, color=muted, pad=8,
    )

    # Watermark
    fig.text(0.985, 0.015, "rebeldividends.com",
             color=muted, fontsize=8, ha="right", alpha=0.7)

    plt.tight_layout(rect=[0, 0, 1, 0.94])

    for out in out_paths:
        os.makedirs(os.path.dirname(out), exist_ok=True)
        fig.savefig(out, facecolor=bg, dpi=150, bbox_inches="tight")
        print(f"wrote {out}")
    plt.close(fig)


# ---------------------------------------------------------------------------
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True, help="run date YYYY-MM-DD")
    p.add_argument("--price", type=float, required=True,
                   help="current close price for the last (MTD) row")
    p.add_argument("--monthly-div", type=float, required=True,
                   help="cumulative dividend per share for the last (MTD) row so far")
    args = p.parse_args()

    run_date = datetime.strptime(args.date, "%Y-%m-%d").date()

    months = [dict(m) for m in MONTHLY_DATA]
    months[-1]["close"] = args.price
    months[-1]["monthly_div"] = args.monthly_div

    points = simulate(months)
    today = points[-1]

    reinv_pct = (today.reinvestor_value / INITIAL_CAPITAL - 1) * 100
    coll_pct = (today.collector_value / INITIAL_CAPITAL - 1) * 100

    print("=" * 60)
    print(f"Run date:           {run_date}")
    print(f"Current price:      ${args.price:.5f}")
    print(f"Pivot price:        ${PIVOT_PRICE:.5f}")
    print(f"Initial shares:     {INITIAL_SHARES:,.2f}")
    print("-" * 60)
    print(f"Reinvestor value:   ${today.reinvestor_value:>12,.2f}   ({reinv_pct:+.1f}%)")
    print(f"Reinvestor shares:  {today.reinvestor_shares:>15,.0f}")
    print(f"Collector value:    ${today.collector_value:>12,.2f}   ({coll_pct:+.1f}%)")
    print(f"  ├─ Share value:   ${INITIAL_SHARES * args.price:>12,.2f}")
    print(f"  └─ Cash collected:${today.collector_cash:>12,.2f}   (sanity: total dividends)")
    print(f"Reinvestor edge:    ${today.reinvestor_value - today.collector_value:>12,.2f}")
    print("=" * 60)

    # Output paths
    mmm = run_date.strftime("%b").lower()  # e.g. "may"
    dd = run_date.strftime("%d")            # "13"
    primary = f"public/charts/{run_date.isoformat()}/reinvest-since-pivot-{mmm}{dd}.png"
    compat = "public/charts/2026-05-12/reinvest-since-pivot-may12.png"

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    primary = os.path.join(repo_root, primary)
    compat = os.path.join(repo_root, compat)

    draw_chart(points, run_date, [primary, compat])


if __name__ == "__main__":
    main()
