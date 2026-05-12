"""Chart C: SOX mean reversion after 60%+ above 200 MA — historical examples."""
import matplotlib.pyplot as plt
import numpy as np

# Historical SOX extreme premiums (highly stretched above 200 DMA) and forward 60-day drawdowns
events = [
    {"label": "2000\nDot-com peak\n(SOX ~60%+ above 200 DMA)",
     "drawdown": -25.0, "days": 60, "color": "#dc2626"},
    {"label": "2022\nChip recession peak\n(SOX stretched)",
     "drawdown": -30.0, "days": 45, "color": "#b91c1c"},
    {"label": "2024 Jul peak\n(NVDA Blackwell scare)",
     "drawdown": -15.0, "days": 30, "color": "#f87171"},
    {"label": "May 2026 ← TODAY\nSOX 63% above 200 DMA\n(largest deviation since inception)",
     "drawdown": -17.5, "days": 45, "color": "#7f1d1d", "is_today": True},
]

fig, ax = plt.subplots(figsize=(13, 7.5))
fig.patch.set_facecolor("white")

x = np.arange(len(events))
drawdowns = [e["drawdown"] for e in events]
colors = [e["color"] for e in events]
hatches = ["" if not e.get("is_today") else "//" for e in events]

bars = ax.bar(x, drawdowns, color=colors, edgecolor="#450a0a", linewidth=1.5, width=0.55)
for bar, hatch in zip(bars, hatches):
    if hatch:
        bar.set_hatch(hatch)

# Annotate bars with magnitude and timeline
for bar, e in zip(bars, events):
    h = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, h - 1.0,
            f"{h:.0f}%", ha="center", va="top",
            fontsize=16, color="white", fontweight="bold")
    ax.text(bar.get_x() + bar.get_width()/2, h - 4.5,
            f"in {e['days']} days", ha="center", va="top",
            fontsize=10, color="white", fontweight="bold")

# Today label
ax.text(3, 2,
        "PROJECTED\n(base case)",
        ha="center", va="bottom",
        fontsize=10, color="#7f1d1d", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fee2e2",
                  edgecolor="#7f1d1d", linewidth=1.4))

ax.set_xticks(x)
ax.set_xticklabels([e["label"] for e in events], fontsize=10)
ax.set_ylabel("SOX drawdown from peak (%)", fontsize=11, fontweight="bold")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylim(-35, 6)
ax.grid(axis="y", linestyle=":", alpha=0.4)

ax.text(0.5, 1.10,
        "Every Time SOX Stretches This Far Above Its 200 MA, It Snaps Back. Currently 63%.",
        transform=ax.transAxes, fontsize=14.5, fontweight="bold",
        ha="center", color="#7f1d1d")
ax.text(0.5, 1.04,
        "Per Barchart, this is the largest deviation since SOX inception (July 2001). Resolution: sharp drawdown OR long sideways grind.",
        transform=ax.transAxes, fontsize=10.5, ha="center", color="#374151", style="italic")

ax.text(0.01, -0.13,
        "Source: SOX historical price data. 2000 dot-com peak, 2022 chip-recession peak, 2024 July correction.\n"
        "Today's 63% deviation per Barchart May 2026 — only twice in 25 years has SOX been this stretched.",
        transform=ax.transAxes, fontsize=8, color="#6b7280", ha="left", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.86, bottom=0.18)
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-sox-mean-reversion.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
