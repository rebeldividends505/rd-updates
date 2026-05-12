"""Generate email-ready HTML sections with charts inlined as base64."""
import os, base64

OUT = os.path.expanduser("~/rd-updates-site/research/macro-charts-2026")

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

charts = {
    "ch1": b64(os.path.join(OUT, "chart1-btc-qqq-correlation.png")),
    "ch2": b64(os.path.join(OUT, "chart2-silver-gold-lag.png")),
    "ch3": b64(os.path.join(OUT, "chart3-gold-btc-180day-lag.png")),
    "ch4": b64(os.path.join(OUT, "chart4-m2-btc-gap.png")),
    "ch5": b64(os.path.join(OUT, "chart5-yen-btc.png")),
    "ch6a": b64(os.path.join(OUT, "chart6a-ai-stocks-returns.png")),
    "ch6b": b64(os.path.join(OUT, "chart6b-ai-stocks-pe.png")),
}

stocks_table = open(os.path.join(OUT, "stocks-table.html")).read()

def section(label, headline, body, chart_key, caption):
    img = f'<img src="data:image/png;base64,{charts[chart_key]}" alt="{headline}" width="640" style="width:100%;max-width:640px;height:auto;display:block;border:1px solid #e5e5e5;border-radius:4px;" />'
    return f"""
<!-- ==================== {label} ==================== -->
<tr><td bgcolor="#ffffff" style="background-color:#ffffff;padding:30px 20px 10px 20px;">
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="padding-bottom:6px;">
<div style="font-size:11px;letter-spacing:2px;color:#ff6600;font-weight:700;text-transform:uppercase;margin-bottom:6px;">{label}</div>
<div style="font-size:22px;font-weight:700;color:#000000;margin-bottom:14px;line-height:1.25;">{headline}</div>
{body}
</td></tr>
<tr><td align="center" style="padding:18px 0 6px 0;">{img}</td></tr>
<tr><td style="padding:6px 0 0 0;">
<div style="font-size:13px;color:#666;line-height:1.5;font-style:italic;text-align:center;">{caption}</div>
</td></tr>
</table>
</td></tr>
"""

s1 = section(
    "Pitch 1 of 6 &bull; BTC vs QQQ",
    "Every BTC/QQQ divergence has resolved with BTC catching up violently. We're in the fifth one now.",
    """<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Since May 2021, the Nasdaq (QQQ) has returned <strong>+125%</strong>. Bitcoin has returned <strong>+62%</strong> — roughly half. Their 90-day return correlation collapsed to <strong>0.18</strong> in late 2024, the deepest divergence since 2022. It's now rebuilding, but the price gap hasn't closed.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Look at the chart. Every shaded period is a divergence: China ban / taper fear in 2021, rate hikes + Luna / FTX in 2022, SVB in 2023. In every case, BTC eventually ripped to close the gap — usually within one to two quarters.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
<strong>Four divergences. Four resolutions. Same direction.</strong> The AI-mania divergence is the fifth.
</div>""",
    "ch1",
    "BTC indexed (orange) vs QQQ indexed (blue), May 2021 = 100. Shaded red regions mark divergence periods. Bottom: 90-day rolling return correlation."
)

s2 = section(
    "Pitch 2 of 6 &bull; Silver/Gold Lag",
    "Silver did nothing for two years. Then ran +111% in eight weeks. BTC is silver now.",
    """<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
From January 2023 through April 2025, gold ripped to ATHs. Silver did <strong>nothing</strong>. The lag spread between gold and silver hit <strong>49 index points</strong> — the widest gap in years.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Then silver broke. Eight weeks ending January 2026: <strong>SLV +111%</strong>. It broke $50 for the first time since 1980. The total silver move since Jan 2023: <strong>+252%</strong>, while gold returned +154%. Silver caught up — and overshot.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
<strong>BTC has been silver since mid-2025.</strong> Gold ran. M2 grew. AI stocks ripped. BTC drifted. When silver moved, it moved in eight weeks. BTC is closer to that breaking point than at any moment since the ETF launch.
</div>""",
    "ch2",
    "Gold (yellow) vs Silver (grey), indexed January 2023 = 100. Cream-shaded period: 2+ years of silver lag. Grey-shaded period: the 8-week silver melt-up."
)

s3 = section(
    "Pitch 3 of 6 &bull; Gold Leads BTC ~6 Months",
    "Gold is at all-time highs. BTC hasn't responded yet. It always does.",
    """<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Cross-correlation analysis on 2022-2026 daily data: gold returns lead BTC returns at an optimal lag of roughly <strong>6 to 8 months</strong>. Every major gold breakout in this window has been followed by a BTC breakout, six months delayed.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Overlay gold shifted +180 days forward onto BTC's chart. The shapes match. Right now, gold is at an all-time high and BTC is well below its September 2025 ATH. The pattern implies a BTC target of <strong>~$121,000</strong> — about <strong>48% above today's ~$82K</strong>.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
<strong>BTC at $121K and HYPE at $60 are not independent assumptions.</strong> The same macro tape delivers both.
</div>""",
    "ch3",
    "BTC actual price (orange) vs gold price shifted +180 days forward (dashed yellow). Gold's recent ATHs project to a BTC target near $121K."
)

s4 = section(
    "Pitch 4 of 6 &bull; M2 Money Supply",
    "BTC has tracked M2 for five years. Today's gap is the widest in that window.",
    """<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
US M2 money supply correlated with BTC at <strong>0.55</strong> from 2020-2023. (Global M2 + BTC correlation is typically cited at 0.85-0.90 in research.) M2 has continued to grow through 2025-2026 — currently <strong>+3.9% YoY and accelerating.</strong>
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
But BTC has stalled. M2 keeps making fresh highs while BTC trades in a wide range below its peak. The bottom panel shows M2 YoY growth ticking back above zero with momentum — historically the "BTC-bullish" regime.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
BTC catches up to M2 expansion with a <strong>60-90 day lag</strong>. M2 expansion is accelerating, not slowing. Either the historical relationship breaks for the first time in five years — or BTC closes the gap.
</div>""",
    "ch4",
    "Top: US M2 money supply (blue) vs BTC price (orange). Red shading: current decoupling. Bottom: M2 YoY % change — back above 0% and accelerating."
)

s5 = section(
    "Pitch 5 of 6 &bull; What's Holding BTC Back?",
    "The yen carry trade is the governor. It's stabilizing — which is exactly when BTC bids hard.",
    """<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
USD/JPY at <strong>156.65</strong> today, off the August 2024 peak of <strong>161.6</strong>. Still loaded, but the yen has stopped weakening.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
The case study: August 2024. Yen spiked 10% in two weeks. BTC dropped <strong>20% in 48 hours</strong> as global carry positions unwound. The shaded vertical band on the chart shows it. The risk to BTC isn't a slow yen recovery — it's a fast one.
</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
The setup right now: <strong>yen drifting, not spiking.</strong> BoJ guidance dovish. USD/JPY rolling slowly back toward the 150s. That's the regime where BTC inherits the unwinding liquidity gracefully.
</div>""",
    "ch5",
    "Top: BTC price. Bottom: USD/JPY inverted (line up = yen strength). Grey shaded band: the August 2024 yen spike and BTC -20% crash."
)

# Pitch 6 — two charts plus table
img6a = f'<img src="data:image/png;base64,{charts["ch6a"]}" alt="AI stock returns" width="640" style="width:100%;max-width:640px;height:auto;display:block;border:1px solid #e5e5e5;border-radius:4px;margin:0 auto;" />'
img6b = f'<img src="data:image/png;base64,{charts["ch6b"]}" alt="AI stock valuations" width="640" style="width:100%;max-width:640px;height:auto;display:block;border:1px solid #e5e5e5;border-radius:4px;margin:0 auto;" />'

s6 = f"""
<!-- ==================== Pitch 6 of 6 — AI stocks ==================== -->
<tr><td bgcolor="#ffffff" style="background-color:#ffffff;padding:30px 20px 10px 20px;">
<table width="100%" cellpadding="0" cellspacing="0" border="0">
<tr><td style="padding-bottom:6px;">
<div style="font-size:11px;letter-spacing:2px;color:#ff6600;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Pitch 6 of 6 &bull; AI Stocks Stretched</div>
<div style="font-size:22px;font-weight:700;color:#000000;margin-bottom:14px;line-height:1.25;">AI stocks are priced for perfection. This isn't a crash call — it's a "smart money takes profits at extremes" call.</div>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Twelve-month returns: <strong>SOXL +996%, MU +756%, AMD +329%, GOOGL +149%, AVGO +94%, NVDA +80%</strong>. The semi names ran 80-1000% in a single year. Retail accounts are stuffed with profits that haven't been taken yet.
</div>
</td></tr>
<tr><td align="center" style="padding:18px 0 6px 0;">{img6a}</td></tr>
<tr><td style="padding:6px 0 18px 0;">
<div style="font-size:13px;color:#666;line-height:1.5;font-style:italic;text-align:center;">12-month total returns for the 9 most-discussed AI / semi names. Red = extreme (above 50%).</div>
</td></tr>

<tr><td style="padding:0 0 6px 0;">
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
Now look at the valuations. Even *forward* P/Es — which already assume analyst earnings estimates hit — are baking in massive growth:
</div>
</td></tr>
<tr><td align="center" style="padding:6px 0 6px 0;">{img6b}</td></tr>
<tr><td style="padding:6px 0 18px 0;">
<div style="font-size:13px;color:#666;line-height:1.5;font-style:italic;text-align:center;">Red bars = current trailing P/E. Orange = forward P/E (assumes analyst estimates hit). Green dashed = S&P 500 long-run average (~25).</div>
</td></tr>

<tr><td style="padding:6px 0 0 0;">
{stocks_table}
</td></tr>

<tr><td style="padding:18px 0 0 0;">
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:10px;">
<strong>What this says:</strong>
</div>
<ul style="font-size:15px;line-height:1.7;color:#1a1a1a;margin:0 0 12px 22px;padding:0;">
  <li><strong>AMD at 148x trailing</strong> is the cleanest "multiple compression on a miss" setup in the market.</li>
  <li><strong>PLTR at 145x trailing and 96x forward</strong> is priced like a SaaS IPO, not a 22-year-old contractor.</li>
  <li><strong>MU's 6.4x forward P/E</strong> isn't cheap. It means analysts are extrapolating peak-cycle earnings forever. Memory cycles always end the same way.</li>
  <li>The "safe" mega-caps that have <strong>already corrected</strong> — META (-6%), MSFT (-9%) — are reporting fine and trading near 22x. The market is already rotating away from the obvious overbought names.</li>
</ul>
<div style="font-size:15px;line-height:1.7;color:#1a1a1a;margin-bottom:0;border-left:4px solid #ff6600;background:#fff5ee;padding:12px 14px;">
<strong>This is not where you add — this is where you trim and rotate to coiled assets.</strong>
</div>
</td></tr>

</table>
</td></tr>
"""

# Wrap it all
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Tuesday Thesis — May 13, 2026</title>
</head>
<body style="margin:0;padding:0;background-color:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#1a1a1a;line-height:1.6;">

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#ffffff;">
<tr><td align="center">
<table width="680" cellpadding="0" cellspacing="0" border="0" style="max-width:680px;width:100%;">

<tr><td bgcolor="#000000" style="background-color:#000000;padding:30px 20px;text-align:center;border-bottom:4px solid #ff6600;">
  <div style="font-size:11px;letter-spacing:3px;color:#ff6600;font-weight:700;text-transform:uppercase;">The Tuesday Thesis &bull; May 13, 2026</div>
  <div style="font-size:30px;font-weight:700;color:#ffffff;line-height:1.2;margin-top:10px;">BTC/HYPE Are Coiled. AI Stocks Are Stretched.</div>
  <div style="font-size:16px;color:#cccccc;margin-top:12px;line-height:1.55;">Six charts. Six setups that historically resolve one way. Real data from FRED, Polygon, Alpha Vantage, Finnhub.</div>
</td></tr>

<tr><td bgcolor="#ffffff" style="background-color:#ffffff;padding:20px;">
  <div style="font-size:15px;line-height:1.75;color:#1a1a1a;">
  Every macro indicator that has historically led BTC is at all-time highs — gold, M2, silver. The things suppressing BTC are stabilizing — yen, rate fear. The AI stocks soaking up all the risk capital are trading at multiples that price in flawless execution.
  </div>
  <div style="font-size:15px;line-height:1.75;color:#1a1a1a;margin-top:10px;">
  Capital rotation isn't a forecast. It's a foregone conclusion. The only variable is when.
  </div>
</td></tr>

{s1}
{s2}
{s3}
{s4}
{s5}
{s6}

<!-- THE TRADE -->
<tr><td bgcolor="#0a0a0a" style="background-color:#0a0a0a;padding:30px 20px;color:#ffffff;">
  <div style="font-size:11px;letter-spacing:3px;color:#ff6600;font-weight:700;text-transform:uppercase;">The Setup &bull; What This Means For RD</div>
  <div style="font-size:26px;font-weight:700;color:#ffffff;line-height:1.2;margin-top:10px;margin-bottom:20px;">If the macro resolves the way it always has, here's the path.</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td width="33%" bgcolor="#111111" style="background-color:#111111;padding:18px;vertical-align:top;">
      <div style="font-size:12px;color:#888;letter-spacing:1.5px;text-transform:uppercase;">BTC Target</div>
      <div style="font-size:28px;font-weight:700;color:#F7931A;margin:6px 0;">$121K</div>
      <div style="font-size:13px;color:#bbb;line-height:1.5;">Implied by gold +180d pattern. +48% from current.</div>
    </td>
    <td width="33%" bgcolor="#111111" style="background-color:#111111;padding:18px;vertical-align:top;">
      <div style="font-size:12px;color:#888;letter-spacing:1.5px;text-transform:uppercase;">HYPE Target</div>
      <div style="font-size:28px;font-weight:700;color:#4ade80;margin:6px 0;">$60</div>
      <div style="font-size:13px;color:#bbb;line-height:1.5;">Just back to Sept 2025 ATH. +47% from $41.33.</div>
    </td>
    <td width="33%" bgcolor="#111111" style="background-color:#111111;padding:18px;vertical-align:top;">
      <div style="font-size:12px;color:#888;letter-spacing:1.5px;text-transform:uppercase;">RD Share</div>
      <div style="font-size:28px;font-weight:700;color:#ffffff;margin:6px 0;">$0.00251</div>
      <div style="font-size:13px;color:#bbb;line-height:1.5;">+47% from today, plus 13 weeks of dividends.</div>
    </td>
  </tr>
  </table>

  <div style="font-size:15px;color:#dddddd;line-height:1.7;margin-top:24px;border-left:4px solid #ff6600;padding:10px 14px;background:#1a1a1a;">
  <strong style="color:#ffffff;">The dividend you get while you wait:</strong> $0.00002 per week &times; 13 weeks &asymp; $0.00026 of additional RoC income per share, regardless of share-price path.
  </div>
</td></tr>

<tr><td bgcolor="#ffffff" style="background-color:#ffffff;padding:20px;text-align:center;font-size:12px;color:#666;line-height:1.6;">
Sources: FRED (M2), Polygon.io (equities, RSI), Alpha Vantage (FX, BTC), Finnhub (P/E, fundamentals), FMP (historical ratios). Data pulled May 11, 2026. Not investment advice. RD distributions are Return of Capital under IRC &sect;301(c)(2); consult your CPA.
</td></tr>

</table>
</td></tr>
</table>

</body>
</html>"""

out_path = os.path.join(OUT, "email-sections.html")
with open(out_path, "w") as f:
    f.write(html)
print(f"Saved: {out_path}")
print(f"File size: {os.path.getsize(out_path) / 1024:.0f} KB")
