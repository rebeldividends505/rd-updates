import os, requests, json, pathlib

PERP = os.environ["PERPLEXITY_API_KEY"]
OUT = pathlib.Path(__file__).parent

searches = [
    ("sox_above_200ma", "What happened to the Philadelphia Semiconductor Index (SOX) historically when it traded 60%+ above its 200-day moving average? Give specific examples: magnitude of correction, timeline, was it fast (1-4 weeks) or slow (3-6 months)? Include 2000, 2022 examples. 2026 context: SOX currently 63% above its 200 DMA per Barchart."),
    ("six_week_rally_followthrough", "S&P 500 rose +16.2% in 6 weeks ending May 8 2026 from near all-time-high levels — the only top-20 6-week rally in 75 years NOT from a bear market bottom. Historically what happens to stocks in the next 30-60 days after a rally of this size from elevated (non-crash) starting levels? What are the RSI mean-reversion statistics? Any similar historical cases?"),
    ("nvda_miss_impact", "What happened to semiconductor stocks (AMD, AVGO, SOXL) in the 10 trading days AFTER Nvidia reported disappointing earnings or weak guidance? Give specific historical examples from 2022-2025. What is the average knockdown effect on the sector? Is it typically 5%, 10%, 15%?"),
    ("sell_may_seasonality", "Sell in May stock market data: what is the average S&P 500 return from May 15 to October 31 historically? What happens specifically to semiconductor/AI stocks in this period? Include: 2000 example, 2021 example. Also: what is the impact of monthly options expiration (May 16 2026) on stocks with extreme call-side open interest?"),
]

results = {}
for slug, query in searches:
    print(f">>> Searching: {slug}")
    r = requests.post("https://api.perplexity.ai/chat/completions",
        headers={"Authorization": f"Bearer {PERP}", "Content-Type": "application/json"},
        json={"model": "sonar-pro", "messages": [{"role": "user", "content": query}]},
        timeout=120)
    if r.status_code == 200:
        data = r.json()
        results[slug] = data["choices"][0]["message"]["content"]
        (OUT / f"{slug}.md").write_text(results[slug])
        print(f"=== {slug} ===")
        print(results[slug][:1200])
        print()
    else:
        print(f"Error {slug}: {r.status_code} {r.text[:300]}")

(OUT / "all_results.json").write_text(json.dumps(results, indent=2))
print(f"\nSaved {len(results)} results to {OUT}")
