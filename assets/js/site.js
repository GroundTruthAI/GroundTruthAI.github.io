/* GroundTruth AI — global behaviour: navigation, business-case menu, print, on-page TOC. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.add("js");

  function ready(fn) {
    if (document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    // ---- mobile navigation
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = toggle.getAttribute("aria-expanded") === "true";
        toggle.setAttribute("aria-expanded", String(!open));
        nav.classList.toggle("open", !open);
      });
    }

    // ---- business cases mega menu (disclosure pattern)
    var mmBtn = document.querySelector(".mm-toggle");
    var mm = document.getElementById("mm-cases");
    function setMenu(open) {
      if (!mmBtn || !mm) return;
      mmBtn.setAttribute("aria-expanded", String(open));
      mm.hidden = !open;
    }
    if (mmBtn && mm) {
      mmBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        setMenu(mmBtn.getAttribute("aria-expanded") !== "true");
      });
      document.addEventListener("click", function (e) {
        if (!mm.hidden && !mm.contains(e.target)) setMenu(false);
      });
      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && !mm.hidden) { setMenu(false); mmBtn.focus(); }
      });
      mm.addEventListener("focusout", function (e) {
        if (e.relatedTarget && !mm.contains(e.relatedTarget) && e.relatedTarget !== mmBtn) setMenu(false);
      });
    }

    // ---- print buttons (hidden without JS)
    Array.prototype.forEach.call(document.querySelectorAll(".js-print"), function (b) {
      b.hidden = false;
      b.addEventListener("click", function () { window.print(); });
    });


    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // ---- reveal on scroll
    var sel = ".sec h2, .fc, .tension, .vg, .flow-steps li, .ev-stat, .bc-card, .more-list li, .approach, .oc, .ev, .comp, .lvl, .pm, " +
              ".con, .ind-card, .ind-case, .arch-fig, .stake > div, .int-grid > div, .case-pso > div, .hero-stats .stat, .rel-list li";
    if (!reduce && "IntersectionObserver" in window) {
      var els = document.querySelectorAll(sel);
      var rio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); rio.unobserve(en.target); } });
      }, { rootMargin: "0px 0px -8% 0px" });
      Array.prototype.forEach.call(els, function (el) {
        var sibs = el.parentNode ? Array.prototype.indexOf.call(el.parentNode.children, el) : 0;
        el.style.transitionDelay = Math.min(sibs, 6) * 85 + "ms";
        el.classList.add("rv");
        rio.observe(el);
      });
      window.addEventListener("beforeprint", function () {
        Array.prototype.forEach.call(els, function (el) { el.classList.add("in"); });
      });
    }

    // ---- on-page TOC highlighting
    var tocLinks = document.querySelectorAll(".case-toc a");
    if (tocLinks.length && "IntersectionObserver" in window) {
      var map = {};
      Array.prototype.forEach.call(tocLinks, function (a) { map[a.getAttribute("href").slice(1)] = a; });
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && map[en.target.id]) {
            Array.prototype.forEach.call(tocLinks, function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
            map[en.target.id].classList.add("is-active");
            map[en.target.id].setAttribute("aria-current", "location");
          }
        });
      }, { rootMargin: "-30% 0px -60% 0px" });
      Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
    }
  });
})();
