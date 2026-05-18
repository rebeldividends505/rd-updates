#!/usr/bin/env python3
"""Comprehensive Hyperliquid ecosystem data pull via HeyZibi API + public APIs"""

import subprocess, json, requests, os, time

OUTPUT_DIR = os.path.expanduser("~/rd-updates-site/outputs/hl-ecosystem-data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

API_KEY = "ShjvHnKgOTrwLwXgqkOnGlvIEhUXRDiqEsfgdXOKCrhoxAxORavbTMUeTUvtJRMh"

def zibi(question, outfile):
    cmd = ['curl', '-s', '-X', 'POST', 'https://heyzibi.xyz/api/chat',
           '-H', 'Content-Type: application/json',
           '-H', f'x-api-key: {API_KEY}',
           '-d', json.dumps({"model": "zibi-default", "messages": [{"role": "user", "parts": [{"type": "text", "text": question}]}]})]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        text = ''
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('data: ') and line != 'data: [DONE]':
                try:
                    d = json.loads(line[6:])
                    if d.get('type') == 'text-delta':
                        text += d.get('delta', '')
                except:
                    pass
        if not text:
            text = f"[No response received]\nRAW STDOUT:\n{result.stdout[:2000]}\nSTDERR:\n{result.stderr[:500]}"
        path = os.path.join(OUTPUT_DIR, outfile)
        with open(path, 'w') as f:
            f.write(text)
        print(f"✅ {outfile}: {len(text)} chars")
        return text
    except Exception as e:
        err = f"[ERROR: {e}]"
        path = os.path.join(OUTPUT_DIR, outfile)
        with open(path, 'w') as f:
            f.write(err)
        print(f"❌ {outfile}: {e}")
        return err

# ─── ZIBI QUERIES ────────────────────────────────────────────────────────────

queries = [
    # HYPERLIQUID L1 CORE
    ("Give me a complete breakdown of Hyperliquid L1 blockchain metrics: TPS, block time, finality, total transactions processed all-time, validator count, staking stats, HyperBFT consensus details, and any recent protocol upgrades in 2026.",
     "hl-l1-core.txt"),

    ("What is Hyperliquid's total all-time cumulative trading volume across all products (perps, spot, HIP-3, HIP-4)? What is the current 24h volume breakdown by product? What is total TVL broken down by component?",
     "hl-volume-tvl.txt"),

    ("What is HYPE token complete tokenomics: total supply, circulating supply, tokens burned to date, daily/weekly burn rate, staking ratio, staking APY, treasury wallet balance, team allocation, and community wallet?",
     "hype-tokenomics.txt"),

    # HIP-2 SPOT MARKETS
    ("Give me comprehensive HIP-2 spot market data on Hyperliquid: total markets listed, 24h volume, 30d volume, TVL, top 20 tokens by volume, top 20 tokens by market cap, fastest growing tokens, and how HIP-2 liquidity bootstrapping works mechanically.",
     "hip2-spot-markets.txt"),

    ("What is the revenue model for Hyperliquid HIP-2 spot markets? How much fee revenue do spot markets generate vs perps? What percentage of fees go to HLP vault vs buyback fund vs validators?",
     "hip2-revenue.txt"),

    # HIP-3 BUILDER MARKETS
    ("Give me complete data on Hyperliquid HIP-3 builder perp markets: what is HIP-3, how many HIP-3 markets exist, who are the top builders, what is total HIP-3 volume and revenue (30d and all-time), how does revenue sharing work between builders and the protocol?",
     "hip3-builder-markets.txt"),

    ("Tell me everything about trade.xyz on Hyperliquid: 24h volume, 30d volume, all-time volume, open interest, active users, what assets they list (RWAs, stocks, commodities), revenue, growth trajectory, and how they compare to traditional brokers for 24/7 trading.",
     "hip3-tradexyz.txt"),

    ("What other HIP-3 builder applications exist on Hyperliquid besides trade.xyz? List all known builders, their focus areas (RWAs, prediction markets, options, etc), volumes, and status.",
     "hip3-other-builders.txt"),

    # HIP-4 PREDICTION MARKETS
    ("Give me complete data on Hyperliquid HIP-4 prediction markets (Outcome Trading): how does it work mechanically, what markets are currently live, what is the total volume since launch, daily volume, top performing markets, how it compares to Polymarket and Kalshi, and what's the revenue model?",
     "hip4-prediction-markets.txt"),

    ("Who are the main builders on Hyperliquid HIP-4? What is Outcomexyz? What other prediction market frontends exist? How much volume has each done?",
     "hip4-builders.txt"),

    # ECOSYSTEM DAPPS
    ("List ALL major dApps and protocols in the Hyperliquid ecosystem. Include: DeFi protocols (lending, liquid staking, yield), DEX aggregators, wallets, bridges, NFT platforms, gaming, AI agents, and any other categories. For each, give TVL, users, volume where available.",
     "ecosystem-dapps-full.txt"),

    ("What are the top Hyperliquid ecosystem protocols by TVL? Give me a ranked list with: name, category, TVL, 30d growth, key features, and whether they're built on HyperEVM or HyperCore.",
     "ecosystem-tvl-ranking.txt"),

    ("Tell me about Hyperliquid liquid staking: what is kHYPE from Kinetiq? What other liquid staking options exist? What are the APYs, TVLs, and how does liquid staked HYPE work?",
     "ecosystem-liquid-staking.txt"),

    ("What DeFi lending protocols exist on Hyperliquid? What is HyperLend? What other lending markets are live? TVL, rates, available assets?",
     "ecosystem-lending.txt"),

    ("What is HyperEVM? How does it integrate with HyperCore? What dApps are built on HyperEVM specifically? What EVM-native protocols have deployed there?",
     "hyperevm-ecosystem.txt"),

    # COMPETITORS
    ("Compare Hyperliquid to dYdX v4 in detail: 30d volume, fees, open interest, market share, active users, TVL, architecture differences, token performance, and why traders prefer one over the other.",
     "competitor-dydx.txt"),

    ("Compare Hyperliquid to GMX v2 in detail: 30d volume, fees, TVL, active users, token performance (GMX vs HYPE), revenue model differences, and competitive positioning.",
     "competitor-gmx.txt"),

    ("Compare Hyperliquid to Vertex Protocol: volume, fees, market share, user base, unique features, and competitive analysis.",
     "competitor-vertex.txt"),

    ("Compare Hyperliquid to Polymarket and Kalshi specifically for prediction markets: volume comparison, user base, fee structures, types of markets available, and why HIP-4 is positioned differently.",
     "competitor-prediction-markets.txt"),

    ("Who are ALL of Hyperliquid's competitors across its full product suite (perps DEX, spot DEX, prediction markets, L1 blockchain)? Give a comprehensive competitive landscape including centralized exchanges (Binance, Coinbase, Bybit) losing market share to Hyperliquid.",
     "competitor-full-landscape.txt"),

    ("What is Hyperliquid's market share trend over the last 12 months? How has it grown vs competitors? What percentage of all onchain perpetual volume does it now control?",
     "hl-market-share-trend.txt"),

    # INSTITUTIONAL + MACRO
    ("What institutional players are now involved with Hyperliquid? List ETFs (THYP, BHYP), validators, custodians, market makers, and any institutional partnerships announced in 2025-2026.",
     "hl-institutional.txt"),

    ("What is the Hyperliquid Assistance Fund? How much HYPE has been bought back and burned? What is the daily/weekly/monthly burn rate? How does this compare to other deflationary crypto assets?",
     "hl-buyback-burn.txt"),
]

print(f"Starting {len(queries)} Zibi queries...\n")
for i, (question, outfile) in enumerate(queries, 1):
    print(f"[{i}/{len(queries)}] Querying: {outfile}")
    zibi(question, outfile)
    time.sleep(1)  # brief pause between requests

# ─── PUBLIC API PULLS ─────────────────────────────────────────────────────────

print("\n--- Running Hyperliquid Public API pulls ---\n")

# Full metaAndAssetCtxs
try:
    r = requests.post('https://api.hyperliquid.xyz/info', json={"type": "metaAndAssetCtxs"}, timeout=30)
    data = r.json()
    with open(os.path.join(OUTPUT_DIR, 'api-meta-asset-ctxs.json'), 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ api-meta-asset-ctxs.json: saved")

    # All perps ranked
    if isinstance(data, list) and len(data) >= 2:
        meta = data[0].get('universe', [])
        ctxs = data[1]
        assets = []
        for m, c in zip(meta, ctxs):
            try:
                oi = float(c.get('openInterest', 0)) * float(c.get('markPx', 0))
                vol = float(c.get('dayNtlVlm', 0))
                assets.append({
                    'name': m['name'],
                    'oi_usd': round(oi),
                    'vol_24h': round(vol),
                    'mark_price': c.get('markPx'),
                    'funding': c.get('funding'),
                    'open_interest_raw': c.get('openInterest')
                })
            except:
                pass
        assets.sort(key=lambda x: x['oi_usd'], reverse=True)
        with open(os.path.join(OUTPUT_DIR, 'api-all-perps-ranked.json'), 'w') as f:
            json.dump({'total_perps': len(assets), 'assets': assets}, f, indent=2)
        print(f"✅ api-all-perps-ranked.json: {len(assets)} perps saved")
except Exception as e:
    print(f"❌ perps API error: {e}")

# Spot markets
try:
    r2 = requests.post('https://api.hyperliquid.xyz/info', json={"type": "spotMetaAndAssetCtxs"}, timeout=30)
    with open(os.path.join(OUTPUT_DIR, 'api-spot-markets.json'), 'w') as f:
        json.dump(r2.json(), f, indent=2)
    print(f"✅ api-spot-markets.json: saved")
except Exception as e:
    print(f"❌ spot markets API error: {e}")

# Additional: global stats
try:
    r3 = requests.post('https://api.hyperliquid.xyz/info', json={"type": "stats"}, timeout=30)
    with open(os.path.join(OUTPUT_DIR, 'api-global-stats.json'), 'w') as f:
        json.dump(r3.json(), f, indent=2)
    print(f"✅ api-global-stats.json: saved")
except Exception as e:
    print(f"ℹ️  api-global-stats.json: {e} (endpoint may not exist)")

# Additional: funding history / open interest
try:
    r4 = requests.post('https://api.hyperliquid.xyz/info', json={"type": "openInterest"}, timeout=30)
    with open(os.path.join(OUTPUT_DIR, 'api-open-interest.json'), 'w') as f:
        json.dump(r4.json(), f, indent=2)
    print(f"✅ api-open-interest.json: saved")
except Exception as e:
    print(f"ℹ️  api-open-interest: {e}")

print("\n--- All API pulls complete ---")
print(f"\nFiles saved to: {OUTPUT_DIR}")
print("\nALL DATA PULLS COMPLETE")
