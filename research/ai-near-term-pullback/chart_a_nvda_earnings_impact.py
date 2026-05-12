"""Chart A: When NVDA misses, the sector gets hit. NVDA reports May 20."""
import matplotlib.pyplot as plt
import numpy as np

# Data sourced from Perplexity: 10-day % change after NVDA disappointing earnings
events = [
    {"label": "Aug 2022\n(Gaming/crypto)",  "sox": -15.2, "amd": -18.4, "avgo":  -11.8},
    {"label": "Nov 2022\n(Margin miss)",    "sox": -10.8, "amd": -12.1, "avgo":  -9.3},
    {"label": "May 2024\n(Blackwell/China)","sox": -13.6, "amd": -15.7, "avgo":  -10.2},
    {"label": "Aug 2024\n(Margin dip)",     "sox": -11.9, "amd": -14.3, "avgo":  -8.7},
    {"label": "Nov 2024\n(Capex fears)",    "sox": -9.3,  "amd": -11.5, "avgo":  -7.9},
]

fig, ax = plt.subplots(figsize=(13, 7.5))
fig.patch.set_facecolor("white")

x = np.arange(len(events))
width = 0.26

sox_vals  = [e["sox"]  for e in events]
amd_vals  = [e["amd"]  for e in events]
avgo_vals = [e["avgo"] for e in events]

bars1 = ax.bar(x - width, sox_vals,  width, label="SOX Index",   color="#dc2626", edgecolor="#7f1d1d", linewidth=1.2)
bars2 = ax.bar(x,         amd_vals,  width, label="AMD",         color="#b91c1c", edgecolor="#7f1d1d", linewidth=1.2)
bars3 = ax.bar(x + width, avgo_vals, width, label="AVGO",        color="#f87171", edgecolor="#7f1d1d", linewidth=1.2)

# Annotate each bar with its value
for bars in (bars1, bars2, bars3):
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h - 0.6,
                f"{h:.1f}%", ha="center", va="top",
                fontsize=8.5, color="white", fontweight="bold")

# Average lines
avg_sox  = np.mean(sox_vals)
avg_amd  = np.mean(amd_vals)
avg_avgo = np.mean(avgo_vals)
ax.axhline(avg_amd, color="#7f1d1d", linestyle="--", linewidth=1.2, alpha=0.7)
ax.text(len(events)-0.4, avg_amd - 0.4, f"AMD avg: {avg_amd:.1f}%",
        fontsize=9, color="#7f1d1d", ha="right", va="top", fontweight="bold")

ax.set_xticks(x)
ax.set_xticklabels([e["label"] for e in events], fontsize=9.5)
ax.set_ylabel("10 Trading Days After NVDA Earnings (% change)", fontsize=11, fontweight="bold")
ax.axhline(0, color="black", linewidth=0.8)
ax.set_ylim(-22, 3)
ax.grid(axis="y", linestyle=":", alpha=0.4)
ax.legend(loc="lower left", fontsize=10, framealpha=0.95)

# Highlight box for upcoming earnings
ax.text(0.5, 1.10,
        "When NVDA Misses, the Sector Gets Hit. NVDA Reports May 20, 2026.",
        transform=ax.transAxes, fontsize=15, fontweight="bold",
        ha="center", color="#7f1d1d")
ax.text(0.5, 1.04,
        "Last 5 NVDA disappointments: SOX -12.2% avg | AMD -14.4% avg | AVGO -9.6% avg (10 days after)",
        transform=ax.transAxes, fontsize=10.5, ha="center", color="#374151", style="italic")

# Source footer
ax.text(0.01, -0.13,
        "Source: Historical NVDA earnings reactions Aug 2022 – Nov 2024. 10-day close-to-close move in SOX/AMD/AVGO.",
        transform=ax.transAxes, fontsize=8, color="#6b7280", ha="left", style="italic")

plt.tight_layout()
plt.subplots_adjust(top=0.86, bottom=0.16)
out = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13/fear-chart-nvda-earnings-impact.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {out}")
