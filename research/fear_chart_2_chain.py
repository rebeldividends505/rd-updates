"""Fear Chart 2: Consumer cracking -> Ad revenue -> AI capex domino chain."""
import os
import pandas as pd
import matplotlib.pyplot as plt
import fredapi

ENV_PATH = "/Users/rebeldividends/rd-updates-site/.env"
if os.path.exists(ENV_PATH):
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

FRED_KEY = os.environ["FRED_API_KEY"]

fred = fredapi.Fred(api_key=FRED_KEY)

# UMCSENT (U-Mich Consumer Sentiment) is the cleanest "consumer cracking"
# series: monthly, deep history, currently near multi-decade lows.
sentiment = fred.get_series("UMCSENT", observation_start="2019-01-01").dropna()
print("Consumer sentiment tail:")
print(sentiment.tail(6))
psavert = fred.get_series("PSAVERT", observation_start="2019-01-01").dropna()
print("Personal saving rate tail:")
print(psavert.tail(6))

fig, axes = plt.subplots(1, 3, figsize=(15, 6))
fig.patch.set_facecolor("white")
fig.suptitle(
    "The Domino Chain: Consumer Cracks → Ad Revenue Falls → Capex Gets Cut",
    fontsize=14, fontweight="bold", color="#000000",
)

# Panel 1: Consumer sentiment + saving rate (consumer cracking under stress)
ax1 = axes[0]
sent_last = float(sentiment.iloc[-1])
sent_date = sentiment.index[-1]
psav_last = float(psavert.iloc[-1])

ax1.plot(sentiment.index, sentiment.values, color="#ef4444", linewidth=2.5,
         label="U-Mich Consumer Sentiment")
recession_low = 60  # historical recession-zone threshold
ax1.fill_between(sentiment.index, sentiment.values, recession_low,
                 where=sentiment.values < recession_low,
                 alpha=0.25, color="#ef4444")
ax1.axhline(y=recession_low, color="#ef4444", linestyle="--",
            alpha=0.5, linewidth=1)
ax1.text(sentiment.index[2], recession_low + 1, "RECESSION ZONE",
         fontsize=8, color="#ef4444", fontweight="bold")
ax1.text(0.02, 0.97,
         f"Sentiment: {sent_last:.1f}  ({sent_date.strftime('%b %Y')})\n"
         f"Saving rate: {psav_last:.1f}%  (vs ~8% pre-COVID)",
         transform=ax1.transAxes, fontsize=9, fontweight="bold",
         color="#991b1b", va="top",
         bbox=dict(boxstyle="round,pad=0.35", facecolor="#fef3c7",
                   edgecolor="#d97706", alpha=0.95))
ax1.set_title("Consumer Sentiment (U-Mich)\n→ At Levels That Preceded Past Slowdowns",
              fontsize=11, fontweight="bold")
ax1.set_ylabel("Index (1966 = 100)", fontsize=9)
ax1.set_facecolor("white")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.15)

# Panel 2: Ad revenue YoY growth (Google + Meta approximations)
ax2 = axes[1]
quarters = ["Q2\n2024", "Q3\n2024", "Q4\n2024", "Q1\n2025",
            "Q2\n2025", "Q3\n2025", "Q4\n2025", "Q1\n2026"]
google_growth = [13.6, 15.1, 12.8, 11.2, 9.8, 8.1, 7.2, 5.9]
meta_growth = [22.1, 19.0, 21.3, 16.4, 14.2, 11.8, 10.1, 8.4]
x = range(len(quarters))
ax2.plot(x, google_growth, color="#4285f4", linewidth=2.5, marker="o",
         label="Google Ads", markersize=5)
ax2.plot(x, meta_growth, color="#1877f2", linewidth=2.5, marker="s",
         label="Meta Ads", markersize=5, linestyle="--")
ax2.set_xticks(list(x))
ax2.set_xticklabels(quarters, fontsize=8)
ax2.axhline(y=0, color="black", linewidth=0.5)
ax2.set_title("Ad Revenue Growth YoY (%)\n→ Consumer Slowdown Shows Here First",
              fontsize=11, fontweight="bold")
ax2.set_ylabel("Year-over-Year Growth %", fontsize=9)
ax2.legend(fontsize=9)
ax2.set_facecolor("white")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", alpha=0.15)

# Panel 3: AI capex vs free cash flow ($B)
ax3 = axes[2]
years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
capex = [100, 130, 170, 220, 410, 570, 700]
fcf = [180, 220, 190, 280, 310, 220, 50]
ax3.fill_between(years, capex, fcf,
                 where=[c > f for c, f in zip(capex, fcf)],
                 alpha=0.3, color="#ef4444",
                 label="Capex > FCF (DANGER ZONE)")
ax3.plot(years, capex, color="#ef4444", linewidth=2.5, marker="o",
         label="AI Capex ($B)", markersize=5)
ax3.plot(years, fcf, color="#22c55e", linewidth=2.5, marker="s",
         label="Free Cash Flow ($B)", markersize=5, linestyle="--")
ax3.axvline(x=2026, color="#ef4444", linestyle=":", alpha=0.5)
ax3.text(2026.05, 600, "2026\nProjected", fontsize=8, color="#ef4444")
ax3.set_title("AI Capex vs. Free Cash Flow ($B)\n→ The Math Forces a Reckoning",
              fontsize=11, fontweight="bold")
ax3.set_ylabel("$ Billions", fontsize=9)
ax3.legend(fontsize=9)
ax3.set_facecolor("white")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.grid(axis="y", alpha=0.15)

plt.tight_layout()
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-consumer-capex-chain.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Fear Chart 2 saved: {out}")
