#!/usr/bin/env python3
"""Build PNG charts for the SOXL Alpha Strategy page.

Reads:
  analysis/equity_curves.csv     (primary, long_short, soxl cumulative)
  analysis/best_strategy.json    (params, metrics, current positions)

Writes to public/charts/sox-alpha/:
  strategy-vs-soxl.png       — hero chart
  drawdown-comparison.png    — drawdown over time
  current-positions.png      — long/short position bars
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "analysis"
OUT = ROOT.parent.parent / "public" / "charts" / "sox-alpha"
OUT.mkdir(parents=True, exist_ok=True)

# Style
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e6e6e6",
    "grid.linewidth": 0.6,
})

INK = "#111111"
BLUE = "#1c4fd6"
GREEN = "#1f8a4c"
RED = "#d12d2d"
AMBER = "#e08f1a"
MUTED = "#888888"


def load():
    eq = pd.read_csv(ANALYSIS / "equity_curves.csv", index_col=0, parse_dates=True)
    best = json.loads((ANALYSIS / "best_strategy.json").read_text())
    return eq, best


def chart_strategy_vs_soxl(eq: pd.DataFrame, best: dict, path: Path):
    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=140)
    # Plot $1 grown into $X
    ax.plot(eq.index, eq["soxl"], label="SOXL (3× SOX ETF)",
            color=MUTED, linewidth=2.0)
    ax.plot(eq.index, eq["long_short"], label="L/S momentum (5L · 8S)",
            color=AMBER, linewidth=2.0)
    ax.plot(eq.index, eq["primary"], label="Alpha (5-long momentum)",
            color=BLUE, linewidth=2.6)
    ax.set_title("$1 invested — Alpha strategy vs SOXL benchmark",
                 fontsize=15, fontweight="bold", color=INK, pad=14, loc="left")
    sub = (f"{best['backtest_start']} → {best['backtest_end']} · "
           f"weekly rebalance · {best['n_weeks']} weeks · "
           f"{best['n_strategies_tested']} strategies tested")
    ax.text(0.0, 1.01, sub, transform=ax.transAxes,
            fontsize=10, color=MUTED, va="bottom")
    ax.set_ylabel("Growth of $1")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left", frameon=False, fontsize=11)

    # Annotate endpoints
    final_pri = eq["primary"].iloc[-1]
    final_ls = eq["long_short"].iloc[-1]
    final_sx = eq["soxl"].iloc[-1]
    for val, color in [(final_pri, BLUE), (final_ls, AMBER), (final_sx, MUTED)]:
        ax.annotate(f"${val:.2f}", xy=(eq.index[-1], val),
                    xytext=(6, 0), textcoords="offset points",
                    color=color, fontsize=10, fontweight="bold", va="center")

    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {path.name}")


def chart_drawdown(eq: pd.DataFrame, best: dict, path: Path):
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=140)
    for name, color, label in [
        ("soxl", MUTED, "SOXL"),
        ("long_short", AMBER, "L/S momentum"),
        ("primary", BLUE, "Alpha (long-only)"),
    ]:
        s = eq[name]
        dd = (s / s.cummax() - 1) * 100
        ax.fill_between(dd.index, dd.values, 0, alpha=0.25 if name == "primary" else 0.12,
                        color=color)
        ax.plot(dd.index, dd, color=color, linewidth=1.6, label=label)
    ax.set_title("Drawdown comparison — Alpha vs SOXL",
                 fontsize=15, fontweight="bold", color=INK, pad=14, loc="left")
    ax.text(0.0, 1.01,
            "Peak-to-trough loss at every weekly close. Lower is better.",
            transform=ax.transAxes, fontsize=10, color=MUTED, va="bottom")
    ax.set_ylabel("Drawdown (%)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.axhline(0, color=INK, linewidth=0.6)
    ax.legend(loc="lower left", frameon=False, fontsize=11)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {path.name}")


def chart_positions(best: dict, path: Path):
    ls_pos = best["long_short"]["current_positions"]
    longs = sorted([p for p in ls_pos if p["weight"] > 0],
                   key=lambda x: -x["weight"])
    shorts = sorted([p for p in ls_pos if p["weight"] < 0],
                    key=lambda x: x["weight"])

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=140)

    items = longs + shorts
    labels = [p["ticker"] for p in items]
    values = [p["weight"] * 100 for p in items]
    colors = [GREEN if v > 0 else RED for v in values]

    y = np.arange(len(items))
    ax.barh(y, values, color=colors, height=0.65)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11, fontweight="bold")
    ax.invert_yaxis()
    ax.axvline(0, color=INK, linewidth=0.7)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:+.0f}%"))
    ax.set_xlabel("Portfolio weight")
    ax.set_title("Current positions — L/S momentum (5 long · 8 short)",
                 fontsize=15, fontweight="bold", color=INK, pad=14, loc="left")
    ax.text(0.0, 1.01,
            f"Signals as of {best['as_of']} · next rebalance {best['next_rebalance']}",
            transform=ax.transAxes, fontsize=10, color=MUTED, va="bottom")

    # Annotate weights + prices
    for i, p in enumerate(items):
        x = p["weight"] * 100
        offset = 0.5 if x > 0 else -0.5
        ha = "left" if x > 0 else "right"
        ax.annotate(f"{x:+.1f}%  ·  ${p['price']:.0f}",
                    xy=(x, i), xytext=(offset, 0), textcoords="offset fontsize",
                    fontsize=10, va="center", ha=ha, color=INK)
    ax.set_xlim(min(values) * 1.5, max(values) * 1.7)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ {path.name}")


def main():
    eq, best = load()
    print(f"Writing charts to {OUT}")
    chart_strategy_vs_soxl(eq, best, OUT / "strategy-vs-soxl.png")
    chart_drawdown(eq, best, OUT / "drawdown-comparison.png")
    chart_positions(best, OUT / "current-positions.png")
    print("Done.")


if __name__ == "__main__":
    main()
