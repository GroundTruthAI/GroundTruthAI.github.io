/* ROI calculator — illustrative financial scenarios on user-entered assumptions.
   Separates direct cost reduction, operational efficiency and strategic enablement.
   Deducts distillation overhead and solution cost. Strategic value is never priced.
   Runs entirely in the browser; nothing is transmitted. */
(function () {
  "use strict";
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

    function n(id) {
      var el = document.getElementById(id);
      var v = parseFloat(el && el.value);
      return isFinite(v) && v > 0 ? v : 0;
    }
    function pct(id) { return Math.min(n(id), 100) / 100; }
    function money(v) {
      var c = curSel.value, a = Math.abs(v), s;
      if (a >= 1e6) s = (a / 1e6).toFixed(a >= 1e7 ? 1 : 2) + "M";
      else if (a >= 1e3) s = Math.round(a / 1e3) + "k";
      else s = Math.round(a).toString();
      return (v < 0 ? "−" : "") + c + s;
    }
    function num(v, unit) { return Math.round(v).toLocaleString("en-US") + " " + unit; }
    function li(label, value, cls) {
      return '<li' + (cls ? ' class="' + cls + '"' : "") + "><span>" + label + "</span><span>" + value + "</span></li>";
    }

    function compute() {
      var sc = scenSel.value, r = pct("c_red");
      var lines = [], over = 0, energy = [], ops = [];
      if (sc === "transfer") {
        var moved = n("t_dom") * n("t_vol") * 12 * pct("t_elig");          // eligible TB moved per year
        var stored = n("t_dom") * n("t_vol") * pct("t_elig") * n("t_ret"); // eligible TB held on average
        lines.push(["Transfer / network", moved * r * n("t_ctr")]);
        lines.push(["Central ingestion & processing", moved * r * n("t_cproc")]);
        lines.push(["Central storage of training copies", stored * r * n("t_cst") * 12]);
        over = moved * n("t_over");
        ops.push(li("Eligible data moved per year", num(moved, "TB")));
        ops.push(li("Avoided transfer volume per year", num(moved * r, "TB")));
      } else if (sc === "training") {
        var spend = n("r_spend") * pct("r_share");
        lines.push(["Training & retraining compute", spend * r]);
        over = n("r_runs") * n("r_rcost");
        var kwh = n("r_kwh") * pct("r_share") * r - n("r_runs") * n("r_dkwh");
        if (n("r_kwh") > 0) {
          energy.push(li("Net training energy avoided", num(kwh, "kWh"), kwh < 0 ? "neg" : ""));
          energy.push(li("Distillation energy included", num(n("r_runs") * n("r_dkwh"), "kWh"), "muted"));
          if (n("r_price") > 0) energy.push(li("Energy cost (inside compute line)", money(kwh * n("r_price")), "muted"));
        }
        if (n("r_hours") > 0) ops.push(li("Training hours avoided per year", num(n("r_hours") * pct("r_share") * r, "h")));
      } else {
        lines.push(["Storage incl. backup & replicas", n("i_tb") * r * n("i_cst") * 12]);
        lines.push(["Data-proportional compute", n("i_comp") * pct("i_share") * r]);
        var ekwh = n("i_kwh") * r - n("i_okwh");
        if (n("i_kwh") > 0) {
          lines.push(["Energy", n("i_kwh") * r * n("i_price")]);
          energy.push(li("Net energy avoided", num(ekwh, "kWh"), ekwh < 0 ? "neg" : ""));
          energy.push(li("Distillation energy included", num(n("i_okwh"), "kWh"), "muted"));
          if (n("i_grid") > 0) energy.push(li("Operational emissions avoided*", num(ekwh * n("i_grid") / 1000, "t CO₂e"), ekwh < 0 ? "neg" : ""));
        }
        over = n("i_ocost") + n("i_okwh") * n("i_price");
      }
      var gross = lines.reduce(function (a, l) { return a + l[1]; }, 0);
      var sol = n("c_sol");
      var net = gross - over - sol;

      var html = lines.map(function (l) { return li(l[0], money(l[1])); }).join("");
      html += li("Gross direct reduction", money(gross), "tot");
      html += li("Distillation overhead", money(-over), "neg");
      html += li("GroundTruth AI subscription", sol ? money(-sol) : "not entered", sol ? "neg" : "muted");
      document.getElementById("o-lines").innerHTML = html;

      var big = document.getElementById("o-net");
      big.textContent = money(net);
      big.classList.toggle("neg", net < 0);
      var s = [];
      s.push("3-year view: " + money(net * 3 - n("c_impl")) + (n("c_impl") ? " after one-time implementation" : ""));
      if (n("c_impl") && net > 0) s.push("simple payback ≈ " + Math.max(1, Math.ceil(n("c_impl") / (net / 12))) + " months");
      if (!sol) s.push("before solution cost");
      document.getElementById("o-net-s").textContent = s.join(" · ");

      var hrs = n("c_hrs") * pct("c_hsave");
      if (hrs > 0) {
        ops.push(li("Team hours freed per year", num(hrs, "h")));
        if (n("c_rate") > 0) ops.push(li("Value of hours freed", money(hrs * n("c_rate"))));
      }
      document.getElementById("o-ops").innerHTML = ops.length ? ops.join("") :
        '<li class="muted"><span>Enter team hours and avoidable share to estimate.</span><span></span></li>';
      document.getElementById("o-energy").innerHTML = energy.length ? energy.join("") + (sc === "infrastructure" && n("i_grid") > 0 ?
        '<li class="muted"><span>*Location-based, operational only. Not a lifecycle assessment.</span><span></span></li>' : "") :
        '<li class="muted"><span>Enter annual energy (kWh) to estimate. Distillation energy is deducted.</span><span></span></li>';
    }

    function showScenario() {
      Array.prototype.forEach.call(scens, function (f) { f.hidden = f.dataset.scen !== scenSel.value; });
      compute();
    }
    function showCase() {
      var id = caseSel.value;
      var opt = caseSel.options[caseSel.selectedIndex];
      if (opt && opt.dataset.scenario) scenSel.value = opt.dataset.scenario;
      Array.prototype.forEach.call(form.querySelectorAll(".strat-list"), function (u) { u.hidden = u.dataset.case !== id; });
      stratEmpty.hidden = !!id;
      pilot.href = "/pilot/" + (id ? "?case=" + id : "");
      var q = new URLSearchParams(location.search);
      if (id) q.set("case", id); else q.delete("case");
      var qs = q.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
      showScenario();
    }

    form.addEventListener("input", function (e) { if (e.target.tagName === "INPUT") compute(); });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    caseSel.addEventListener("change", showCase);
    scenSel.addEventListener("change", showScenario);
    curSel.addEventListener("change", compute);

    var pre = new URLSearchParams(location.search).get("case");
    if (pre && caseSel.querySelector('option[value="' + pre.replace(/[^A-Z0-9]/g, "") + '"]')) caseSel.value = pre;
    showCase();
  });
})();
