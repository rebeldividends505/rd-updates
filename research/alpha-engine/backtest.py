#!/usr/bin/env python3
"""
RD Alpha Engine — Backtest 3 active strategies vs HYPE buy-and-hold.

Data sources:
  - Equities (QQQ, SOXL, SOXX, NVDA, MU, AMD, GLD, USO): yfinance (no lag)
  - Crypto (BTC, ETH, HYPE):                            CoinGecko (last 365d)

HYPE launched late 2024, so the honest backtest horizon is ~12 months —
that's what the strategies are evaluated over.

Writes:
  - research/alpha-engine/backtest-results.json
  - research/alpha-engine/raw-weekly.json
  - public/charts/alpha-engine/strategy-comparison.png
  - public/charts/alpha-engine/drawdown-comparison.png
  - public/charts/alpha-engine/signal-calendar.png
"""
from __future__ import annotations

import json
import os
import warnings
from datetime import datetime, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import yfinance as yf

REPO = Path("/Users/rebeldividends/rd-updates-site")
DATA_DIR = REPO / "research" / "alpha-engine"
CHART_DIR = REPO / "public" / "charts" / "alpha-engine"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

EQUITY_TICKERS = ["QQQ", "SOXL", "SOXX", "NVDA", "MU", "AMD", "GLD", "USO"]
CRYPTO_TICKERS = {"BTC": "bitcoin", "ETH": "ethereum", "HYPE": "hyperliquid"}

END = datetime.utcnow()
START = END - timedelta(days=370)


def fetch_equity_weekly(ticker: str) -> pd.DataFrame | None:
    try:
        df = yf.download(
            ticker,
            start=START.strftime("%Y-%m-%d"),
            end=END.strftime("%Y-%m-%d"),
            interval="1wk",
            progress=False,
            auto_adjust=True,
        )
        if df is None or len(df) == 0:
            print(f"  ! {ticker}: empty")
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [c[0] for c in df.columns]
        df = df[["Close"]].rename(columns={"Close": "c"})
        df.index = pd.to_datetime(df.index).tz_localize(None)
        # Align weekly close to following Sunday for join consistency
        df = df.resample("W").last().dropna()
        df["return"] = df["c"].pct_change()
        print(f"  + {ticker:6s}: {len(df):3d}w  {df.index[0].date()}..{df.index[-1].date()}  last=${float(df['c'].iloc[-1]):.2f}")
        return df
    except Exception as e:
        print(f"  ! {ticker}: {e}")
        return None


def fetch_crypto_weekly(coin_id: str, name: str) -> pd.DataFrame | None:
    try:
        r = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": "365"},
            timeout=30,
        )
        if r.status_code != 200:
            print(f"  ! {name}: CoinGecko HTTP {r.status_code}")
            return None
        prices = r.json().get("prices", [])
        if not prices:
            return None
        df = pd.DataFrame(prices, columns=["ts", "price"])
        df["date"] = pd.to_datetime(df["ts"], unit="ms").dt.tz_localize(None)
        df.set_index("date", inplace=True)
        weekly = df["price"].resample("W").last().to_frame("c")
        weekly["return"] = weekly["c"].pct_change()
        print(f"  + {name:6s}: {len(weekly):3d}w  {weekly.index[0].date()}..{weekly.index[-1].date()}  last=${float(weekly['c'].iloc[-1]):,.2f}")
        return weekly
    except Exception as e:
        print(f"  ! {name}: {e}")
        return None


def metrics(returns: pd.Series, label: str) -> dict:
    r = returns.fillna(0)
    cum = (1 + r).cumprod()
    if len(cum) == 0:
        return {"label": label, "total_return": 0, "cagr": 0, "ann_vol": 0,
                "sharpe": 0, "max_drawdown": 0, "weeks": 0}
    total = float(cum.iloc[-1] - 1)
    weeks = int(len(r))
    ann_vol = float(r.std() * np.sqrt(52)) if r.std() and weeks > 1 else 0.0
    sharpe = float(r.mean() / r.std() * np.sqrt(52)) if r.std() and weeks > 1 else 0.0
    dd = float(((cum / cum.cummax()) - 1).min())
    cagr = float((1 + total) ** (52 / weeks) - 1) if weeks > 0 else 0.0
    return {
        "label": label,
        "total_return": total,
        "cagr": cagr,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "max_drawdown": dd,
        "weeks": weeks,
    }


def main():
    print("[1] Pulling equities via yfinance...")
    prices: dict[str, pd.DataFrame] = {}
    for t in EQUITY_TICKERS:
        df = fetch_equity_weekly(t)
        if df is not None:
            prices[t] = df

    print("\n[2] Pulling crypto via CoinGecko...")
    for name, coin_id in CRYPTO_TICKERS.items():
        df = fetch_crypto_weekly(coin_id, name)
        if df is not None:
            prices[name] = df

    if "HYPE" not in prices:
        print("  using BTC as HYPE proxy (CoinGecko unavailable)")
        prices["HYPE"] = prices["BTC"]

    # Save raw closes
    raw = {
        k: [{"date": idx.strftime("%Y-%m-%d"), "close": float(row["c"])}
            for idx, row in v.iterrows() if pd.notna(row["c"])]
        for k, v in prices.items()
    }
    (DATA_DIR / "raw-weekly.json").write_text(json.dumps(raw, indent=2))

    results: dict = {"as_of": END.strftime("%Y-%m-%d"), "strategies": {}}

    # ============================ STRATEGY A ============================
    print("\n[3] Strategy A — Macro Rotation (HYPE leveraged by QQQ/BTC divergence)")
    hype = prices["HYPE"]; qqq = prices.get("QQQ"); btc = prices.get("BTC")
    m = pd.concat(
        [hype["return"].rename("hype"), qqq["return"].rename("qqq"), btc["return"].rename("btc")],
        axis=1, join="inner",
    ).dropna()
    print(f"  joined frame: {len(m)} weeks  {m.index[0].date()}..{m.index[-1].date()}")
    # 13-week rolling divergence (more responsive on a 12mo window)
    m["qqq_btc_div"] = m["qqq"].rolling(13, min_periods=4).sum() - m["btc"].rolling(13, min_periods=4).sum()
    m["signal"] = 1.0
    m.loc[m["qqq_btc_div"] > 0.15, "signal"] = 1.5
    m.loc[m["qqq_btc_div"] < -0.05, "signal"] = 0.8
    m["strategy_return"] = m["hype"] * m["signal"]
    a_metrics = metrics(m["strategy_return"], "Macro Rotation")
    bh_metrics = metrics(m["hype"], "HYPE buy & hold")
    a_metrics["alpha_vs_hype"] = a_metrics["total_return"] - bh_metrics["total_return"]
    latest_sig = float(m["signal"].iloc[-1])
    a_metrics["latest_signal"] = latest_sig
    a_metrics["latest_signal_label"] = (
        "MAX LONG (1.5x)" if latest_sig > 1.2
        else "DEFENSIVE (0.8x)" if latest_sig < 0.95
        else "HOLD (1.0x)"
    )
    a_metrics["latest_qqq_btc_div"] = float(m["qqq_btc_div"].iloc[-1])
    weeks_max = int((m["signal"] > 1.2).sum())
    weeks_def = int((m["signal"] < 0.95).sum())
    weeks_hold = len(m) - weeks_max - weeks_def
    a_metrics["weeks_max_long"] = weeks_max
    a_metrics["weeks_defensive"] = weeks_def
    a_metrics["weeks_hold"] = weeks_hold
    results["strategies"]["macro_rotation"] = a_metrics
    results["strategies"]["buy_hold_hype"] = bh_metrics

    master_dates = m.index
    results["_series"] = {
        "dates": [d.strftime("%Y-%m-%d") for d in master_dates],
        "hype": m["hype"].tolist(),
        "strategy_a": m["strategy_return"].tolist(),
        "signal_a": m["signal"].tolist(),
    }
    print(f"   A: ret={a_metrics['total_return']:+.1%}  bh={bh_metrics['total_return']:+.1%}  alpha={a_metrics['alpha_vs_hype']:+.1%}  shp={a_metrics['sharpe']:.2f}  dd={a_metrics['max_drawdown']:.1%}")
    print(f"   A latest: {a_metrics['latest_signal_label']}  (QQQ-BTC 13w div = {a_metrics['latest_qqq_btc_div']:+.2f})")
    print(f"   A regime weeks: MAX={weeks_max}  HOLD={weeks_hold}  DEF={weeks_def}")

    # ============================ STRATEGY B ============================
    print("\n[4] Strategy B — SOXL Short + HYPE Long pair (rotation capture)")
    soxl = prices.get("SOXL")
    b = pd.concat(
        [hype["return"].rename("hype"), soxl["return"].rename("soxl")],
        axis=1, join="inner",
    ).dropna()
    b["soxl_4w"] = b["soxl"].rolling(4, min_periods=2).sum()
    b["sig_hype"] = 1.0
    b["sig_soxl_short"] = 0.0
    overbought = b["soxl_4w"] > 0.12
    b.loc[overbought, "sig_hype"] = 1.5
    b.loc[overbought, "sig_soxl_short"] = -0.3
    b["strategy_return"] = (b["hype"] * b["sig_hype"]) + (b["soxl"] * b["sig_soxl_short"])
    bm = metrics(b["strategy_return"], "SOXL-Short + HYPE")
    bh = metrics(b["hype"], "HYPE buy & hold")
    bm["alpha_vs_hype"] = bm["total_return"] - bh["total_return"]
    bm["latest_signal_label"] = "PAIR ON (short SOXL, long HYPE 1.5x)" if bool(overbought.iloc[-1]) else "PAIR OFF (HYPE 1.0x)"
    bm["latest_soxl_4w"] = float(b["soxl_4w"].iloc[-1])
    bm["weeks_pair_on"] = int(overbought.sum())
    bm["weeks_pair_off"] = int((~overbought).sum())
    results["strategies"]["soxl_short_hype_long"] = bm
    b_series = b["strategy_return"].reindex(master_dates).fillna(0)
    sig_b_series = overbought.reindex(master_dates).fillna(False).astype(int).map(lambda x: 1.5 if x else 1.0)
    results["_series"]["strategy_b"] = b_series.tolist()
    results["_series"]["signal_b"] = sig_b_series.tolist()
    print(f"   B: ret={bm['total_return']:+.1%}  bh={bh['total_return']:+.1%}  alpha={bm['alpha_vs_hype']:+.1%}  shp={bm['sharpe']:.2f}  dd={bm['max_drawdown']:.1%}")
    print(f"   B latest: {bm['latest_signal_label']}  (SOXL 4w = {bm['latest_soxl_4w']:+.1%})  ON weeks={bm['weeks_pair_on']}/{len(b)}")

    # ============================ STRATEGY C ============================
    print("\n[5] Strategy C — Multi-Asset Momentum (BTC/ETH/HYPE top picks)")
    universe = [k for k in ["BTC", "ETH", "HYPE"] if k in prices]
    cm = pd.concat({k: prices[k]["return"] for k in universe}, axis=1, join="inner").dropna(how="all")
    mom = cm.rolling(4, min_periods=2).sum()
    c_returns, c_signals = [], []
    for i in range(len(cm)):
        if i < 4:
            c_returns.append(0.0); c_signals.append("warmup"); continue
        row = mom.iloc[i].dropna().sort_values(ascending=False)
        wk = cm.iloc[i]
        port = 0.0; parts = []
        if len(row) >= 1:
            top = row.index[0]; v = wk.get(top, 0.0)
            port += 1.5 * (v if pd.notna(v) else 0.0); parts.append(f"1.5x {top}")
        if len(row) >= 2:
            second = row.index[1]; v = wk.get(second, 0.0)
            port += 0.5 * (v if pd.notna(v) else 0.0); parts.append(f"0.5x {second}")
        c_returns.append(port / 2.0)
        c_signals.append(" / ".join(parts))
    c_series = pd.Series(c_returns, index=cm.index)
    cm_m = metrics(c_series, "Multi-Asset Momentum")
    ref_hype = cm["HYPE"] if "HYPE" in cm else cm.iloc[:, 0]
    ref = metrics(ref_hype, "HYPE buy & hold")
    cm_m["alpha_vs_hype"] = cm_m["total_return"] - ref["total_return"]
    cm_m["latest_signal_label"] = c_signals[-1] if c_signals else "n/a"
    cm_m["universe"] = universe
    results["strategies"]["multi_asset_momentum"] = cm_m
    c_aligned = c_series.reindex(master_dates).fillna(0).tolist()
    sig_c_aligned = pd.Series(
        [0.0 if t == "warmup" else 1.5 for t in c_signals], index=cm.index,
    ).reindex(master_dates).fillna(0).tolist()
    results["_series"]["strategy_c"] = c_aligned
    results["_series"]["signal_c"] = sig_c_aligned
    results["_series"]["signal_c_text"] = c_signals
    print(f"   C: ret={cm_m['total_return']:+.1%}  bh={ref['total_return']:+.1%}  alpha={cm_m['alpha_vs_hype']:+.1%}  shp={cm_m['sharpe']:.2f}  dd={cm_m['max_drawdown']:.1%}")
    print(f"   C latest: {cm_m['latest_signal_label']}")

    # ============================ WINNER ============================
    candidates = {k: v for k, v in results["strategies"].items() if k != "buy_hold_hype"}
    winner_key, winner_m = max(candidates.items(), key=lambda kv: kv[1]["total_return"])
    results["winner"] = {"key": winner_key, **winner_m}
    print(f"\n[6] Winner: {winner_m['label']}  ret={winner_m['total_return']:+.1%}  shp={winner_m['sharpe']:.2f}  alpha={winner_m['alpha_vs_hype']:+.1%}")

    # ============================ CHARTS ============================
    print("\n[7] Building charts...")
    dates = pd.to_datetime(results["_series"]["dates"])
    hype_cum = (1 + pd.Series(results["_series"]["hype"], index=dates)).cumprod()
    a_cum = (1 + pd.Series(results["_series"]["strategy_a"], index=dates)).cumprod()
    b_cum = (1 + pd.Series(results["_series"]["strategy_b"], index=dates)).cumprod()
    c_cum = (1 + pd.Series(results["_series"]["strategy_c"], index=dates)).cumprod()

    # ---- Chart 1: cumulative comparison
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=140)
    ax.plot(hype_cum.index, hype_cum.values, lw=2.0, color="#888", linestyle="--",
            label=f"HYPE buy & hold ({bh_metrics['total_return']:+.0%})")
    ax.plot(a_cum.index, a_cum.values, lw=2.4, color="#1c4fd6",
            label=f"A · Macro Rotation ({a_metrics['total_return']:+.0%})")
    ax.plot(b_cum.index, b_cum.values, lw=2.4, color="#d12d2d",
            label=f"B · SOXL-Short pair ({bm['total_return']:+.0%})")
    ax.plot(c_cum.index, c_cum.values, lw=2.4, color="#1f8a4c",
            label=f"C · Multi-Asset Mom. ({cm_m['total_return']:+.0%})")
    ax.set_title("RD Alpha Engine — 12-month backtest, growth of $1", fontsize=14, fontweight="bold")
    ax.set_ylabel("Equity multiple")
    ax.axhline(1.0, color="#ccc", lw=0.8)
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    ax.grid(alpha=0.25)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    fig.text(0.99, 0.01, f"Built {datetime.utcnow().strftime('%Y-%m-%d')} · CoinGecko + yfinance · weekly bars",
             ha="right", va="bottom", fontsize=8, color="#888")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "strategy-comparison.png", facecolor="white")
    plt.close()
    print("   + strategy-comparison.png")

    # ---- Chart 2: drawdown
    def ddpct(s): return ((s / s.cummax()) - 1) * 100
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=140)
    ax.fill_between(hype_cum.index, ddpct(hype_cum), 0, color="#888", alpha=0.30, label="HYPE buy & hold")
    ax.plot(a_cum.index, ddpct(a_cum), lw=1.9, color="#1c4fd6", label="A · Macro Rotation")
    ax.plot(b_cum.index, ddpct(b_cum), lw=1.9, color="#d12d2d", label="B · SOXL-Short pair")
    ax.plot(c_cum.index, ddpct(c_cum), lw=1.9, color="#1f8a4c", label="C · Multi-Asset Mom.")
    ax.set_title("Drawdown profile — how deep does each go?", fontsize=14, fontweight="bold")
    ax.set_ylabel("Drawdown (%)")
    ax.legend(loc="lower left", frameon=False, fontsize=10)
    ax.grid(alpha=0.25)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "drawdown-comparison.png", facecolor="white")
    plt.close()
    print("   + drawdown-comparison.png")

    # ---- Chart 3: signal calendar
    rows = pd.DataFrame(
        {
            "A · Macro Rotation": results["_series"]["signal_a"],
            "B · SOXL-Short pair": results["_series"]["signal_b"],
            "C · Multi-Asset Mom.": results["_series"]["signal_c"],
        },
        index=dates,
    ).T
    fig, ax = plt.subplots(figsize=(12, 3.4), dpi=140)
    im = ax.imshow(rows.values, aspect="auto", cmap="RdYlGn", vmin=0.6, vmax=1.6, interpolation="nearest")
    ax.set_yticks(range(len(rows.index))); ax.set_yticklabels(rows.index, fontsize=10)
    step = max(1, len(dates) // 10)
    ax.set_xticks(range(0, len(dates), step))
    ax.set_xticklabels([d.strftime("%b %Y") for d in dates[::step]], rotation=45, ha="right", fontsize=9)
    ax.set_title("Signal calendar — green = leveraged ON; red = de-risked OFF", fontsize=13, fontweight="bold")
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
    cbar.set_label("Position multiplier", fontsize=9)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "signal-calendar.png", facecolor="white")
    plt.close()
    print("   + signal-calendar.png")

    # ============================ PERSIST ============================
    out = {k: v for k, v in results.items() if k != "_series"}
    out["data_range"] = {
        "start": dates[0].strftime("%Y-%m-%d"),
        "end": dates[-1].strftime("%Y-%m-%d"),
        "weeks": int(len(dates)),
    }
    out["instruments_loaded"] = sorted(prices.keys())
    (DATA_DIR / "backtest-results.json").write_text(json.dumps(out, indent=2))
    print(f"\n[8] Wrote {DATA_DIR / 'backtest-results.json'}")


if __name__ == "__main__":
    main()
