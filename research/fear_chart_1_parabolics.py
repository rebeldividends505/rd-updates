"""Fear Chart 1: AI/Semi parabolic runs (NVDA, PLTR, AMD, SOXL)."""
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ENV_PATH = "/Users/rebeldividends/rd-updates-site/.env"
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            v = v.strip().strip('"').strip("'")
            os.environ.setdefault(k.strip(), v)

POLYGON = os.environ["POLYGON_API_KEY"]

stocks = {
    "NVDA": {"pe": 41, "note": "P/E: 41x | +1,400% since 2023 low", "color": "#22c55e"},
    "PLTR": {"pe": 145, "note": "P/E: 145x | Retail favorite", "color": "#3b82f6"},
    "AMD": {"pe": 148, "note": "P/E: 148x | Goldman: Final Innings", "color": "#ef4444"},
    "SOXL": {"pe": 0, "note": "+996% in 12 months | 3x leveraged ETF", "color": "#f97316"},
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor("white")
fig.suptitle(
    "AI/Semiconductor Stocks: The Parabolic Run\n"
    "Every Green Line Has a Gravity. What Goes Parabolic Comes Back.",
    fontsize=14, fontweight="bold", color="#000000", y=0.98,
)

def fetch_polygon_weekly(ticker, start, end):
    """Fetch full weekly history, paginating through next_url."""
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/week/"
        f"{start}/{end}?apiKey={POLYGON}&limit=50000&adjusted=true&sort=asc"
    )
    rows = []
    while url:
        resp = requests.get(url).json()
        rows.extend(resp.get("results", []) or [])
        nxt = resp.get("next_url")
        if nxt:
            sep = "&" if "?" in nxt else "?"
            url = f"{nxt}{sep}apiKey={POLYGON}"
        else:
            url = None
    return rows


for idx, (ticker, info) in enumerate(stocks.items()):
    ax = axes[idx // 2][idx % 2]
    results = fetch_polygon_weekly(ticker, "2024-01-01", "2026-05-11")
    if not results:
        print(f"WARN: No data for {ticker}")
        ax.text(0.5, 0.5, f"No data for {ticker}", ha="center", va="center",
                transform=ax.transAxes)
        continue

    df = pd.DataFrame(results)
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("date", inplace=True)

    ax.fill_between(df.index, df["c"], df["c"].min() * 0.95,
                    alpha=0.15, color=info["color"])
    ax.plot(df.index, df["c"], color=info["color"], linewidth=2.5)

    ax.text(0.97, 0.95, info["note"], transform=ax.transAxes,
            fontsize=9, color="#374151", ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#fef3c7",
                      edgecolor="#d97706", alpha=0.9))

    peak_val = df["c"].max()
    peak_date = df["c"].idxmax()
    ax.annotate("↑ PARABOLIC", xy=(peak_date, peak_val),
                xytext=(peak_date, peak_val * 0.85),
                fontsize=9, color="#ef4444", fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#ef4444", lw=1.5))

    last_price = df["c"].iloc[-1]
    print(f"{ticker}: last close ${last_price:.2f} on {df.index[-1].date()}, peak ${peak_val:.2f}")

    ax.set_title(ticker, fontsize=13, fontweight="bold", color="#000000")
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:.0f}"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.grid(axis="y", alpha=0.15)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30)

plt.tight_layout()
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-ai-parabolics.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Fear Chart 1 saved: {out}")
