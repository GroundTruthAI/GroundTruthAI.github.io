/* Executive brief viewer: one slide at a time, previous/next, keyboard, swipe, #slide-N links,
   full screen and language switch that keeps the current slide. Without JavaScript all slides are shown. */
(function () {
  "use strict";
  // PDF generation (tools/build_pdf.py adds ?pdf=1): load the static print fonts up front so no text is
  // printed while its font is still loading.
  if (/[?&]pdf=1\b/.test(location.search) && document.fonts && document.fonts.load) {
    [[400, 500, 600, 700, 800, "GT Print Sans"], [600, 700, 800, "GT Print Display"]].forEach(function (f) {
      var fam = f.pop();
      f.forEach(function (w) { document.fonts.load(w + ' 16px "' + fam + '"', "Aa0≈€%"); });
    });
  }
  document.addEventListener("DOMContentLoaded", function () {
    var deck = document.getElementById("deck");
    if (!deck) return;
    var slides = Array.prototype.slice.call(deck.querySelectorAll(".slide"));
    var ui = deck.querySelector(".deck-ui");
    var prev = deck.querySelector(".deck-prev");
    var next = deck.querySelector(".deck-next");
    var count = deck.querySelector(".deck-i");
    var full = document.querySelector(".deck-full");
    var lang = document.querySelector("[data-keep-hash]");
    var n = slides.length, cur = 0;
    document.body.classList.add("js-deck");
    ui.hidden = false;

    function fromHash() {
      var m = /^#slide-(\d+)$/.exec(location.hash);
      var i = m ? parseInt(m[1], 10) - 1 : 0;
      return i >= 0 && i < n ? i : 0;
    }
    function show(i, push) {
      cur = Math.max(0, Math.min(n - 1, i));
      slides.forEach(function (s, k) { s.hidden = k !== cur; });
      count.textContent = String(cur + 1);
      prev.disabled = cur === 0;
      next.disabled = cur === n - 1;
      var h = "#slide-" + (cur + 1);
      if (push && location.hash !== h) history.replaceState(null, "", h);
      if (lang) lang.setAttribute("href", lang.getAttribute("href").split("#")[0] + h);
    }
    prev.addEventListener("click", function () { show(cur - 1, true); });
    next.addEventListener("click", function () { show(cur + 1, true); });
    window.addEventListener("hashchange", function () { show(fromHash(), false); });

    document.addEventListener("keydown", function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      var tag = (e.target && e.target.tagName) || "";
      if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
      var k = e.key;
      if (k === "ArrowRight" || k === "PageDown" || (k === " " && tag !== "BUTTON" && tag !== "A")) { e.preventDefault(); show(cur + 1, true); }
      else if (k === "ArrowLeft" || k === "PageUp") { e.preventDefault(); show(cur - 1, true); }
      else if (k === "Home") { e.preventDefault(); show(0, true); }
      else if (k === "End") { e.preventDefault(); show(n - 1, true); }
      else if ((k === "f" || k === "F") && full && !full.hidden) { toggleFull(); }
    });

    var x0 = null, y0 = null;
    deck.addEventListener("touchstart", function (e) { var t = e.changedTouches[0]; x0 = t.clientX; y0 = t.clientY; }, { passive: true });
    deck.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var t = e.changedTouches[0], dx = t.clientX - x0, dy = t.clientY - y0;
      if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(cur + (dx < 0 ? 1 : -1), true);
      x0 = y0 = null;
    }, { passive: true });

    function toggleFull() {
      if (document.fullscreenElement) document.exitFullscreen();
      else if (deck.requestFullscreen) deck.requestFullscreen().catch(function () {});
    }
    if (full && deck.requestFullscreen && document.fullscreenEnabled) {
      full.hidden = false;
      full.addEventListener("click", toggleFull);
    }

    window.addEventListener("beforeprint", function () { slides.forEach(function (s) { s.hidden = false; }); });
    window.addEventListener("afterprint", function () { show(cur, false); });

    show(fromHash(), false);
  });
})();
