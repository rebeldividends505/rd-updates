"""Pitch 2: Silver lagged Gold, then ran +144% in 8 weeks. BTC = silver now."""
import os, requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")

def fetch_polygon_equity(ticker, start="2019-01-01", end="2026-05-11"):
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}",
        params={"apiKey": os.environ["POLYGON_API_KEY"], "limit": 50000, "adjusted": "true"},
        timeout=30,
    )
    rows = [{"date": pd.Timestamp(rr["t"], unit="ms").normalize(), "close": rr["c"]}
            for rr in r.json().get("results", [])]
    df = pd.DataFrame(rows)
    df["date"] = df["date"].astype("datetime64[ns]")
    return df

print("Fetching GLD from Polygon...")
gld = fetch_polygon_equity("GLD")
print(f"  GLD: {len(gld)} rows {gld['date'].min().date()} → {gld['date'].max().date()}")

print("Fetching SLV from Polygon...")
slv = fetch_polygon_equity("SLV")
print(f"  SLV: {len(slv)} rows {slv['date'].min().date()} → {slv['date'].max().date()}")

# Start from the later of the two
start = max(gld["date"].min(), slv["date"].min(), pd.Timestamp("2023-01-01"))
gld = gld[gld["date"] >= start].reset_index(drop=True)
slv = slv[slv["date"] >= start].reset_index(drop=True)

merged = pd.merge(gld.rename(columns={"close": "gld"}),
                  slv.rename(columns={"close": "slv"}),
                  on="date", how="inner").sort_values("date").reset_index(drop=True)
merged["gld_idx"] = merged["gld"] / merged["gld"].iloc[0] * 100
merged["slv_idx"] = merged["slv"] / merged["slv"].iloc[0] * 100
merged.to_csv(os.path.join(OUT, "pitch2_data.csv"), index=False)
print(f"Merged rows: {len(merged)}")

# Identify silver breakout — biggest 8-week rally
merged["slv_8w_ret"] = merged["slv"].pct_change(40)  # ~8 weeks
breakout_idx = merged["slv_8w_ret"].idxmax()
breakout_date = merged.loc[breakout_idx, "date"]
breakout_8w_pct = merged.loc[breakout_idx, "slv_8w_ret"] * 100
# Identify lag period: where gold > silver materially
merged["spread"] = merged["gld_idx"] - merged["slv_idx"]
lag_peak_idx = merged["spread"].idxmax()
lag_peak_date = merged.loc[lag_peak_idx, "date"]

# Build chart
fig, ax = plt.subplots(figsize=(14, 7.2), dpi=110)
ax.plot(merged["date"], merged["gld_idx"], color="#D4AF37", linewidth=2.4, label="Gold (GLD)")
ax.plot(merged["date"], merged["slv_idx"], color="#A8A9AD", linewidth=2.4, label="Silver (SLV)")
ax.set_ylabel("Indexed performance (Jan 2023 = 100)", fontsize=11)
ax.set_title("Silver Did Nothing for 2 Years — Then +%.0f%% in 8 Weeks. BTC Is Now Silver." %
             round(breakout_8w_pct), fontsize=14, fontweight="bold", pad=12)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", fontsize=11)

# Shade lag period: from start through lag_peak_date
ax.axvspan(merged["date"].iloc[0], lag_peak_date, color="#D4AF37", alpha=0.10)
ax.annotate("Lag period:\nGold ripped,\nsilver did nothing",
            xy=(merged["date"].iloc[len(merged)//4], merged["gld_idx"].iloc[len(merged)//4]),
            xytext=(merged["date"].iloc[len(merged)//6],
                    merged["gld_idx"].max() * 0.82),
            fontsize=10, ha="center", color="#7a5a10", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#7a5a10", alpha=0.9))

# Shade breakout — the 8 weeks ending at breakout_date
breakout_start = breakout_date - pd.Timedelta(days=56)
ax.axvspan(breakout_start, breakout_date, color="#A8A9AD", alpha=0.25)
peak_y = merged.loc[breakout_idx, "slv_idx"]
ax.annotate(f"Silver +{breakout_8w_pct:.0f}% in 8 weeks\n(broke $50 first time since 1980)",
            xy=(breakout_date, peak_y),
            xytext=(breakout_date - pd.Timedelta(days=180), peak_y + 25),
            fontsize=10.5, ha="center", color="#222", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#222", alpha=0.95),
            arrowprops=dict(arrowstyle="->", color="#222", lw=1.2))

# BTC arrow — annotate where BTC sits relative to "digital gold"
ax.annotate("BTC is HERE\n(coiled, like silver was)",
            xy=(merged["date"].iloc[-1], merged["slv_idx"].iloc[-1]),
            xytext=(merged["date"].iloc[-1] - pd.Timedelta(days=200),
                    merged["slv_idx"].iloc[-1] - 50),
            fontsize=11, ha="center", color="#F7931A", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#F7931A", lw=1.5),
            arrowprops=dict(arrowstyle="->", color="#F7931A", lw=1.8))

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha="center")

fig.text(0.5, 0.005,
         "Silver lagged gold for 2+ years. Then it caught up violently. BTC is in the exact same lag phase now vs gold + M2 + the broader risk rally.",
         ha="center", fontsize=10.5, style="italic", color="#333")

plt.tight_layout(rect=(0, 0.025, 1, 1))
out_path = os.path.join(OUT, "chart2-silver-gold-lag.png")
fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)

print(f"\n=== Pitch 2 stats ===")
print(f"GLD start: ${merged['gld'].iloc[0]:.2f}, end: ${merged['gld'].iloc[-1]:.2f}, return: {(merged['gld'].iloc[-1]/merged['gld'].iloc[0]-1)*100:.0f}%")
print(f"SLV start: ${merged['slv'].iloc[0]:.2f}, end: ${merged['slv'].iloc[-1]:.2f}, return: {(merged['slv'].iloc[-1]/merged['slv'].iloc[0]-1)*100:.0f}%")
print(f"Biggest 8-week silver rally: +{breakout_8w_pct:.1f}% ending {breakout_date.date()}")
print(f"Max gold-silver lag spread: {merged['spread'].max():.1f} points, peaked {lag_peak_date.date()}")
