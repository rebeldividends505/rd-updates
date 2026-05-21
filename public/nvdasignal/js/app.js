/* AI SHORT-SIGNAL SYSTEM — app logic (vanilla JS, no build step) */
(function () {
  "use strict";
  const VERSION = 4;
  const LS_KEY = "ai-short-signal-system-v" + VERSION;
  const ORDER = ["na", "intact", "watch", "short"];
  const STATUS = {
    na:     { label: "—",      cls: "s-na" },
    intact: { label: "INTACT", cls: "s-intact" },
    watch:  { label: "WATCH",  cls: "s-watch" },
    short:  { label: "SHORT",  cls: "s-short" },
  };
  const SCOREVAL = { na: null, intact: 0, watch: 0.5, short: 1 };

  let model, selected;

  /* ---------- model build / persistence ---------- */
  function freshModel() {
    return {
      version: VERSION, asof: ASOF,
      macro: structuredClone(MACRO),
      tickers: structuredClone(TICKERS),
    };
  }
  function load() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (raw) {
        const m = JSON.parse(raw);
        if (m && m.version === VERSION) return m;
      }
    } catch (e) { /* ignore */ }
    return freshModel();
  }
  function save() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(model)); flash("saved"); }
    catch (e) { flash("save failed"); }
  }

  /* ---------- scoring ---------- */
  function score(signals) {
    let num = 0, den = 0, counts = { short: 0, watch: 0, intact: 0, na: 0 };
    signals.forEach(s => {
      counts[s.status] = (counts[s.status] || 0) + 1;
      const v = SCOREVAL[s.status];
      if (v === null) return;
      num += v * (s.weight || 1);
      den += (s.weight || 1);
    });
    const pct = den ? Math.round((num / den) * 100) : 0;
    return { pct, counts, assessed: den > 0 };
  }
  function band(pct, signals) {
    // Tier-1 gate: a "confirmed" short needs Tier-1 corroboration
    const t1short = signals.filter(s => /Tier 1/.test(s.group) && s.status === "short").length;
    if (pct >= 60 && t1short >= 1) return { txt: "SHORT SETUP CONFIRMING", cls: "s-short" };
    if (pct >= 35) return { txt: "WATCH — building", cls: "s-watch" };
    if (pct > 0)  return { txt: "EARLY WATCH", cls: "s-watch2" };
    return { txt: "NO SHORT SIGNAL", cls: "s-intact" };
  }

  /* ---------- rendering ---------- */
  const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };

  function statusChip(sig, onCycle) {
    const st = STATUS[sig.status];
    const b = el("button", "chip " + st.cls, `<span class="dot"></span>${st.label}`);
    b.title = "click to cycle: — → INTACT → WATCH → SHORT";
    b.onclick = () => { sig.status = ORDER[(ORDER.indexOf(sig.status) + 1) % ORDER.length]; onCycle(); };
    return b;
  }
  function provBadge(p) {
    const map = { v: ["verified", "p-v"], r: ["filing", "p-r"], u: ["feed·verify", "p-u"], n: ["illustrative", "p-n"] };
    const m = map[p] || map.u;
    return el("span", "prov " + m[1], m[0]);
  }
  function signalRow(sig, onChange) {
    const row = el("div", "sigrow " + STATUS[sig.status].cls + "-bg");
    row.appendChild(statusChip(sig, onChange));
    const main = el("div", "sigmain");
    const head = el("div", "sighead");
    head.appendChild(el("span", "signame", sig.name));
    if (sig.weight >= 3) head.appendChild(el("span", "w3", "T1"));
    head.appendChild(provBadge(sig.prov));
    main.appendChild(head);
    if (sig.plain) main.appendChild(el("div", "plain", sig.plain));
    const ta = el("textarea", "reading"); ta.value = sig.reading || ""; ta.rows = 1;
    ta.oninput = () => { sig.reading = ta.value; debounceSave(); };
    main.appendChild(ta);
    main.appendChild(el("div", "meta", `<b>src</b> ${esc(sig.source || "—")} &nbsp;·&nbsp; <b class="trg">trigger</b> ${esc(sig.trigger || "—")}`));
    row.appendChild(main);
    return row;
  }
  function grouped(signals) {
    const groups = [];
    signals.forEach(s => { let g = groups.find(x => x.name === s.group); if (!g) { g = { name: s.group, items: [] }; groups.push(g); } g.items.push(s); });
    return groups;
  }

  function gauge(pct, label, bandObj) {
    const g = el("div", "gauge");
    g.appendChild(el("div", "gauge-label", label));
    const bar = el("div", "gauge-bar");
    const fill = el("div", "gauge-fill " + bandObj.cls); fill.style.width = pct + "%";
    bar.appendChild(fill);
    g.appendChild(bar);
    g.appendChild(el("div", "gauge-verdict " + bandObj.cls, `${bandObj.txt} · ${pct}/100`));
    return g;
  }

  function render() {
    const root = document.getElementById("app");
    root.innerHTML = "";

    /* header */
    const macroScore = score(model.macro);
    const macroBand = band(macroScore.pct, model.macro);
    const header = el("div", "header");
    header.appendChild(el("div", "brand", `<span class="cursor">▮</span> AI SHORT-SIGNAL SYSTEM`));
    const ctrl = el("div", "controls");
    ctrl.appendChild(mkBtn("◳ webinar", () => { document.body.classList.toggle("webinar"); }));
    ctrl.appendChild(mkBtn("⭳ export", exportJSON));
    ctrl.appendChild(mkBtn("⭱ import", importJSON));
    ctrl.appendChild(mkBtn("↺ reset", () => { if (confirm("Reset all readings to seeded state?")) { model = freshModel(); save(); render(); } }));
    header.appendChild(ctrl);
    root.appendChild(header);
    root.appendChild(el("div", "asof",
      `regime as of <b>${model.asof}</b> · short-state: ` +
      `<span class="lg s-intact">●</span>intact ` +
      `<span class="lg s-watch">●</span>watch ` +
      `<span class="lg s-short">●</span>short trigger &nbsp;|&nbsp; ` +
      `data: <span class="prov p-v">verified</span> <span class="prov p-r">filing</span> ` +
      `<span class="prov p-u">feed·verify</span> &nbsp;·&nbsp; <span id="flash"></span>`));

    /* macro regime strip */
    const macroWrap = el("div", "panel macro");
    const mh = el("div", "panel-h"); mh.appendChild(el("div", "panel-title", "GLOBAL MACRO & CYCLE REGIME"));
    mh.appendChild(gauge(macroScore.pct, "complex-wide risk", macroBand));
    macroWrap.appendChild(mh);
    const mgrid = el("div", "macro-grid");
    grouped(model.macro).forEach(grp => {
      const col = el("div", "macro-col");
      col.appendChild(el("div", "grp", grp.name));
      grp.items.forEach(s => col.appendChild(signalRow(s, () => { save(); render(); })));
      mgrid.appendChild(col);
    });
    macroWrap.appendChild(mgrid);
    root.appendChild(macroWrap);

    /* ticker nav grouped by archetype */
    const nav = el("div", "tnav");
    ARCHETYPE_ORDER.forEach(arch => {
      const syms = Object.keys(model.tickers).filter(k => model.tickers[k].archetype === arch);
      if (!syms.length) return;
      const grp = el("div", "tnav-grp");
      grp.appendChild(el("div", "tnav-arch", arch));
      const rowEl = el("div", "tnav-row");
      syms.forEach(sym => {
        const t = model.tickers[sym];
        const sc = score(t.signals); const bd = band(sc.pct, t.signals);
        const btn = el("button", "tbtn " + (sym === selected ? "active " : "") + bd.cls);
        btn.innerHTML = `<span class="tsym">${sym}</span><span class="tscore">${sc.pct}</span>`;
        btn.onclick = () => { selected = sym; render(); };
        rowEl.appendChild(btn);
      });
      grp.appendChild(rowEl);
      nav.appendChild(grp);
    });
    root.appendChild(nav);

    /* selected ticker detail */
    const t = model.tickers[selected];
    const sc = score(t.signals); const bd = band(sc.pct, t.signals);
    const panel = el("div", "panel ticker");
    const th = el("div", "panel-h");
    const left = el("div");
    left.appendChild(el("div", "panel-title", `${selected} · ${esc(t.name)}`));
    left.appendChild(el("div", "arch", esc(t.archetype) + " · YTD " + esc(t.ytd)));
    left.appendChild(el("div", "thesis", esc(t.thesis)));
    left.appendChild(el("div", "keyline", "★ " + esc(t.key)));
    th.appendChild(left);
    th.appendChild(gauge(sc.pct, "short-readiness", bd));
    panel.appendChild(th);
    grouped(t.signals).forEach(grp => {
      panel.appendChild(el("div", "grp", grp.name));
      grp.items.forEach(s => panel.appendChild(signalRow(s, () => { save(); render(); })));
    });
    root.appendChild(panel);

    /* footer */
    root.appendChild(el("div", "footer",
      `Educational research framework — <b>not investment advice</b>. ` +
      `A "SHORT SETUP CONFIRMING" reading means ≥60/100 with at least one Tier-1 trigger; it is a prompt to investigate, not a signal to trade. ` +
      `Refresh fast-moving numeric readings regularly (see docs/DEPLOY.md for the automation hook).`));
  }

  /* ---------- helpers ---------- */
  function mkBtn(label, fn) { const b = el("button", "ctl", label); b.onclick = fn; return b; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])); }
  let flashT; function flash(msg) { const f = document.getElementById("flash"); if (!f) return; f.textContent = msg; clearTimeout(flashT); flashT = setTimeout(() => { f.textContent = ""; }, 1800); }
  let saveT; function debounceSave() { clearTimeout(saveT); saveT = setTimeout(save, 500); }

  function exportJSON() {
    const blob = new Blob([JSON.stringify(model, null, 2)], { type: "application/json" });
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob);
    a.download = "short-signal-state-" + new Date().toISOString().slice(0, 10) + ".json"; a.click();
  }
  function importJSON() {
    const inp = document.createElement("input"); inp.type = "file"; inp.accept = "application/json";
    inp.onchange = () => { const fr = new FileReader(); fr.onload = () => { try { const m = JSON.parse(fr.result); if (m.version !== VERSION) { alert("Version mismatch — import skipped."); return; } model = m; save(); render(); } catch (e) { alert("Invalid file."); } }; fr.readAsText(inp.files[0]); };
    inp.click();
  }

  /* optional live-data override: if data/live.json exists, apply numeric refreshes */
  async function applyLive() {
    try {
      const r = await fetch("data/live.json", { cache: "no-store" });
      if (!r.ok) return;
      const live = await r.json();           // { asof, readings: { "MU:0": {reading,status}, "MACRO:dram_spot":{...} } }
      if (live.asof) model.asof = live.asof;
      Object.entries(live.readings || {}).forEach(([k, v]) => {
        const [scope, key] = k.split(":");
        if (scope === "MACRO") { const s = model.macro.find(x => x.id === key); if (s) Object.assign(s, v); }
        else { const t = model.tickers[scope]; if (!t) return; let s = t.signals.find(x => x.id === key); if (!s && /^\d+$/.test(key)) s = t.signals[+key]; if (s) Object.assign(s, v); }
      });
    } catch (e) { /* no live feed; fine */ }
  }

  /* ---------- boot ---------- */
  (async function () {
    model = load();
    await applyLive();
    selected = Object.keys(model.tickers)[0];
    render();
  })();
})();
