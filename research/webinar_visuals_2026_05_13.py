"""Generate 5 visual webinar deck charts for Rebel Dividends Tuesday May 13, 2026."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT_DIR = "/Users/rebeldividends/rd-updates-site/public/charts/2026-05-13"


def visual1_rotation_infographic():
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.text(5, 9.5, "The Goldilocks Scenario", fontsize=20, fontweight="bold",
            ha="center", color="#000000")
    ax.text(5, 9.0, "This is what we expect. A rebalance — not a crash.", fontsize=13,
            ha="center", color="#374151")

    events = [
        ("May 14-15", "Trump-Xi Summit", "Technology concession risk\npressures AI stocks"),
        ("May 20", "NVDA Earnings", "Any guidance caution\ntriggers 10-15% sector drop"),
        ("June-July", "AI Stocks Cool 10-20%", "Not a crash — a profit-taking\nrebalance from overbought levels"),
        ("H2 2026", "Fed Cuts Rates", "Slower economy = Powell acts\nRate cuts = liquidity surge"),
    ]

    for i, (date, event, desc) in enumerate(events):
        y = 7.5 - i * 2
        rect = mpatches.FancyBboxPatch((0.3, y - 0.5), 4.0, 1.4,
            boxstyle="round,pad=0.1", facecolor="#fef3c7", edgecolor="#d97706", linewidth=2)
        ax.add_patch(rect)
        ax.text(0.6, y + 0.6, date, fontsize=9, color="#92400e", fontweight="bold")
        ax.text(0.6, y + 0.2, event, fontsize=11, color="#000000", fontweight="bold")
        ax.text(0.6, y - 0.2, desc, fontsize=8.5, color="#374151")
        if i < 3:
            ax.annotate("", xy=(2.3, y - 0.55), xytext=(2.3, y - 0.45),
                       arrowprops=dict(arrowstyle="->", color="#d97706", lw=2))

    ax.annotate("", xy=(5.5, 5.5), xytext=(4.4, 5.5),
               arrowprops=dict(arrowstyle="->", color="#22c55e", lw=3))
    ax.text(4.95, 5.7, "RESULT", fontsize=11, fontweight="bold", color="#22c55e", ha="center")

    outcomes = [
        ("BTC", "$82K → $124K+", "+51% (closes M2 gap)"),
        ("HYPE", "$41 → $60-90", "+47% to +120% (3-5x BTC)"),
        ("RD", "$0.00171 → $0.0027", "+58% base case"),
        ("Dividends", "$0.000016/share/week", "Paid every Monday while waiting"),
    ]

    ax.text(5.7, 8.3, "RD SHAREHOLDERS GET:", fontsize=13, fontweight="bold", color="#0a7c42")
    for i, (asset, target, gain) in enumerate(outcomes):
        y = 7.5 - i * 1.8
        rect = mpatches.FancyBboxPatch((5.6, y - 0.3), 4.0, 1.2,
            boxstyle="round,pad=0.1", facecolor="#f0fff4", edgecolor="#0a7c42", linewidth=2)
        ax.add_patch(rect)
        ax.text(5.8, y + 0.55, asset, fontsize=10, color="#0a7c42", fontweight="bold")
        ax.text(5.8, y + 0.2, target, fontsize=13, color="#000000", fontweight="bold")
        ax.text(5.8, y - 0.1, gain, fontsize=9, color="#374151")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/infographic-rotation-not-crash.png",
               dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Visual 1: Rotation infographic saved")


def visual2_ai_performance_table():
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")

    ax.text(6, 6.8, "AI/Semi Stocks vs Bitcoin Since BTC's All-Time High",
            fontsize=16, fontweight="bold", ha="center", color="#000000")
    ax.text(6, 6.4, "September 28, 2025 → May 11, 2026 (Polygon live data)",
            fontsize=11, ha="center", color="#666666")

    columns = ["Stock", "Category", "Since BTC Peak", "Verdict"]
    rows = [
        ["SOXL", "3x Semi ETF", "+462.5%", "EXTREME RISK"],
        ["AMD", "Semiconductor", "+184.5%", "Take Some Profits"],
        ["GOOGL", "Hyperscaler Ads", "+58.1%", "Watch Q2 Earnings"],
        ["AVGO", "AI Networking", "+27.5%", "Watch Q2 Earnings"],
        ["NVDA", "AI Chips", "+23.5%", "Earnings May 20"],
        ["MSFT", "Azure AI", "−18.6%", "Already Rolling"],
        ["META", "AI Ads", "−20.0%", "Already Rolling"],
        ["PLTR", "AI Software", "−23.6%", "Already Rolling"],
        ["─────", "─────────", "─────", "──────────────"],
        ["BTC", "Bitcoin", "−24.7%", "Did Its Homework"],
        ["HYPE", "Hyperliquid", "−31%", "Buy the Discount"],
        ["RD", "Rebel Dividends", "−24%", "107 Divs Paid"],
    ]

    colors_row = ["#fef2f2", "#fef2f2", "#fffbeb", "#fffbeb", "#fffbeb",
                  "#fee2e2", "#fee2e2", "#fee2e2", "#f9fafb",
                  "#f0fff4", "#f0fff4", "#f0fff4"]

    y_start = 5.8
    row_h = 0.48

    for j, col in enumerate(columns):
        x = [0.2, 2.5, 5.0, 7.5][j]
        ax.text(x, y_start, col, fontsize=11, fontweight="bold", color="#ffffff",
                bbox=dict(facecolor="#0a0a0a", edgecolor="#0a0a0a", pad=3, boxstyle="square"))

    for i, (row, bg) in enumerate(zip(rows, colors_row)):
        y = y_start - (i + 1) * row_h
        ax.axhspan(y - row_h / 2 + 0.05, y + row_h / 2, 0.0, 1.0,
                  facecolor=bg, alpha=0.6)
        green_verdicts = {"Did Its Homework", "Buy the Discount", "107 Divs Paid"}
        red_verdicts = {"EXTREME RISK", "Already Rolling"}
        for j, val in enumerate(row):
            x = [0.2, 2.5, 5.0, 7.5][j]
            if val in green_verdicts:
                color = "#15803d"
            elif val in red_verdicts:
                color = "#dc2626"
            else:
                color = "#000000"
            weight = "bold" if j == 2 or j == 3 else "normal"
            ax.text(x, y, val, fontsize=10, color=color, fontweight=weight, va="center")

    ax.set_xlim(0, 11.5)
    ax.set_ylim(-0.5, 7.2)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/table-ai-performance.png",
               dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Visual 2: Performance table saved")


def visual3_catalyst_timeline():
    fig, ax = plt.subplots(figsize=(13, 5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)

    ax.text(6.5, 5.6, "The Catalyst Calendar: Every Trigger Fires in the Next 9-90 Days",
            fontsize=14, fontweight="bold", ha="center", color="#000000")

    ax.plot([0.5, 12.5], [3, 3], color="#374151", linewidth=3, zorder=2)

    catalysts = [
        (1.0, "Trump-Xi\nSummit", "May 14-15", "#ef4444", "TOMORROW"),
        (2.5, "Options\nExpiry", "May 16", "#f97316", "4 DAYS"),
        (4.0, "NVDA\nEarnings", "May 20", "#dc2626", "9 DAYS"),
        (6.5, "Sell in May\nSeason Starts", "May 15→", "#7c3aed", "ENTERING NOW"),
        (9.5, "Google + Meta\nAd Revenue Q2", "Late July", "#2563eb", "60 DAYS"),
        (12.0, "Fed Decision\n+ NVDA Q2", "Late July/Aug", "#0a7c42", "90 DAYS"),
    ]

    for x, label, date, color, urgency in catalysts:
        ax.plot(x, 3, "o", markersize=18, color=color, zorder=3)
        ax.plot(x, 3, "o", markersize=12, color="white", zorder=4)
        ax.plot(x, 3, "o", markersize=8, color=color, zorder=5)
        ax.text(x, 4.2, label, fontsize=9, ha="center", color="#000000", fontweight="bold",
                multialignment="center")
        ax.text(x, 1.8, date, fontsize=8, ha="center", color=color, fontweight="bold")
        ax.text(x, 1.2, urgency, fontsize=7.5, ha="center", color=color,
                bbox=dict(facecolor=color + "22", edgecolor=color, pad=2, boxstyle="round"))

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6)
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/timeline-catalysts.png",
               dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Visual 3: Timeline saved")


def visual4_rd_math_infographic():
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)

    ax.text(6, 6.7, "The $10,000 Question: What Does RD Look Like?",
            fontsize=16, fontweight="bold", ha="center", color="#000000")
    ax.text(6, 6.2, "$10,000 invested today at $0.00171 = 5,847,953 shares",
            fontsize=12, ha="center", color="#374151")

    scenarios = [
        ("BASE CASE", "HYPE: $60", "90 days", "$0.00271", "$15,856", "+$1,217", "$17,073", "#0a7c42"),
        ("MID CASE", "HYPE: $120", "12 months", "$0.00541", "$31,637", "+$4,869", "$36,506", "#2563eb"),
        ("BULL CASE", "HYPE: $180", "12 months", "$0.00811", "$47,426", "+$4,869", "$52,295", "#7c3aed"),
        ("MOON CASE", "HYPE: $360", "24 months", "$0.01622", "$94,862", "+$9,737", "$104,599", "#ef4444"),
    ]

    for i, (label, hype, timeline, rd, capital, divs, total, color) in enumerate(scenarios):
        x = 0.3 + i * 3.0
        rect = mpatches.FancyBboxPatch((x, 0.3), 2.7, 5.5,
            boxstyle="round,pad=0.15", facecolor=color + "11", edgecolor=color, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(x + 1.35, 5.6, label, fontsize=11, ha="center", color=color, fontweight="bold")
        ax.text(x + 1.35, 5.1, hype, fontsize=16, ha="center", color="#000000", fontweight="bold")
        ax.text(x + 1.35, 4.6, timeline, fontsize=9, ha="center", color="#666666")
        ax.plot([x + 0.2, x + 2.5], [4.3, 4.3], color=color, alpha=0.3, linewidth=1)
        ax.text(x + 1.35, 3.9, "RD Share", fontsize=8, ha="center", color="#666666")
        ax.text(x + 1.35, 3.5, rd, fontsize=12, ha="center", color=color, fontweight="bold")
        ax.text(x + 1.35, 3.0, "Capital Gain", fontsize=8, ha="center", color="#666666")
        ax.text(x + 1.35, 2.6, capital, fontsize=11, ha="center", color="#000000", fontweight="bold")
        ax.text(x + 1.35, 2.1, "Dividends", fontsize=8, ha="center", color="#666666")
        ax.text(x + 1.35, 1.7, divs, fontsize=10, ha="center", color="#0a7c42")
        ax.plot([x + 0.2, x + 2.5], [1.3, 1.3], color=color, alpha=0.5, linewidth=1.5)
        ax.text(x + 1.35, 0.9, "TOTAL", fontsize=9, ha="center", color="#666666")
        ax.text(x + 1.35, 0.4, total, fontsize=14, ha="center", color=color, fontweight="bold")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/infographic-rd-math.png",
               dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Visual 4: RD math infographic saved")


def visual5_capex_constraints():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor("white")
    fig.suptitle("Why AI Capex Must Slow Down:\nPhysical and Financial Constraints Building",
                fontsize=14, fontweight="bold", color="#000000")

    constraints = ["Power Grid Bottleneck\n(40GW needed,\n13GW/yr historical)",
                   "Chip Lead Times\n(H100/B200:\n6-9 months)",
                   "Water Shortage\n(1-5M gal/day\nper data center)",
                   "Permitting Delays\n(18-24 months\nper facility)",
                   "Skilled Labor\nShortage"]
    sizes = [35, 25, 15, 15, 10]
    colors_pie = ["#ef4444", "#f97316", "#eab308", "#3b82f6", "#8b5cf6"]
    wedges, texts, autotexts = ax1.pie(sizes, colors=colors_pie, autopct="%1.0f%%",
                                        startangle=90, pctdistance=0.75,
                                        wedgeprops=dict(linewidth=2, edgecolor="white"))
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")
        autotext.set_color("white")
    ax1.set_title("Physical Build Constraints\n(Even With Unlimited Cash)", fontsize=12, fontweight="bold")
    ax1.legend(wedges, constraints, loc="lower center", fontsize=7,
              bbox_to_anchor=(0.5, -0.45), ncol=1)

    companies = ["Microsoft", "Google", "Meta", "Amazon", "Oracle"]
    from_ocf = [45, 38, 52, 28, 14]
    from_debt = [22, 18, 30, 32, 31]

    x = np.arange(len(companies))
    ax2.bar(x - 0.2, from_ocf, 0.35, label="From Operating Cash Flow", color="#22c55e", alpha=0.85)
    ax2.bar(x + 0.2, from_debt, 0.35, label="From New Debt ($B)", color="#ef4444", alpha=0.85)
    ax2.set_xticks(x)
    ax2.set_xticklabels(companies, fontsize=10)
    ax2.set_ylabel("$ Billions", fontsize=10)
    ax2.set_title("How They Fund $700B Capex:\nCash vs. Borrowed Money (2026)", fontsize=12, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.set_facecolor("white")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.grid(axis="y", alpha=0.2)
    ax2.text(3.5, max(from_debt) * 1.05, "Debt issuance at\n7x historical avg",
            fontsize=9, color="#ef4444", fontweight="bold", ha="center")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/pie-capex-constraints.png",
               dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Visual 5: Capex constraints saved")


if __name__ == "__main__":
    visual1_rotation_infographic()
    visual2_ai_performance_table()
    visual3_catalyst_timeline()
    visual4_rd_math_infographic()
    visual5_capex_constraints()
    print("\nAll 5 visuals generated.")
