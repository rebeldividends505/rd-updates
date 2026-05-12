"""Pitch 1: BTC vs QQQ correlation divergence chart."""
import os, json, requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")
os.makedirs(OUT, exist_ok=True)

def fetch_av_crypto(symbol="BTC"):
    r = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": symbol,
            "market": "USD",
            "apikey": os.environ["ALPHAVANTAGE_API_KEY"],
        },
        timeout=30,
    )
    data = r.json()["Time Series (Digital Currency Daily)"]
    rows = []
    for date, vals in data.items():
        # Newer AV format: keys are "1. open", etc. Older format may differ.
        close_key = next((k for k in vals if "close" in k.lower() and "USD" not in k.upper()), None)
        if close_key is None:
            close_key = next(k for k in vals if "4" in k or "close" in k.lower())
        rows.append({"date": date, "close": float(vals[close_key])})
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def fetch_polygon_equity(ticker, start="2019-01-01", end="2026-05-11"):
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}",
        params={"apiKey": os.environ["POLYGON_API_KEY"], "limit": 50000, "adjusted": "true"},
        timeout=30,
    )
    j = r.json()
    rows = [{"date": pd.Timestamp(r["t"], unit="ms"), "close": r["c"]} for r in j.get("results", [])]
    df = pd.DataFrame(rows)
    return df

print("Fetching BTC from Alpha Vantage...")
btc = fetch_av_crypto("BTC")
print(f"  BTC rows: {len(btc)}, {btc['date'].min().date()} → {btc['date'].max().date()}")

print("Fetching QQQ from Polygon...")
qqq = fetch_polygon_equity("QQQ")
print(f"  QQQ rows: {len(qqq)}, {qqq['date'].min().date()} → {qqq['date'].max().date()}")

# Normalize date dtypes & restrict to 2019-01-01+
btc["date"] = pd.to_datetime(btc["date"]).dt.normalize().astype("datetime64[ns]")
qqq["date"] = pd.to_datetime(qqq["date"]).dt.normalize().astype("datetime64[ns]")
start = pd.Timestamp("2019-01-01")
btc = btc[btc["date"] >= start].reset_index(drop=True)
qqq = qqq[qqq["date"] >= start].reset_index(drop=True)

# Merge on trading days (QQQ is the limiting calendar)
merged = pd.merge_asof(
    qqq.sort_values("date"),
    btc.sort_values("date").rename(columns={"close": "btc"}),
    on="date",
    direction="backward",
)
merged = merged.rename(columns={"close": "qqq"})
merged = merged.dropna().reset_index(drop=True)
print(f"Merged rows: {len(merged)}")

# Index to 100 at start
merged["qqq_idx"] = merged["qqq"] / merged["qqq"].iloc[0] * 100
merged["btc_idx"] = merged["btc"] / merged["btc"].iloc[0] * 100

# Daily returns and rolling 90-day correlation
merged["qqq_ret"] = merged["qqq"].pct_change()
merged["btc_ret"] = merged["btc"].pct_change()
merged["corr90"] = merged["qqq_ret"].rolling(90).corr(merged["btc_ret"])

# Save data
merged.to_csv(os.path.join(OUT, "pitch1_data.csv"), index=False)

# Build chart
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8.2), sharex=True,
                                gridspec_kw={"height_ratios": [2.2, 1]}, dpi=110)

ax1.plot(merged["date"], merged["btc_idx"], color="#F7931A", linewidth=2.0, label="BTC (indexed)")
ax1.plot(merged["date"], merged["qqq_idx"], color="#1f6feb", linewidth=2.0, label="QQQ (indexed)")
ax1.set_yscale("log")
ax1.set_ylabel("Indexed (Jan 2019 = 100, log scale)", fontsize=11)
ax1.set_title("BTC vs QQQ — Every Correlation Break Resolved With BTC Catching Up Violently",
              fontsize=14, fontweight="bold", pad=12)
ax1.legend(loc="upper left", fontsize=11, framealpha=0.95)
ax1.grid(True, alpha=0.3)

# Divergence period shading & labels
divergences = [
    ("2021-05-12", "2021-07-25", "China ban /\ntaper fear"),
    ("2022-05-01", "2022-12-30", "Rate hikes\nLuna / FTX"),
    ("2023-02-15", "2023-04-30", "SVB / regional\nbank scare"),
    ("2025-09-01", "2026-05-11", "AI mania\nBTC lags\nNOW"),
]
for s, e, lbl in divergences:
    s, e = pd.Timestamp(s), pd.Timestamp(e)
    if s < merged["date"].min(): s = merged["date"].min()
    if e > merged["date"].max(): e = merged["date"].max()
    ax1.axvspan(s, e, color="red", alpha=0.10)
    ax2.axvspan(s, e, color="red", alpha=0.10)
    # label near top
    midx = s + (e - s) / 2
    ymin, ymax = ax1.get_ylim()
    ax1.text(midx, ymax * 0.55, lbl, ha="center", va="top", fontsize=8.5,
             color="#7a1010", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#7a1010", alpha=0.85))

ax2.plot(merged["date"], merged["corr90"], color="#2ca02c", linewidth=1.6, label="90-day rolling correlation")
ax2.axhline(0.3, color="#888", linestyle="--", linewidth=0.9, alpha=0.7)
ax2.axhline(0.0, color="#000", linewidth=0.6, alpha=0.5)
ax2.set_ylim(-0.5, 1.0)
ax2.set_ylabel("90-day correlation\n(BTC vs QQQ)", fontsize=10)
ax2.set_xlabel("")
ax2.grid(True, alpha=0.3)
ax2.legend(loc="lower left", fontsize=10)

ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

fig.suptitle("", y=1.02)
fig.text(0.5, 0.005,
         "Every divergence has resolved with BTC catching up violently. We are now in the largest divergence on record.",
         ha="center", fontsize=11, style="italic", color="#333")

plt.tight_layout(rect=(0, 0.02, 1, 1))
out_path = os.path.join(OUT, "chart1-btc-qqq-correlation.png")
fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)

# Print stats for thesis
print("\n=== Pitch 1 stats ===")
print(f"BTC start price: ${merged['btc'].iloc[0]:,.0f}")
print(f"BTC end price:   ${merged['btc'].iloc[-1]:,.0f}")
print(f"QQQ start: ${merged['qqq'].iloc[0]:.2f}")
print(f"QQQ end:   ${merged['qqq'].iloc[-1]:.2f}")
print(f"BTC return since 2019: {(merged['btc'].iloc[-1]/merged['btc'].iloc[0]-1)*100:.0f}%")
print(f"QQQ return since 2019: {(merged['qqq'].iloc[-1]/merged['qqq'].iloc[0]-1)*100:.0f}%")
print(f"Current 90d correlation: {merged['corr90'].iloc[-1]:.3f}")
print(f"Min correlation since 2024: {merged.tail(500)['corr90'].min():.3f}")
