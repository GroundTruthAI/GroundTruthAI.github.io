/* Distributed intelligence simulator — illustrative architecture, not a forecast.
   Pure calculation in simulate(); the DOM part draws an SVG with native APIs (no inline styles, CSP-safe).
   Runs entirely in the browser; nothing is transmitted. */
(function (root) {
  "use strict";

  // inp: n (domains), vol (TB eligible per domain), tx (0..1 share transferred today),
  //      el (0..1 share of transferred data eligible for distillation), red (0..0.99 reduction),
  //      ctr, cproc (cost per TB, optional)
  function simulate(inp) {
    var original = inp.n * inp.vol;
    var baseline = original * inp.tx;
    var eligible = baseline * inp.el;                     // transferred data that distillation can replace
    var rawResidual = baseline * (1 - inp.el);          // still transferred raw (not eligible)
    var distilled = baseline * inp.el * (1 - inp.red);  // optimized datasets transferred
    var optimized = rawResidual + distilled;
    var avoided = baseline - optimized;                  // = baseline * el * red
    return {
      original: original, baseline: baseline, eligible: eligible, rawResidual: rawResidual, distilled: distilled,
      optimized: optimized, avoided: avoided,
      relative: baseline > 0 ? avoided / baseline : 0,
      money: avoided * ((inp.ctr || 0) + (inp.cproc || 0))
    };
  }

  function fmtTB(v) {
    if (!isFinite(v) || v <= 0) return "0 TB";
    if (v >= 1000) return (v / 1000).toLocaleString("en-US", { maximumFractionDigits: v >= 10000 ? 0 : 1 }) + " PB";
    if (v >= 1) return v.toLocaleString("en-US", { maximumFractionDigits: v >= 10 ? 0 : 1 }) + " TB";
    return (v * 1000).toLocaleString("en-US", { maximumFractionDigits: 0 }) + " GB";
  }

  var api = { simulate: simulate, fmtTB: fmtTB };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.GTSim = api;
  if (typeof document === "undefined") return;

  var NS = "http://www.w3.org/2000/svg";
  function el(tag, attrs, text) {
    var e = document.createElementNS(NS, tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (text != null) e.textContent = text;
    return e;
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("sim");
    if (!form) return;
    form.hidden = false;
    var host = document.getElementById("sim-svg");
    var errBox = document.getElementById("sim-err");
    var FIELDS = {
      s_n: { label: "facilities or data domains", max: 200, int: true },
      s_vol: { label: "eligible data per domain", max: 100000 },
      s_tx: { label: "share transferred today", max: 100 },
      s_el: { label: "share eligible for distillation", max: 100 },
      s_red: { label: "assumed reduction", max: 99 },
      s_ctr: { label: "transfer cost", max: 1e9 },
      s_cproc: { label: "ingestion and processing cost", max: 1e9 }
    };

    function read() {
      var v = {}, bad = [];
      Object.keys(FIELDS).forEach(function (id) {
        var f = FIELDS[id], input = document.getElementById(id), raw = input.value.trim();
        var x = raw === "" ? 0 : Number(raw), ok = true;
        if (!isFinite(x) || x < 0) { x = 0; ok = raw === ""; }
        if (x > f.max) { x = f.max; ok = false; }
        if (f.int) x = Math.floor(x);
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) bad.push(f.label + " (0–" + f.max.toLocaleString("en-US") + ")");
        v[id] = x;
      });
      errBox.hidden = !bad.length;
      errBox.textContent = bad.length ? "Out of range, so capped or treated as 0: " + bad.join("; ") + "." : "";
      return { n: v.s_n, vol: v.s_vol, tx: v.s_tx / 100, el: v.s_el / 100, red: v.s_red / 100, ctr: v.s_ctr, cproc: v.s_cproc };
    }

    var lastDraw = null;
    function draw(inp, r) {
      lastDraw = [inp, r];
      var narrow = host.clientWidth > 0 && host.clientWidth < 520;
      var L = narrow
        ? { W: 420, max: 4, domW: 170, origX: 82, origW: 30, val: false, gtX: 140, bx: 206, cx: 248, cw: 166, bar: 134,
            capL: "DATA STAYS AT SOURCE", capB: "BOUNDARY" }
        : { W: 660, max: 6, domW: 240, origX: 92, origW: 70, val: true, gtX: 214, bx: 318, cx: 452, cw: 200, bar: 168,
            capL: "ORIGINAL DATA STAYS AT SOURCE", capB: "AUTHORIZED BOUNDARY" };
      var shown = Math.min(inp.n, L.max), extra = inp.n - shown;
      var rowH = 52, top = 34, rows = shown + (extra > 0 ? 1 : 0);
      var H = Math.max(top + rows * rowH + 24, 230), W = L.W, cx = L.cx;
      var svg = el("svg", { viewBox: "0 0 " + W + " " + H, class: "viz sim-viz", role: "img" });
      var perBase = inp.n ? r.baseline / inp.n : 0;
      var perRaw = inp.n ? r.rawResidual / inp.n : 0;
      var perDist = inp.n ? r.distilled / inp.n : 0;
      var perOrig = inp.vol;
      var scale = perBase > 0 ? 12 / perBase : 0;
      svg.appendChild(el("text", { x: 12, y: 18, class: "hv-cap" }, L.capL));
      svg.appendChild(el("text", { x: L.bx, y: 18, class: "hv-cap", "text-anchor": "middle" }, L.capB));
      var midY = top + (rows * rowH) / 2 - 6;
      for (var i = 0; i < rows; i++) {
        var y = top + i * rowH, cy = y + 20;
        var g = el("g", {});
        if (i === shown) {
          g.appendChild(el("text", { x: 20, y: cy + 4, class: "sim-more" }, "+ " + extra + " more, same pattern"));
          svg.appendChild(g); continue;
        }
        var gx = L.gtX + 24;
        g.appendChild(el("rect", { x: 8, y: y, width: L.domW, height: 40, rx: 9, class: "sim-dom" }));
        g.appendChild(el("text", { x: 20, y: cy + 4, class: "sim-t" }, "Domain " + (i + 1)));
        var wOrig = perOrig > 0 ? L.origW : 0;
        g.appendChild(el("rect", { x: L.origX, y: cy - 6, width: wOrig, height: 12, rx: 3, class: "sim-orig" }));
        if (L.val) g.appendChild(el("text", { x: L.origX + wOrig + 6, y: cy + 4, class: "sim-v" }, fmtTB(perOrig)));
        g.appendChild(el("rect", { x: L.gtX, y: cy - 11, width: 24, height: 22, rx: 6, class: "sim-gt" }));
        var path = "M" + gx + " " + cy + " C" + (L.bx + 12) + " " + cy + " " + (L.bx + 42) + " " + midY + " " + (cx - 6) + " " + midY;
        if (perBase > 0) g.appendChild(el("path", { d: path, class: "sim-ghost", "stroke-width": Math.max(perBase * scale, 1) }));
        if (perRaw > 0) g.appendChild(el("path", { d: path, class: "sim-raw", "stroke-width": Math.max(perRaw * scale, 1.2) }));
        if (perDist > 0) g.appendChild(el("path", { d: path, class: "sim-dist", "stroke-width": Math.max(perDist * scale, 1.2) }));
        svg.appendChild(g);
      }
      svg.appendChild(el("path", { d: "M" + L.bx + " 26 V" + (H - 8), class: "sim-bound" }));
      var bh = 150, by = Math.max(midY - bh / 2, 24);
      svg.appendChild(el("rect", { x: cx, y: by, width: L.cw, height: bh, rx: 12, class: "sim-central" }));
      svg.appendChild(el("text", { x: cx + L.cw / 2, y: by + 22, class: "sim-t", "text-anchor": "middle" }, "Central enterprise AI"));
      var maxW = L.bar, wb = r.baseline > 0 ? maxW : 0, wo = r.baseline > 0 ? maxW * r.optimized / r.baseline : 0;
      svg.appendChild(el("text", { x: cx + 16, y: by + 52, class: "hv-cap" }, "BASELINE TRANSFER"));
      svg.appendChild(el("rect", { x: cx + 16, y: by + 58, width: wb, height: 12, rx: 3, class: "sim-bar-base" }));
      svg.appendChild(el("text", { x: cx + 16, y: by + 86, class: "sim-v" }, fmtTB(r.baseline)));
      svg.appendChild(el("text", { x: cx + 16, y: by + 108, class: "hv-cap" }, "OPTIMIZED TRANSFER"));
      svg.appendChild(el("rect", { x: cx + 16, y: by + 114, width: Math.max(wo, r.optimized > 0 ? 2 : 0), height: 12, rx: 3, class: "sim-bar-opt" }));
      svg.appendChild(el("text", { x: cx + 16, y: by + 142, class: "sim-v" }, fmtTB(r.optimized)));
      svg.setAttribute("aria-label", "Illustrative architecture: " + inp.n + " domains each keep " + fmtTB(perOrig) +
        " of source data in place and distill locally. Baseline transfer " + fmtTB(r.baseline) + "; estimated optimized transfer " +
        fmtTB(r.optimized) + " across the authorized boundary to central enterprise AI.");
      host.replaceChildren(svg);
    }

    function money(v) {
      return v.toLocaleString("en-US", { maximumFractionDigits: 0 });
    }

    function update() {
      var inp = read(), r = simulate(inp);
      document.getElementById("k-orig").textContent = fmtTB(r.original);
      document.getElementById("k-elig").textContent = fmtTB(r.eligible);
      document.getElementById("k-elig-s").textContent = Math.round(inp.el * 100) + "% of the baseline transfer";
      var f = { "f-n": inp.n, "f-vol": fmtTB(inp.vol), "f-tx": Math.round(inp.tx * 100) + "%", "f-base": fmtTB(r.baseline),
                "f-el": Math.round(inp.el * 100) + "%", "f-elig": fmtTB(r.eligible), "f-red": Math.round(inp.red * 100) + "%",
                "f-raw": fmtTB(r.rawResidual), "f-dist": fmtTB(r.distilled), "f-opt": fmtTB(r.optimized), "f-avoid": fmtTB(r.avoided),
                "f-cost": money((inp.ctr || 0) + (inp.cproc || 0)), "f-money": money(r.money) };
      Object.keys(f).forEach(function (k) { var e = document.getElementById(k); if (e) e.textContent = String(f[k]); });
      document.getElementById("k-base").textContent = fmtTB(r.baseline);
      document.getElementById("k-opt").textContent = fmtTB(r.optimized);
      document.getElementById("k-opt-s").textContent = r.rawResidual > 0
        ? fmtTB(r.distilled) + " distilled + " + fmtTB(r.rawResidual) + " raw not eligible"
        : "approved distilled datasets";
      document.getElementById("k-avoid").textContent = fmtTB(r.avoided);
      document.getElementById("k-rel").textContent = r.baseline > 0 ? Math.round(r.relative * 100) + "% less data moved" : "no baseline transfer";
      var mw = document.getElementById("k-money-w");
      mw.hidden = !(inp.ctr > 0 || inp.cproc > 0);
      document.getElementById("k-money").textContent = money(r.money) + " (your currency)";
      draw(inp, r);
    }

    form.addEventListener("input", update);
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(function () { if (lastDraw) draw(lastDraw[0], lastDraw[1]); }, 150);
    });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    Array.prototype.forEach.call(form.querySelectorAll("[data-preset]"), function (b) {
      b.addEventListener("click", function () {
        var p = { s_n: 20, s_vol: 10, s_tx: 100, s_el: 100, s_red: 90 };
        Object.keys(p).forEach(function (k) { document.getElementById(k).value = p[k]; });
        update();
      });
    });
    update();
  });
})(typeof window !== "undefined" ? window : this);
