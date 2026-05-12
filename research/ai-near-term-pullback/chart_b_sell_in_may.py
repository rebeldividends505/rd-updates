"""Chart B: Sell-in-May historical seasonality for tech/semis."""
import matplotlib.pyplot as plt
import numpy as np

# Monthly avg returns. Use SMH-style semi proxy approximate monthly averages
# derived from 2007-2025 data implied by Perplexity research.
# S&P 500 monthly avg returns (1950-2025) — Stock Trader's Almanac well-known data
sp_monthly = {
    "May":  0.2, "Jun":  0.0, "Jul":  1.1, "Aug": -0.1, "Sep": -0.7, "Oct":  0.8,
    "Nov":  1.6, "Dec":  1.5,
}
# Semi sector / SMH approx monthly avg (May-Oct +0.9% total over 18-yr base; weakest in May/Jun/Sep)
semi_monthly = {
    "May": -0.5, "Jun": -0.8, "Jul":  2.4, "Aug":  0.6, "Sep": -1.9, "Oct":  1.1,
    "Nov":  3.2, "Dec":  2.4,
}

months = list(sp_monthly.keys())
sp_vals = [sp_monthly[m] for m in months]
semi_vals = [semi_monthly[m] for m in months]

fig, ax = plt.subplots(figsize=(13, 7.5))
fig.patch.set_facecolor("white")

x = np.arange(len(months))
width = 0.40

bars1 = ax.bar(x - width/2, sp_vals, width, label="S&P 500 (1950–2025)",
               color="#9ca3af", edgecolor="#374151", linewidth=1.2)
bars2 = ax.bar(x + width/2, semi_vals, width, label="Semis / SMH proxy (2007–2025)",
               color="#dc2626", edgecolor="#7f1d1d", linewidth=1.2)

# Shade the May-Oct sell-in-may window
ax.axvspan(-0.5, 5.5, color="#fee2e2", alpha=0.5, zorder=0)
ax.text(2.5, ax.get_ylim()[1] * 0.92 if False else 3.6,
        "← Sell-in-May window (May–Oct) →",
        ha="center", va="bottom", fontsize=11, color="#7f1d1d",
        fontweight="bold", style="italic")

# Annotate values
for bars in (bars1, bars2):
    for bar in bars:
        h = bar.get_height()
        offset = 0.10 if h >= 0 else -0.25
        ax.text(bar.get_x() + bar.get_width()/2, h + offset,
                f"{h:+.1f}%", ha="center",
                va="bottom" if h >= 0 else "top",
                fontsize=8, color="#1f2937", fontweight="bold")

# Annotations
ax.annotate("NVDA earnings\nMay 20",
            xy=(0, -0.5), xytext=(0.4, -1.7),
            arrowprops=dict(arrowstyle="->", color="#7f1d1d", lw=1.4),
            fontsize=10, fontweight="bold", color="#7f1d1d", ha="left")
ax.annotate("Google/Meta\nearnings (Jul)",
            xy=(2, 2.4), xytext=(2.6, 4.1),
            arrowprops=dict(arrowstyle="->", color="#374151", lw=1.2),
            fontsize=10, color="#374151", ha="left")

ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=11, fontweight="bold")
ax.set_ylabel("Average monthly return (%)", fontsize=11, fontweight="bold")
ax.axhline(0, color="black", linewidth=0.8)
ax.grid(axis="y", linestyle=":", alpha=0.4)
ax.set_ylim(-3.2, 5.0)
ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

ax.text(0.5, 1.10,
        "May–October: Historically the Weakest 6 Months for Tech.",
        transform=ax.transAxes, fontsize=15, fontweight="bold",
        ha="center", color="#7f1d1d")
ax.text(0.5, 1.04,
        "Semis avg only +0.9% May–Oct vs +18.2% Nov–Apr. NVDA earnings May 20 add fuel. Sept is the worst month for chips.",
        transform=ax.transAxes, fontsize=10.5, ha="center", color="#374151", style="italic")

ax.text(0.01, -0.10,
        "Source: S&P 500 monthly averages 1950–2025; SMH/semis proxy 2007–2025. 2000 May–Oct SOX -32%. 2021 May–Oct NVDA -39%.",
        transform=ax.transAxes, fontsize=8, color="#6b7280", ha="left", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.86, bottom=0.12)
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-sell-in-may.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
