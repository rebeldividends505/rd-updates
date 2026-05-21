#!/usr/bin/env python3
"""
signal_loader.py — shared utility for loading the AI Short-Signal model.

Loads data.js via node, applies live.json overrides, computes scores.
Imported by alert_engine.py, snapshot.py, and run_all.py.
"""
import json, re, subprocess, datetime as dt
from pathlib import Path

HERE      = Path(__file__).resolve().parent
DATA_JS   = HERE.parent / "js" / "data.js"
LIVE_JSON = HERE.parent / "data" / "live.json"

SCORE_VAL = {"intact": 0.0, "watch": 0.5, "short": 1.0, "na": None}
TICKERS   = ["MU", "SNDK", "WDC", "STX", "NVDA", "AVGO", "AMD", "AEHR", "CIEN", "INTC"]

# ---------------------------------------------------------------------------
def _load_via_node():
    script = (
        "const m=require(" + json.dumps(str(DATA_JS)) + ");"
        "console.log(JSON.stringify({ASOF:m.ASOF,MACRO:m.MACRO,TICKERS:m.TICKERS}));"
    )
    try:
        r = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
    except Exception as e:
        print(f"[signal_loader] node load failed: {e}")
    return None

def load_model():
    """Load seed model from data.js via node. Raises on failure."""
    m = _load_via_node()
    if m is None:
        raise RuntimeError(
            "Cannot load signal model — node.js required.\n"
            "Install: brew install node  (or nvm / system package)"
        )
    return m

# ---------------------------------------------------------------------------
def apply_live(model, live_path=LIVE_JSON):
    """Apply live.json overrides to model in-place. Safe if file missing."""
    try:
        live = json.loads(live_path.read_text())
    except FileNotFoundError:
        return model
    for key, val in live.get("readings", {}).items():
        scope, _, sig_id = key.partition(":")
        update = {k: v for k, v in val.items() if k in ("reading", "status")}
        if scope == "MACRO":
            for s in model["MACRO"]:
                if s.get("id") == sig_id:
                    s.update(update)
                    break
        else:
            t = model["TICKERS"].get(scope)
            if t:
                for s in t.get("signals", []):
                    if s.get("id") == sig_id:
                        s.update(update)
                        break
    if live.get("asof"):
        model["ASOF"] = live["asof"]
    return model

# ---------------------------------------------------------------------------
def compute_ticker_score(signals):
    """Returns (pct:int, tier1_signals:list[dict])  — Tier-1 signals with status=short."""
    num = den = 0.0
    t1_shorts = []
    for s in signals:
        v = SCORE_VAL.get(s.get("status", "na"))
        if v is None:
            continue
        w = s.get("weight", 1)
        num += v * w
        den += w
        if re.search(r"Tier 1", s.get("group", "")) and s.get("status") == "short":
            t1_shorts.append({"id": s.get("id", ""), "name": s.get("name", "")})
    pct = round((num / den) * 100) if den else 0
    return pct, t1_shorts

def compute_macro_score(macro_signals):
    num = den = 0.0
    for s in macro_signals:
        v = SCORE_VAL.get(s.get("status", "na"))
        if v is None:
            continue
        w = s.get("weight", 1)
        num += v * w
        den += w
    return round((num / den) * 100) if den else 0

def verdict(pct, t1_short_count):
    if pct >= 60 and t1_short_count >= 1:
        return "SHORT SETUP CONFIRMING"
    if pct >= 35:
        return "WATCH — building"
    if pct > 0:
        return "EARLY WATCH"
    return "NO SHORT SIGNAL"

# ---------------------------------------------------------------------------
def build_state(model):
    """Build a JSON-serialisable state snapshot from the loaded model."""
    tickers_state = {}
    for sym, t in model["TICKERS"].items():
        signals = t.get("signals", [])
        pct, t1_shorts = compute_ticker_score(signals)
        # Capture all Tier-1 signal statuses for change detection
        tier1_all = [
            {"id": s.get("id", ""), "name": s.get("name", ""), "status": s.get("status", "na")}
            for s in signals if re.search(r"Tier 1", s.get("group", ""))
        ]
        tickers_state[sym] = {
            "score": pct,
            "verdict": verdict(pct, len(t1_shorts)),
            "tier1_signals": tier1_all,
        }
    return {
        "asof": model.get("ASOF", dt.date.today().isoformat()),
        "macro_score": compute_macro_score(model["MACRO"]),
        "tickers": tickers_state,
    }
