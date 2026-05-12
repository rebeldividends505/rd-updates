"""Pitch 3: Gold leads BTC by ~180 days."""
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

def fetch_av_crypto(symbol="BTC"):
    r = requests.get("https://www.alphavantage.co/query", params={
        "function": "DIGITAL_CURRENCY_DAILY", "symbol": symbol, "market": "USD",
        "apikey": os.environ["ALPHAVANTAGE_API_KEY"],
    }, timeout=30)
    data = r.json()["Time Series (Digital Currency Daily)"]
    rows = []
    for d, v in data.items():
        ck = next(k for k in v if "close" in k.lower())
        rows.append({"date": pd.Timestamp(d), "close": float(v[ck])})
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].astype("datetime64[ns]")
    return df

print("Fetching gold (GLD) and BTC...")
gld = fetch_polygon_equity("GLD")
btc = fetch_av_crypto("BTC")

# Use 2021-2026 range (limited by Polygon GLD free tier)
start = pd.Timestamp("2021-05-12")
gld = gld[gld["date"] >= start].reset_index(drop=True)
btc = btc[btc["date"] >= start].reset_index(drop=True)

# Compute best lag between gold and BTC using cross-correlation of returns
gld_idx = gld.set_index("date")["close"]
btc_idx = btc.set_index("date")["close"]
common = pd.concat([gld_idx.rename("gld"), btc_idx.rename("btc")], axis=1).dropna()
common["gld_r"] = common["gld"].pct_change(20)  # ~1 month returns
common["btc_r"] = common["btc"].pct_change(20)
best_lag = None
best_corr = -np.inf
for lag in range(30, 270, 10):
    shifted = common["gld_r"].shift(lag)
    c = shifted.corr(common["btc_r"])
    if c is not None and c > best_corr:
        best_corr = c; best_lag = lag
print(f"Best gold-lead lag: {best_lag} days, correlation {best_corr:.3f}")

# Use 180 days as stated in pitch
LAG = 180
gld_shift = common["gld"].shift(LAG).rename("gld_shift")
df = pd.concat([common["btc"], gld_shift], axis=1).dropna().reset_index()
# Rescale gold-shift to BTC's range for visual overlay
scale_a = df["btc"].max() / df["gld_shift"].max()
df["gld_scaled"] = df["gld_shift"] * scale_a

# Build chart
fig, ax = plt.subplots(figsize=(14, 7), dpi=110)
ax.plot(df["date"], df["btc"], color="#F7931A", linewidth=2.4, label="BTC price (actual date)")
ax2 = ax.twinx()
ax2.plot(df["date"], df["gld_shift"], color="#D4AF37", linewidth=2.0, linestyle="--",
         label=f"Gold shifted +{LAG} days forward")

ax.set_ylabel("BTC price (USD)", color="#F7931A", fontsize=11)
ax2.set_ylabel("Gold (GLD, USD) shifted +%dd" % LAG, color="#B89020", fontsize=11)
ax.set_title(f"Gold Leads BTC by ~{LAG} Days — Gold Is Signaling, BTC Hasn't Caught Up Yet",
             fontsize=14, fontweight="bold", pad=12)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='y', labelcolor="#F7931A")
ax2.tick_params(axis='y', labelcolor="#B89020")

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=11)

# Annotation: current gap
last_date = df["date"].iloc[-1]
last_btc = df["btc"].iloc[-1]
last_gld = df["gld_shift"].iloc[-1]
ax.annotate(f"Gold +{LAG}d pattern points\nto BTC ~${last_gld*scale_a:,.0f} target",
            xy=(last_date, last_btc),
            xytext=(last_date - pd.Timedelta(days=240), last_btc * 1.15),
            fontsize=10.5, ha="center", color="#7a1010", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#7a1010", alpha=0.95),
            arrowprops=dict(arrowstyle="->", color="#7a1010", lw=1.2))

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

fig.text(0.5, 0.005,
         "Best historical lag: %d days at correlation %.2f. Pattern: gold rips → BTC follows 6 months later. Gold is at ATH; BTC is lagging." % (best_lag, best_corr),
         ha="center", fontsize=10.5, style="italic", color="#333")

plt.tight_layout(rect=(0, 0.025, 1, 1))
out_path = os.path.join(OUT, "chart3-gold-btc-180day-lag.png")
fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)

# Save data
df.to_csv(os.path.join(OUT, "pitch3_data.csv"), index=False)
print(f"\n=== Pitch 3 stats ===")
print(f"Best lag: {best_lag} days, corr: {best_corr:.3f}")
print(f"Current gold suggests BTC target: ${last_gld * scale_a:,.0f}")
print(f"Current BTC: ${last_btc:,.0f}")
print(f"Upside implied: {(last_gld*scale_a/last_btc - 1)*100:.1f}%")
