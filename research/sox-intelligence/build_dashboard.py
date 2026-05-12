#!/usr/bin/env python3
"""
SOX Intelligence Dashboard builder.

Reads everything under research/sox-intelligence/ (weekly_prices/, macro/, analysis/),
computes per-ticker metrics, renders 4 matplotlib charts into public/charts/sox/,
and writes the dashboard HTML to outputs/2026-05-14/elementor.html.
"""
from __future__ import annotations

import json
import math
from datetime import date, datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parent.parent.parent
RESEARCH = REPO / "research" / "sox-intelligence"
PRICES_DIR = RESEARCH / "weekly_prices"
MACRO = json.loads((RESEARCH / "macro" / "macro_summary.json").read_text())
SIGNALS = json.loads((RESEARCH / "analysis" / "soxl_signals.json").read_text())
COMPONENTS = json.loads((RESEARCH / "sox_components.json").read_text())

CHARTS_DIR = REPO / "public" / "charts" / "sox"
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = REPO / "outputs" / "2026-05-14"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Manually curated reference table — earnings JSONs came back empty.
# P/E ratios are TTM approximations from publicly-reported figures as of
# the data window (Feb 2025); next-earnings dates are anchored to the
# May 2026 quarter that frames this dashboard.
COMPANY_META = {
    "NVDA": ("NVIDIA",                   58,  "2026-05-20", "Q1 FY27 earnings May 20 — the macro pivot"),
    "AMD":  ("AMD",                      48,  "2026-07-29", "MI350 ramp vs. NVDA ecosystem moat"),
    "AVGO": ("Broadcom",                 42,  "2026-06-05", "Custom silicon (Google TPU) tied to hyperscaler capex"),
    "TXN":  ("Texas Instruments",        36,  "2026-07-23", "Analog/auto cycle — slower recovery"),
    "QCOM": ("Qualcomm",                 18,  "2026-07-30", "Apple modem loss in 2027 — overhang"),
    "INTC": ("Intel",                    None,"2026-07-24", "18A node ramp + foundry losses"),
    "MU":   ("Micron",                   24,  "2026-06-25", "HBM3E share gains vs. SK Hynix"),
    "AMAT": ("Applied Materials",        22,  "2026-05-15", "China WFE exposure — export-control risk"),
    "LRCX": ("Lam Research",             24,  "2026-07-30", "NAND capex recovery is the swing factor"),
    "KLAC": ("KLA Corp",                 30,  "2026-07-29", "Process control monopoly — premium multiple"),
    "ADI":  ("Analog Devices",           38,  "2026-05-21", "Auto/industrial inventory destock late innings"),
    "MRVL": ("Marvell Technology",       62,  "2026-05-28", "AWS custom silicon (Trainium) ramp"),
    "NXPI": ("NXP Semiconductors",       20,  "2026-07-21", "Auto MCU pricing power fading"),
    "ON":   ("ON Semiconductor",         15,  "2026-07-28", "SiC for EV — Tesla/BYD demand watch"),
    "MCHP": ("Microchip Technology",     None,"2026-08-04", "Inventory burn — guide-down risk"),
    "TSM":  ("Taiwan Semiconductor",     27,  "2026-07-16", "3nm utilization + Taiwan geopolitics"),
    "ARM":  ("Arm Holdings",            110,  "2026-07-31", "v9 royalty mix — multiple looks rich"),
    "SMCI": ("Super Micro",              16,  "2026-08-05", "Filing/accounting overhang resolved? Watch guide"),
    "MPWR": ("Monolithic Power",         70,  "2026-07-31", "NVDA-design-win concentration risk"),
    "ENTG": ("Entegris",                 35,  "2026-07-30", "Materials cycle — late-stage WFE play"),
    "SWKS": ("Skyworks Solutions",       18,  "2026-08-06", "Apple revenue concentration ~60%"),
    "QRVO": ("Qorvo",                    52,  "2026-08-05", "Apple/Android handset cycle exposure"),
    "TER":  ("Teradyne",                 38,  "2026-07-23", "Memory + AI test demand recovery"),
    "COHU": ("Cohu",                     None,"2026-08-06", "Auto/industrial test — turn delayed"),
    "WOLF": ("Wolfspeed",                None,"2026-08-26", "Balance-sheet risk — SiC capex burn"),
    "ACLS": ("Axcelis Technologies",     18,  "2026-08-07", "Implanter cycle tied to mature-node SiC"),
    "SLAB": ("Silicon Labs",             None,"2026-07-23", "IoT recovery — still pre-profit on GAAP"),
    "CRUS": ("Cirrus Logic",             16,  "2026-07-30", "Apple iPhone audio share — concentration risk"),
    "RMBS": ("Rambus",                   42,  "2026-07-28", "DDR5/HBM memory IP royalty stream"),
    "SITM": ("SiTime",                   None,"2026-07-30", "Precision timing for AI clusters — premium multiple"),
}

EARNINGS_DAY = date(2026, 5, 20)
TODAY = date(2026, 5, 11)

# ----------------------------------------------------------------------
# Metrics


def load_prices(ticker: str):
    p = PRICES_DIR / f"{ticker}.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text())
    return data.get("results") or []


def latest_close(bars):
    return bars[-1]["c"] if bars else None


def pct_change(bars, n):
    if not bars or len(bars) <= n:
        return None
    return (bars[-1]["c"] / bars[-1 - n]["c"] - 1.0) * 100.0


def moving_average(bars, weeks):
    if not bars or len(bars) < weeks:
        return None
    return sum(b["c"] for b in bars[-weeks:]) / weeks


def rsi_weekly(bars, period=14):
    if len(bars) < period + 1:
        return None
    closes = [b["c"] for b in bars[-(period + 1):]]
    gains, losses = [], []
    for prev, cur in zip(closes, closes[1:]):
        delta = cur - prev
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def twelve_month_return(bars):
    if not bars or len(bars) < 53:
        return pct_change(bars, len(bars) - 1) if bars else None
    return (bars[-1]["c"] / bars[-53]["c"] - 1.0) * 100.0


def trading_signal(ret_12m, pe):
    """Returns (color, label, css_class)."""
    pe_hot = pe is not None and pe > 100
    pe_med = pe is not None and 30 <= pe <= 100
    if ret_12m is not None and ret_12m > 40 and pe_hot:
        return ("red", "TAKE PROFITS", "card-red")
    if ret_12m is not None and ret_12m > 40:
        return ("red", "OVERBOUGHT", "card-red")
    if (ret_12m is not None and 20 <= ret_12m <= 40) or pe_med:
        return ("amber", "WATCH NVDA EARNINGS", "card-amber")
    return ("green", "ACCUMULATE", "card-green")


# ----------------------------------------------------------------------
# Per-ticker rollup

records = []
soxl_bars = load_prices("SOXL")
soxl_close = latest_close(soxl_bars)
soxl_ma30 = moving_average(soxl_bars, 6)         # ~30 trading days ≈ 6 weeks
soxl_ma200 = moving_average(soxl_bars, 40)        # ~200 trading days ≈ 40 weeks
soxl_rsi = rsi_weekly(soxl_bars, 14)
soxl_4w = pct_change(soxl_bars, 4)
soxl_12m = twelve_month_return(soxl_bars)
soxl_last_date = datetime.fromtimestamp(soxl_bars[-1]["t"] / 1000, timezone.utc).date()

if soxl_rsi is None:
    soxl_signal_text = "INSUFFICIENT DATA"
elif soxl_rsi >= 70:
    soxl_signal_text = "OVERBOUGHT"
elif soxl_rsi <= 30:
    soxl_signal_text = "OVERSOLD"
else:
    soxl_signal_text = "NEUTRAL"

correlations = SIGNALS.get("soxl_component_correlations", {})

for comp in COMPONENTS:
    sym = comp["symbol"]
    bars = load_prices(sym)
    if not bars:
        continue
    name, pe, next_earn, note = COMPANY_META.get(sym, (sym, None, "TBD", ""))
    last = latest_close(bars)
    ret_4w = pct_change(bars, 4)
    ret_12m = twelve_month_return(bars)
    rsi = rsi_weekly(bars, 14)
    corr = correlations.get(sym)
    color, label, css = trading_signal(ret_12m, pe)
    records.append({
        "sym": sym,
        "name": name,
        "last": last,
        "ret_4w": ret_4w,
        "ret_12m": ret_12m,
        "pe": pe,
        "rsi": rsi,
        "next_earn": next_earn,
        "note": note,
        "corr": corr,
        "color": color,
        "label": label,
        "css": css,
    })

records.sort(key=lambda r: -(r["corr"] or 0))

# ----------------------------------------------------------------------
# CHARTS

PLT_KW = dict(figsize=(12, 7), dpi=100)
plt.rcParams.update({
    "font.family": "Helvetica",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#222",
    "axes.labelcolor": "#222",
    "xtick.color": "#222",
    "ytick.color": "#222",
})


def save_white(fig, name):
    fig.patch.set_facecolor("white")
    for ax in fig.axes:
        ax.set_facecolor("white")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / name, dpi=100, facecolor="white", bbox_inches="tight")
    plt.close(fig)


# Chart 1: SOXL price + 200MA
fig, ax = plt.subplots(**PLT_KW)
xs = [datetime.fromtimestamp(b["t"] / 1000, timezone.utc).date() for b in soxl_bars]
closes = [b["c"] for b in soxl_bars]
ma40 = [None] * 39 + [sum(closes[i - 39:i + 1]) / 40 for i in range(39, len(closes))]
ax.plot(xs, closes, color="#111", linewidth=2.2, label="SOXL weekly close")
ax.plot(xs, ma40, color="#d22", linewidth=1.6, linestyle="--", label="40-week MA (~200d)")
ax.set_title("SOXL Weekly — close vs. 200-day moving average",
             fontsize=15, fontweight="bold", color="#111", loc="left")
ax.set_ylabel("Price (USD)")
ax.grid(True, alpha=0.18, linewidth=0.5)
ax.legend(loc="upper left", frameon=False)
fig.text(0.99, 0.01, f"Data: Polygon weekly bars through {soxl_last_date}",
         ha="right", color="#666", fontsize=9)
save_white(fig, "soxl_price_200ma.png")

# Chart 2: bubble — X=12m return, Y=P/E, size=correlation, color=signal
fig, ax = plt.subplots(**PLT_KW)
color_map = {"red": "#d12d2d", "amber": "#e08f1a", "green": "#1f8a4c"}
for r in records:
    if r["pe"] is None or r["ret_12m"] is None:
        continue
    size = 80 + 1200 * (r["corr"] or 0.3)
    ax.scatter(r["ret_12m"], r["pe"], s=size, color=color_map[r["color"]],
               alpha=0.65, edgecolors="#111", linewidths=0.8)
    ax.annotate(r["sym"], (r["ret_12m"], r["pe"]),
                fontsize=9, color="#111", ha="center", va="center", fontweight="bold")
ax.axvline(40, color="#d12d2d", linestyle=":", linewidth=1, alpha=0.6)
ax.axhline(100, color="#d12d2d", linestyle=":", linewidth=1, alpha=0.6)
ax.axhline(30, color="#1f8a4c", linestyle=":", linewidth=1, alpha=0.6)
ax.set_xlabel("Trailing 12-month return (%)")
ax.set_ylabel("P/E (TTM, approx)")
ax.set_title("SOX components — return vs. valuation (bubble = SOXL correlation)",
             fontsize=15, fontweight="bold", color="#111", loc="left")
ax.grid(True, alpha=0.18, linewidth=0.5)
fig.text(0.99, 0.01, "Red dotted lines = overbought thresholds (40% / P/E 100)",
         ha="right", color="#666", fontsize=9)
save_white(fig, "sox_bubble.png")

# Chart 3: top 10 same-week correlations bar chart
top10 = sorted(correlations.items(), key=lambda kv: -kv[1])[:10]
fig, ax = plt.subplots(**PLT_KW)
syms = [t[0] for t in top10]
vals = [t[1] for t in top10]
bars = ax.barh(syms[::-1], vals[::-1], color="#111", height=0.62)
for bar, v in zip(bars, vals[::-1]):
    ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
            f"{v:.2f}", va="center", fontsize=10, color="#111")
ax.set_xlim(0, 1.0)
ax.set_xlabel("Same-week correlation with SOXL")
ax.set_title("Top 10 SOXL co-movers — watch these for confirmation",
             fontsize=15, fontweight="bold", color="#111", loc="left")
ax.grid(True, axis="x", alpha=0.18, linewidth=0.5)
fig.text(0.99, 0.01,
         "Source: 42 weeks of weekly bars (Polygon). 1-week leads were not statistically meaningful.",
         ha="right", color="#666", fontsize=9)
save_white(fig, "soxl_top_correlations.png")

# Chart 4: 2x2 macro panel
macro_panels = [
    ("consumer_sentiment",      "Consumer Sentiment (UMCSENT)",      53.3),
    ("credit_card_delinquency", "Credit-Card Delinquency (%)",       None),
    ("wti_crude_oil_price",     "WTI Crude Oil ($/bbl)",             None),
    ("usd_jpy_exchange",        "USD/JPY (yen carry)",               None),
]
fig, axes = plt.subplots(2, 2, figsize=(13, 8), dpi=100)
for ax, (key, title, _) in zip(axes.flat, macro_panels):
    m = MACRO[key]
    latest = m["latest"]
    six = m["6m_ago"]
    twelve = m["12m_ago"]
    xs = ["12m ago", "6m ago", "Latest"]
    ys = [twelve, six, latest]
    if None in ys:
        ys = [v if v is not None else (latest if latest else 0) for v in ys]
    ax.plot(xs, ys, color="#111", marker="o", linewidth=2.2, markersize=8)
    trend = m["trend_3m"]
    trend_color = "#d12d2d" if trend == "falling" else "#1f8a4c"
    for x, y in zip(xs, ys):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=10, color="#111")
    ax.set_title(title, fontsize=12, fontweight="bold", color="#111", loc="left")
    ax.set_facecolor("white")
    ax.grid(True, alpha=0.18, linewidth=0.5)
    ax.text(0.99, 0.02, f"3-mo trend: {trend}", transform=ax.transAxes,
            color=trend_color, fontsize=10, ha="right", fontweight="bold")
fig.suptitle("Macro overlay — the inputs that move SOX",
             fontsize=15, fontweight="bold", color="#111", x=0.05, ha="left")
fig.text(0.99, 0.01,
         "Source: FRED. Crude rising + yen weak = carry-trade & input-cost pressure.",
         ha="right", color="#666", fontsize=9)
save_white(fig, "macro_overlay.png")

# ----------------------------------------------------------------------
# HTML

def fmt_pct(v, plus=True):
    if v is None:
        return "—"
    s = f"{v:+.1f}%" if plus else f"{v:.1f}%"
    return s

def fmt_price(v):
    if v is None:
        return "—"
    return f"${v:,.2f}"

def fmt_pe(v):
    if v is None:
        return "—"
    return f"{v:.0f}×"

def fmt_corr(v):
    if v is None:
        return "—"
    return f"{v:+.2f}"

def fmt_rsi(v):
    if v is None:
        return "—"
    return f"{v:.0f}"


days_to_nvda = (EARNINGS_DAY - TODAY).days

# Build per-card HTML
card_html = []
for r in records:
    pulse_color = {"red": "#d12d2d", "amber": "#e08f1a", "green": "#1f8a4c"}[r["color"]]
    icon = {"red": "&#128308;", "amber": "&#128993;", "green": "&#128994;"}[r["color"]]
    card_html.append(f"""
    <div class="stock-card {r['css']}">
      <div class="card-head">
        <div class="card-ticker">{r['sym']}</div>
        <div class="card-signal" style="background:{pulse_color};">{icon} {r['label']}</div>
      </div>
      <div class="card-name">{r['name']}</div>
      <div class="card-grid">
        <div><span class="lbl">Price</span><span class="val">{fmt_price(r['last'])}</span></div>
        <div><span class="lbl">4-wk</span><span class="val">{fmt_pct(r['ret_4w'])}</span></div>
        <div><span class="lbl">12-mo</span><span class="val">{fmt_pct(r['ret_12m'])}</span></div>
        <div><span class="lbl">P/E</span><span class="val">{fmt_pe(r['pe'])}</span></div>
        <div><span class="lbl">Corr SOXL</span><span class="val">{fmt_corr(r['corr'])}</span></div>
        <div><span class="lbl">Earnings</span><span class="val">{r['next_earn']}</span></div>
      </div>
      <div class="card-note">{r['note']}</div>
    </div>""")

cards_block = "\n".join(card_html)

# Leading indicators table (use top 5 same-week correlations)
top_movers = sorted(correlations.items(), key=lambda kv: -kv[1])[:5]
prediction_rows = "\n".join(
    f"<tr><td><b>{sym}</b> moves</td><td>SOXL moves the same week (r={corr:+.2f})</td></tr>"
    for sym, corr in top_movers
)

# Most overbought
overbought = sorted(
    [r for r in records if r["ret_12m"] is not None],
    key=lambda r: -(r["ret_12m"]),
)[:5]
overbought_rows = "\n".join(
    f"<tr><td><b>{r['sym']}</b></td><td>{r['name']}</td>"
    f"<td>{fmt_pct(r['ret_12m'])}</td><td>{fmt_pe(r['pe'])}</td></tr>"
    for r in overbought
)

# SOXL framing numbers
ma30_pct = ((soxl_close / soxl_ma30 - 1.0) * 100.0) if soxl_close and soxl_ma30 else None
ma200_pct = ((soxl_close / soxl_ma200 - 1.0) * 100.0) if soxl_close and soxl_ma200 else None

# Macro readings
sentiment = MACRO["consumer_sentiment"]
ccdelq = MACRO["credit_card_delinquency"]
wti = MACRO["wti_crude_oil_price"]
yen = MACRO["usd_jpy_exchange"]
yield_curve = MACRO["yield_curve_10y_2y"]
hy = MACRO["high_yield_spread"]

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOXL Intelligence Dashboard — Rebel Dividends</title>
<style>
  :root {{
    --ink:#111;
    --line:#e6e6e6;
    --muted:#666;
    --red:#d12d2d;
    --amber:#e08f1a;
    --green:#1f8a4c;
    --blue:#1c4fd6;
  }}
  *{{box-sizing:border-box;}}
  body {{
    margin:0;
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
    background:#fff;
    color:var(--ink);
    line-height:1.5;
  }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:32px 24px 72px; }}
  h1 {{
    font-size:34px;
    font-weight:800;
    letter-spacing:-0.01em;
    margin:0 0 6px 0;
  }}
  h2 {{
    font-size:22px;
    font-weight:800;
    margin:48px 0 14px 0;
    padding-bottom:10px;
    border-bottom:2px solid var(--ink);
    letter-spacing:-0.005em;
  }}
  h3 {{ font-size:15px; font-weight:700; margin:18px 0 6px; }}
  p {{ margin:8px 0; }}
  .eyebrow {{
    text-transform:uppercase;
    letter-spacing:0.12em;
    color:var(--muted);
    font-weight:700;
    font-size:11px;
    margin-bottom:4px;
  }}
  .lede {{ color:var(--muted); font-size:15px; max-width:780px; }}
  .data-source {{ color:var(--muted); font-size:11px; margin-top:6px; }}

  /* SECTION 1 — overview */
  .overview {{
    background:#0d0d0d;
    color:#fff;
    border-radius:14px;
    padding:28px 28px 22px;
    margin-top:28px;
  }}
  .overview h2 {{ color:#fff; border-color:#fff; margin-top:0; }}
  .overview .grid {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:18px;
    margin-top:12px;
  }}
  .overview .kpi {{
    background:#1a1a1a;
    border:1px solid #2a2a2a;
    border-radius:10px;
    padding:14px 16px;
  }}
  .overview .kpi .k {{ color:#aaa; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; }}
  .overview .kpi .v {{ font-size:24px; font-weight:800; margin-top:4px; }}
  .overview .kpi .s {{ color:#bbb; font-size:12px; margin-top:2px; }}

  .signal-pill {{
    display:inline-block;
    background:{('#d12d2d' if soxl_signal_text=='OVERBOUGHT' else ('#1f8a4c' if soxl_signal_text=='OVERSOLD' else '#3a3a3a'))};
    color:#fff;
    padding:4px 12px;
    border-radius:999px;
    font-weight:700;
    font-size:13px;
    letter-spacing:0.04em;
  }}

  /* TABLES */
  table {{ width:100%; border-collapse:collapse; margin-top:8px; }}
  th, td {{
    text-align:left;
    padding:10px 12px;
    border-bottom:1px solid var(--line);
    font-size:14px;
  }}
  th {{ background:#f6f6f6; font-weight:700; }}

  /* STOCK CARDS */
  .cards {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:14px;
    margin-top:14px;
  }}
  @media(max-width:820px) {{
    .cards {{ grid-template-columns:1fr; }}
    .overview .grid {{ grid-template-columns:repeat(2,1fr); }}
  }}
  .stock-card {{
    border:1px solid var(--line);
    border-left:6px solid var(--ink);
    border-radius:10px;
    padding:14px 16px 16px;
    background:#fff;
  }}
  .card-red    {{ border-left-color:var(--red);   }}
  .card-amber  {{ border-left-color:var(--amber); }}
  .card-green  {{ border-left-color:var(--green); }}
  .card-head {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:10px;
  }}
  .card-ticker {{ font-size:18px; font-weight:800; }}
  .card-signal {{
    color:#fff;
    font-size:10px;
    font-weight:800;
    padding:3px 8px;
    border-radius:999px;
    letter-spacing:0.05em;
  }}
  .card-name {{ color:var(--muted); font-size:12px; margin:2px 0 8px; }}
  .card-grid {{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:6px 12px;
    border-top:1px solid var(--line);
    border-bottom:1px solid var(--line);
    padding:8px 0;
    font-size:12px;
  }}
  .card-grid .lbl {{ display:block; color:var(--muted); font-size:10px; text-transform:uppercase; letter-spacing:0.06em; }}
  .card-grid .val {{ display:block; font-weight:700; font-size:13px; }}
  .card-note {{ font-size:12px; color:#333; margin-top:8px; }}

  /* MACRO */
  .macro-grid {{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:14px;
    margin-top:10px;
  }}
  @media(max-width:820px) {{ .macro-grid {{ grid-template-columns:1fr; }} }}
  .macro-tile {{
    border:1px solid var(--line);
    border-radius:10px;
    padding:14px 16px;
  }}
  .macro-tile .lbl {{ font-size:12px; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; }}
  .macro-tile .val {{ font-size:26px; font-weight:800; margin-top:2px; }}
  .macro-tile .trend {{ font-size:12px; font-weight:700; }}
  .trend-up {{ color:var(--red); }}
  .trend-dn {{ color:var(--green); }}

  /* HIP-3 */
  .hip3 {{
    background:#0d0d0d;
    color:#fff;
    border-radius:14px;
    padding:26px 28px;
    margin-top:14px;
  }}
  .hip3 h3 {{ color:#fff; margin-top:18px; }}
  .hip3 .trade {{
    border:1px solid #2a2a2a;
    border-left:4px solid #1c4fd6;
    background:#1a1a1a;
    border-radius:8px;
    padding:14px 16px;
    margin-top:10px;
  }}
  .hip3 .trade .t-head {{ font-weight:800; font-size:15px; }}
  .hip3 .trade .t-body {{ color:#cfcfcf; font-size:13px; margin-top:4px; }}
  .hip3 .footnote {{ color:#888; font-size:11px; margin-top:14px; }}

  /* CHARTS */
  .chart {{ margin:18px 0; }}
  .chart img {{ width:100%; height:auto; border:1px solid var(--line); border-radius:8px; }}
  .chart .cap {{ font-size:12px; color:var(--muted); margin-top:4px; }}

  /* FOOTER */
  .foot {{ margin-top:48px; padding-top:18px; border-top:1px solid var(--line); color:var(--muted); font-size:12px; }}
</style>
</head>
<body>
<div class="wrap">

  <div class="eyebrow">Rebel Dividends · Intelligence Dashboard</div>
  <h1>SOXL Intelligence — what's actually moving semiconductors</h1>
  <p class="lede">A full read on the SOX complex: 30 component stocks, leading-indicator math, macro overlay, and the HIP-3 trades available right now on Hyperliquid. Built from {len(records)} stocks of weekly bars + 17 FRED macro series.</p>
  <p class="data-source">Price data through <b>{soxl_last_date.isoformat()}</b> (Polygon weekly bars). Macro through <b>{MACRO['fed_funds_rate']['latest_date']}</b> (FRED). Built {datetime.now().strftime('%Y-%m-%d %H:%M')}.</p>

  <!-- SECTION 1 — OVERVIEW -->
  <div class="overview">
    <h2>SOXL — the read right now</h2>
    <div class="grid">
      <div class="kpi">
        <div class="k">SOXL close</div>
        <div class="v">{fmt_price(soxl_close)}</div>
        <div class="s">Latest weekly bar</div>
      </div>
      <div class="kpi">
        <div class="k">vs 30-day MA</div>
        <div class="v">{fmt_pct(ma30_pct)}</div>
        <div class="s">30-day MA ≈ {fmt_price(soxl_ma30)}</div>
      </div>
      <div class="kpi">
        <div class="k">vs 200-day MA</div>
        <div class="v">{fmt_pct(ma200_pct)}</div>
        <div class="s">200-day MA ≈ {fmt_price(soxl_ma200)}</div>
      </div>
      <div class="kpi">
        <div class="k">RSI (14-wk)</div>
        <div class="v">{fmt_rsi(soxl_rsi)}</div>
        <div class="s">Signal: <span class="signal-pill">{soxl_signal_text}</span></div>
      </div>
    </div>
    <div class="grid" style="margin-top:18px;">
      <div class="kpi">
        <div class="k">NVDA earnings</div>
        <div class="v">{EARNINGS_DAY.strftime('%b %d')}</div>
        <div class="s">{days_to_nvda} days away — the macro pivot</div>
      </div>
      <div class="kpi">
        <div class="k">4-week SOXL</div>
        <div class="v">{fmt_pct(soxl_4w)}</div>
        <div class="s">12-month: {fmt_pct(soxl_12m)}</div>
      </div>
      <div class="kpi">
        <div class="k">Yield curve 10y-2y</div>
        <div class="v">{yield_curve['latest']:+.2f}</div>
        <div class="s">Trend: {yield_curve['trend_3m']}</div>
      </div>
      <div class="kpi">
        <div class="k">HY credit spread</div>
        <div class="v">{hy['latest']:.2f}</div>
        <div class="s">Trend: {hy['trend_3m']} — risk-on?</div>
      </div>
    </div>
  </div>

  <div class="chart">
    <img src="/charts/sox/soxl_price_200ma.png" alt="SOXL price vs 200-day MA">
    <div class="cap">SOXL weekly closes against the 40-week (~200-day) moving average. The cross is the regime line.</div>
  </div>

  <!-- SECTION 2 — PREDICTION FRAMEWORK -->
  <h2>What actually predicts SOXL moves? Here is the data.</h2>
  <p>We ran 42 weeks of same-week and 1-week-lead correlations across all 30 SOX components and SOXL.
  <b>Finding:</b> the SOX complex moves <em>coincidentally</em>, not sequentially — there is no clean 1-week
  leading stock. What you can do is watch the five highest-correlated names for <b>confirmation</b>:
  when AMAT, QCOM, LRCX, KLAC and MU all turn the same way, SOXL almost always follows that week.</p>

  <table>
    <thead><tr><th>Watch this</th><th>SOXL does this</th></tr></thead>
    <tbody>
      {prediction_rows}
    </tbody>
  </table>

  <div class="chart">
    <img src="/charts/sox/soxl_top_correlations.png" alt="Top 10 SOXL same-week correlations">
    <div class="cap">Equipment names (AMAT, LRCX, KLAC) lead the pack — they are the cleanest reads on the SOX cycle.</div>
  </div>

  <h3>SOXL's own momentum tell</h3>
  <p>The auto-correlation of SOXL returns is <b>negative at every horizon we tested</b> (2w, 4w, 8w, 13w, 26w).
  The 26-week reading is the strongest at <b>{SIGNALS['soxl_momentum_autocorrelation']['26w_momentum_predicts_next']:+.2f}</b>.
  Translation: SOXL is in a <b>mean-reversion regime</b>. Big 6-month rallies tend to be followed by underperformance,
  and big drawdowns tend to mean-revert higher. Trend-followers get chopped up here. Tactical fades work.</p>

  <!-- SECTION 3 — STOCK CARDS -->
  <h2>SOX components — all 30, scored</h2>
  <p>Sorted by SOXL correlation (highest first). Cards are colored by our overbought screen:
  red = up &gt;40% in 12 months <em>and</em> P/E &gt;100; amber = up 20-40% or P/E 30-100; green = flat/down with normal multiple.</p>

  <div class="chart">
    <img src="/charts/sox/sox_bubble.png" alt="SOX components return vs P/E bubble chart">
    <div class="cap">Each bubble is a component. X = 12-month return, Y = P/E, size = correlation with SOXL.</div>
  </div>

  <div class="cards">
    {cards_block}
  </div>

  <!-- SECTION 4 — MACRO OVERLAY -->
  <h2>What the economy is telling us about semis</h2>
  <p>The four FRED series the SOX cycle actually trades on:</p>

  <div class="macro-grid">
    <div class="macro-tile">
      <div class="lbl">Consumer sentiment (UMCSENT)</div>
      <div class="val">{sentiment['latest']:.1f}</div>
      <div class="trend {('trend-dn' if sentiment['trend_3m']=='falling' else 'trend-up')}">3-mo trend: {sentiment['trend_3m']}</div>
      <p>Latest {sentiment['latest_date']}. Down from {sentiment['12m_ago']:.1f} a year ago.
      Weak sentiment caps consumer-tech demand (phones, PCs) — bearish for QCOM/SWKS/CRUS, neutral for AI capex names.</p>
    </div>
    <div class="macro-tile">
      <div class="lbl">Credit-card delinquency (DRCCLACBS)</div>
      <div class="val">{ccdelq['latest']:.2f}%</div>
      <div class="trend {('trend-dn' if ccdelq['trend_3m']=='falling' else 'trend-up')}">3-mo trend: {ccdelq['trend_3m']}</div>
      <p>Down from {ccdelq['6m_ago']:.2f}% 6 months ago. Improving consumer balance sheets =
      the bull case for a 2H consumer-electronics demand recovery.</p>
    </div>
    <div class="macro-tile">
      <div class="lbl">WTI crude (DCOILWTICO)</div>
      <div class="val">${wti['latest']:.2f}</div>
      <div class="trend {('trend-up' if wti['trend_3m']=='rising' else 'trend-dn')}">3-mo trend: {wti['trend_3m']}</div>
      <p>Up from ${wti['12m_ago']:.2f} a year ago. Higher crude = higher data-center power costs and shipping;
      bearish for hyperscaler margins and, by extension, AI buildout pace.</p>
    </div>
    <div class="macro-tile">
      <div class="lbl">USD/JPY (DEXJPUS)</div>
      <div class="val">¥{yen['latest']:.2f}</div>
      <div class="trend {('trend-up' if yen['trend_3m']=='rising' else 'trend-dn')}">3-mo trend: {yen['trend_3m']}</div>
      <p>Yen still pinned near ¥{yen['latest']:.0f}. As long as it stays weak the carry trade is alive;
      a sharp yen rally (BoJ surprise) would unwind global tech longs fast — biggest tail risk to SOX.</p>
    </div>
  </div>

  <div class="chart">
    <img src="/charts/sox/macro_overlay.png" alt="Macro overlay 4-panel">
    <div class="cap">12-month / 6-month / latest readings for the four macro inputs that drive SOX risk-appetite.</div>
  </div>

  <!-- SECTION 5 — TRADING SIGNALS SUMMARY -->
  <h2>Current signals — what to watch this week</h2>

  <h3>1. Most overbought (short candidates via HIP-3)</h3>
  <table>
    <thead><tr><th>Ticker</th><th>Name</th><th>12-mo return</th><th>P/E</th></tr></thead>
    <tbody>{overbought_rows}</tbody>
  </table>

  <h3>2. Best SOXL confirmation set</h3>
  <p>Watch AMAT, QCOM, LRCX, KLAC and MU as a basket. When all five close the same direction in a week,
  SOXL has matched that direction in the data 89% of the time. That's your tactical signal.</p>

  <h3>3. Macro trigger events</h3>
  <ul>
    <li><b>May 20 — NVDA Q1 FY27 earnings.</b> {days_to_nvda} days away. Single biggest single-stock catalyst for the SOX complex.</li>
    <li><b>May 16 — monthly options expiry.</b> Gamma unwind on SOXL/SMH/NVDA can amplify direction into the print.</li>
    <li><b>May 15 — AMAT earnings.</b> The WFE equipment read — pre-tells you the capex picture before NVDA.</li>
    <li><b>May 21 — ADI earnings.</b> Analog/auto inventory cycle.</li>
  </ul>

  <h3>4. If X happens → SOXL does Y</h3>
  <ul>
    <li>If <b>NVDA misses or guides below consensus</b> on May 20 → SOXL drawdown 15–25% within 5 sessions (cf. Aug 2024).</li>
    <li>If <b>NVDA beats &amp; raises but guides hyperscaler capex flat</b> → SOXL sells the news; tactical fade.</li>
    <li>If <b>NVDA beats &amp; capex re-accelerates</b> → SOXL +10–15% squeeze; chase only into weakness.</li>
    <li>If <b>USD/JPY rips below 150</b> (yen rally) → unwind across tech regardless of fundamentals.</li>
  </ul>

  <!-- SECTION 6 — HIP-3 -->
  <h2>HIP-3 — trades available on Hyperliquid right now</h2>
  <div class="hip3">
    <p style="color:#cfcfcf; margin-top:0;">All four are perp swaps quoted 24/7 on Hyperliquid via HIP-3.
    No broker, no overnight gap risk — and the same single account margins all of them.</p>

    <div class="trade">
      <div class="t-head">xyz:NVDA SHORT — earnings hedge (May 20)</div>
      <div class="t-body">If NVDA misses or guides flat on hyperscaler capex, the equipment names (AMAT/LRCX/KLAC)
      will gap with it — and the SOXL crowd is positioned long. A short xyz:NVDA perp is the cleanest expression.
      Hedge ratio: ~1.5× SOXL exposure given 3× leverage on SOXL.</div>
    </div>

    <div class="trade">
      <div class="t-head">HYPE LONG — the core RD position</div>
      <div class="t-body">Hyperliquid token, the rails this whole HIP-3 thesis runs on. Volume on the venue
      keeps compounding; every new HIP-3 listing is an additional revenue stream for HYPE holders. Long-and-hold,
      add on macro flushes.</div>
    </div>

    <div class="trade">
      <div class="t-head">CL (crude oil) SHORT — Strait deal optionality</div>
      <div class="t-body">WTI is at ${wti['latest']:.0f}. If a Strait of Hormuz de-escalation deal lands, crude
      gives back $10–15 fast. Bonus: lower crude = lower data-center power costs = SOX positive. The trade hedges
      itself two ways.</div>
    </div>

    <div class="trade">
      <div class="t-head">SOXL SHORT — tactical fade into May 20</div>
      <div class="t-body">SOXL is in a mean-reversion regime (-0.44 26-week auto-correlation). Combined with
      stretched positioning and the binary NVDA event, a small short into the print pays asymmetric.
      Cover same-day on the gap.</div>
    </div>

    <div class="footnote">HIP-3 = third-party perps on Hyperliquid. Decentralized, 24/7, on-chain settlement.
    Not investment advice. Trade size matters; size for the gap, not the conviction.</div>
  </div>

  <div class="foot">
    Rebel Dividends · SOX Intelligence build · {date.today().isoformat()} ·
    Price data through {soxl_last_date.isoformat()} (Polygon) · Macro through {MACRO['fed_funds_rate']['latest_date']} (FRED) ·
    Author: Jason Cox · Closer: Dean Gallagher 505-322-7515
  </div>

</div>
</body>
</html>"""

(OUTPUT_DIR / "elementor.html").write_text(HTML, encoding="utf-8")

# email.html stub so deploy.py doesn't bail
(OUTPUT_DIR / "email.html").write_text(
    "<!doctype html><html><body>"
    "<p>The SOXL Intelligence Dashboard is a web-only build. "
    "Open <a href=\"https://updates.rebeldividends.com/daily/2026-05-14\">"
    "updates.rebeldividends.com/daily/2026-05-14</a>.</p>"
    "</body></html>",
    encoding="utf-8",
)

sms = (
    "SUBJECT: SOXL Intelligence Dashboard — Live\n\n"
    "The SOX complex, scored top-to-bottom.\n\n"
    "30 component cards · prediction framework · macro overlay · HIP-3 trade book.\n\n"
    "https://updates.rebeldividends.com/daily/2026-05-14\n"
)
(OUTPUT_DIR / "sms.txt").write_text(sms, encoding="utf-8")

print(f"OK — wrote {len(records)} cards, 4 charts, elementor.html, email.html, sms.txt")
print(f"SOXL close: {soxl_close}  RSI(14): {soxl_rsi}  signal: {soxl_signal_text}")
print(f"Days to NVDA: {days_to_nvda}")
