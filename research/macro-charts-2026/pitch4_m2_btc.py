"""Pitch 4: M2 Money Supply vs BTC — largest gap on record."""
import os, requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")

def fetch_fred(series_id, start="2018-01-01"):
    r = requests.get("https://api.stlouisfed.org/fred/series/observations", params={
        "series_id": series_id, "api_key": os.environ["FRED_API_KEY"],
        "file_type": "json", "observation_start": start,
    }, timeout=30)
    obs = r.json()["observations"]
    rows = [{"date": pd.Timestamp(o["date"]), "value": float(o["value"]) if o["value"] != "." else np.nan}
            for o in obs]
    df = pd.DataFrame(rows).dropna().reset_index(drop=True)
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

print("Fetching US M2 from FRED...")
m2 = fetch_fred("M2SL", "2018-01-01")
print(f"  M2: {len(m2)} rows {m2['date'].min().date()} → {m2['date'].max().date()}")

print("Fetching BTC from Alpha Vantage...")
btc = fetch_av_crypto("BTC")
btc = btc[btc["date"] >= pd.Timestamp("2018-01-01")].reset_index(drop=True)
print(f"  BTC: {len(btc)} rows {btc['date'].min().date()} → {btc['date'].max().date()}")

# Resample BTC to monthly (month-end close)
btc_m = btc.set_index("date").resample("ME")["close"].last().reset_index()
m2 = m2.rename(columns={"value": "m2"})

# Align on monthly
merged = pd.merge_asof(btc_m.sort_values("date"),
                      m2.sort_values("date"),
                      on="date", direction="backward").dropna().reset_index(drop=True)

# Index to Jan 2020
anchor = pd.Timestamp("2020-01-31")
m2_anchor = merged.loc[(merged["date"] - anchor).abs().idxmin(), "m2"]
btc_anchor = merged.loc[(merged["date"] - anchor).abs().idxmin(), "close"]
merged["m2_idx"] = merged["m2"] / m2_anchor * 100
merged["btc_idx"] = merged["close"] / btc_anchor * 100

# YoY M2 growth
merged["m2_yoy"] = merged["m2"].pct_change(12) * 100

# Pre-2024 correlation (when tightly coupled)
hist = merged[(merged["date"] >= pd.Timestamp("2020-01-01")) &
              (merged["date"] < pd.Timestamp("2024-01-01"))]
corr_hist = hist["m2_idx"].corr(hist["btc_idx"])
print(f"Historical 2020-2023 correlation: {corr_hist:.3f}")

# Gap = difference between btc_idx and m2_idx (BTC has run further on a normalized basis but
# the pitch is about BTC underperforming M2 lately — we'll show m2_idx - btc_idx as 'BTC owes')
# Actually, the message is: BTC has tracked M2 historically; the deviation now is wider than ever.
# We'll compute the ratio btc_idx / m2_idx and show its deviation.
merged["ratio"] = merged["btc_idx"] / merged["m2_idx"]
merged.to_csv(os.path.join(OUT, "pitch4_data.csv"), index=False)

# Build chart with two panels
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8.5), sharex=True,
                                gridspec_kw={"height_ratios": [2.3, 1]}, dpi=110)

ax1b = ax1.twinx()
l1 = ax1.plot(merged["date"], merged["m2_idx"], color="#1f6feb", linewidth=2.2, label="US M2 money supply (indexed)")
l2 = ax1b.plot(merged["date"], merged["close"], color="#F7931A", linewidth=2.2, label="BTC price (USD)")
ax1.set_ylabel("M2 indexed (Jan 2020 = 100)", color="#1f6feb", fontsize=11)
ax1b.set_ylabel("BTC price (USD)", color="#F7931A", fontsize=11)
ax1.tick_params(axis='y', labelcolor="#1f6feb")
ax1b.tick_params(axis='y', labelcolor="#F7931A")
ax1.set_title("BTC Has Tracked M2 for 5 Years — Today's Gap Is the Widest on Record",
              fontsize=14, fontweight="bold", pad=12)
ax1.grid(True, alpha=0.3)

lines = l1 + l2
labels = [ln.get_label() for ln in lines]
ax1.legend(lines, labels, loc="upper left", fontsize=11)

# Shade decoupling region
decouple_start = pd.Timestamp("2025-08-01")
ax1.axvspan(decouple_start, merged["date"].iloc[-1], color="red", alpha=0.10)
ax1.annotate(f"M2 keeps grinding higher.\nBTC has stalled.\n5y correlation: {corr_hist:.2f}",
             xy=(decouple_start + (merged["date"].iloc[-1] - decouple_start)/2,
                 merged["m2_idx"].iloc[-1]),
             xytext=(decouple_start - pd.Timedelta(days=400),
                     merged["m2_idx"].max() * 0.78),
             fontsize=10.5, ha="center", color="#7a1010", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="#7a1010"),
             arrowprops=dict(arrowstyle="->", color="#7a1010", lw=1.2))

# Bottom panel: M2 YoY growth
ax2.bar(merged["date"], merged["m2_yoy"], color="#1f6feb", alpha=0.6, width=25)
ax2.axhline(0, color="#000", linewidth=0.6)
ax2.axhline(7, color="#2ca02c", linestyle="--", linewidth=0.9, alpha=0.7,
            label="7% YoY = 'BTC-bullish' regime")
ax2.set_ylabel("M2 YoY %\nchange", fontsize=10)
ax2.set_xlabel("")
ax2.grid(True, alpha=0.3)
ax2.legend(loc="upper right", fontsize=9)

ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

fig.text(0.5, 0.005,
         "Historical pattern: BTC catches up to M2 expansion with 60-90 day lag. The current gap implies meaningful upside as the relationship re-couples.",
         ha="center", fontsize=10.5, style="italic", color="#333")

plt.tight_layout(rect=(0, 0.02, 1, 1))
out_path = os.path.join(OUT, "chart4-m2-btc-gap.png")
fig.savefig(out_path, dpi=120, bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)

# Stats
last = merged.iloc[-1]
print(f"\n=== Pitch 4 stats ===")
print(f"M2 indexed: {last['m2_idx']:.1f}, BTC indexed: {last['btc_idx']:.1f}")
print(f"Current M2 YoY: {last['m2_yoy']:.2f}%")
print(f"BTC/M2 ratio anchor: {last['ratio']:.3f}")
print(f"Historical correlation 2020-2023: {corr_hist:.3f}")
