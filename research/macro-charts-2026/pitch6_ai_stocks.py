"""Pitch 6: AI stocks overbought — returns, P/E, RSI, key risks."""
import os, requests, time, json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")

TICKERS = ["NVDA", "MSFT", "GOOGL", "META", "AVGO", "MU", "AMD", "PLTR", "SOXL"]

FMP = os.environ["FMP_API_KEY"]
POLY = os.environ["POLYGON_API_KEY"]
FINNHUB = os.environ["FINNHUB_API_KEY"]


def fmp(url, params=None):
    p = dict(params or {}); p["apikey"] = FMP
    r = requests.get(url, params=p, timeout=20)
    try: return r.json()
    except Exception: return None


def finnhub_metrics(ticker):
    r = requests.get(
        "https://finnhub.io/api/v1/stock/metric",
        params={"symbol": ticker, "metric": "all", "token": FINNHUB}, timeout=15,
    )
    return r.json().get("metric", {}) if r.status_code == 200 else {}


def polygon_aggs(ticker, start, end):
    r = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}",
        params={"apiKey": POLY, "limit": 50000, "adjusted": "true"}, timeout=20,
    )
    return r.json().get("results", [])


def polygon_rsi(ticker):
    r = requests.get(
        f"https://api.polygon.io/v1/indicators/rsi/{ticker}",
        params={"timespan": "day", "window": 14, "series_type": "close",
                "apiKey": POLY, "limit": 1}, timeout=15,
    )
    j = r.json()
    vals = j.get("results", {}).get("values", [])
    return vals[0]["value"] if vals else None


def collect():
    rows = []
    for t in TICKERS:
        print(f"  {t}...")
        # 12-month return from Polygon
        aggs = polygon_aggs(t, "2025-05-11", "2026-05-11")
        if not aggs or len(aggs) < 2:
            print(f"    no aggs for {t}, skipping")
            continue
        ret_12m = (aggs[-1]["c"] / aggs[0]["c"] - 1) * 100
        price = aggs[-1]["c"]

        # Finnhub metrics (works for all our symbols, gives forwardPE, peTTM, pfcfTTM, etc.)
        fh = finnhub_metrics(t)
        ttm_pe = fh.get("peTTM") or fh.get("peExclExtraTTM")
        fwd_pe = fh.get("forwardPE")
        p_fcf = fh.get("pfcfShareTTM") or fh.get("currentEv/freeCashFlowTTM")
        pe_5y_norm = fh.get("peNormalizedAnnual")  # Normalized PE (5y normalized)

        # 5-year average from FMP ratios (more accurate when available)
        ratios = fmp("https://financialmodelingprep.com/stable/ratios", {"symbol": t, "limit": 5}) or []
        if not isinstance(ratios, list): ratios = []
        pes = [r.get("priceToEarningsRatio") for r in ratios if r.get("priceToEarningsRatio")]
        avg_5y_pe = float(np.mean(pes)) if pes else pe_5y_norm

        # RSI
        rsi = polygon_rsi(t)
        time.sleep(0.15)

        rows.append({
            "ticker": t,
            "price": price,
            "return_12m": ret_12m,
            "trailing_pe": ttm_pe,
            "forward_pe": fwd_pe,
            "p_fcf": p_fcf,
            "avg_5y_pe": avg_5y_pe,
            "rsi": rsi,
        })
    return pd.DataFrame(rows)


print("Collecting stock data...")
df = collect()
print(df.to_string())
df.to_csv(os.path.join(OUT, "pitch6_data.csv"), index=False)

# Hard-coded key risks (sourced via secondary research, kept current)
KEY_RISKS = {
    "NVDA": "China export bans + AMD MI400 ramp + hyperscaler capex digestion",
    "MSFT": "Azure growth decel + Copilot monetization slower than priced",
    "GOOGL": "AI search disruption (Perplexity/ChatGPT) + DOJ antitrust remedies",
    "META": "Reality Labs cash burn + EU regulatory drag on ads",
    "AVGO": "Hyperscaler capex digestion + customer concentration (META/GOOG)",
    "MU": "Memory oversupply cycle + SK Hynix HBM4 lead",
    "AMD": "MI400 execution risk + NVDA pricing pressure on data-center GPUs",
    "PLTR": "200x+ earnings multiple + gov contract concentration + insider selling",
    "SOXL": "3x leverage decay + correction would compound -50%+ losses fast",
}

# ============================================================
# Chart 6a: 12-month returns horizontal bar
# ============================================================
df_sorted = df.sort_values("return_12m", ascending=True).reset_index(drop=True)
colors = []
for r in df_sorted["return_12m"]:
    if r > 100: colors.append("#7a0000")
    elif r > 50: colors.append("#cc0000")
    elif r > 25: colors.append("#ff7700")
    elif r > 10: colors.append("#ffc500")
    else: colors.append("#8aab3a")

fig, ax = plt.subplots(figsize=(13, 7), dpi=110)
bars = ax.barh(df_sorted["ticker"], df_sorted["return_12m"], color=colors,
               edgecolor="black", linewidth=0.7)
for b, v in zip(bars, df_sorted["return_12m"]):
    ax.text(v + 3 if v >= 0 else v - 8, b.get_y() + b.get_height()/2,
            f"+{v:.0f}%" if v >= 0 else f"{v:.0f}%",
            va="center", ha="left" if v >= 0 else "right",
            fontweight="bold", fontsize=11)
ax.set_xlabel("12-month total return (%)", fontsize=11)
ax.set_title("These AI Stocks Ran 50–500%. Who's Still Buying at These Prices?",
             fontsize=14, fontweight="bold", pad=12)
ax.grid(True, alpha=0.3, axis="x")
ax.axvline(0, color="black", linewidth=0.7)
fig.text(0.5, 0.005,
         "Red = extreme (>50% in 12 months). The bigger the bar, the more profits sitting in retail accounts that haven't been taken yet.",
         ha="center", fontsize=10.5, style="italic", color="#333")
plt.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(os.path.join(OUT, "chart6a-ai-stocks-returns.png"), dpi=120, bbox_inches="tight")
print(f"Saved: chart6a-ai-stocks-returns.png")
plt.close(fig)

# ============================================================
# Chart 6b: Trailing P/E vs Forward P/E (priced for perfection)
# ============================================================
df_pe = df.dropna(subset=["trailing_pe", "forward_pe"]).copy()
df_pe = df_pe[df_pe["trailing_pe"] < 500]
df_pe = df_pe.sort_values("trailing_pe", ascending=False).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 7), dpi=110)
x = np.arange(len(df_pe))
w = 0.4
b1 = ax.bar(x - w/2, df_pe["trailing_pe"], w, color="#cc0000", label="Trailing P/E (what you pay today)", edgecolor="black", linewidth=0.6)
b2 = ax.bar(x + w/2, df_pe["forward_pe"], w, color="#ff9933", label="Forward P/E (assumes analyst estimates hit)", edgecolor="black", linewidth=0.6)
for bar in b1:
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+1, f"{h:.0f}", ha="center", fontsize=9.5, fontweight="bold", color="#7a0000")
for bar in b2:
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+1, f"{h:.0f}", ha="center", fontsize=9.5, color="#7a4400")

# Reference lines for "expensive" vs "reasonable"
ax.axhline(25, color="#2ca02c", linestyle="--", linewidth=1, alpha=0.6,
           label="P/E 25 (S&P 500 long-run avg)")

ax.set_xticks(x)
ax.set_xticklabels(df_pe["ticker"], fontsize=11)
ax.set_ylabel("P/E ratio", fontsize=11)
ax.set_title("Priced for Perfection: Even Forward P/Es Bake In Massive Earnings Growth",
             fontsize=14, fontweight="bold", pad=12)
ax.legend(loc="upper right", fontsize=10)
ax.grid(True, alpha=0.3, axis="y")

fig.text(0.5, 0.005,
         "Forward P/E assumes analysts are right. If they miss by even 10%, multiple compression could deliver a 20-40% pullback.",
         ha="center", fontsize=10.5, style="italic", color="#333")
plt.tight_layout(rect=(0, 0.02, 1, 1))
fig.savefig(os.path.join(OUT, "chart6b-ai-stocks-pe.png"), dpi=120, bbox_inches="tight")
print(f"Saved: chart6b-ai-stocks-pe.png")
plt.close(fig)

# ============================================================
# Stocks table — HTML
# ============================================================
def fmt(v, kind="num"):
    if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
        return "—"
    if kind == "pct": return f"+{v:.0f}%" if v >= 0 else f"{v:.0f}%"
    if kind == "pe":  return f"{v:.1f}"
    if kind == "rsi":
        s = f"{v:.0f}"
        if v >= 70: s += " (overbought)"
        return s
    return f"{v:.1f}"

rows_html = []
for _, r in df.iterrows():
    risk = KEY_RISKS.get(r["ticker"], "—")
    rows_html.append(f"""    <tr>
      <td><strong>{r['ticker']}</strong></td>
      <td>{fmt(r['return_12m'],'pct')}</td>
      <td>{fmt(r['trailing_pe'],'pe')}</td>
      <td>{fmt(r['forward_pe'],'pe')}</td>
      <td>{fmt(r['p_fcf'],'pe')}</td>
      <td>{fmt(r['rsi'],'rsi')}</td>
      <td>{risk}</td>
    </tr>""")

html = f"""<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif;font-size:14px">
  <thead style="background:#1a1a1a;color:white">
    <tr>
      <th style="padding:8px;text-align:left">Stock</th>
      <th style="padding:8px;text-align:left">12M Return</th>
      <th style="padding:8px;text-align:left">Trailing P/E</th>
      <th style="padding:8px;text-align:left">Forward P/E</th>
      <th style="padding:8px;text-align:left">P/FCF</th>
      <th style="padding:8px;text-align:left">RSI</th>
      <th style="padding:8px;text-align:left">Key Risk</th>
    </tr>
  </thead>
  <tbody style="background:white;color:#111">
{chr(10).join(rows_html)}
  </tbody>
</table>"""

with open(os.path.join(OUT, "stocks-table.html"), "w") as f:
    f.write(html)
print(f"Saved: stocks-table.html")

print("\n=== Pitch 6 stats ===")
print(df[["ticker", "return_12m", "trailing_pe", "avg_5y_pe", "rsi"]].to_string())
