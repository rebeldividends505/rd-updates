#!/usr/bin/env python3
"""
BTC Suppression Debate — research 3 candidate explanations for why BTC is below ATH.
Outputs evidence + verdict to VERDICT.md.
"""
import os, json, time, sys
from pathlib import Path
import requests

PERP = os.environ["PERPLEXITY_API_KEY"]
POLY = os.environ["POLYGON_API_KEY"]
OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True, parents=True)


def perplexity_search(query: str, retries: int = 2) -> str:
    for attempt in range(retries + 1):
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {PERP}", "Content-Type": "application/json"},
                json={"model": "sonar-pro", "messages": [{"role": "user", "content": query}]},
                timeout=90,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            print(f"perplexity {r.status_code}: {r.text[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"perplexity error attempt {attempt}: {e}", file=sys.stderr)
        time.sleep(2 + attempt * 3)
    return ""


def poly_aggs(ticker: str, start: str, end: str, span: str = "week") -> list[dict]:
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{span}/{start}/{end}"
        f"?apiKey={POLY}&limit=5000&adjusted=true"
    )
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        print(f"polygon {ticker} {r.status_code}: {r.text[:200]}", file=sys.stderr)
        return []
    return r.json().get("results", []) or []


def fmt_date(ts_ms: int) -> str:
    import datetime as dt
    return dt.datetime.utcfromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d")


def summarize_series(name: str, bars: list[dict]) -> dict:
    """Return key stats: peak, trough, peak date, trough date, drawdown, current."""
    if not bars:
        return {"name": name, "error": "no data"}
    closes = [(b["t"], b["c"]) for b in bars]
    peak_t, peak_v = max(closes, key=lambda x: x[1])
    trough_t, trough_v = min(closes, key=lambda x: x[1])
    cur_t, cur_v = closes[-1]
    first_t, first_v = closes[0]
    return {
        "name": name,
        "first_date": fmt_date(first_t),
        "first": round(first_v, 2),
        "peak_date": fmt_date(peak_t),
        "peak": round(peak_v, 2),
        "trough_date": fmt_date(trough_t),
        "trough": round(trough_v, 2),
        "current_date": fmt_date(cur_t),
        "current": round(cur_v, 2),
        "drawdown_from_peak_pct": round((cur_v / peak_v - 1) * 100, 2),
        "ytd_or_period_pct": round((cur_v / first_v - 1) * 100, 2),
        "n_bars": len(bars),
    }


def find_largest_weekly_drops(bars: list[dict], n: int = 5) -> list[dict]:
    drops = []
    for i in range(1, len(bars)):
        prev = bars[i - 1]["c"]
        cur = bars[i]["c"]
        pct = (cur / prev - 1) * 100
        drops.append({"week_end": fmt_date(bars[i]["t"]), "close": round(cur, 2), "pct": round(pct, 2)})
    drops.sort(key=lambda x: x["pct"])
    return drops[:n]


print("=== Fetching Polygon price data ===")
start, end = "2024-01-01", "2026-05-11"
btc_bars = poly_aggs("X:BTCUSD", start, end, "week")
print(f"BTC weekly bars: {len(btc_bars)}")
qqq_bars = poly_aggs("QQQ", start, end, "week")
print(f"QQQ weekly bars: {len(qqq_bars)}")
oil_bars = poly_aggs("USO", start, end, "week")
print(f"USO weekly bars: {len(oil_bars)}")
jpy_bars = poly_aggs("C:USDJPY", start, end, "week")
print(f"USDJPY weekly bars: {len(jpy_bars)}")

btc_stats = summarize_series("BTC", btc_bars)
qqq_stats = summarize_series("QQQ", qqq_bars)
oil_stats = summarize_series("USO (oil ETF)", oil_bars)
jpy_stats = summarize_series("USDJPY", jpy_bars)

btc_drops = find_largest_weekly_drops(btc_bars, 6)
print("Largest BTC weekly drops:", json.dumps(btc_drops, indent=2))

# Build daily series for correlation around Oct 2025
def daily(ticker, s, e):
    return poly_aggs(ticker, s, e, "day")

btc_daily = daily("X:BTCUSD", "2025-08-01", "2025-12-31")
jpy_daily = daily("C:USDJPY", "2025-08-01", "2025-12-31")
print(f"BTC daily Aug-Dec 2025: {len(btc_daily)}")
print(f"USDJPY daily Aug-Dec 2025: {len(jpy_daily)}")

# Find specific Oct 2025 BTC moves
oct_btc = [b for b in btc_daily if "2025-10" in fmt_date(b["t"])]
nov_btc = [b for b in btc_daily if "2025-11" in fmt_date(b["t"])]
if oct_btc:
    o_start = oct_btc[0]["c"]
    o_low = min(b["c"] for b in oct_btc)
    o_low_date = fmt_date(next(b["t"] for b in oct_btc if b["c"] == o_low))
    o_end = oct_btc[-1]["c"]
    oct_summary = {
        "oct_start_close": round(o_start, 2),
        "oct_low_close": round(o_low, 2),
        "oct_low_date": o_low_date,
        "oct_end_close": round(o_end, 2),
        "oct_drawdown_pct": round((o_low / o_start - 1) * 100, 2),
    }
else:
    oct_summary = {}
print("Oct 2025 BTC:", json.dumps(oct_summary, indent=2))

# Simple Pearson correlation between BTC and USDJPY daily closes Aug-Dec 2025
def correl(a, b):
    n = min(len(a), len(b))
    if n < 3:
        return None
    xs = [x["c"] for x in a[:n]]
    ys = [y["c"] for y in b[:n]]
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)

btc_jpy_corr = correl(btc_daily, jpy_daily)
print(f"BTC vs USDJPY daily correlation Aug-Dec 2025: {btc_jpy_corr}")

# Now also pull a longer correlation: BTC vs oil and BTC vs QQQ across the full period
btc_daily_full = daily("X:BTCUSD", "2024-01-01", "2026-05-11")
uso_daily_full = daily("USO", "2024-01-01", "2026-05-11")
qqq_daily_full = daily("QQQ", "2024-01-01", "2026-05-11")
print(f"BTC daily full: {len(btc_daily_full)}, USO: {len(uso_daily_full)}, QQQ: {len(qqq_daily_full)}")

# Align by date string
def to_map(bars):
    return {fmt_date(b["t"]): b["c"] for b in bars}

btc_m = to_map(btc_daily_full)
uso_m = to_map(uso_daily_full)
qqq_m = to_map(qqq_daily_full)
shared_btc_uso = sorted(set(btc_m) & set(uso_m))
shared_btc_qqq = sorted(set(btc_m) & set(qqq_m))

def corr_maps(dates, a, b):
    xs = [a[d] for d in dates]
    ys = [b[d] for d in dates]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)

# Use daily returns rather than levels for a more honest correlation
def returns(dates, m):
    out = []
    for i in range(1, len(dates)):
        out.append(m[dates[i]] / m[dates[i - 1]] - 1)
    return out

btc_r_uso = returns(shared_btc_uso, btc_m)
uso_r = returns(shared_btc_uso, uso_m)
btc_r_qqq = returns(shared_btc_qqq, btc_m)
qqq_r = returns(shared_btc_qqq, qqq_m)

def pearson(xs, ys):
    n = min(len(xs), len(ys))
    if n < 3: return None
    xs, ys = xs[:n], ys[:n]
    mx = sum(xs)/n; my = sum(ys)/n
    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
    dx = (sum((x-mx)**2 for x in xs))**0.5
    dy = (sum((y-my)**2 for y in ys))**0.5
    return num/(dx*dy) if dx and dy else None

corr_btc_oil = pearson(btc_r_uso, uso_r)
corr_btc_qqq = pearson(btc_r_qqq, qqq_r)
print(f"BTC vs Oil daily-return correlation 2024-2026: {corr_btc_oil}")
print(f"BTC vs QQQ daily-return correlation 2024-2026: {corr_btc_qqq}")

print("\n=== Querying Perplexity ===")
queries = {
    "A_oil": "What is the daily-return correlation between WTI crude oil prices and Bitcoin price from 2024 through 2026? Did Bitcoin sell off when oil spiked? Did Bitcoin rally when oil dropped? Quote specific data, percentages, and dates. Also: how has Fed policy been tracking with oil/inflation in 2025-2026, and is the Fed currently hawkish or cutting?",
    "B_yen": "What happened to Bitcoin in October 2025? Specifically: did the yen carry trade unwind cause a Bitcoin crash? How much did BTC fall, what were the dates, and what were the leveraged-position liquidation numbers? What did USD/JPY do in October 2025? How much in total carry trade unwound? Has BTC fully recovered since then or not?",
    "C_ai": "Is there evidence in 2025-2026 that institutional and retail capital rotated out of cryptocurrency and into AI stocks? Cite Bitcoin spot ETF flow data (IBIT, FBTC) for late 2025 and 2026, AI-related ETF inflows, and any survey or positioning data showing the rotation. Also: what is QQQ year-to-date in 2026 vs Bitcoin year-to-date in 2026?",
    "D_general": "As of May 2026, what is the consensus among market strategists for the single biggest reason Bitcoin is trading well below its all-time high? Cite specific analyst reports, fund managers, or sell-side notes from April-May 2026.",
}

evidence = {}
for k, q in queries.items():
    print(f"  -> {k}")
    evidence[k] = perplexity_search(q)
    time.sleep(1)

# Save raw evidence
(OUT / "evidence_raw.json").write_text(json.dumps(evidence, indent=2))
(OUT / "price_data.json").write_text(json.dumps({
    "btc_weekly": btc_stats,
    "qqq_weekly": qqq_stats,
    "uso_weekly": oil_stats,
    "usdjpy_weekly": jpy_stats,
    "btc_largest_weekly_drops": btc_drops,
    "oct_2025_btc_summary": oct_summary,
    "btc_usdjpy_daily_corr_aug_dec_2025": btc_jpy_corr,
    "btc_oil_daily_return_corr_2024_2026": corr_btc_oil,
    "btc_qqq_daily_return_corr_2024_2026": corr_btc_qqq,
}, indent=2))

print("\n=== Data fetched, evidence saved ===")
print(f"BTC peak: ${btc_stats['peak']} on {btc_stats['peak_date']}")
print(f"BTC current: ${btc_stats['current']} on {btc_stats['current_date']}")
print(f"BTC drawdown from peak: {btc_stats['drawdown_from_peak_pct']}%")
print(f"QQQ peak->current: ${qqq_stats['peak']} on {qqq_stats['peak_date']} -> ${qqq_stats['current']} ({qqq_stats['drawdown_from_peak_pct']}% from peak)")
print(f"USO (oil) peak->current: ${oil_stats['peak']} -> ${oil_stats['current']} ({oil_stats['drawdown_from_peak_pct']}% from peak)")
print(f"USDJPY: peak {jpy_stats['peak']} on {jpy_stats['peak_date']}, trough {jpy_stats['trough']} on {jpy_stats['trough_date']}, current {jpy_stats['current']}")
print(f"BTC-Oil daily return correlation: {corr_btc_oil}")
print(f"BTC-QQQ daily return correlation: {corr_btc_qqq}")
print(f"BTC-USDJPY level correlation Aug-Dec 2025: {btc_jpy_corr}")

print("\nDONE")
