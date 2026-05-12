"""Pitch 5: Yen carry trade is the governor keeping BTC suppressed."""
import os, requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")

def fetch_av_fx(from_sym="USD", to_sym="JPY"):
    r = requests.get("https://www.alphavantage.co/query", params={
        "function": "FX_DAILY", "from_symbol": from_sym, "to_symbol": to_sym,
        "outputsize": "full", "apikey": os.environ["ALPHAVANTAGE_API_KEY"],
    }, timeout=30)
    ts = r.json()["Time Series FX (Daily)"]
    rows = [{"date": pd.Timestamp(d), "close": float(v["4. close"])} for d, v in ts.items()]
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].astype("datetime64[ns]")
    return df

def fetch_av_crypto(symbol="BTC"):
    import json
    cache = os.path.join(OUT, "btc_cache.json")
    if os.path.exists(cache):
        j = json.load(open(cache))
    else:
        r = requests.get("https://www.alphavantage.co/query", params={
            "function": "DIGITAL_CURRENCY_DAILY", "symbol": symbol, "market": "USD",
            "apikey": os.environ["ALPHAVANTAGE_API_KEY"],
        }, timeout=30)
        j = r.json()
        json.dump(j, open(cache, "w"))
    data = j["Time Series (Digital Currency Daily)"]
    rows = []
    for d, v in data.items():
        ck = next(k for k in v if "close" in k.lower())
        rows.append({"date": pd.Timestamp(d), "close": float(v[ck])})
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    df["date"] = df["date"].astype("datetime64[ns]")
    return df

print("Fetching USD/JPY...")
jpy = fetch_av_fx("USD", "JPY")
jpy = jpy[jpy["date"] >= pd.Timestamp("2022-01-01")].reset_index(drop=True)
print(f"  USDJPY: {len(jpy)} rows {jpy['date'].min().date()} → {jpy['date'].max().date()}")

print("Fetching BTC...")
btc = fetch_av_crypto("BTC")
btc = btc[btc["date"] >= pd.Timestamp("2022-01-01")].reset_index(drop=True)

merged = pd.merge(jpy.rename(columns={"close": "usdjpy"}),
                  btc.rename(columns={"close": "btc"}),
                  on="date", how="inner").sort_values("date").reset_index(drop=True)
merged.to_csv(os.path.join(OUT, "pitch5_data.csv"), index=False)
print(f"Merged rows: {len(merged)}")

# Build chart with two panels
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8.5), sharex=True,
                                gridspec_kw={"height_ratios": [1.4, 1]}, dpi=110)

ax1.plot(merged["date"], merged["btc"], color="#F7931A", linewidth=2.2, label="BTC price")
ax1.set_ylabel("BTC (USD)", color="#F7931A", fontsize=11)
ax1.tick_params(axis='y', labelcolor="#F7931A")
ax1.set_title("Yen Carry Trade — The Governor Keeping BTC Suppressed",
              fontsize=14, fontweight="bold", pad=12)
ax1.grid(True, alpha=0.3)
ax1.legend(loc="upper left", fontsize=11)

# Inverted USD/JPY: lower line = stronger yen
ax2.plot(merged["date"], merged["usdjpy"], color="#cc0000", linewidth=2.0, label="USD/JPY")
ax2.invert_yaxis()
ax2.set_ylabel("USD/JPY\n(inverted ↑ = yen strength)", color="#cc0000", fontsize=10)
ax2.tick_params(axis='y', labelcolor="#cc0000")
ax2.grid(True, alpha=0.3)
ax2.legend(loc="upper left", fontsize=10)

# August 2024 yen spike shading
aug24_s = pd.Timestamp("2024-07-25")
aug24_e = pd.Timestamp("2024-08-12")
for ax in (ax1, ax2):
    ax.axvspan(aug24_s, aug24_e, color="#222", alpha=0.18)

# Annotate Aug 2024
crash_idx = (merged["date"] - pd.Timestamp("2024-08-05")).abs().idxmin()
crash_y_btc = merged.loc[crash_idx, "btc"]
ax1.annotate("Aug 2024:\nyen spiked, BTC -20% in 48h",
             xy=(merged.loc[crash_idx, "date"], crash_y_btc),
             xytext=(merged.loc[crash_idx, "date"] - pd.Timedelta(days=240),
                     crash_y_btc * 1.35),
             fontsize=10, ha="center", color="#000", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#000"),
             arrowprops=dict(arrowstyle="->", color="#000", lw=1.2))

# Current — annotate yen position
last = merged.iloc[-1]
ax2.annotate(f"USD/JPY now: {last['usdjpy']:.1f}\n(yen recovering but\ncarry trade still loaded)",
             xy=(last["date"], last["usdjpy"]),
             xytext=(last["date"] - pd.Timedelta(days=300), last["usdjpy"]),
             fontsize=10, ha="center", color="#7a1010", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#7a1010"),
             arrowprops=dict(arrowstyle="->", color="#7a1010", lw=1.0))

ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

fig.text(0.5, 0.005,
         "Pattern: yen strength spikes → BTC sells off as carry positions unwind. Yen is stabilizing now — when it goes slowly, BTC bids hard.",
         ha="center", fontsize=10.5, style="italic", color="#333")

plt.tight_layout(rect=(0, 0.02, 1, 1))
out_path = os.path.join(OUT, "chart5-yen-btc.png")
fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)

# Correlation BTC vs USD/JPY returns
merged["btc_r"] = merged["btc"].pct_change()
merged["jpy_r"] = merged["usdjpy"].pct_change()
corr = merged["btc_r"].corr(merged["jpy_r"])
print(f"\n=== Pitch 5 stats ===")
print(f"USD/JPY current: {last['usdjpy']:.2f}")
print(f"USD/JPY peak weak: {merged['usdjpy'].max():.2f}")
print(f"BTC current: ${last['btc']:,.0f}")
print(f"BTC/USDJPY returns correlation: {corr:.3f}")
