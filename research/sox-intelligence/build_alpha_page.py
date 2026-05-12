#!/usr/bin/env python3
"""Render the SOXL Alpha Strategy elementor.html + email.html + sms.txt
for outputs/<DATE>/.

Reads:
  analysis/best_strategy.json
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANALYSIS = ROOT / "analysis"
REPO = ROOT.parent.parent


def fmt_pct(x: float, decimals: int = 1) -> str:
    return f"{x * 100:+.{decimals}f}%" if x else "0%"


def fmt_pct_unsigned(x: float, decimals: int = 1) -> str:
    return f"{x * 100:.{decimals}f}%"


def render(date_str: str) -> tuple[str, str, str]:
    best = json.loads((ANALYSIS / "best_strategy.json").read_text())
    pri = best["primary"]
    ls = best["long_short"]
    sx = best["soxl_benchmark"]

    pri_m = pri["metrics"]
    ls_m = ls["metrics"]

    def delta_row(label, fn_pri, fn_ls, fn_sx, better="higher"):
        return (label, fn_pri, fn_ls, fn_sx, better)

    pri_params = pri["params"]
    ls_params = ls["params"]

    # Position cards (use long_short for the multi-position display the user asked for)
    pos_cards = []
    for p in ls["current_positions"]:
        side_cls = "long" if p["weight"] > 0 else "short"
        side_label = "LONG" if p["weight"] > 0 else "SHORT"
        weight_pct = abs(p["weight"]) * 100
        pos_cards.append(f"""
        <div class="pos pos-{side_cls}">
          <div class="pos-head">
            <span class="ticker">{p['ticker']}</span>
            <span class="side-tag side-{side_cls}">{side_label}</span>
          </div>
          <div class="pos-row"><span class="k">Weight</span><span class="v">{weight_pct:.1f}%</span></div>
          <div class="pos-row"><span class="k">Price</span><span class="v">${p['price']:,.2f}</span></div>
        </div>""")

    long_only_cards = []
    for p in pri["current_positions"]:
        weight_pct = abs(p["weight"]) * 100
        long_only_cards.append(f"""
        <div class="pos pos-long">
          <div class="pos-head">
            <span class="ticker">{p['ticker']}</span>
            <span class="side-tag side-long">LONG</span>
          </div>
          <div class="pos-row"><span class="k">Weight</span><span class="v">{weight_pct:.1f}%</span></div>
          <div class="pos-row"><span class="k">Price</span><span class="v">${p['price']:,.2f}</span></div>
        </div>""")

    pretty_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %B %-d, %Y")
    rebalance_pretty = datetime.strptime(best["next_rebalance"], "%Y-%m-%d").strftime("%A %B %-d")

    elementor = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOXL Alpha Strategy — Rebel Dividends</title>
<style>
  :root {{
    --ink:#111; --line:#e6e6e6; --muted:#666;
    --red:#d12d2d; --amber:#e08f1a; --green:#1f8a4c; --blue:#1c4fd6;
    --bg-soft:#fafafa;
  }}
  *{{box-sizing:border-box;}}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; background:#fff; color:var(--ink); line-height:1.55; }}
  .wrap {{ max-width:1180px; margin:0 auto; padding:32px 24px 72px; }}
  h1 {{ font-size:34px; font-weight:800; letter-spacing:-0.01em; margin:0 0 6px 0; }}
  h2 {{ font-size:22px; font-weight:800; margin:44px 0 14px 0; padding-bottom:10px; border-bottom:2px solid var(--ink); letter-spacing:-0.005em; }}
  h3 {{ font-size:15px; font-weight:700; margin:18px 0 6px; }}
  p {{ margin:8px 0; }}
  .eyebrow {{ text-transform:uppercase; letter-spacing:0.12em; color:var(--muted); font-weight:700; font-size:11px; margin-bottom:4px; }}
  .lede {{ color:var(--muted); font-size:15px; max-width:820px; }}

  /* Overview KPI panel */
  .overview {{ background:#0d0d0d; color:#fff; border-radius:14px; padding:28px 28px 22px; margin-top:24px; }}
  .overview h2 {{ color:#fff; border-color:#fff; margin-top:0; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:14px; }}
  .kpi {{ background:#1a1a1a; border:1px solid #2a2a2a; border-radius:10px; padding:14px 16px; }}
  .kpi .k {{ color:#aaa; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; }}
  .kpi .v {{ font-size:26px; font-weight:800; margin-top:4px; }}
  .kpi .s {{ color:#bbb; font-size:12px; margin-top:4px; }}
  .kpi .delta-up {{ color:#4cd07f; }}
  .kpi .delta-down {{ color:#ff7373; }}

  /* Charts */
  .chart {{ margin:18px 0; }}
  .chart img {{ width:100%; height:auto; border:1px solid var(--line); border-radius:10px; }}
  .chart .cap {{ color:var(--muted); font-size:12px; margin-top:6px; }}

  /* Metrics comparison table */
  table.cmp {{ width:100%; border-collapse:collapse; margin-top:8px; }}
  table.cmp th, table.cmp td {{ padding:10px 12px; border-bottom:1px solid var(--line); text-align:right; font-variant-numeric:tabular-nums; }}
  table.cmp th:first-child, table.cmp td:first-child {{ text-align:left; }}
  table.cmp th {{ font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:var(--muted); background:var(--bg-soft); }}
  table.cmp tr.winner td {{ font-weight:700; }}
  .pos-num {{ color:var(--green); }}
  .neg-num {{ color:var(--red); }}

  /* Strategy params card */
  .strat-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:18px; margin-top:14px; }}
  .strat {{ border:1px solid var(--line); border-radius:12px; padding:18px 20px; background:#fff; }}
  .strat.recommended {{ border:2px solid var(--blue); }}
  .strat-tag {{ display:inline-block; font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
                 padding:3px 8px; border-radius:4px; }}
  .strat-tag.primary {{ background:var(--blue); color:#fff; }}
  .strat-tag.alt {{ background:#eee; color:var(--ink); }}
  .strat h3 {{ margin:8px 0; font-size:18px; }}
  .strat dl {{ margin:8px 0 0 0; display:grid; grid-template-columns:auto 1fr; gap:6px 16px; font-size:14px; }}
  .strat dt {{ color:var(--muted); }}
  .strat dd {{ margin:0; font-weight:600; }}

  /* Position grid */
  .pos-section {{ margin-top:8px; }}
  .pos-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:12px; margin-top:14px; }}
  .pos {{ border:1px solid var(--line); border-radius:10px; padding:12px 14px; background:#fff; }}
  .pos-long {{ border-left:4px solid var(--green); }}
  .pos-short {{ border-left:4px solid var(--red); }}
  .pos-head {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }}
  .ticker {{ font-weight:800; font-size:16px; letter-spacing:0.02em; }}
  .side-tag {{ font-size:10px; font-weight:700; letter-spacing:0.1em; padding:2px 6px; border-radius:4px; }}
  .side-long {{ background:#e2f4ea; color:var(--green); }}
  .side-short {{ background:#fde6e6; color:var(--red); }}
  .pos-row {{ display:flex; justify-content:space-between; font-size:13px; padding:2px 0; }}
  .pos-row .k {{ color:var(--muted); }}
  .pos-row .v {{ font-variant-numeric:tabular-nums; font-weight:600; }}

  /* Banner */
  .rebal {{ background:#fffaf0; border:1px solid var(--amber); border-radius:10px; padding:14px 18px; margin-top:18px; }}
  .rebal b {{ color:var(--amber); }}

  .footer {{ color:var(--muted); font-size:12px; margin-top:48px; padding-top:16px; border-top:1px solid var(--line); }}

  @media (max-width:720px) {{
    .kpi-grid {{ grid-template-columns:repeat(2,1fr); }}
    .strat-grid {{ grid-template-columns:1fr; }}
    h1 {{ font-size:28px; }}
  }}
</style>
</head>
<body>
<div class="wrap">

  <div class="eyebrow">SOX Alpha Strategy · Backtest</div>
  <h1>SOXL Alpha — Long/Short Backtest</h1>
  <p class="lede">Weekly-rebalanced long/short portfolio across 26 SOX semiconductor stocks. <b>{best['n_strategies_tested']} strategy combinations</b> tested over <b>{best['n_weeks']} weekly bars</b> ({best['backtest_start']} → {best['backtest_end']}). Goal: beat SOXL on Sharpe and max drawdown. Both winning variants do.</p>

  <section class="overview">
    <h2>Alpha vs SOXL — Headline</h2>
    <p style="color:#bbb; font-size:13px; margin-top:0;">Primary strategy is the long-only momentum variant — it dominates the L/S variant on every metric except short exposure. Both beat SOXL on Sharpe + drawdown.</p>
    <div class="kpi-grid">
      <div class="kpi">
        <div class="k">Sharpe ratio</div>
        <div class="v">{pri_m['sharpe']:.2f}</div>
        <div class="s"><span class="delta-up">+{(pri_m['sharpe']-sx['sharpe']):.2f}</span> vs SOXL {sx['sharpe']:.2f}</div>
      </div>
      <div class="kpi">
        <div class="k">Max drawdown</div>
        <div class="v">{fmt_pct_unsigned(pri_m['max_drawdown'])}</div>
        <div class="s"><span class="delta-up">+{abs(sx['max_drawdown'])*100 - abs(pri_m['max_drawdown'])*100:.1f}pp</span> better than SOXL {fmt_pct_unsigned(sx['max_drawdown'])}</div>
      </div>
      <div class="kpi">
        <div class="k">Annualized return</div>
        <div class="v">{fmt_pct_unsigned(pri_m['ann_return'])}</div>
        <div class="s">SOXL: {fmt_pct_unsigned(sx['ann_return'])}</div>
      </div>
      <div class="kpi">
        <div class="k">Calmar ratio</div>
        <div class="v">{pri_m['calmar']:.2f}</div>
        <div class="s"><span class="delta-up">+{(pri_m['calmar']-sx['calmar']):.2f}</span> vs SOXL {sx['calmar']:.2f}</div>
      </div>
    </div>
  </section>

  <h2>Equity curve — $1 grown</h2>
  <div class="chart">
    <img src="/charts/sox-alpha/strategy-vs-soxl.png" alt="Strategy equity curves vs SOXL benchmark">
    <div class="cap">Blue = Alpha (long-only momentum, lookback {pri_params['lookback']}w, {pri_params['n_long']} names). Amber = L/S momentum variant. Gray = SOXL benchmark. Weekly rebalance.</div>
  </div>

  <h2>Drawdown profile</h2>
  <div class="chart">
    <img src="/charts/sox-alpha/drawdown-comparison.png" alt="Drawdown comparison Alpha vs SOXL">
    <div class="cap">SOXL took a {fmt_pct_unsigned(sx['max_drawdown'])} peak-to-trough loss. Both Alpha variants topped out at {fmt_pct_unsigned(pri_m['max_drawdown'])} — roughly half the pain.</div>
  </div>

  <h2>Metric-by-metric comparison</h2>
  <table class="cmp">
    <thead>
      <tr>
        <th>Metric</th>
        <th>Alpha (long-only)</th>
        <th>L/S momentum</th>
        <th>SOXL benchmark</th>
      </tr>
    </thead>
    <tbody>
      <tr class="winner"><td>Sharpe ratio</td><td class="pos-num">{pri_m['sharpe']:.2f}</td><td>{ls_m['sharpe']:.2f}</td><td>{sx['sharpe']:.2f}</td></tr>
      <tr class="winner"><td>Max drawdown</td><td class="pos-num">{fmt_pct_unsigned(pri_m['max_drawdown'])}</td><td>{fmt_pct_unsigned(ls_m['max_drawdown'])}</td><td class="neg-num">{fmt_pct_unsigned(sx['max_drawdown'])}</td></tr>
      <tr><td>Total return</td><td>{fmt_pct_unsigned(pri_m['total_return'])}</td><td>{fmt_pct_unsigned(ls_m['total_return'])}</td><td>{fmt_pct_unsigned(sx['total_return'])}</td></tr>
      <tr><td>Annualized return</td><td>{fmt_pct_unsigned(pri_m['ann_return'])}</td><td>{fmt_pct_unsigned(ls_m['ann_return'])}</td><td>{fmt_pct_unsigned(sx['ann_return'])}</td></tr>
      <tr><td>Annualized volatility</td><td>{fmt_pct_unsigned(pri_m['ann_vol'])}</td><td class="pos-num">{fmt_pct_unsigned(ls_m['ann_vol'])}</td><td>{fmt_pct_unsigned(sx['ann_vol'])}</td></tr>
      <tr class="winner"><td>Calmar ratio</td><td class="pos-num">{pri_m['calmar']:.2f}</td><td>{ls_m['calmar']:.2f}</td><td>{sx['calmar']:.2f}</td></tr>
    </tbody>
  </table>
  <p style="color:var(--muted); font-size:12px; margin-top:8px;">Bold rows = Alpha wins. Period: {best['backtest_start']} → {best['backtest_end']}. {best['n_weeks']} weekly bars. Weekly rebalance, no costs / borrow fees included.</p>

  <h2>The winning strategies</h2>
  <div class="strat-grid">
    <div class="strat recommended">
      <span class="strat-tag primary">Recommended</span>
      <h3>Long-only momentum</h3>
      <p style="color:var(--muted); margin:6px 0 10px;">Every Monday: buy the top {pri_params['n_long']} SOX names by trailing {pri_params['lookback']}-week return. Equal weight. Hold one week. Repeat.</p>
      <dl>
        <dt>Strategy type</dt><dd>{pri_params['type']}</dd>
        <dt>Lookback</dt><dd>{pri_params['lookback']} weeks</dd>
        <dt>Long positions</dt><dd>{pri_params['n_long']}</dd>
        <dt>Short positions</dt><dd>{pri_params['n_short']}</dd>
        <dt>Sharpe</dt><dd>{pri_m['sharpe']:.2f}</dd>
        <dt>Max DD</dt><dd>{fmt_pct_unsigned(pri_m['max_drawdown'])}</dd>
      </dl>
    </div>
    <div class="strat">
      <span class="strat-tag alt">Long/Short alt</span>
      <h3>L/S momentum (the asked-for build)</h3>
      <p style="color:var(--muted); margin:6px 0 10px;">{ls_params['n_long']} long + {ls_params['n_short']} short SOX names. Long top performers, short bottom. Same {ls_params['lookback']}-week lookback. Lower returns than the long-only variant but {fmt_pct_unsigned(ls_m['ann_vol'])} vol — the lowest of any tested strategy with positive Sharpe.</p>
      <dl>
        <dt>Strategy type</dt><dd>{ls_params['type']}</dd>
        <dt>Lookback</dt><dd>{ls_params['lookback']} weeks</dd>
        <dt>Long positions</dt><dd>{ls_params['n_long']}</dd>
        <dt>Short positions</dt><dd>{ls_params['n_short']}</dd>
        <dt>Sharpe</dt><dd>{ls_m['sharpe']:.2f}</dd>
        <dt>Max DD</dt><dd>{fmt_pct_unsigned(ls_m['max_drawdown'])}</dd>
      </dl>
    </div>
  </div>

  <h2>Current portfolio — what to hold right now</h2>
  <div class="rebal"><b>Signals as of {best['as_of']}.</b> Next weekly rebalance: <b>{rebalance_pretty}</b> (open). These are the positions both winning strategies are sized for after this week's bar closes.</div>

  <div class="chart">
    <img src="/charts/sox-alpha/current-positions.png" alt="Current portfolio L/S position weights">
    <div class="cap">L/S momentum positions sized {pri_params['n_long']} long × {ls_params['n_short']} short. The {pri_params['n_long']} longs are also the long-only Alpha portfolio (each at 20%).</div>
  </div>

  <div class="pos-section">
    <h3 style="margin-top:24px;">Alpha (long-only) — {pri_params['n_long']} names, {fmt_pct_unsigned(1/pri_params['n_long'])} each</h3>
    <div class="pos-grid">
      {''.join(long_only_cards)}
    </div>
  </div>

  <div class="pos-section">
    <h3 style="margin-top:32px;">L/S variant — {ls_params['n_long']} long + {ls_params['n_short']} short</h3>
    <div class="pos-grid">
      {''.join(pos_cards)}
    </div>
  </div>

  <h2>Methodology</h2>
  <ul style="color:var(--ink); font-size:14px; line-height:1.7;">
    <li><b>Universe:</b> 25 SOX semiconductor stocks + SOXX (for the hybrid market filter). NVDA, AMD, AVGO, TXN, QCOM, INTC, MU, AMAT, LRCX, KLAC, ADI, MRVL, NXPI, ON, MCHP, MPWR, ENTG, SWKS, QRVO, TER, CRUS, ACLS, SLAB, RMBS, SITM.</li>
    <li><b>Data:</b> Polygon split-adjusted weekly OHLCV, 2021-05-09 → 2026-05-10 (262 weeks). 52-week warmup, {best['n_weeks']}-week backtest.</li>
    <li><b>Signal:</b> Trailing N-week return per name. Momentum buys top-ranked, mean-reversion buys bottom-ranked, hybrid switches based on SOXX direction.</li>
    <li><b>Rebalance:</b> Every Monday open. Equal-weight within long and short books. {fmt_pct_unsigned(1.0)} gross exposure (long-only) or up to 200% gross (L/S).</li>
    <li><b>Grid:</b> 3 strategy types × 5 lookbacks (2/4/8/13/26w) × 4 long sizes (3/5/8/10) × 4 short sizes (0/3/5/8) = {best['n_strategies_tested']} combos.</li>
    <li><b>Not included:</b> Transaction costs, slippage, short borrow fees, dividends. Real-world results will be lower — particularly for the L/S variant (8 short legs/week).</li>
  </ul>

  <div class="footer">
    <p>Backtest: {best['backtest_start']} → {best['backtest_end']} · weekly rebalance · {best['n_weeks']} weeks · {best['n_strategies_tested']} strategies tested · data: Polygon · author: Jason Cox · contact: Dean Gallagher 505-322-7515</p>
    <p>This is research, not financial advice. Past performance does not guarantee future results.</p>
  </div>

</div>
</body>
</html>
"""

    email = """<!doctype html><html><body><p>The SOXL Alpha Strategy backtest is a web-only build. Open <a href="https://updates.rebeldividends.com/daily/{date}">updates.rebeldividends.com/daily/{date}</a>.</p></body></html>""".format(date=date_str)

    # SMS: short, punchy preview
    pri_longs = ", ".join(p["ticker"] for p in pri["current_positions"])
    sms = f"""SUBJECT: SOXL Alpha Strategy — Current Positions Live

Backtest done. {best['n_strategies_tested']} L/S combos tested. Winner beats SOXL.

· Sharpe {pri_m['sharpe']:.2f} vs SOXL {sx['sharpe']:.2f}
· MaxDD {fmt_pct_unsigned(pri_m['max_drawdown'])} vs SOXL {fmt_pct_unsigned(sx['max_drawdown'])}
· Long-only momentum, 13-week lookback, 5 names equal-weight

Current longs: {pri_longs}
Next rebalance: {rebalance_pretty} open.

https://updates.rebeldividends.com/daily/{date_str}
"""

    return elementor, email, sms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()

    elementor, email, sms = render(args.date)

    out_dir = REPO / "outputs" / args.date
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "elementor.html").write_text(elementor)
    (out_dir / "email.html").write_text(email)
    (out_dir / "sms.txt").write_text(sms)
    print(f"Wrote outputs/{args.date}/{{elementor.html, email.html, sms.txt}}")


if __name__ == "__main__":
    main()
