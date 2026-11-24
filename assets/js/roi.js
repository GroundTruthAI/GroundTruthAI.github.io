/* ROI calculator — illustrative financial scenarios on user-entered assumptions.
   Three value categories: 1 direct financial savings, 2 operational efficiency, 3 strategic enablement (never priced).
   Savings apply only to eligible, data-proportional cost lines; distillation, validation, license and
   implementation costs are deducted. Pure maths in calc(); runs entirely in the browser. */
(function (root) {
  "use strict";

  // model: "transfer" | "training" | "infrastructure"; v: sanitized numbers, percentages as fractions (0..1)
  function calc(model, v) {
    var r = v.c_red, lines = [], ded = [], ops = [], energy = {}, baseline = 0, eligible = 0;
    if (model === "transfer") {
      var movedAll = v.t_dom * v.t_vol * 12;                  // all TB moved per year
      var moved = movedAll * v.t_elig;                        // eligible TB moved per year
      var stored = v.t_dom * v.t_vol * v.t_elig * v.t_ret;    // eligible TB of central copies held on average
      var unit = v.t_ctr + v.t_cing + v.t_cproc;
      baseline = movedAll * unit + v.t_dom * v.t_vol * v.t_ret * v.t_cst * 12;
      eligible = moved * unit + stored * v.t_cst * 12;
      lines.push(["Data transfer", moved * r * v.t_ctr]);
      lines.push(["Central ingestion", moved * r * v.t_cing]);
      lines.push(["Central processing", moved * r * v.t_cproc]);
      lines.push(["Central storage of training copies", stored * r * v.t_cst * 12]);
      ded.push(["Source-side distillation compute", moved * v.t_over]);
      ops.push(["Eligible data moved per year", moved, "TB"]);
      ops.push(["Avoided transfer per year", moved * r, "TB"]);
    } else if (model === "training") {
      baseline = v.r_spend;
      eligible = v.r_spend * v.r_share;
      lines.push(["Training & retraining compute", v.r_spend * v.r_share * r]);
      ded.push(["Distillation compute", v.r_runs * v.r_rcost]);
      if (v.r_kwh > 0) {
        energy.net = v.r_kwh * v.r_share * r - v.r_runs * v.r_dkwh;   // informational: cost already in compute
        energy.dist = v.r_runs * v.r_dkwh;
        energy.cost = energy.net * v.r_price;
        energy.inCompute = true;
      }
      if (v.r_hours > 0) ops.push(["Training hours avoided per year", v.r_hours * v.r_share * r, "h"]);
    } else {
      baseline = v.i_tb * v.i_cst * 12 + v.i_comp + v.i_kwh * v.i_price;
      eligible = v.i_tb * v.i_cst * 12 + v.i_comp * v.i_share + v.i_kwh * v.i_price;
      lines.push(["Storage incl. backup & replicas", v.i_tb * r * v.i_cst * 12]);
      lines.push(["Data-proportional compute", v.i_comp * v.i_share * r]);
      if (v.i_kwh > 0) lines.push(["Energy outside compute", v.i_kwh * r * v.i_price]);
      ded.push(["Distillation compute", v.i_ocost]);
      if (v.i_okwh > 0) ded.push(["Distillation energy", v.i_okwh * v.i_price]);
      if (v.i_kwh > 0 || v.i_okwh > 0) {
        energy.net = v.i_kwh * r - v.i_okwh;
        energy.dist = v.i_okwh;
        if (v.i_grid > 0) energy.co2 = energy.net * v.i_grid / 1000;
      }
    }
    ded.push(["Validation & dataset maintenance", v.c_val]);
    ded.push(["GroundTruth AI license", v.c_sol]);
    var gross = lines.reduce(function (a, l) { return a + l[1]; }, 0);
    var deductions = ded.reduce(function (a, l) { return a + l[1]; }, 0);
    var net = gross - deductions;
    var hrs = v.c_hrs * v.c_hsave;
    if (hrs > 0) {
      ops.push(["Team hours freed per year", hrs, "h"]);
      if (v.c_rate > 0) ops.push(["Value of hours freed (not in net)", hrs * v.c_rate, "money"]);
    }
    var three = net * 3 - v.c_impl;
    var first = net - v.c_impl;
    var costs = deductions + v.c_impl;                        // recurring costs + one-time implementation
    var roi = costs > 0 ? first / costs : null;               // first-year ROI; undefined when no costs are entered
    // payback in months: null = not reached (net <= 0); 0 = immediate (no implementation cost)
    var payback = net <= 0 ? null : (v.c_impl > 0 ? Math.max(1, Math.ceil(v.c_impl / (net / 12))) : 0);
    return { baseline: baseline, eligible: eligible, lines: lines, ded: ded, gross: gross, deductions: deductions, net: net,
             first: first, roi: roi, three: three, payback: payback, ops: ops, energy: energy };
  }

  var api = { calc: calc };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.GTRoi = api;
  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("roi");
    if (!form) return;
    form.hidden = false;

    var caseSel = document.getElementById("roi-case");
    var scenSel = document.getElementById("roi-scen");
    var curSel = document.getElementById("roi-cur");
    var scens = form.querySelectorAll(".scen");
    var pilot = document.getElementById("o-pilot");
    var stratEmpty = document.getElementById("o-strat-empty");
    var errBox = document.getElementById("roi-err");
    var copyBtn = document.getElementById("o-copy");
    var copyS = document.getElementById("o-copy-s");
    var domLabel = document.querySelector('label[for="t_dom"]');
    var PCT = ["t_elig", "r_share", "i_share", "c_red", "c_hsave"];
    var last = null;

    function model() { var o = scenSel.options[scenSel.selectedIndex]; return o ? o.dataset.model : "transfer"; }

    function values() {
      var v = {}, bad = [];
      Array.prototype.forEach.call(form.querySelectorAll("input[type=number]"), function (input) {
        var raw = input.value.trim(), x = raw === "" ? 0 : Number(raw), ok = true;
        if (!isFinite(x) || x < 0) { x = 0; ok = raw === ""; }
        var max = input.getAttribute("max");
        if (max !== null && x > Number(max)) { x = Number(max); ok = false; }
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) {
          var l = form.querySelector('label[for="' + input.id + '"]');
          bad.push(l ? l.textContent : input.id);
        }
        v[input.id] = PCT.indexOf(input.id) !== -1 ? x / 100 : x;
      });
      errBox.hidden = !bad.length;
      errBox.textContent = bad.length ? "Out of range, so capped or treated as 0: " + bad.join("; ") + "." : "";
      return v;
    }

    function money(v) {
      var c = curSel.value, a = Math.abs(v), s;
      if (a >= 1e9) s = (a / 1e9).toFixed(a >= 1e10 ? 1 : 2) + "B";
      else if (a >= 1e6) s = (a / 1e6).toFixed(a >= 1e7 ? 1 : 2) + "M";
      else if (a >= 1e3) s = Math.round(a / 1e3) + "k";
      else s = Math.round(a).toString();
      return (v < 0 ? "−" : "") + c + s;
    }
    function num(v, unit) { return Math.round(v).toLocaleString("en-US") + " " + unit; }
    function esc(s) { return String(s).replace(/[&<>"]/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]; }); }
    function li(label, value, cls) {
      return "<li" + (cls ? ' class="' + cls + '"' : "") + "><span>" + esc(label) + "</span><span>" + esc(value) + "</span></li>";
    }

    function compute() {
      var m = model(), v = values(), o = calc(m, v);
      last = { m: m, v: v, o: o };
      var html = li("In-scope annual expenditure", money(o.baseline), "muted") + li("Eligible, data-proportional expenditure", money(o.eligible), "muted");
      html += o.lines.map(function (l) { return li(l[0], money(l[1])); }).join("");
      html += li("Gross direct reduction", money(o.gross), "tot");
      html += o.ded.map(function (d) {
        var notEntered = d[1] === 0 && /license/i.test(d[0]);
        return li("− " + d[0], notEntered ? "not entered" : money(-d[1]), notEntered ? "muted" : "neg");
      }).join("");
      document.getElementById("o-lines").innerHTML = html;

      var big = document.getElementById("o-net");
      var s = [];
      if (o.baseline <= 0) {
        big.textContent = "—";
        big.classList.remove("neg");
        s.push("Enter in-scope expenditure to estimate savings.");
      } else {
        big.textContent = money(o.net);
        big.classList.toggle("neg", o.net < 0);
        s.push("First year: " + money(o.first) + (v.c_impl ? " after implementation" : ""));
        s.push(o.roi === null ? "ROI: not defined (no costs entered)" : "First-year ROI: " + String(Math.round(o.roi * 100)).replace("-", "−") + "%");
        s.push(o.payback === null ? "Payback: not reached (net annual value ≤ 0)" :
               o.payback === 0 ? "Payback: immediate (no implementation cost)" : "Payback ≈ " + o.payback + " months");
        s.push("3-year view: " + money(o.three));
        if (!v.c_sol) s.push("ROI and payback exclude the license (not entered)");
      }
      document.getElementById("o-net-s").textContent = s.join(" · ");

      document.getElementById("o-ops").innerHTML = o.ops.length ? o.ops.map(function (x) {
        return li(x[0], x[2] === "money" ? money(x[1]) : num(x[1], x[2]));
      }).join("") : '<li class="muted"><span>Enter team hours and avoidable share to estimate.</span><span></span></li>';

      var e = o.energy, eh = "";
      if (e.net !== undefined) {
        eh += li("Net energy avoided", num(e.net, "kWh"), e.net < 0 ? "neg" : "");
        eh += li("Distillation energy included", num(e.dist, "kWh"), "muted");
        if (e.inCompute && v.r_price > 0) eh += li("Energy cost (already inside compute line)", money(e.cost), "muted");
        if (e.co2 !== undefined) eh += li("Operational emissions avoided*", num(e.co2, "t CO₂e"), e.co2 < 0 ? "neg" : "") +
          '<li class="muted"><span>*Location-based, operational only. Not a lifecycle assessment.</span><span></span></li>';
      }
      document.getElementById("o-energy").innerHTML = eh ||
        '<li class="muted"><span>Enter annual energy (kWh) to estimate. Distillation energy is deducted.</span><span></span></li>';
    }

    function summary() {
      if (!last) return "";
      var o = last.o, lines = ["GroundTruth AI — illustrative ROI scenario (not a forecast or a quote)",
        "Business case: " + (caseSel.value ? caseSel.options[caseSel.selectedIndex].text : "not selected"),
        "Commercial scenario: " + scenSel.options[scenSel.selectedIndex].text,
        "Assumed reduction on eligible data: " + Math.round(last.v.c_red * 100) + "%", ""];
      o.lines.forEach(function (l) { lines.push(l[0] + ": " + money(l[1])); });
      lines.splice(5, 0, "In-scope annual expenditure: " + money(o.baseline), "Eligible expenditure: " + money(o.eligible), "");
      lines.push("Gross direct reduction: " + money(o.gross));
      o.ded.forEach(function (d) { lines.push("− " + d[0] + ": " + money(d[1])); });
      lines.push("Net annual direct value: " + money(o.net), "First-year value after implementation: " + money(o.first),
        "First-year ROI: " + (o.roi === null ? "not defined" : Math.round(o.roi * 100) + "%"),
        "Payback: " + (o.payback === null ? "not reached" : o.payback === 0 ? "immediate" : o.payback + " months"),
        "3-year view after implementation: " + money(o.three), "",
        "Strategic enablement is listed separately and not priced. Source data is assumed to be retained.",
        "Not contractual: illustrative estimate based on internal experiments and the assumptions above; no warranty or guarantee of results.",
        "Actual results require a workload-specific evaluation and any commitment a separate written agreement.", location.href);
      return lines.join("\n");
    }

    function showScenario() {
      var m = model(), o = scenSel.options[scenSel.selectedIndex];
      Array.prototype.forEach.call(scens, function (f) { f.hidden = f.dataset.scen !== m; });
      if (domLabel && o && o.dataset.domain) domLabel.textContent = o.dataset.domain;
      compute();
    }
    function showCase() {
      var id = caseSel.value;
      var opt = caseSel.options[caseSel.selectedIndex];
      if (opt && opt.dataset.preset) scenSel.value = opt.dataset.preset;
      Array.prototype.forEach.call(form.querySelectorAll(".strat-list"), function (u) { u.hidden = u.dataset.case !== id; });
      stratEmpty.hidden = !!id;
      pilot.href = "/pilot/?type=assessment" + (id ? "&case=" + id : "");
      var q = new URLSearchParams(location.search);
      if (id) q.set("case", id); else q.delete("case");
      var qs = q.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
      showScenario();
    }

    form.addEventListener("input", function (e) { if (e.target.tagName === "INPUT" && e.target.type === "number") compute(); });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    caseSel.addEventListener("change", showCase);
    scenSel.addEventListener("change", showScenario);
    curSel.addEventListener("change", compute);
    copyBtn.hidden = false;
    copyBtn.addEventListener("click", function () {
      var t = summary();
      function done() { copyS.textContent = "Summary copied to the clipboard."; }
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(t).then(done, function () { copyS.textContent = "Copy failed; use Print scenario instead."; });
      else copyS.textContent = "Copy is not available in this browser; use Print scenario instead.";
    });

    var pre = new URLSearchParams(location.search).get("case");
    if (pre && caseSel.querySelector('option[value="' + pre.replace(/[^A-Z0-9]/g, "") + '"]')) caseSel.value = pre;
    showCase();
  });
})(typeof window !== "undefined" ? window : this);
