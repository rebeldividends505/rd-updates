# QA Report — RD Tue May 19 Webinar v3.2-FINAL

**Build completed:** 2026-05-17
**Source:** instructions/may19-webinar/v3.2/RD-Tue-May19-v3.2-FINAL-FIX-ORDER.md
**Overrides applied:** User-supplied verified data (May 17 PM pull) takes precedence over numbers in the fix order where they differ.

---

## Verified data inputs used

| Metric | Value | Notes |
|---|---|---|
| Hyperliquid cumulative volume | $4.4 Trillion | Per user verified (not $4.62T from fix order draft) |
| Hyperliquid total OI | $6.18 Billion | Per user verified (not $38.7B from fix order draft) |
| Hyperliquid 24h volume | $2.08 Billion | Per user verified |
| Hyperliquid perp markets | 230 | Per user verified |
| Hyperliquid spot markets | 458 | Per user verified (not 297) |
| Hyperliquid active users | ~400K+ | Per user verified |
| HYPE price reference | $43.49 | May 17 |
| Warsh framing | "First Fed Chair confirmed in the crypto ETF era" | Per user verified (NOT "pro-Bitcoin Fed Chair") |
| Coinbase USDC deal date | May 15, 2026 | Per user verified (not May 14) |
| Bitwise framing | "Bitwise is staking HYPE through Bitwise Onchain Solutions" | Per user verified (NO FalconX validator claim) |
| CPI April 2026 YoY | 3.8% | BLS official (rounded from 3.81%) |
| Jan→Apr CPI delta | 141 bps | 2.39% → 3.8% |
| YTD SLV / GLD / XLE | +7.17% / +5.29% / +33.81% | May 17 yfinance |
| YTD NVDA / SMH / SOXL | +20.82% / +54.48% / +290.63% | May 17 yfinance |
| YTD BTC | -10.72% | May 17 yfinance |
| 30Y Treasury | 5.128% | FRED DGS30, May 17 |
| VIX | 18.43 | Crossed 18 warning threshold |

---

## Content QA checklist

### Catalyst table
- [x] **7 catalyst rows in table (not 5)** — verified in both email and elementor (7 data rows + 1 header)
- [x] May 7 — McElligott $2.6T gamma trap
- [x] May 12 — 21Shares THYP launches on Nasdaq
- [x] May 12 — BTC bull-bear indicator turns GREEN
- [x] May 13 — Warsh confirmed as Fed Chair (54-45), framed as "First Fed Chair confirmed in the crypto ETF era. Closest vote in modern era."
- [x] May 15 — Coinbase makes Hyperliquid its USDC home
- [x] May 15 — Bitwise BHYP launches on NYSE, with Bitwise Onchain Solutions framing (no FalconX validator claim)
- [x] May 15 (Fri) — Powell's 8-year term ends (orange-highlighted row preserved)

### Protocol Behind Your Shares (NEW section)
- [x] "Protocol Behind Your Shares" section present
- [x] Uses **$4.4 Trillion** cumulative volume figure
- [x] 8-row stats table with $4.4T, ~400K+ users, $6.18B OI, $2.08B daily, 230 perp, 458 spot, 24/31 validators, prediction markets Live
- [x] hyperliquid-market-share.png image embedded
- [x] Institutional callout uses "staking HYPE through Bitwise Onchain Solutions" (no FalconX)
- [x] Coinbase USDC mention
- [x] Anchorage Digital Bank named

### YTD section (Surgical Edit 3)
- [x] YTD paragraph rewritten with verified May 17 data
- [x] Uses **3.8% CPI** (April 2026)
- [x] Uses **5.128% 30Y Treasury**
- [x] Includes SOXL +291%, SMH +54%, NVDA +21%, Silver +7%, Gold +5%, BTC -11%
- [x] References "141 basis point re-acceleration in four months"
- [x] Why RD silver line updated — no longer says "Silver's stretched +21.9% YTD"; uses Gold/silver/energy/semis updated framing
- [x] YTD chart src swapped to soxl-ytd-insanity.png

### Webinar banner / bridge
- [x] Hero headline updated: "7 Days. 7 Catalysts."
- [x] Banner subhead updated: "$2.6T gamma trap loaded. Powell exits Friday. New Fed Chair confirmed. Two spot HYPE ETFs trading. Coinbase picks Hyperliquid for USDC. BTC indicator turns green."
- [x] Bridge headline: "Seven days ago we walked through the setup. Today seven catalysts have landed at once."
- [x] Bridge body updated with two ETFs (THYP May 12, BHYP May 15), Coinbase USDC, no "yesterday" stale reference

### Brand voice / framing rules
- [x] **No "pro-Bitcoin Fed Chair" language anywhere** — verified by grep (0 matches in email/elementor/sms)
- [x] **No "pro-BTC Fed" language** — verified
- [x] **No "first-ever HYPE ETF" / "first-ever spot HYPE" / "first-ever Hyperliquid ETF"** — verified (0 matches)
- [x] **No FalconX validator claim** — verified (0 matches in email/elementor/sms)
- [x] "First Fed Chair confirmed in the crypto ETF era" framing used consistently

### Preserved v3.1 content
- [x] "The Case For RD Right Now" eyebrow present in both email and elementor
- [x] "And If We're Early?" section present in both email and elementor
- [x] Shareholder Acknowledgment block intact
- [x] Gamma Trap section intact
- [x] Safety Case section intact
- [x] What We're Doing In Our Own Book block intact
- [x] Early Warning Dashboard intact
- [x] Forward Macro 5 Pillars intact (elementor "pro-BTC" cell label fixed to "the new Fed Chair")
- [x] HYPE Target Ladder at climax intact
- [x] Dean Box (505-322-7515) intact
- [x] 3-paragraph disclaimer intact

### SMS file
- [x] **No em dashes (—) in SMS** — verified by grep
- [x] **No en dashes (–) in SMS** — verified
- [x] 4 subject lines (primary, Warsh angle, comparison, convergence)
- [x] Primary SMS ~340 chars with 7 catalysts + Coinbase line
- [x] Shorter alt SMS ~220 chars
- [x] Uses "new Fed Chair" framing throughout (not "pro-Bitcoin")
- [x] Both SMSes link to https://rebeldividends.com/startwebinar/

### Charts (all 6 built)
- [x] charts/hyperliquid-market-share.png — $4.4T hero, 4 stat cards
- [x] charts/cpi-reacceleration.png — 6-month line, +141bp annotation, Nov25→Apr26
- [x] charts/30y-treasury-above-5.png — FRED DGS30 since 2000, current 5.128% annotated
- [x] charts/vix-threshold-crossing.png — 90-day VIX, 18/20 thresholds, current 18.43 annotated
- [x] charts/soxl-ytd-insanity.png — horizontal bars, SOXL +290.63% leading
- [x] charts/hype-target-ladder-may19.png — PLACEHOLDER labeled, regenerate Tuesday AM

---

## File manifest

```
outputs/2026-05-19/
├── email-v3.2-FINAL.html          (52K, edited from email.html)
├── elementor-v3.2-FINAL.html      (66K, edited from elementor.html)
├── sms-v3.2-FINAL.txt             (replaces sms.txt)
├── qa-report-v3.2.md              (this file)
└── charts/
    ├── hyperliquid-market-share.png
    ├── cpi-reacceleration.png
    ├── 30y-treasury-above-5.png
    ├── vix-threshold-crossing.png
    ├── soxl-ytd-insanity.png
    └── hype-target-ladder-may19.png
```

---

## Open items for Tuesday AM refresh (5 AM MDT)

1. **HYPE Target Ladder regenerate** — pull live HYPE price from CoinGecko + RD daily Gmail share price; rerun the ladder math; replace placeholder chart.
2. **YTD figures refresh** — flag drift >3pp from May 17 baseline (per Task 4.1 in fix order).
3. **VIX Tuesday level** — re-check; if it has crossed 20, update Early Warning Dashboard prose to red status.
4. **Hyperliquid stats refresh** — repull metaAndAssetCtxs; if shifted >5% from May 17, regenerate hyperliquid-market-share.png.
5. **Breaking news scan** — Hyperliquid / S&P / VIX news May 18–19; log to DEPLOYMENT-NOTES.txt.

## Permission checks still pending from Jason (per fix order Part 7)

1. Greenlight Coinbase + Bitwise in catalyst table (currently included).
2. HYPE Target Ladder placeholder accepted (will refresh Tuesday AM).
3. HeyZibi / HIP-4 — omitted from this build per worker bot guidance.
