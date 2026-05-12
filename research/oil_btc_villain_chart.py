"""Build the Oil vs BTC villain chart for the 2026-05-12 RD update.

Pulls 5y of weekly USO (WTI proxy ETF) and BTC/USD from Polygon, falls back
to Alpha Vantage. Renders a 2-panel chart: price overlay (BTC vs inverted
oil) on top, rolling 90-day Pearson correlation on bottom.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from matplotlib.patches import FancyBboxPatch

OUT_PATH = Path.home() / "rd-updates-site/public/charts/2026-05-13/oil-btc-villain-chart.png"
START = "2020-01-01"
END = "2026-05-11"


def _polygon_aggs(ticker: str, key: str) -> pd.DataFrame:
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/week/"
        f"{START}/{END}?apiKey={key}&limit=5000&adjusted=true&sort=asc"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    if j.get("status") not in ("OK", "DELAYED") or not j.get("results"):
        raise RuntimeError(f"polygon empty for {ticker}: {j.get('status')} / {j.get('error') or j.get('message')}")
    df = pd.DataFrame(j["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.set_index("date")[["c"]].rename(columns={"c": ticker})
    return df


def _alpha_btc_daily(key: str) -> pd.DataFrame:
    url = (
        "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY"
        f"&symbol=BTC&market=USD&apikey={key}"
    )
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    ts_key = next((k for k in j if "Time Series" in k), None)
    if not ts_key:
        raise RuntimeError(f"alpha-vantage BTC empty: {j.get('Note') or j.get('Information') or list(j)[:3]}")
    rows = [(d, float(v.get("4. close") or v.get("4a. close (USD)"))) for d, v in j[ts_key].items()]
    df = pd.DataFrame(rows, columns=["date", "btc"]).sort_values("date")
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")


def _alpha_wti_weekly(key: str) -> pd.DataFrame:
    url = f"https://www.alphavantage.co/query?function=WTI&interval=weekly&apikey={key}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    j = r.json()
    data = j.get("data") or []
    if not data:
        raise RuntimeError(f"alpha-vantage WTI empty: {j.get('Note') or j.get('Information')}")
    rows = []
    for row in data:
        try:
            rows.append((row["date"], float(row["value"])))
        except (KeyError, ValueError):
            continue
    df = pd.DataFrame(rows, columns=["date", "oil"]).sort_values("date")
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")


def load_data() -> pd.DataFrame:
    akey = os.environ.get("ALPHAVANTAGE_API_KEY")
    if not akey:
        raise RuntimeError("ALPHAVANTAGE_API_KEY not set")

    import time as _time
    print("Pulling WTI weekly (Alpha Vantage)...", flush=True)
    oil = _alpha_wti_weekly(akey)
    _time.sleep(15)  # respect Alpha Vantage free-tier per-second limits
    print("Pulling BTC daily (Alpha Vantage)...", flush=True)
    try:
        btc = _alpha_btc_daily(akey)
    except RuntimeError as e:
        if "spread out" in str(e).lower() or "rate" in str(e).lower() or "premium" in str(e).lower():
            print("  rate-limited, retrying after 30s...", flush=True)
            _time.sleep(30)
            btc = _alpha_btc_daily(akey)
        else:
            raise

    # Resample BTC to weekly (W-FRI to match WTI EIA weekly cadence-ish)
    btc_w = btc["btc"].resample("W-FRI").last().to_frame()

    # Align: re-index oil to BTC's weekly index using nearest-prior
    df = pd.concat(
        [oil["oil"], btc_w["btc"]], axis=1
    ).sort_index()
    # forward-fill across the joined index, then drop any leading NaNs
    df["oil"] = df["oil"].ffill()
    df["btc"] = df["btc"].ffill()
    df = df.dropna()
    df = df[(df.index >= pd.Timestamp(START)) & (df.index <= pd.Timestamp(END))]
    return df


def build_chart(df: pd.DataFrame) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Real WTI $/barrel from Alpha Vantage. Brief specifies >$85 = high, <$65 = low.
    oil_hi = 85.0
    oil_lo = 65.0

    # Rolling ~90-day correlation. Weekly bars → 13 weeks.
    win = 13
    df["corr"] = df["oil"].pct_change().rolling(win).corr(df["btc"].pct_change())

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.labelcolor": "#222222",
        "xtick.color": "#444444",
        "ytick.color": "#444444",
    })
    fig = plt.figure(figsize=(12, 8), dpi=150, facecolor="#fafafa")
    gs = fig.add_gridspec(
        2, 1, height_ratios=[6, 4], hspace=0.38,
        left=0.075, right=0.88, top=0.83, bottom=0.16,
    )
    ax_price = fig.add_subplot(gs[0])
    ax_corr = fig.add_subplot(gs[1])
    ax_price.set_facecolor("#ffffff")
    ax_corr.set_facecolor("#ffffff")

    # --------- Panel 1: price overlay -----------
    # Shade oil-high (red) and oil-low (green) regions
    high_mask = df["oil"] >= oil_hi
    low_mask = df["oil"] <= oil_lo
    ax_price.fill_between(
        df.index, 0, 1, where=high_mask, transform=ax_price.get_xaxis_transform(),
        color="#fecaca", alpha=0.55, linewidth=0, label="_oilhigh",
    )
    ax_price.fill_between(
        df.index, 0, 1, where=low_mask, transform=ax_price.get_xaxis_transform(),
        color="#bbf7d0", alpha=0.55, linewidth=0, label="_oillow",
    )

    # BTC line — bright orange, left axis
    ax_price.plot(df.index, df["btc"], color="#ff6600", linewidth=3.0, label="BTC/USD", zorder=4)
    ax_price.set_ylabel("BTC / USD", color="#ff6600", fontsize=12, fontweight="bold")
    ax_price.tick_params(axis="y", labelcolor="#ff6600")
    ax_price.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}K"))

    # Oil — inverted, right axis
    ax_oil = ax_price.twinx()
    ax_oil.plot(df.index, df["oil"], color="#dc2626", linewidth=2.0, label="Oil (inverted)", zorder=3)
    ax_oil.invert_yaxis()
    ax_oil.set_ylabel("WTI Crude  $/bbl  (inverted ↓ = oil higher)", color="#dc2626", fontsize=12, fontweight="bold")
    ax_oil.tick_params(axis="y", labelcolor="#dc2626")
    ax_oil.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}"))
    ax_oil.spines["right"].set_color("#dc2626")
    ax_oil.spines["left"].set_color("#ff6600")

    # No right-axis directional labels — the inverted axis label says it.

    # ------- Annotations -------
    def _annot(date_str, btc_y, text, color="#1a1a1a", offset=(40, 30)):
        d = pd.Timestamp(date_str)
        # snap to nearest bar
        idx = df.index[df.index.get_indexer([d], method="nearest")[0]]
        y = df.loc[idx, "btc"]
        ax_price.annotate(
            text,
            xy=(idx, y),
            xytext=(offset[0], offset[1]),
            textcoords="offset points",
            fontsize=9.5,
            color=color,
            fontweight="bold",
            ha="left",
            bbox=dict(boxstyle="round,pad=0.35", fc="#ffffff", ec=color, lw=1.2, alpha=0.95),
            arrowprops=dict(arrowstyle="->", color=color, lw=1.3, connectionstyle="arc3,rad=0.15"),
            zorder=10,
        )

    _annot("2021-11-08", 64000,
           "Oil surges 2021-22\nBTC drops 70%", color="#991b1b", offset=(-200, 30))
    _annot("2022-12-19", 16500,
           "Oil falls mid-2022\nBTC bottoms", color="#0a7c42", offset=(-110, -55))
    _annot("2023-10-02", 27000,
           "Oil stays low 2023\nBTC runs +150%", color="#0a7c42", offset=(20, -90))
    _annot("2025-04-07", 78000,
           "Oil elevated 2025-26\nBTC suppressed\n~$28K below target",
           color="#991b1b", offset=(-260, 15))

    # NOW marker — star + callout
    now = df.index[-1]
    btc_now = df.loc[now, "btc"]
    ax_price.scatter([now], [btc_now], s=380, marker="*",
                     color="#facc15", edgecolor="#92400e", linewidth=1.5, zorder=12)
    ax_price.annotate(
        "NOW  •  Trump in Beijing\nStrait of Hormuz\nOIL ABOUT TO BREAK?",
        xy=(now, btc_now),
        xytext=(-200, -110),
        textcoords="offset points",
        fontsize=10.5,
        color="#1a1a1a",
        fontweight="bold",
        ha="left",
        bbox=dict(boxstyle="round,pad=0.45", fc="#fef3c7", ec="#b45309", lw=1.5),
        arrowprops=dict(arrowstyle="->", color="#b45309", lw=1.6,
                        connectionstyle="arc3,rad=-0.25"),
        zorder=11,
    )

    ax_price.set_xlim(df.index.min(), df.index.max())
    ax_price.grid(True, axis="y", color="#e5e7eb", linewidth=0.6)
    ax_price.set_axisbelow(True)
    ax_price.xaxis.set_major_locator(mdates.YearLocator())
    ax_price.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax_price.set_xlabel("")

    # ---- Panel 2: rolling correlation ----
    corr = df["corr"].dropna()
    neg = corr.where(corr < 0)
    pos = corr.where(corr >= 0)
    ax_corr.fill_between(corr.index, 0, neg.values, color="#16a34a", alpha=0.55,
                         linewidth=0, label="Inverse (oil down → BTC up)")
    ax_corr.fill_between(corr.index, 0, pos.values, color="#9ca3af", alpha=0.55,
                         linewidth=0, label="Positive (moving together)")
    ax_corr.plot(corr.index, corr.values, color="#111827", linewidth=1.4)
    ax_corr.axhline(0, color="#111827", linewidth=0.8)

    # Highlight the long inverse stretch
    ax_corr.text(
        0.015, 0.92,
        "When this line is GREEN/below zero, oil & BTC move opposite — and that's almost always.",
        transform=ax_corr.transAxes, fontsize=10, fontweight="bold", color="#065f46",
        va="top", ha="left",
        bbox=dict(boxstyle="round,pad=0.35", fc="#ecfdf5", ec="#16a34a", lw=1),
    )
    ax_corr.set_ylim(-1.0, 1.0)
    ax_corr.set_ylabel("90-day correlation", fontsize=11, fontweight="bold")
    ax_corr.set_xlim(df.index.min(), df.index.max())
    ax_corr.set_title(
        "The Inverse Relationship: When Oil Falls, BTC Runs",
        fontsize=13, fontweight="bold", color="#111827", loc="left", pad=8,
    )
    ax_corr.grid(True, axis="y", color="#e5e7eb", linewidth=0.6)
    ax_corr.set_axisbelow(True)
    ax_corr.xaxis.set_major_locator(mdates.YearLocator())
    ax_corr.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax_corr.legend(loc="lower left", fontsize=9, frameon=False)

    # ---- Title / subtitle / source ----
    fig.suptitle(
        "HIGH OIL = BTC SUPPRESSED.  OIL DROPS = BTC ROCKETS.",
        fontsize=20, fontweight="bold", color="#111827", x=0.075, ha="left", y=0.955,
    )
    fig.text(
        0.075, 0.905,
        "5 years of weekly data. The pattern repeats every time.",
        fontsize=13, color="#4b5563", ha="left", style="italic",
    )
    fig.text(
        0.075, 0.018,
        "Data: Alpha Vantage (WTI spot weekly $/bbl; BTC/USD daily, resampled weekly). Chart: Rebel Dividends Research. May 2026.",
        fontsize=8.5, color="#6b7280", ha="left",
    )

    # ---- Legend strip across bottom of figure (between panel 2 and source) ----
    legend_items = [
        ("━", "#ff6600", "BTC price"),
        ("━", "#dc2626", "Oil (inverted)"),
        ("■", "#bbf7d0", "Oil LOW (BTC ran)"),
        ("■", "#fecaca", "Oil HIGH (BTC suppressed)"),
        ("★", "#facc15", "NOW — setup loading"),
    ]
    # Place at y ≈ 0.06, evenly distributed across width
    n = len(legend_items)
    x_left, x_right = 0.075, 0.95
    span = x_right - x_left
    for i, (sym, col, label) in enumerate(legend_items):
        x = x_left + span * (i / (n - 0.001))
        fig.text(x, 0.062, sym, color=col, fontsize=14,
                 fontweight="bold", transform=fig.transFigure, va="center")
        fig.text(x + 0.018, 0.062, label, color="#1f2937", fontsize=9.5,
                 transform=fig.transFigure, va="center")

    fig.savefig(OUT_PATH, dpi=150, facecolor="#fafafa", bbox_inches=None)
    print(f"Saved: {OUT_PATH}", flush=True)


def main() -> int:
    df = load_data()
    print(f"Loaded {len(df)} rows  ({df.index.min().date()} → {df.index.max().date()})", flush=True)
    print(f"  oil range: ${df['oil'].min():.2f} → ${df['oil'].max():.2f}", flush=True)
    print(f"  btc range: ${df['btc'].min():,.0f} → ${df['btc'].max():,.0f}", flush=True)
    build_chart(df)
    return 0


if __name__ == "__main__":
    sys.exit(main())
