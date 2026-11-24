/* ROI calculator — illustrative estimate on user-editable assumptions.
   Every saving line is added up (transfer, processing, storage, training, energy, team time); distillation and
   validation, license and implementation are deducted. Strategic enablement is listed, never priced.
   Pure maths in calc(); runs entirely in the browser. */
(function (root) {
  "use strict";

  var KEYS = ["transfer", "processing", "storage", "training", "energy", "prep"];

  // v: { s_<key>: annual spend, r_<key>: reduction 0..1, c_dist, c_sol, c_impl }
  function calc(v) {
    var lines = KEYS.map(function (k) { return [k, (v["s_" + k] || 0) * (v["r_" + k] || 0)]; });
    var spend = KEYS.reduce(function (a, k) { return a + (v["s_" + k] || 0); }, 0);
    var gross = lines.reduce(function (a, l) { return a + l[1]; }, 0);
    var costs = (v.c_dist || 0) + (v.c_sol || 0);
    var impl = v.c_impl || 0;
    var net = gross - costs;
    var first = net - impl;
    var invest = costs + impl;
    var roi = invest > 0 ? first / invest : null;                 // first-year ROI; undefined without costs
    // payback in months: null = not reached (net <= 0); 0 = immediate (no implementation cost)
    var payback = net <= 0 ? null : (impl > 0 ? Math.max(1, Math.ceil(impl / (net / 12))) : 0);
    return { lines: lines, spend: spend, gross: gross, costs: costs, net: net, first: first,
             three: net * 3 - impl, roi: roi, payback: payback, share: spend > 0 ? gross / spend : 0 };
  }

  var api = { calc: calc, KEYS: KEYS };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.GTRoi = api;
  if (typeof document === "undefined") return;

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("roi");
    if (!form) return;
    form.hidden = false;
    var caseSel = document.getElementById("roi-case");
    var curSel = document.getElementById("roi-cur");
    var pilot = document.getElementById("o-pilot");
    var stratEmpty = document.getElementById("o-strat-empty");
    var errBox = document.getElementById("roi-err");
    var copyBtn = document.getElementById("o-copy");
    var copyS = document.getElementById("o-copy-s");
    var inputs = Array.prototype.slice.call(form.querySelectorAll("input[type=number]"));
    var defaults = {};
    inputs.forEach(function (i) { defaults[i.id] = i.value; });
    var labels = {};
    Array.prototype.forEach.call(form.querySelectorAll(".sv-row"), function (r) {
      var inp = r.querySelector("input"); if (inp) labels[inp.id.slice(2)] = r.querySelector(".sv-h").textContent;
    });
    var last = null;

    function values() {
      var v = {}, bad = [];
      inputs.forEach(function (input) {
        var raw = input.value.trim(), x = raw === "" ? 0 : Number(raw), ok = true;
        if (!isFinite(x) || x < 0) { x = 0; ok = raw === ""; }
        var max = input.getAttribute("max");
        if (max !== null && x > Number(max)) { x = Number(max); ok = false; }
        input.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) {
          var row = input.closest(".sv-row"), l = form.querySelector('label[for="' + input.id + '"]');
          bad.push((row ? row.querySelector(".sv-h").textContent + " — " : "") + (l ? l.textContent : input.id));
        }
        v[input.id] = input.id.indexOf("r_") === 0 ? x / 100 : x;
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
    function esc(s) { return String(s).replace(/[&<>"]/g, function (ch) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch]; }); }
    function li(label, value, cls) {
      return "<li" + (cls ? ' class="' + cls + '"' : "") + "><span>" + esc(label) + "</span><span>" + esc(value) + "</span></li>";
    }

    function compute() {
      var v = values(), o = calc(v);
      last = { v: v, o: o };
      var html = o.lines.map(function (l) { return li(labels[l[0]] || l[0], money(l[1])); }).join("");
      html += li("Total savings", money(o.gross), "tot");
      html += li("− Distillation and validation", money(-v.c_dist), v.c_dist ? "neg" : "muted");
      html += li("− GroundTruth AI license", v.c_sol ? money(-v.c_sol) : "not entered", v.c_sol ? "neg" : "muted");
      html += li("Annual spend in scope", money(o.spend), "muted");
      document.getElementById("o-lines").innerHTML = html;

      var big = document.getElementById("o-net"), s = [];
      if (o.spend <= 0) {
        big.textContent = "—"; big.classList.remove("neg");
        s.push("Enter the annual spend in scope to estimate savings.");
      } else {
        big.textContent = money(o.net);
        big.classList.toggle("neg", o.net < 0);
        s.push(Math.round(o.share * 100) + "% of the spend in scope");
        s.push("3 years: " + money(o.three));
        s.push("First year: " + money(o.first) + (v.c_impl ? " after implementation" : ""));
        s.push(o.roi === null ? "ROI: not defined (no costs entered)" : "First-year ROI: " + String(Math.round(o.roi * 100)).replace("-", "−") + "%");
        s.push(o.payback === null ? "Payback: not reached (net annual value ≤ 0)" :
               o.payback === 0 ? "Payback: immediate (no implementation cost)" : "Payback ≈ " + o.payback + " months");
        if (!v.c_sol) s.push("license not entered");
      }
      document.getElementById("o-net-s").textContent = s.join(" · ");
    }

    function summary() {
      if (!last) return "";
      var o = last.o, v = last.v, lines = ["GroundTruth AI — illustrative ROI estimate (not a forecast or a quote)",
        "Business case: " + (caseSel.value ? caseSel.options[caseSel.selectedIndex].text : "not selected"), ""];
      o.lines.forEach(function (l) {
        lines.push((labels[l[0]] || l[0]) + ": " + money(v["s_" + l[0]]) + " × " + Math.round(v["r_" + l[0]] * 100) + "% = " + money(l[1]));
      });
      lines.push("Total savings: " + money(o.gross), "− Distillation and validation: " + money(v.c_dist),
        "− License: " + (v.c_sol ? money(v.c_sol) : "not entered"), "Net annual value: " + money(o.net),
        "3-year value after implementation: " + money(o.three), "",
        "Not contractual: illustrative estimate based on the assumptions above; no warranty or guarantee of results.",
        "Source data is assumed to be retained. Strategic enablement is not priced.", location.href);
      return lines.join("\n");
    }

    function showCase() {
      var id = caseSel.value;
      Array.prototype.forEach.call(form.querySelectorAll(".strat-list"), function (u) { u.hidden = u.dataset.case !== id; });
      stratEmpty.hidden = !!id;
      pilot.href = "/pilot/?type=assessment" + (id ? "&case=" + id : "");
      var q = new URLSearchParams(location.search);
      if (id) q.set("case", id); else q.delete("case");
      var qs = q.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
    }

    form.addEventListener("input", function (e) { if (e.target.tagName === "INPUT" && e.target.type === "number") compute(); });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    caseSel.addEventListener("change", showCase);
    curSel.addEventListener("change", compute);
    document.getElementById("roi-reset").addEventListener("click", function () {
      inputs.forEach(function (i) { i.value = defaults[i.id]; });
      compute();
    });
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
    compute();
  });
})(typeof window !== "undefined" ? window : this);
