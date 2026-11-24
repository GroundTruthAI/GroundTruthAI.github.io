/* Pilot request form. No network requests: prepares a mailto: link or a copyable request. */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("pilot-form");
    if (!form) return;
    var q = new URLSearchParams(location.search);
    var caseSel = document.getElementById("p-case");
    var indSel = document.getElementById("p-ind");
    var typeSel = document.getElementById("p-type");
    var submit = document.getElementById("p-submit");
    var err = document.getElementById("p-err");
    var out = document.getElementById("p-out");
    var outH = document.getElementById("p-out-h");
    var outMsg = document.getElementById("p-out-msg");
    var text = document.getElementById("p-text");
    var copy = document.getElementById("p-copy");

    function setIf(sel, v) {
      if (v && sel.querySelector('option[value="' + v.replace(/[^A-Za-z0-9-]/g, "") + '"]')) sel.value = v;
    }
    setIf(caseSel, q.get("case"));
    setIf(indSel, q.get("industry"));
    setIf(typeSel, q.get("type"));

    function syncLabel() {
      var opt = caseSel.options[caseSel.selectedIndex];
      var t = typeSel.value;
      if (t === "partnership") submit.textContent = "Discuss a partnership";
      else if (t === "diligence") submit.textContent = "Request technical due diligence";
      else if (t === "assessment") submit.textContent = "Request an architecture assessment";
      else submit.textContent = (opt && opt.dataset.cta) ? opt.dataset.cta : "Request a Pilot";
    }
    caseSel.addEventListener("change", syncLabel);
    typeSel.addEventListener("change", syncLabel);
    syncLabel();

    function label(sel) { var o = sel.options[sel.selectedIndex]; return o && o.value ? o.text : "—"; }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var required = ["p-name", "p-email", "p-org", "p-consent"];
      var bad = [];
      required.forEach(function (id) {
        var el = document.getElementById(id);
        var ok = el.type === "checkbox" ? el.checked : el.value.trim() !== "" && el.checkValidity();
        el.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) bad.push(el);
      });
      if (bad.length) {
        err.hidden = false;
        err.textContent = "Please complete the required fields: name, a valid work email, organization and consent.";
        bad[0].focus();
        return;
      }
      err.hidden = true;
      var v = function (id) { return document.getElementById(id).value.trim() || "—"; };
      var body = [
        "Request type: " + label(typeSel),
        "Business case: " + label(caseSel),
        "Industry: " + label(indSel),
        "Name: " + v("p-name"),
        "Work email: " + v("p-email"),
        "Organization: " + v("p-org"),
        "Role: " + v("p-role"),
        "Timeline: " + label(document.getElementById("p-time")),
        "",
        "Data environment and constraint:",
        v("p-env")
      ].join("\n");
      var subject = submit.textContent + " — " + v("p-org");
      text.value = "Subject: " + subject + "\n\n" + body;
      out.hidden = false;
      var to = form.dataset.to;
      if (to) {
        outMsg.textContent = "Your email client should open with this request. If it does not, copy the text and send it to " + to + ".";
        window.location.href = "mailto:" + encodeURIComponent(to) + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      } else {
        outMsg.textContent = "Copy this request and send it to your GroundTruth AI contact. Nothing has been sent from this page.";
      }
      outH.focus();
    });

    copy.addEventListener("click", function () {
      function done() { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy request"; }, 2000); }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text.value).then(done, function () { text.select(); });
      } else { text.select(); try { document.execCommand("copy"); done(); } catch (e) { /* user can copy manually */ } }
    });
  });
})();
