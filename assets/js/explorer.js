/* Business case explorer: progressive enhancement over a fully linked, indexable list. */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("explorer");
    var grid = document.getElementById("bc-grid");
    if (!form || !grid) return;
    form.hidden = false;

    var cards = Array.prototype.slice.call(grid.querySelectorAll(".bc-card"));
    var chips = Array.prototype.slice.call(form.querySelectorAll(".fchip"));
    var selects = Array.prototype.slice.call(form.querySelectorAll("select[data-dim]"));
    var count = document.getElementById("f-n");
    var empty = document.getElementById("f-empty");
    var more = form.querySelector(".f-more");

    function state() {
      var s = { objectives: [] };
      chips.forEach(function (c) { if (c.getAttribute("aria-pressed") === "true") s.objectives.push(c.dataset.val); });
      selects.forEach(function (sel) { if (sel.value) s[sel.dataset.dim] = sel.value; });
      return s;
    }

    function apply(push) {
      var s = state(), shown = 0;
      cards.forEach(function (card) {
        var ok = true;
        if (s.objectives.length) {
          var have = (card.dataset.objectives || "").split(" ");
          ok = s.objectives.some(function (o) { return have.indexOf(o) !== -1; });
        }
        Object.keys(s).forEach(function (dim) {
          if (dim === "objectives" || !ok) return;
          ok = (card.dataset[dim] || "").split(" ").indexOf(s[dim]) !== -1;
        });
        card.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = String(shown);
      empty.hidden = shown !== 0;
      if (push) {
        var q = new URLSearchParams();
        if (s.objectives.length) q.set("objective", s.objectives.join(","));
        Object.keys(s).forEach(function (d) { if (d !== "objectives") q.set(d, s[d]); });
        var qs = q.toString();
        history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
      }
    }

    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") === "true" ? "false" : "true");
        apply(true);
      });
    });
    selects.forEach(function (sel) { sel.addEventListener("change", function () { apply(true); }); });
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    form.addEventListener("reset", function () {
      setTimeout(function () {
        chips.forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
        apply(true);
      }, 0);
    });

    // restore from URL
    var q = new URLSearchParams(location.search);
    (q.get("objective") || "").split(",").forEach(function (o) {
      chips.forEach(function (c) { if (c.dataset.val === o) c.setAttribute("aria-pressed", "true"); });
    });
    var anySelect = false;
    selects.forEach(function (sel) {
      var v = q.get(sel.dataset.dim);
      if (v && sel.querySelector('option[value="' + v.replace(/[^a-z0-9-]/g, "") + '"]')) { sel.value = v; anySelect = true; }
    });
    if (anySelect && more) more.open = true;
    apply(false);
  });
})();
