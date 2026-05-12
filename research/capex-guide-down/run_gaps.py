#!/usr/bin/env python3
"""Second wave — fill gaps in evidence for the capex guide-down debate."""
import os, sys, json, time
import concurrent.futures as cf
from pathlib import Path
import requests

PERP = os.environ["PERPLEXITY_API_KEY"]
OUT = Path(__file__).parent


def perp(q: str) -> str:
    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={"Authorization": f"Bearer {PERP}", "Content-Type": "application/json"},
                json={"model": "sonar-pro", "messages": [{"role": "user", "content": q}]},
                timeout=120,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            print(f"[{r.status_code}] {r.text[:200]}", file=sys.stderr)
        except Exception as e:
            print(f"err {attempt}: {e}", file=sys.stderr)
        time.sleep(2 + attempt * 3)
    return ""


queries = {
    "G1_consumer_sentiment_2026": (
        "What is the latest Conference Board Consumer Confidence Index and University of Michigan Consumer Sentiment "
        "reading in 2026? Give me exact monthly readings from January through May 2026. "
        "How do those compare to historical lows in 2008, 2011 (debt ceiling), 2020 (Covid), and 2022 (inflation peak)? "
        "Also: what is the latest US personal savings rate (BEA) and Q1 2026 retail sales growth (Commerce Department)? "
        "Cite specific numbers and release dates."
    ),
    "G2_mcdonalds_walmart_consumer": (
        "What did McDonald's, Walmart, Target, and Dollar General say about the US consumer in Q4 2025 and Q1 2026 earnings calls? "
        "Quote management commentary about the low and middle-income consumer. "
        "Cite same-store sales results and any guidance changes."
    ),
    "G3_openai_revenue_microsoft_oracle_dependence": (
        "Has OpenAI missed 2025 or 2026 revenue targets, and what reporting (Wall Street Journal, The Information, Reuters) has covered this? "
        "What percentage of Microsoft Azure backlog or remaining performance obligations (RPO) is attributable to OpenAI? "
        "What percentage of Oracle's $455B+ RPO is attributable to OpenAI/Stargate? "
        "Cite specific articles and analyst estimates with dates."
    ),
    "G4_hyperscaler_bond_issuance_2026": (
        "How much have Alphabet (Google), Meta, Microsoft, Amazon, and Oracle each issued in bonds during 2025 and 2026 "
        "to fund AI infrastructure capex? Give specific deal sizes, dates, tenors, and yields where possible. "
        "Has Meta's $30 billion bond deal in October 2025 been the largest tech bond issuance ever? "
        "How does total 2025-2026 hyperscaler debt issuance compare to prior years?"
    ),
    "G5_historical_capex_cuts_2001_2022": (
        "When telecom/tech companies cut capex guidance, what happened to their stocks in the following 3-6 months? "
        "Give specific examples with stock-price drawdown %: "
        "(1) Cisco capex/inventory write-downs in 2001, "
        "(2) Nortel Networks 2001, "
        "(3) Lucent Technologies 2001, "
        "(4) Meta's October-November 2022 'Year of Efficiency' capex pivot — what did the stock do in the 6 months before that pivot? "
        "(5) Snap Q3 2022 ad-revenue miss and what SNAP and ad-tech stocks did after. "
        "Cite stock prices, dates, and capex change amounts."
    ),
    "G6_btc_fed_easing_history": (
        "Quantify Bitcoin performance during each Fed easing cycle since BTC's creation: "
        "(a) July 2019 to October 2019 — three Fed cuts of 25bp each; what did BTC do in that period and the 6 months after? "
        "(b) March 2020 — emergency cuts to zero; what did BTC do over the following 12 months? "
        "(c) September 2024 to December 2024 — Fed cut 100bp; what did BTC do? "
        "(d) Any 2025 Fed cuts and BTC performance. "
        "Give starting price, ending price, and % move for each window. "
        "Also: what is the historical correlation between Fed easing and BTC returns?"
    ),
    "G7_retail_options_positioning_2026": (
        "What is current US retail investor positioning data as of April-May 2026? "
        "Specifically: "
        "(a) FINRA total margin debt level in April 2026 — what was the record and when? "
        "(b) Total 0DTE (zero-day-to-expiry) options volume on SPX and SPY — has it hit record levels in 2026? "
        "(c) Single-stock call option volume on Nvidia, AMD, Palantir, Tesla in early 2026; "
        "(d) AAII bullish sentiment % in April-May 2026; "
        "(e) NAAIM Exposure Index in April-May 2026; "
        "(f) Bank of America Global Fund Manager Survey AI/tech exposure in 2026. "
        "Cite exact numbers and dates."
    ),
    "G8_etf_flows_recession_odds": (
        "As of May 2026: "
        "(a) what are spot Bitcoin ETF (IBIT, FBTC, ARKB) cumulative inflows and recent April-May 2026 net flows? "
        "(b) what is the Kalshi or Polymarket prediction-market odds for a US recession by year-end 2026? Has it changed in the past 3 months? "
        "(c) What does the Fed funds futures curve imply for the number of Fed rate cuts in 2026? "
        "(d) What is the 2-year US Treasury yield and how has it moved in 2026? "
        "Cite specific data points and dates."
    ),
}


def run_one(item):
    k, q = item
    print(f"  -> {k}")
    return k, perp(q)


print("=== Filling gaps ===")
results = {}
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    for k, ans in ex.map(run_one, queries.items()):
        results[k] = ans

(OUT / "evidence_gaps.json").write_text(json.dumps(results, indent=2))
print(f"Saved {sum(1 for v in results.values() if v)} / {len(queries)} gap answers")
print("DONE")
