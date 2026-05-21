/* =============================================================================
   AI SHORT-SIGNAL SYSTEM — data config
   -----------------------------------------------------------------------------
   This file drives the entire dashboard. To extend the system:
     - add a ticker  -> add an entry to TICKERS
     - add a signal  -> add an object to a signals[] array
     - add a group   -> just use a new `group` string; the UI renders it
   Status reflects the SHORT thesis:
     na     = not assessed
     intact = trend healthy / no short (bullish for the stock)
     watch  = warning sign emerging
     short  = short-trigger firing
   `weight` (1-3) sets how much a signal moves the composite score (Tier-1 = 3).
   Seed readings are AS OF 2026-05-20. Numeric, fast-moving fields are meant to
   be refreshed (manually, or by automation writing data/live.json — see DEPLOY).
   Provenance: v = independently web-verified; u = user/feed-provided (verify);
               r = real from filings; n = normalized/illustrative.
   ============================================================================= */

const ASOF = "2026-05-20";

/* ---------- GLOBAL MACRO & CYCLE LAYER (affects every name) ---------- */
const MACRO = [
  { group: "AI demand engine", id: "cap_rev", name: "Hyperscaler capex revision", weight: 3,
    plain: "Are the big cloud buyers raising or cutting their AI spending plans?",
    reading: "$725B '26, +77% YoY; 3 of 4 RAISED", status: "intact", prov: "v",
    source: "MSFT/AMZN/GOOG/META calls", trigger: "First flat/down guide" },
  { group: "AI demand engine", id: "cap_react", name: "Market reaction to capex", weight: 3,
    plain: "Is the market rewarding or punishing more spending?",
    reading: "Meta −9% on raised guide — first rebellion", status: "watch", prov: "v",
    source: "price reaction to prints", trigger: "Capex raises consistently sell off" },
  { group: "AI demand engine", id: "cap_sales", name: "Capex-to-sales (untenable?)", weight: 2,
    plain: "How much of revenue is being plowed into buildout?",
    reading: "ORCL ~86%, META ~54%, MSFT ~47%", status: "watch", prov: "v",
    source: "10-Qs", trigger: "Forces a financing/FCF reckoning" },
  { group: "AI demand engine", id: "ai_roi", name: "AI revenue run-rate / ROI proxy", weight: 2,
    plain: "Is the spending actually producing returns yet?",
    reading: "Run-rates rising; ROI gap still open", status: "intact", prov: "u",
    source: "hyperscaler AI disclosures", trigger: "AI rev flatlines while capex climbs" },

  { group: "Memory/storage pricing chain", id: "dram_spot", name: "DRAM spot price", weight: 3,
    plain: "Spot is the first place a memory cycle turns.",
    reading: "Still firm / rising", status: "intact", prov: "v",
    source: "TrendForce/DRAMeXchange (weekly)", trigger: "Spot rolls while contract still up" },
  { group: "Memory/storage pricing chain", id: "dram_contract", name: "DRAM contract momentum", weight: 3,
    plain: "The size of each quarter's price increase — is it shrinking?",
    reading: "+58–63% Q2 (decel from +90–95% Q1); PC DRAM slowed Apr", status: "watch", prov: "v",
    source: "TrendForce (monthly)", trigger: "QoQ increase decelerates → flat" },
  { group: "Memory/storage pricing chain", id: "nand", name: "NAND / flash pricing", weight: 2,
    plain: "Same cycle logic for flash memory (SSDs).",
    reading: "+70–75% Q2; sold-out conditions", status: "intact", prov: "v",
    source: "TrendForce", trigger: "Momentum decelerates" },
  { group: "Memory/storage pricing chain", id: "hbm", name: "HBM sold-out status", weight: 2,
    plain: "High-bandwidth memory for AI — booked solid or loosening?",
    reading: "Sold out 2026 (binding contracts)", status: "intact", prov: "v",
    source: "earnings calls", trigger: "No longer fully booked; HBM4 pricing soft" },
  { group: "Memory/storage pricing chain", id: "ssd_hdd", name: "SSD/HDD cost gap", weight: 1,
    plain: "Drives the storage (Seagate/WDC) demand backdrop.",
    reading: "Gap blew out to ~16x; HDDs sold out 2026", status: "intact", prov: "v",
    source: "industry pricing", trigger: "Gap narrows / hyperscalers slow orders" },

  { group: "Semiconductor cycle", id: "btb", name: "SEMI book-to-bill", weight: 2,
    plain: "Equipment orders vs shipments — above 1.0 is expansion.",
    reading: "—", status: "na", prov: "u",
    source: "SEMI (monthly)", trigger: "Falls below 1.0 and trending down" },
  { group: "Semiconductor cycle", id: "sox_rs", name: "SOX relative strength", weight: 2,
    plain: "Is the chip sector leading or lagging the market?",
    reading: "Leading; watch for lower highs", status: "intact", prov: "u",
    source: "PHLX Semi index", trigger: "Underperforms SPX on lower highs" },
  { group: "Semiconductor cycle", id: "sox_breadth", name: "SOX breadth (% > 200dma)", weight: 1,
    plain: "Are most chip names healthy, or just a few?",
    reading: "—", status: "na", prov: "u",
    source: "breadth data", trigger: "Narrowing while index holds up" },

  { group: "Liquidity & macro", id: "real_rate", name: "Real 10Y yield (TIPS)", weight: 2,
    plain: "The discount rate on long-duration growth stocks.",
    reading: "—", status: "na", prov: "u",
    source: "FRED DFII10", trigger: "Spiking = multiple compression" },
  { group: "Liquidity & macro", id: "credit", name: "HY credit spreads (OAS)", weight: 2,
    plain: "Stress in risky credit — leads equity risk-off.",
    reading: "—", status: "na", prov: "u",
    source: "FRED BAMLH0A0HYM2", trigger: "Widening sharply" },
  { group: "Liquidity & macro", id: "dxy", name: "US dollar (DXY)", weight: 1,
    plain: "A strong dollar tightens global liquidity.",
    reading: "—", status: "na", prov: "u",
    source: "DXY", trigger: "Sharp spike" },
  { group: "Liquidity & macro", id: "ism", name: "ISM manufacturing", weight: 1,
    plain: "Broad cyclical demand pulse.",
    reading: "—", status: "na", prov: "u",
    source: "ISM (monthly)", trigger: "Rolling below 50" },

  { group: "Sentiment & positioning", id: "concentration", name: "AI-complex % of S&P", weight: 2,
    plain: "How top-heavy the index is — fragility gauge.",
    reading: "Near record concentration", status: "watch", prov: "u",
    source: "index weights", trigger: "Record % → any wobble self-reinforces" },
  { group: "Sentiment & positioning", id: "vix", name: "VIX / put-call", weight: 1,
    plain: "Fear gauge and option positioning.",
    reading: "—", status: "na", prov: "u",
    source: "CBOE", trigger: "Complacent lows into catalysts" },
];

/* ---------- universal froth/exhaustion signals attached to each ticker ---------- */
function froth(seed) {
  // seed: { ytd, ma200, issuance, target, si, ivp, react }  (status/reading per name)
  return [
    { group: "Froth & exhaustion", id: "ytd", name: "YTD gain (froth)", weight: 1,
      plain: "How stretched the year-to-date run is.", ...seed.ytd,
      source: "price", trigger: "Parabolic move = mean-reversion risk" },
    { group: "Froth & exhaustion", id: "ma200", name: "Distance above 200-day avg", weight: 2,
      plain: "How far price has run above its long-term trend line.", ...seed.ma200,
      source: "price vs 200dma", trigger: ">2 std-dev extension" },
    { group: "Froth & exhaustion", id: "issuance", name: "Equity issuance into strength", weight: 3,
      plain: "Companies selling stock near highs = insiders think it's rich.", ...seed.issuance,
      source: "S-1/424B/8-K, ATM filings", trigger: "Secondary or ATM launched near highs" },
    { group: "Froth & exhaustion", id: "target", name: "Price vs analyst target", weight: 2,
      plain: "Has the stock run past where analysts value it?", ...seed.target,
      source: "consensus target", trigger: "Price at/above mean target (re-rating spent)" },
    { group: "Froth & exhaustion", id: "si", name: "Short interest / borrow / squeeze", weight: 1,
      plain: "Risk that a short gets squeezed against you.", ...seed.si,
      source: "exchange SI, borrow desk", trigger: "High SI = squeeze fuel (manage size)" },
    { group: "Froth & exhaustion", id: "react", name: "Post-earnings reaction", weight: 2,
      plain: "Does the stock fade even on good prints?", ...seed.react,
      source: "price action", trigger: "Persistent beat-and-fade" },
  ];
}

/* ---------- TICKERS ---------- */
const TICKERS = {
  /* ===== Archetype A: cyclical-peak (memory/storage) ===== */
  MU: { name: "Micron", archetype: "Cyclical peak — memory", ytd: "≈ +130–170%", ytdProv: "u",
    thesis: "Memory at peak margins. Trade the PRICING roll, not the earnings. Earnings confirm far too late.",
    key: "DRAM/NAND spot inflection + contract momentum.",
    signals: [
      { group: "Tier 1 — pricing", name: "Cycle pricing roll (see macro chain)", weight: 3, reading: "Contract +58–63% Q2 (decel from +90–95% Q1); PC DRAM slowed Apr; spot still firm — watch for spot inflection", status: "watch", prov: "v", source: "TrendForce", trigger: "Spot turns / contract goes flat" },
      { group: "Tier 1 — pricing", name: "Gross-margin direction", weight: 3, reading: "~81% guided (Q2 FY26 print in Jun); near all-time peak for memory — first seq. dip off 81% = trigger", status: "intact", prov: "r", source: "MU earnings", trigger: "First sequential decline off peak" },
      { group: "Tier 2 — supply", name: "Industry capex (big-3)", weight: 2, reading: "MU ~$20B FY26; SK Hynix & Samsung also ramping — oversupply clock ticking for 2027–28", status: "watch", prov: "v", source: "MU/Samsung/SK Hynix", trigger: "Capex up = oversupply in 18–24 mo" },
      { group: "Tier 2 — supply", name: "Days of inventory", weight: 2, reading: "Lean / tight; channel still absorbing; Q3 FY26 print ~late June is next check", status: "intact", prov: "u", source: "MU 10-Q", trigger: "Inventory days rising" },
      { group: "Tier 2 — supply", name: "HBM sold-out erosion", weight: 2, reading: "Sold out 2026; SK Hynix & Samsung accelerating HBM capacity into 2027 — monitor booking commentary", status: "intact", prov: "v", source: "earnings", trigger: "Bookings loosen" },
      { group: "Tier 3 — valuation trap", name: "P/E on PEAK earnings", weight: 2, reading: "Fwd P/E ~8x on peak EPS — single-digit multiple on peak is the classic memory-cycle SELL tell", status: "watch", prov: "v", source: "market data", trigger: "Single-digit P/E on peak = SELL tell" },
    ],
    seed: {
      ytd:{reading:"≈ +130–170%",status:"watch",prov:"u"}, ma200:{reading:"Well extended; +130–170% YTD from memory cycle lows",status:"watch",prov:"u"},
      issuance:{reading:"None recent",status:"intact",prov:"u"}, target:{reading:"Below Street targets (upgrades ongoing); re-rating still absorbing",status:"intact",prov:"u"},
      si:{reading:"Moderate",status:"intact",prov:"u"}, react:{reading:"Strong reaction to Q2 FY26 print; next key print ~late June 2026 (Q3 FY26)",status:"intact",prov:"u"} } },

  SNDK: { name: "SanDisk", archetype: "Cyclical peak — NAND/flash", ytd: "≈ +509%", ytdProv: "v",
    thesis: "NAND supercycle, reframed as 'AI infra.' Spun from WDC Feb-2025; huge base effects. Peak-cycle euphoria.",
    key: "NAND pricing roll + the single-digit P/E-on-peak trap + the $3.2B raise.",
    signals: [
      { group: "Tier 1 — pricing", name: "NAND pricing momentum", weight: 3, reading: "+70–75% Q2; sold out", status: "intact", prov: "v", source: "TrendForce", trigger: "Momentum decelerates" },
      { group: "Tier 1 — pricing", name: "Gross-margin direction", weight: 3, reading: "78.4% (was 51% prior qtr) — blow-off", status: "watch", prov: "v", source: "SNDK Q3 FY26", trigger: "First sequential decline" },
      { group: "Tier 2 — fundamentals", name: "Revenue base effects", weight: 1, reading: "Q3 +251% YoY off post-spin base", status: "intact", prov: "v", source: "earnings", trigger: "YoY comps normalize → growth optics fade" },
      { group: "Tier 3 — valuation trap", name: "P/E on PEAK earnings", weight: 2, reading: "Fwd P/E ~7x FY27 on peak EPS — top setup", status: "watch", prov: "v", source: "market data", trigger: "Single-digit P/E on peak = SELL tell" },
    ],
    seed: {
      ytd:{reading:"≈ +509% YTD",status:"short",prov:"v"}, ma200:{reading:"Extremely extended (>3,000% off lows)",status:"short",prov:"v"},
      issuance:{reading:"$3.17B follow-on near highs",status:"short",prov:"v"}, target:{reading:"Price ≈ consensus target ($928 cluster) — re-rating spent",status:"watch",prov:"v"},
      si:{reading:"Elevated — squeeze risk",status:"watch",prov:"u"}, react:{reading:"+12% on last print (still rewarded)",status:"intact",prov:"v"} } },

  WDC: { name: "Western Digital", archetype: "Cyclical peak — storage/HDD", ytd: "≈ +160%", ytdProv: "v",
    thesis: "HDD up-cycle on AI cost-per-TB advantage. Record margins, sold out 2026 — but valuation caught up.",
    key: "HDD demand backdrop vs froth: margins at record, target only ~3% above price.",
    signals: [
      { group: "Tier 1 — demand", name: "HDD sold-out / LTAs", weight: 3, reading: "Sold out 2026 under long-term agreements", status: "intact", prov: "v", source: "earnings", trigger: "Hyperscaler LTAs not renewed" },
      { group: "Tier 1 — margin", name: "Gross-margin direction", weight: 3, reading: "Record ~46%", status: "watch", prov: "v", source: "earnings", trigger: "First sequential decline off record" },
      { group: "Tier 2 — supply", name: "HAMR / capacity ramp", weight: 1, reading: "Ramping 50TB+; supply still tight", status: "intact", prov: "v", source: "roadmap", trigger: "Supply catches demand" },
    ],
    seed: {
      ytd:{reading:"≈ +152–169% YTD",status:"watch",prov:"v"}, ma200:{reading:"Extended; −16% off peak",status:"watch",prov:"v"},
      issuance:{reading:"Divested SanDisk stake (deleveraging)",status:"intact",prov:"v"}, target:{reading:"Mean target only ~3% above price — re-rating spent",status:"short",prov:"v"},
      si:{reading:"Moderate; very volatile (48 5%+ moves/yr)",status:"watch",prov:"v"}, react:{reading:"Beat last print",status:"intact",prov:"v"} } },

  STX: { name: "Seagate", archetype: "Cyclical peak — storage/HDD", ytd: "≈ +135%", ytdProv: "v",
    thesis: "HDD twin of WDC. Same AI-storage tailwind, same late-cycle froth question.",
    key: "HDD demand vs valuation; analyst targets being chased upward (late-cycle behavior).",
    signals: [
      { group: "Tier 1 — demand", name: "HDD sold-out / LTAs", weight: 3, reading: "Strong; targets raised (Rosenblatt $750)", status: "intact", prov: "v", source: "earnings/analysts", trigger: "Order momentum slows" },
      { group: "Tier 1 — margin", name: "Gross-margin direction", weight: 3, reading: "Expanding", status: "intact", prov: "u", source: "earnings", trigger: "First sequential decline" },
    ],
    seed: {
      ytd:{reading:"≈ +135% YTD",status:"watch",prov:"v"}, ma200:{reading:"Extended after +65% April",status:"watch",prov:"v"},
      issuance:{reading:"None recent",status:"intact",prov:"u"}, target:{reading:"Analysts chasing price up (6 revisions in a day)",status:"watch",prov:"v"},
      si:{reading:"Moderate",status:"intact",prov:"u"}, react:{reading:"Strong reaction to prints",status:"intact",prov:"u"} } },

  /* ===== Archetype B: secular-growth de-rating (GPU/ASIC/networking) ===== */
  NVDA: { name: "NVIDIA", archetype: "Secular growth — GPU", ytd: "≈ +75–85%", ytdProv: "u",
    thesis: "Concentrated grower. Needs demand decel + margin crack + multiple compression. Squeeze-prone — prefer defined-risk options. ⚠ Q1 FY27 earnings MAY 21 AH.",
    key: "Trio: hyperscaler capex revision + DC sequential growth + gross margin. EARNINGS TOMORROW.",
    signals: [
      { group: "Tier 1 — thesis", name: "Data-center seq. growth", weight: 3, reading: "Q1 FY27 REPORTS TOMORROW (May 21 AH) — prior qtr +20% QoQ; bar is high; watch for decel", status: "watch", prov: "u", source: "NVDA Q1 FY27 earnings", trigger: "Sequential growth decelerating" },
      { group: "Tier 1 — thesis", name: "Gross margin trend", weight: 3, reading: "~74.9% prior qtr; Q1 FY27 guide/print TOMORROW — any compression off 74–75% is the trigger", status: "watch", prov: "u", source: "NVDA Q1 FY27 earnings", trigger: "Sustained compression off ~75%" },
      { group: "Tier 2 — confirming", name: "Inventory + commitments", weight: 2, reading: "Inv $25.8B (was $21.4B); commits $119B — building faster than rev growth", status: "watch", prov: "r", source: "10-Q", trigger: "Inventory builds faster than rev" },
      { group: "Tier 2 — confirming", name: "Vendor-financing loop", weight: 2, reading: "~$73B portfolio; $18.6B/qtr; $15.9B equity gains — CoreWeave dependency watch", status: "watch", prov: "r", source: "10-Q + customer filings", trigger: "Financed customer stumbles" },
      { group: "Tier 2 — confirming", name: "Custom-ASIC share", weight: 2, reading: "TPU/Trainium growing; 'not yet meaningful' — TOMORROW earnings will update this", status: "intact", prov: "v", source: "hyperscaler disclosures", trigger: "Measurable share loss" },
      { group: "Tier 2 — confirming", name: "GPU depreciation narrative", weight: 1, reading: "CoreWeave: 6-yr life 'conservative'", status: "intact", prov: "v", source: "customer commentary", trigger: "Useful-life narrative cracks" },
      { group: "Tier 3 — positioning", name: "Insider selling", weight: 1, reading: "$3.3B/18mo into $1,138 highs; zero buys — 10b5-1 but pace accelerating", status: "watch", prov: "v", source: "Form 4", trigger: "Acceleration / non-10b5-1 sales" },
      { group: "Tier 3 — positioning", name: "Expectations vs guide", weight: 1, reading: "Street above guide; Q1 FY27 prints TOMORROW — consensus ~$43B DC; high bar sets up fade risk", status: "watch", prov: "v", source: "consensus", trigger: "Unmeetable bar set" },
    ],
    seed: {
      ytd:{reading:"≈ +75–85% YTD (price ~$1,138; massive '26 run)",status:"watch",prov:"u"}, ma200:{reading:"Est. ~30–35% above 200-day avg at $1,138",status:"watch",prov:"u"},
      issuance:{reading:"None",status:"intact",prov:"u"}, target:{reading:"Near Street targets after run; re-rating largely spent",status:"watch",prov:"u"},
      si:{reading:"Low float-relative SI; extreme squeeze monster — size carefully",status:"watch",prov:"u"}, react:{reading:"Beat-and-fade 4 of last 5 prints; EARNINGS TOMORROW May 21 AH — the key print",status:"watch",prov:"v"} } },

  AVGO: { name: "Broadcom", archetype: "Secular growth — custom ASIC", ytd: "≈ +18–20%", ytdProv: "u",
    thesis: "The ASIC enabler — benefits as hyperscalers build custom chips (the NVDA bear case is the AVGO bull case).",
    key: "Custom-ASIC order momentum + the same capex master variable.",
    signals: [
      { group: "Tier 1 — thesis", name: "Custom-ASIC bookings", weight: 3, reading: "Strong hyperscaler ASIC demand", status: "intact", prov: "u", source: "earnings", trigger: "Order momentum slows" },
      { group: "Tier 1 — thesis", name: "Gross/operating margin", weight: 2, reading: "Healthy", status: "intact", prov: "u", source: "earnings", trigger: "Margin compression" },
      { group: "Tier 2 — confirming", name: "AI revenue mix", weight: 2, reading: "Rising share of total", status: "intact", prov: "u", source: "earnings", trigger: "AI mix growth stalls" },
    ],
    seed: {
      ytd:{reading:"≈ +18–20% YTD",status:"intact",prov:"u"}, ma200:{reading:"Near trend",status:"intact",prov:"u"},
      issuance:{reading:"None",status:"intact",prov:"u"}, target:{reading:"Below targets",status:"intact",prov:"u"},
      si:{reading:"Low",status:"intact",prov:"u"}, react:{reading:"Mixed",status:"intact",prov:"u"} } },

  AMD: { name: "AMD", archetype: "Secular growth — GPU challenger", ytd: "≈ +45–60%", ytdProv: "u",
    thesis: "NVDA's merchant-GPU challenger. Short thesis = MI-series share gains disappoint or AI GPU TAM optimism unwinds.",
    key: "MI-series hyperscaler wins + gross margin + the capex master variable.",
    signals: [
      { group: "Tier 1 — thesis", name: "MI-series share / wins", weight: 3, reading: "MI300X/325X winning sockets at MSFT, Meta, GOOG; AMD DC rev ~$3.7B Q1 FY26 (+57% YoY) — growing fast but NVDA still dominant", status: "watch", prov: "u", source: "AMD Q1 FY26 earnings", trigger: "Socket wins disappoint vs. hyped share-gain narrative" },
      { group: "Tier 1 — thesis", name: "Gross margin", weight: 2, reading: "~53% Q1 FY26; roughly flat QoQ — healthy but structurally 20+ pts below NVDA; MI-series mix is the lever", status: "intact", prov: "u", source: "AMD Q1 FY26 earnings", trigger: "Compression as MI-series ramp costs bite" },
    ],
    seed: {
      ytd:{reading:"≈ +45–60% YTD (~$165; AI GPU tailwind)",status:"watch",prov:"u"}, ma200:{reading:"Est. ~20–25% above 200-day avg — extended but not parabolic",status:"watch",prov:"u"},
      issuance:{reading:"None recent",status:"intact",prov:"u"}, target:{reading:"Near consensus target; upgrade cycle ongoing as MI-series gains traction",status:"intact",prov:"u"},
      si:{reading:"Moderate — options-driven positioning",status:"intact",prov:"u"}, react:{reading:"Strong on Q1 FY26 beat; DC acceleration rewarded; next print ~July 2026",status:"intact",prov:"u"} } },

  /* ===== Archetype C: parabolic momentum (test/optical small-caps) ===== */
  AEHR: { name: "Aehr Test Systems", archetype: "Parabolic momentum — test/burn-in", ytd: "≈ +379%", ytdProv: "v",
    thesis: "Small-cap riding AI-chip + optical test orders. Stock +379% while REVENUE FELL 27% YoY — pure order/booking story. Exhaustion-driven short.",
    key: "Order/booking run-rate is the whole driver. Watch revenue-vs-stock divergence + the ATM raise.",
    signals: [
      { group: "Tier 1 — the driver", name: "Order / booking run-rate", weight: 3, reading: "$41M follow-on order; $37M bookings/qtr", status: "intact", prov: "v", source: "8-K order PRs", trigger: "Order cadence slows / a quarter with no win" },
      { group: "Tier 1 — divergence", name: "Revenue vs stock", weight: 3, reading: "Rev −27% YoY while stock +379% — wide divergence", status: "watch", prov: "v", source: "earnings vs price", trigger: "Divergence persists into a print" },
      { group: "Tier 2 — concentration", name: "Customer concentration", weight: 2, reading: "Heavy reliance on a few hyperscale wins", status: "watch", prov: "v", source: "filings", trigger: "Lead customer pauses" },
    ],
    seed: {
      ytd:{reading:"≈ +379% YTD (most in <2 weeks)",status:"short",prov:"v"}, ma200:{reading:"Vertical / extreme extension",status:"short",prov:"v"},
      issuance:{reading:"ATM equity distribution agreement (Apr 8)",status:"short",prov:"v"}, target:{reading:"Valuation cited as key risk by bulls",status:"watch",prov:"v"},
      si:{reading:"Elevated; options 1.6x normal, calls 3:1",status:"watch",prov:"v"}, react:{reading:"+26% on a revenue MISS — sentiment-driven",status:"watch",prov:"v"} } },

  CIEN: { name: "Ciena", archetype: "Parabolic momentum — optical networking", ytd: "≈ +100%+", ytdProv: "u",
    thesis: "Optical networking for AI data centers. Doubled-plus on the interconnect theme; watch for order digestion.",
    key: "Optical order momentum + froth signals.",
    signals: [
      { group: "Tier 1 — the driver", name: "Optical order momentum", weight: 3, reading: "Strong on AI interconnect demand", status: "intact", prov: "u", source: "earnings", trigger: "Order momentum slows" },
      { group: "Tier 2 — margin", name: "Gross margin", weight: 2, reading: "—", status: "na", prov: "u", source: "earnings", trigger: "Compression" },
    ],
    seed: {
      ytd:{reading:"≈ doubled YTD",status:"watch",prov:"u"}, ma200:{reading:"Extended",status:"watch",prov:"u"},
      issuance:{reading:"—",status:"na",prov:"u"}, target:{reading:"—",status:"na",prov:"u"},
      si:{reading:"—",status:"na",prov:"u"}, react:{reading:"—",status:"na",prov:"u"} } },

  /* ===== Archetype D: turnaround / foundry ===== */
  INTC: { name: "Intel", archetype: "Turnaround — foundry", ytd: "≈ +150% (verify)", ytdProv: "u",
    thesis: "Turnaround/foundry re-rating. Execution-driven, not cycle-driven. Short thesis = foundry milestones slip or the re-rating outruns fundamentals.",
    key: "Foundry execution + margin recovery + FCF burn — different signal set entirely.",
    signals: [
      { group: "Tier 1 — execution", name: "Foundry milestones / yields", weight: 3, reading: "—", status: "na", prov: "u", source: "earnings/roadmap", trigger: "Node/yield slips, customer losses" },
      { group: "Tier 1 — financials", name: "Gross-margin recovery", weight: 2, reading: "—", status: "na", prov: "u", source: "earnings", trigger: "Recovery stalls" },
      { group: "Tier 2 — financials", name: "Capex burn / FCF", weight: 2, reading: "Heavy capex; FCF pressured", status: "watch", prov: "u", source: "10-Q", trigger: "FCF deteriorates without offset" },
    ],
    seed: {
      ytd:{reading:"≈ +150% YTD (verify)",status:"watch",prov:"u"}, ma200:{reading:"Extended after doubling",status:"watch",prov:"u"},
      issuance:{reading:"Prior dilution / external financing",status:"watch",prov:"u"}, target:{reading:"—",status:"na",prov:"u"},
      si:{reading:"—",status:"na",prov:"u"}, react:{reading:"Turnaround-narrative driven",status:"watch",prov:"u"} } },
};

/* attach the universal froth signals to every ticker + assign stable ids */
const _slug = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 24);
Object.entries(TICKERS).forEach(([sym, t]) => {
  t.sym = sym;
  t.signals = t.signals.concat(froth(t.seed)); delete t.seed;
  const seen = {};
  t.signals.forEach(s => { let id = s.id || _slug(s.name); if (seen[id]) id = id + "-" + (++seen[id]); else seen[id] = 1; s.id = id; });
});

const ARCHETYPE_ORDER = [
  "Cyclical peak — memory", "Cyclical peak — NAND/flash", "Cyclical peak — storage/HDD",
  "Secular growth — GPU", "Secular growth — custom ASIC", "Secular growth — GPU challenger",
  "Parabolic momentum — test/burn-in", "Parabolic momentum — optical networking",
  "Turnaround — foundry",
];

if (typeof module !== "undefined") module.exports = { ASOF, MACRO, TICKERS, ARCHETYPE_ORDER };
