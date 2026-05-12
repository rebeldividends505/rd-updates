#!/usr/bin/env python3
"""Extract both long-only and long/short winners. Produces:
  analysis/best_strategy.json (updated, now has both 'primary' long-only and 'long_short')
  analysis/equity_curves.csv  (now has both strategies + SOXL)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "analysis"

sys.path.insert(0, str(ROOT))
from backtest_long_short import (  # noqa: E402
    SOXBacktest, load_all, benchmark_metrics,
)


def main():
    all_data = load_all()
    universe = [
        "NVDA", "AMD", "AVGO", "TXN", "QCOM", "INTC", "MU", "AMAT", "LRCX", "KLAC",
        "ADI", "MRVL", "NXPI", "ON", "MCHP", "MPWR", "ENTG", "SWKS", "QRVO",
        "TER", "CRUS", "ACLS", "SLAB", "RMBS", "SITM", "SOXX",
    ]
    universe = [t for t in universe if t in all_data]
    bt = SOXBacktest(all_data, universe)
    start_idx = 52

    df = pd.read_csv(ANALYSIS / "grid_search_results.csv")

    # Primary: best overall by sharpe with n_long>=3 & ann_return>0
    eligible = df[(df["n_long"] >= 3) & (df["ann_return"] > 0)]
    primary = eligible.sort_values("sharpe", ascending=False).iloc[0].to_dict()

    # Long/short: best with n_short >= 3
    ls_pool = df[(df["n_long"] >= 3) & (df["n_short"] >= 3) & (df["ann_return"] > 0)]
    ls_best = ls_pool.sort_values("sharpe", ascending=False).iloc[0].to_dict()

    # SOXL benchmark for same horizon
    soxl_aligned = all_data["SOXL"]["c"].reindex(bt.closes.index).ffill()
    soxl_metrics = benchmark_metrics(soxl_aligned, start_idx)

    def package(row):
        params = {
            "type": row["type"],
            "lookback": int(row["lookback"]),
            "n_long": int(row["n_long"]),
            "n_short": int(row["n_short"]),
        }
        res = bt.run(params, start_idx=start_idx)
        cur = bt.compute_signal(len(bt.closes) - 1, params)
        prices = {t: float(bt.closes[t].iloc[-1]) for t in cur}
        return {
            "params": params,
            "metrics": {k: float(row[k]) for k in
                        ["total_return", "ann_return", "ann_vol", "sharpe",
                         "max_drawdown", "calmar"]},
            "current_positions": [
                {"ticker": t, "weight": float(w),
                 "side": "LONG" if w > 0 else "SHORT", "price": prices[t]}
                for t, w in sorted(cur.items(), key=lambda x: -x[1])
            ],
            "cum_returns": res["cum_returns"],
        }

    pri = package(primary)
    ls = package(ls_best)

    out = {
        "as_of": bt.closes.index[-1].strftime("%Y-%m-%d"),
        "next_rebalance": "2026-05-18",
        "backtest_start": bt.closes.index[start_idx].strftime("%Y-%m-%d"),
        "backtest_end": bt.closes.index[-1].strftime("%Y-%m-%d"),
        "n_weeks": int(primary["n_weeks"]),
        "universe": bt.universe,
        "soxl_benchmark": {k: float(soxl_metrics[k]) for k in
                           ["total_return", "ann_return", "ann_vol", "sharpe",
                            "max_drawdown", "calmar"]},
        "primary": {
            "params": pri["params"],
            "metrics": pri["metrics"],
            "current_positions": pri["current_positions"],
        },
        "long_short": {
            "params": ls["params"],
            "metrics": ls["metrics"],
            "current_positions": ls["current_positions"],
        },
        "n_strategies_tested": len(df),
    }
    (ANALYSIS / "best_strategy.json").write_text(json.dumps(out, indent=2))
    print("Wrote best_strategy.json")
    print(f"  primary: {out['primary']['params']} sharpe={out['primary']['metrics']['sharpe']:.2f}")
    print(f"  long_short: {out['long_short']['params']} sharpe={out['long_short']['metrics']['sharpe']:.2f}")

    chart_df = pd.DataFrame({
        "primary": pri["cum_returns"],
        "long_short": ls["cum_returns"],
        "soxl": soxl_metrics["cum_returns"].reindex(pri["cum_returns"].index).ffill(),
    })
    chart_df.to_csv(ANALYSIS / "equity_curves.csv")
    print(f"Wrote equity_curves.csv ({len(chart_df)} rows)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
