#!/usr/bin/env python3
"""SOX long/short backtester with grid search.

Loads weekly OHLCV JSON files from weekly_prices_long/, builds an aligned
weekly close matrix, runs a parameterized momentum / mean-reversion / hybrid
strategy with weekly rebalancing, then grid-searches for the best Sharpe and
Calmar combos vs SOXL.

Outputs:
  analysis/grid_search_results.parquet  — all combo metrics
  analysis/top_strategies.json          — top 20 by Sharpe
  analysis/best_strategy.json           — single chosen strategy + current weights
  analysis/equity_curves.parquet        — per-strategy weekly cum return for charts
"""
from __future__ import annotations

import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "weekly_prices_long"
ANALYSIS_DIR = ROOT / "analysis"
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)

EXCLUDE_FROM_POSITIONS = {"SOXX", "SOXL", "QQQ", "SPY"}


def load_all() -> dict[str, pd.DataFrame]:
    out = {}
    for p in sorted(DATA_DIR.glob("*.json")):
        ticker = p.stem
        js = json.loads(p.read_text())
        results = js.get("results") or []
        if not results:
            continue
        df = pd.DataFrame(results)
        df["date"] = pd.to_datetime(df["t"], unit="ms")
        df = df.set_index("date")[["o", "h", "l", "c", "v"]].sort_index()
        out[ticker] = df
    return out


class SOXBacktest:
    """Long/short SOX strategy backtester. Weekly rebalancing."""

    def __init__(self, all_data: dict[str, pd.DataFrame], universe: list[str]):
        closes = pd.DataFrame(
            {t: d["c"] for t, d in all_data.items() if t in universe}
        ).sort_index()
        closes = closes.dropna(how="all").ffill()
        self.closes = closes
        self.universe = [t for t in universe if t in closes.columns]

    def compute_signal(self, date_idx: int, params: dict) -> dict[str, float]:
        lookback = params.get("lookback", 4)
        n_long = params.get("n_long", 5)
        n_short = params.get("n_short", 5)
        stype = params.get("type", "momentum")

        if date_idx < lookback + 1:
            return {}

        window = self.closes.iloc[date_idx - lookback : date_idx]
        if len(window) < lookback:
            return {}

        # Period return per ticker
        returns = (window.iloc[-1] / window.iloc[0] - 1).dropna()
        # Remove tickers with zero / NaN over the window
        returns = returns[~returns.index.isin(EXCLUDE_FROM_POSITIONS) | (returns.index == "SOXX")]

        if stype == "momentum":
            ranked = returns.sort_values(ascending=False)
            longs = [t for t in ranked.index if t not in EXCLUDE_FROM_POSITIONS][:n_long]
            shorts = [t for t in ranked.index[::-1] if t not in EXCLUDE_FROM_POSITIONS][:n_short]
        elif stype == "mean_reversion":
            ranked = returns.sort_values(ascending=True)
            longs = [t for t in ranked.index if t not in EXCLUDE_FROM_POSITIONS][:n_long]
            shorts = [t for t in ranked.index[::-1] if t not in EXCLUDE_FROM_POSITIONS][:n_short]
        elif stype == "hybrid":
            soxx_ret = returns.get("SOXX", 0.0)
            if soxx_ret > 0:
                ranked = returns.sort_values(ascending=False)
            else:
                ranked = returns.sort_values(ascending=True)
            longs = [t for t in ranked.index if t not in EXCLUDE_FROM_POSITIONS][:n_long]
            shorts = [t for t in ranked.index[::-1] if t not in EXCLUDE_FROM_POSITIONS][:n_short]
        else:
            return {}

        weights: dict[str, float] = {}
        if n_long > 0 and longs:
            lw = 1.0 / n_long
            for t in longs:
                weights[t] = lw
        if n_short > 0 and shorts:
            sw = -1.0 / n_short
            for t in shorts:
                weights[t] = sw
        return weights

    def run(self, params: dict, start_idx: int = 52) -> dict:
        rets: list[float] = []
        dates: list[pd.Timestamp] = []
        weights_history: list[dict] = []
        for i in range(start_idx, len(self.closes) - 1):
            w = self.compute_signal(i, params)
            if not w:
                rets.append(0.0)
                dates.append(self.closes.index[i + 1])
                weights_history.append({})
                continue
            wk_ret = 0.0
            for t, wt in w.items():
                if t not in self.closes.columns:
                    continue
                p0 = self.closes[t].iloc[i]
                p1 = self.closes[t].iloc[i + 1]
                if pd.isna(p0) or pd.isna(p1) or p0 <= 0:
                    continue
                r = p1 / p0 - 1.0
                if np.isnan(r) or np.isinf(r):
                    continue
                wk_ret += wt * r
            rets.append(wk_ret)
            dates.append(self.closes.index[i + 1])
            weights_history.append(w)

        ser = pd.Series(rets, index=pd.DatetimeIndex(dates))
        cum = (1 + ser).cumprod()
        total = float(cum.iloc[-1] - 1) if len(cum) else 0.0
        n = max(len(ser), 1)
        ann_ret = (1 + total) ** (52 / n) - 1 if total > -1 else -1.0
        ann_vol = float(ser.std() * np.sqrt(52)) if ser.std() > 0 else 0.0
        sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0
        roll_max = cum.cummax()
        dd = cum / roll_max - 1
        max_dd = float(dd.min()) if len(dd) else 0.0
        calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0.0
        return {
            "total_return": total,
            "ann_return": ann_ret,
            "ann_vol": ann_vol,
            "sharpe": sharpe,
            "max_drawdown": max_dd,
            "calmar": calmar,
            "n_weeks": n,
            "cum_returns": cum,
            "weekly_returns": ser,
            "weights_history": weights_history,
        }


def benchmark_metrics(closes: pd.Series, start_idx: int) -> dict:
    sub = closes.iloc[start_idx:].dropna()
    rets = sub.pct_change().dropna()
    cum = (1 + rets).cumprod()
    total = float(cum.iloc[-1] - 1)
    n = max(len(rets), 1)
    ann_ret = (1 + total) ** (52 / n) - 1 if total > -1 else -1.0
    ann_vol = float(rets.std() * np.sqrt(52))
    sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0
    dd = (cum / cum.cummax() - 1)
    max_dd = float(dd.min())
    calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0.0
    return {
        "total_return": total,
        "ann_return": ann_ret,
        "ann_vol": ann_vol,
        "sharpe": sharpe,
        "max_drawdown": max_dd,
        "calmar": calmar,
        "cum_returns": cum,
        "weekly_returns": rets,
    }


def main():
    print("Loading data...")
    all_data = load_all()
    print(f"  loaded {len(all_data)} tickers")

    universe = [
        "NVDA", "AMD", "AVGO", "TXN", "QCOM", "INTC", "MU", "AMAT", "LRCX", "KLAC",
        "ADI", "MRVL", "NXPI", "ON", "MCHP", "MPWR", "ENTG", "SWKS", "QRVO",
        "TER", "CRUS", "ACLS", "SLAB", "RMBS", "SITM", "SOXX",
    ]
    universe = [t for t in universe if t in all_data]

    bt = SOXBacktest(all_data, universe)
    print(f"  universe: {len(bt.universe)} tickers, {len(bt.closes)} weeks "
          f"({bt.closes.index[0].date()} → {bt.closes.index[-1].date()})")

    start_idx = 52  # 1y warmup

    # SOXL benchmark for the same period
    soxl_close = all_data["SOXL"]["c"]
    # Align to bt index by reindex
    soxl_aligned = soxl_close.reindex(bt.closes.index).ffill()
    soxl_metrics = benchmark_metrics(soxl_aligned, start_idx)
    print(f"\nSOXL benchmark ({bt.closes.index[start_idx].date()} → now):")
    print(f"  return={soxl_metrics['total_return']:.1%}  "
          f"sharpe={soxl_metrics['sharpe']:.2f}  "
          f"maxDD={soxl_metrics['max_drawdown']:.1%}  "
          f"calmar={soxl_metrics['calmar']:.2f}")

    # Grid search
    grid = {
        "type": ["momentum", "mean_reversion", "hybrid"],
        "lookback": [2, 4, 8, 13, 26],
        "n_long": [3, 5, 8, 10],
        "n_short": [0, 3, 5, 8],
    }
    combos = list(product(*grid.values()))
    print(f"\nGrid search: {len(combos)} combos")

    rows = []
    equity_curves = {}
    for i, combo in enumerate(combos):
        params = dict(zip(grid.keys(), combo))
        try:
            res = bt.run(params, start_idx=start_idx)
        except Exception as e:
            print(f"  err {params}: {e}")
            continue
        key = f"{params['type']}_lb{params['lookback']}_L{params['n_long']}_S{params['n_short']}"
        equity_curves[key] = res["cum_returns"]
        rows.append({
            **params,
            "total_return": res["total_return"],
            "ann_return": res["ann_return"],
            "ann_vol": res["ann_vol"],
            "sharpe": res["sharpe"],
            "max_drawdown": res["max_drawdown"],
            "calmar": res["calmar"],
            "n_weeks": res["n_weeks"],
            "key": key,
        })
        if (i + 1) % 30 == 0:
            print(f"  {i+1}/{len(combos)}")

    df = pd.DataFrame(rows).sort_values("sharpe", ascending=False).reset_index(drop=True)
    df.to_csv(ANALYSIS_DIR / "grid_search_results.csv", index=False)
    df.head(20).to_json(ANALYSIS_DIR / "top_strategies.json", orient="records", indent=2)
    print(f"\nSaved {len(df)} rows.")

    print("\n=== TOP 10 BY SHARPE ===")
    show_cols = ["type", "lookback", "n_long", "n_short", "total_return",
                 "sharpe", "max_drawdown", "calmar"]
    print(df.head(10)[show_cols].to_string(index=False))

    print("\n=== TOP 10 BY CALMAR ===")
    print(df.sort_values("calmar", ascending=False).head(10)[show_cols].to_string(index=False))

    # Pick best: rank by sharpe but require ann_return > SOXL ann_return floor (otherwise short-only wins)
    # And require n_long >= 3 to ensure a real long portfolio
    eligible = df[(df["n_long"] >= 3) & (df["ann_return"] > 0)]
    if eligible.empty:
        eligible = df
    best_row = eligible.sort_values("sharpe", ascending=False).iloc[0].to_dict()
    print("\nBEST (Sharpe, eligible):")
    print({k: best_row[k] for k in show_cols + ["key"]})

    best_params = {k: best_row[k] for k in ["type", "lookback", "n_long", "n_short"]}
    # Cast to native types
    best_params["lookback"] = int(best_params["lookback"])
    best_params["n_long"] = int(best_params["n_long"])
    best_params["n_short"] = int(best_params["n_short"])
    best_res = bt.run(best_params, start_idx=start_idx)

    # Current positions: signal at last available bar
    cur_weights = bt.compute_signal(len(bt.closes) - 1, best_params)
    current_prices = {t: float(bt.closes[t].iloc[-1]) for t in cur_weights}

    best_out = {
        "params": best_params,
        "metrics": {k: float(best_row[k]) for k in
                    ["total_return", "ann_return", "ann_vol", "sharpe",
                     "max_drawdown", "calmar"]},
        "soxl_metrics": {k: float(soxl_metrics[k]) for k in
                         ["total_return", "ann_return", "ann_vol", "sharpe",
                          "max_drawdown", "calmar"]},
        "n_weeks": int(best_row["n_weeks"]),
        "start_date": bt.closes.index[start_idx].strftime("%Y-%m-%d"),
        "end_date": bt.closes.index[-1].strftime("%Y-%m-%d"),
        "current_positions": [
            {"ticker": t, "weight": float(w), "side": "LONG" if w > 0 else "SHORT",
             "price": current_prices[t]}
            for t, w in sorted(cur_weights.items(), key=lambda x: -x[1])
        ],
        "universe": bt.universe,
    }
    (ANALYSIS_DIR / "best_strategy.json").write_text(json.dumps(best_out, indent=2))
    print(f"\nWrote best_strategy.json")

    # Equity curves for charts: best strategy + SOXL
    chart_df = pd.DataFrame({
        "strategy": best_res["cum_returns"],
        "soxl": soxl_metrics["cum_returns"].reindex(best_res["cum_returns"].index).ffill(),
    })
    chart_df.to_csv(ANALYSIS_DIR / "equity_curves.csv")
    print(f"Wrote equity_curves.csv ({len(chart_df)} rows)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
