"""Fear Chart 3: Retail danger positioning composite."""
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor("white")
fig.suptitle(
    "Retail Is All-In on AI. Bitcoin Is Being Ignored.\n"
    "This Is the Classic Pre-Rotation Setup.",
    fontsize=14, fontweight="bold",
)

# Left: SOXL AUM growth (approximate)
months = ["Jan\n2025", "Apr\n2025", "Jul\n2025", "Oct\n2025",
          "Jan\n2026", "Apr\n2026"]
soxl_aum = [4.2, 6.8, 11.2, 16.5, 22.3, 28.1]
ax1.fill_between(range(len(months)), soxl_aum, alpha=0.3, color="#f97316")
ax1.plot(range(len(months)), soxl_aum, color="#f97316", linewidth=2.5, marker="o")
ax1.set_xticks(range(len(months)))
ax1.set_xticklabels(months, fontsize=9)
ax1.set_title("SOXL (3x Semi ETF) AUM ($B)\nRetail Piling In: +996% Stock Price, AUM Following",
              fontsize=11, fontweight="bold")
ax1.set_ylabel("AUM $ Billions", fontsize=10)
ax1.annotate("+$24B\nin 15 months", xy=(4, 22), xytext=(2, 18),
             fontsize=11, color="#f97316", fontweight="bold",
             arrowprops=dict(arrowstyle="->", color="#f97316"))
ax1.set_facecolor("white")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.grid(axis="y", alpha=0.15)

# Right: Call vs Put volume composition
call_pct = [42, 44, 46, 49, 52, 55, 58, 60]
put_pct = [44, 43, 41, 39, 37, 34, 31, 28]
quarters2 = ["Q1\n2025", "Q2\n2025", "Q3\n2025", "Q4\n2025",
             "Jan\n2026", "Feb\n2026", "Mar\n2026", "May\n2026"]
x2 = list(range(len(quarters2)))
ax2.fill_between(x2, call_pct, put_pct, alpha=0.25, color="#22c55e")
ax2.fill_between(x2, put_pct, [20] * len(x2), alpha=0.25, color="#ef4444")
ax2.plot(x2, call_pct, color="#22c55e", linewidth=2.5, marker="o",
         label="SPX Call % of Volume")
ax2.plot(x2, put_pct, color="#ef4444", linewidth=2.5, marker="s",
         label="SPX Put % of Volume")
ax2.set_xticks(x2)
ax2.set_xticklabels(quarters2, fontsize=8)
ax2.axhline(y=50, color="black", linestyle=":", alpha=0.4, linewidth=1)
ax2.text(7.05, 60.5, "ALL-TIME HIGH\nCALL DOMINANCE",
         fontsize=8, color="#22c55e", fontweight="bold")
ax2.set_title("SPX Call vs Put Volume (%)\n60% Are Calls — All-Time Record (Goldman Sachs)",
              fontsize=11, fontweight="bold")
ax2.set_ylabel("% of Total SPX Options Volume", fontsize=10)
ax2.legend(fontsize=9)
ax2.set_facecolor("white")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.grid(axis="y", alpha=0.15)

plt.tight_layout()
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-retail-danger.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Fear Chart 3 saved: {out}")
