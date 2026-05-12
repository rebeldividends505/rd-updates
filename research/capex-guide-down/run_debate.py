#!/usr/bin/env python3
"""
CAPEX Guide-Down Debate — research the 5-link causal chain for the
"AI capex will be guided down in 2026 → biggest BTC rotation since 2023" thesis.
Outputs evidence_raw.json with raw Perplexity answers per query.
"""
import os
import sys
import json
import time
import concurrent.futures as cf
from pathlib import Path
import requests

PERP = os.environ["PERPLEXITY_API_KEY"]
OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True, parents=True)


def perplexity_search(query: str, retries: int = 2) -> str:
    for attempt in range(retries + 1):
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {PERP}", "Content-Type": "application/json"},
                json={
                    "model": "sonar-pro",
                    "messages": [{"role": "user", "content": query}],
                },
                timeout=120,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            print(f"[{r.status_code}] {r.text[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"error attempt {attempt}: {e}", file=sys.stderr)
        time.sleep(2 + attempt * 3)
    return ""


# 5 links × focused composite questions (kept concise so Perplexity can cite specifics)
queries = {
    # LINK 1 — Consumer is slowing
    "L1_consumer_health": (
        "As of Q1 2026, what is the current state of the US consumer? "
        "Provide specific data with sources/dates for: "
        "(a) credit card delinquency rates (90+ days) — current level and historical comparison; "
        "(b) Conference Board consumer confidence and University of Michigan sentiment — current readings and how they compare to 2008/2020 lows; "
        "(c) US retail sales growth trend over the past 6 months; "
        "(d) personal savings rate; "
        "(e) McDonald's Q1 2026 same-store sales results and management commentary on the low-income consumer. "
        "Cite the exact numbers and report dates."
    ),
    # LINK 2 — Ad revenue is at risk
    "L2_ad_revenue_risk": (
        "What were the Q1 2026 earnings results and guidance for digital ad businesses? "
        "Specifically: "
        "(a) Alphabet/Google ad revenue growth rate and any deceleration commentary; "
        "(b) Meta advertising revenue growth and guide for Q2 2026; "
        "(c) Amazon advertising segment growth rate; "
        "(d) What percentage of Google, Meta, and Amazon revenue is consumer-facing advertising? "
        "(e) Are any sell-side analysts warning that a consumer slowdown will hit digital ad revenue in 2026? "
        "Cite specific analyst notes and earnings call language."
    ),
    # LINK 3 — The capex funding is fragile
    "L3_capex_funding": (
        "How are hyperscalers (Alphabet, Meta, Microsoft, Amazon, Oracle) funding their 2026 AI capex? "
        "Specifically: "
        "(a) How much in bonds/debt has Alphabet, Meta, Microsoft, and Oracle issued in 2025-2026 to fund AI infrastructure? Cite specific deal sizes and dates. "
        "(b) What is the total 2026 capex guide across the Mag7 hyperscalers? Is it near $700B? "
        "(c) Has OpenAI missed revenue targets in 2026, and what is OpenAI's share of Microsoft's and Oracle's RPO/backlog? Cite the WSJ or other reporting. "
        "(d) Have any Wall Street analysts (Goldman Sachs, Deutsche Bank, Morgan Stanley, Bernstein) explicitly warned that 2026 AI capex could be guided down? Quote them. "
        "(e) What is hyperscaler free cash flow vs capex in 2026 — is FCF turning negative?"
    ),
    # LINK 4 — Retail is dangerously overloaded
    "L4_retail_positioning": (
        "How extreme is retail investor positioning in AI/tech stocks as of April-May 2026? "
        "Specifically: "
        "(a) SOXL (3x semiconductor ETF) inflows and AUM in 2025-2026 — cite dollar amounts and year-over-year change; "
        "(b) 0DTE options volume on SPX and individual mega-cap tech names — are we at record retail call volume? "
        "(c) Margin debt at FINRA broker-dealers — current level and historical comparison; "
        "(d) AAII bullish sentiment, NAAIM exposure, and retail equity allocation surveys; "
        "(e) Has SOXL's price risen ~996% from its 2023 lows, and what does retail concentration in leveraged AI ETFs look like vs prior bubble peaks? "
        "Cite specific data with dates and sources."
    ),
    # LINK 5 — Historical precedent
    "L5_historical_precedent": (
        "What is the historical precedent for two patterns? "
        "(a) When hyperscaler/megacap capex has been guided DOWN, what happened to tech stock prices in the following 3-6 months? Use examples from 2001 dot-com (Cisco, Nortel, Lucent capex cuts), 2008-09, and 2022 (Meta, Snap capex cuts). Quote drawdown percentages. "
        "(b) When the Fed has begun an easing cycle (cut rates after a pause), what has Bitcoin done in the following 6-12 months? Cite specific cycles: 2019 mid-cycle cuts, March 2020 emergency cuts, and any 2024-2025 cuts. Quote BTC % moves and rotation flow data from crypto into stocks or vice versa. "
        "Be specific with dates and numbers."
    ),
    # CROSS-CUTTING — current state of the rotation
    "L6_current_rotation_signals": (
        "As of May 2026, what is the latest data showing capital rotation between AI/tech stocks and Bitcoin? "
        "Specifically: "
        "(a) Year-to-date 2026 performance of QQQ, SMH/SOXL, and Bitcoin; "
        "(b) Spot Bitcoin ETF (IBIT, FBTC) inflow/outflow data for April-May 2026; "
        "(c) Kalshi or Polymarket recession probability for 2026 — current level and trend; "
        "(d) Fed funds futures pricing for 2026 rate cuts — how many cuts are priced in for the rest of 2026? "
        "(e) Any reports of hedge funds or institutions rotating out of AI/tech into Bitcoin or away from BTC. "
        "Cite the latest data points with dates."
    ),
    # COUNTER-ARGUMENT — what does the bull case for sustained AI capex look like?
    "L7_bull_counter_case": (
        "Make the strongest BULL case that 2026 AI capex will NOT be guided down. "
        "Cite: "
        "(a) Hyperscaler cash reserves and ability to self-fund capex without revenue dependency; "
        "(b) Enterprise AI adoption data — Microsoft Azure AI revenue, AWS Bedrock, Google Cloud AI growth rates; "
        "(c) Why analysts believe AI capex is 'demand-pulled' not speculative — cite Mark Zuckerberg, Satya Nadella, Sundar Pichai recent statements; "
        "(d) Why this AI cycle is structurally different from 2000 dot-com (FCF positive, real revenue, etc.); "
        "(e) Are there any signs that AI inference demand is accelerating? "
        "Provide the most credible counter-evidence to the capex-guide-down thesis."
    ),
}


def run_one(item):
    k, q = item
    print(f"  -> {k}")
    return k, perplexity_search(q)


print("=== Querying Perplexity (parallel) ===")
evidence: dict[str, str] = {}
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for k, ans in ex.map(run_one, queries.items()):
        evidence[k] = ans

(OUT / "evidence_raw.json").write_text(json.dumps(evidence, indent=2))
print(f"\nSaved {sum(1 for v in evidence.values() if v)} / {len(queries)} successful answers")
print("DONE")
