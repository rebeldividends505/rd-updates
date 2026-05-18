# MASTER DATA SUMMARY — Hyperliquid Research Pull
**Date:** May 17, 2026  
**Output Directory:** `outputs/2026-05-19/data/`  
**Data Sources:** Hyperliquid public API (api.hyperliquid.xyz), web research, Alpha Vantage/FMP YTD snapshots

---

## ⚠️ HeyZibi API Status
All HeyZibi queries (zibi-*.json files) returned **401 Unauthorized**. No API key is configured in the environment. Data for those files was sourced from:
- Hyperliquid public REST API (`api.hyperliquid.xyz/info`)
- Web research (datawallet.com, financefeeds.com, hyperpc.app)

---

## 📁 Files Generated

| File | Source | Status |
|------|--------|--------|
| `ytd-snapshot-may19.json` | Alpha Vantage / FMP | ✅ Live data |
| `hl-public-stats-may17.json` | HL Public API | ✅ Live data |
| `zibi-hl-volume.json` | HeyZibi | ❌ 401 auth |
| `zibi-hl-fees-tvl.json` | HeyZibi | ❌ 401 auth |
| `zibi-hl-l1-metrics.json` | HeyZibi | ❌ 401 auth |
| `zibi-hl-oi-liquidations.json` | HeyZibi | ❌ 401 auth |
| `zibi-hl-competitive.json` | HeyZibi | ❌ 401 auth |
| `zibi-hype-tokenomics.json` | HeyZibi | ❌ 401 auth |
| `zibi-hip2-markets.json` | HL API + web research | ✅ Researched |
| `zibi-hip4-prediction.json` | Web research | ✅ Researched |
| `zibi-hl-ecosystem-full.json` | HL API + web research | ✅ Researched |

---

## 📊 YTD Performance Snapshot (as of May 13, 2026)

| Asset | YTD % | Start | Latest |
|-------|-------|-------|--------|
| XLE (Energy) | +29.7% | $44.42 | $57.63 |
| SLV (Silver) | +23.2% | $64.42 | $79.35 |
| NVDA | +21.1% | $186.49 | $225.83 |
| QQQ | +16.5% | $613.54 | $714.71 |
| SPY | +9.2% | $680.06 | $742.31 |
| GLD (Gold) | +8.6% | $396.31 | $430.50 |

**Content angle:** Gold, silver, and energy have all had strong runs in 2026 — "those trades already worked." The thesis is to rotate those gains into RD/HYPE for the next leg up.

---

## ⚡ Hyperliquid Live Market Data (May 17, 2026)

### Perpetuals
| Metric | Value |
|--------|-------|
| Total perp markets | 230 |
| 24h perp volume | **$2.01 billion** |
| Total open interest | **$6.21 billion** |
| 30-day perp volume | $172.6 billion |
| Cumulative all-time volume | $4.4 trillion |
| Perp DEX market share | **31.9%** |

**Top Perp Markets by 24h Volume:**
1. BTC — $943.5M vol / $2.15B OI
2. ETH — $345.1M vol / $1.30B OI
3. **HYPE — $325.7M vol / $951.5M OI** ← 3rd largest perp on HL
4. ZEC — $102.5M vol
5. SOL — $94.7M vol

### Spot Markets (HYPE price as of pull)
| Metric | Value |
|--------|-------|
| HYPE mark price | **$43.50** |
| HYPE 24h change | +6.5% (WOW/USDC leading) |
| BTC mark price | ~$78,017 |
| ETH mark price | ~$2,182 |

---

## 🟣 HIP-2: Native Spot Markets

**What is HIP-2?**  
HIP-2 (Hyperliquid Improvement Proposal 2) is the liquidity bootstrapping protocol for HIP-1 tokens. When a new token is deployed on Hyperliquid L1 via HIP-1 (the token creation standard), HIP-2 automatically seeds the order book with AMM-style liquidity funded by the deployer's reserve. This enables permissionless spot trading from day one — no external market makers required.

**Key Stats (May 17, 2026):**
| Metric | Value |
|--------|-------|
| Total spot markets listed | **297** |
| Canonical (named) markets | 1 (PURR/USDC) |
| HIP-2 non-canonical markets | 296 (@N notation, resolves via token registry) |
| Total tokens registered | 458 |
| Active markets with >$0 volume | **87** (29% of all listed) |
| Total 24h spot volume | **$105.4 million** |

**Top HIP-2 Markets by 24h Volume:**
| Token | 24h Vol | 24h Chg | Mark Price |
|-------|---------|---------|------------|
| WOW/USDC | $67.7M | +6.5% | $43.48 |
| NEKO/USDC | $17.2M | -0.2% | $78,042 |
| QUANT/USDC | $4.4M | +0.3% | $2,181 |
| BUDDY/USDC | $3.1M | -0.4% | $86.26 |
| NBT/USDC | $2.5M | +0.0% | $1.00 |
| FI/USDC | $1.8M | +6.4% | $43.48 |
| QQQ/USDC | $1.7M | +2.2% | $514.37 |
| SOON/USDC | $1.2M | +8.7% | $0.15 |
| PURR/USDC | $405K | +8.6% | $0.068 |

**Best Performers (24h):** SOON (+8.7%), PURR (+8.6%), WOW (+6.5%), HOOD (+6.5%), FI (+6.4%)

**Key Insight:** WOW/USDC alone accounts for 64% of total spot volume ($67.7M of $105.4M). Spot volume is ~5% of perp volume — spot is growing but still nascent.

---

## 🔮 HIP-4: Prediction Markets (Outcome Trading)

**What is HIP-4?**  
HIP-4 brings permissionless binary prediction markets to Hyperliquid HyperCore L1. Users trade YES or NO outcome contracts on real-world events — protocol upgrades, governance votes, macro milestones. Contracts are:
- **Fully collateralized** (no liquidation risk)
- **On-chain settled** (deterministic, sub-second finality)
- **No leverage** — pure binary directional bet
- **Portfolio margin compatible** — hold alongside perp positions in same account

**How to Create a Market:**  
Anyone can launch a prediction market by staking **1,000,000 HYPE**. No platform approval needed — fully permissionless, unlike Polymarket.

**Key Dates:**
- Announced on testnet: **February 2, 2026**
- First mainnet event contract: **May 4, 2026**

**Performance:**
| Metric | Value |
|--------|-------|
| First contract 24h volume | **$6.2 million** |
| First contract trades | 6.05 million contracts |
| Market share at launch | ~0.7% of all daily prediction market volume |
| Competitive comparison | "Orders of magnitude higher than prior governance-trading instruments on competing platforms" |

**Active Markets (May 2026):**
1. **HIP-4 Governance Implementation** — Will Hyperliquid successfully implement HIP-4 sharding by Q2 2026?  
   Launched May 4, 2026 | $6.2M opening volume

**Why It Matters for RD Content:**  
Hyperliquid isn't just a perp DEX anymore. It's building a full derivatives ecosystem: perps + spot + builder markets (HIP-3) + prediction markets (HIP-4). This is the platform thesis that justifies holding HYPE — every new product expansion captures more trading fee revenue, more HYPE burns, more ecosystem gravity.

---

## 🏗️ HIP-3: Builder-Deployed Perp DEXs

Third parties can deploy custom perpetual markets on HyperCore via HIP-3:

| DEX | Full Name | Assets |
|-----|-----------|--------|
| xyz | XYZ | 77 (stocks, commodities, forex, crypto indices) |
| flx | Felix Exchange | 15 |
| vntl | Ventuals | 15 |
| hyna | HyENA | 24 |
| km | Kinetiq Markets | 22 |
| cash | dreamcash | 15 |
| para | Paragon | 3 |

**8 builder DEXs total | 171 additional assets**

---

## 🌐 Full Ecosystem Activity Summary

| Product Layer | 24h Volume | Status |
|---------------|------------|--------|
| Perps (HyperCore native) | $2.01B | 230 markets |
| Spot markets (HIP-1/HIP-2) | $105.4M | 87 active of 297 |
| Builder perp DEXs (HIP-3) | TBD (not in public API) | 8 DEXs, 171 assets |
| Prediction markets (HIP-4) | ~$1-6M est. | 1 active contract |
| **TOTAL ESTIMATED** | **~$2.12B+** | — |

**Unique Users / Wallets:**  
- ~300,000+ monthly active wallets (30-day basis)
- 400,000+ cumulative unique users
- *(Exact data requires auth on stats-data.hyperliquid.xyz)*

**HYPE Token Metrics:**
| Metric | Value |
|--------|-------|
| Market cap | $10.66 billion |
| 24h volume | $315.27 million |
| Perp OI | $951.5 million |
| Total burned | $1.3B+ bought back and burned |
| Community wallet | 388M HYPE (untouched — potential airdrop signal) |
| DEX market share | 31.9% of all perp DEX volume |

---

## 🧠 Content Angles (for Emails/SMS)

1. **Ecosystem expansion angle:** Hyperliquid is no longer just a perp DEX — it has spot markets, builder-deployed perp exchanges (stocks, gold, commodities), and now prediction markets. This is why HYPE has platform value.

2. **Volume dominance:** $2.01B in 24h perp volume, 31.9% market share. #1 perp DEX by a wide margin.

3. **HIP-4 growth story:** Prediction markets just launched. Day one saw $6.2M. Polymarket does $50-100M/day at peak. Hyperliquid has massive TAM expansion ahead.

4. **HYPE as fee capture:** Every trade on every HIP layer burns HYPE or flows fees to token holders. More products = more fees = more value for HYPE holders.

5. **Rotation angle:** XLE +29.7% YTD, Silver +23.2% YTD, NVDA +21.1% YTD. Those trades worked. Smart money rotates into asymmetric opportunities — like HYPE at $43 vs $60 ATH target.

---

*Generated by Scout (RD Agent) — 2026-05-17*
