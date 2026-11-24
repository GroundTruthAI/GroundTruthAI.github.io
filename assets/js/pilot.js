/* Engagement request form (discovery, feasibility, pilot, partnership, diligence).
   Sends via the FormSubmit AJAX endpoint; on any failure prepares a mailto: link and a copyable request.
   Success is only reported when the delivery service confirms it. */
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

    var LABELS = { assessment: "Request a feasibility assessment", pilot: "Request an enterprise pilot",
                   partnership: "Discuss a technology integration", diligence: "Request technical due diligence" };
    function syncLabel() {
      var opt = caseSel.options[caseSel.selectedIndex];
      var t = typeSel.value;
      if (LABELS[t]) submit.textContent = LABELS[t];
      else submit.textContent = (opt && opt.dataset.cta) ? opt.dataset.cta : "Discuss your use case";
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
      var to = form.dataset.to;
      var endpoint = form.dataset.endpoint;
      var status = document.getElementById("p-status");
      var label0 = submit.textContent;

      function fallback(reason) {
        text.value = "Subject: " + subject + "\n\n" + body;
        out.hidden = false;
        out.classList.remove("ok");
        outH.textContent = "We could not send your request automatically";
        outMsg.textContent = reason + (to ? " Your email client will open with the request pre-filled; if it does not, copy the text below and send it to " + to + "." :
          " Please copy the text below and send it to your GroundTruth AI contact.");
        copy.hidden = false; text.hidden = false;
        outH.focus();
        if (to) window.location.href = "mailto:" + encodeURIComponent(to) + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      }

      if (document.getElementById("p-hp").value) return; // bot trap
      if (!endpoint || !window.fetch) { fallback("Online delivery is not available in this browser."); return; }

      submit.disabled = true;
      submit.textContent = "Sending…";
      status.textContent = "Sending your request…";
      var payload = {
        _subject: subject, _template: "table", _captcha: "false",
        request_type: label(typeSel), business_case: label(caseSel), industry: label(indSel),
        name: v("p-name"), email: v("p-email"), organization: v("p-org"), role: v("p-role"),
        timeline: label(document.getElementById("p-time")), data_environment: v("p-env"),
        page: location.href
      };
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          submit.disabled = false; submit.textContent = label0; status.textContent = "";
          if (res.ok && String(res.j.success) === "true") {
            form.reset(); syncLabel();
            out.hidden = false; out.classList.add("ok");
            outH.textContent = "Request sent";
            outMsg.textContent = "Thank you. The delivery service confirmed your request for the GroundTruth AI team. We will reply to " + payload.email + " with a proposal for a short call.";
            copy.hidden = true; text.hidden = true;
            outH.focus();
          } else {
            fallback("The delivery service did not accept the request" + (res.j && res.j.message ? " (" + res.j.message + ")." : "."));
          }
        })
        .catch(function () {
          submit.disabled = false; submit.textContent = label0; status.textContent = "";
          fallback("The network request failed.");
        });
    });

    copy.addEventListener("click", function () {
      function done() { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy request"; }, 2000); }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text.value).then(done, function () { text.select(); });
      } else { text.select(); try { document.execCommand("copy"); done(); } catch (e) { /* user can copy manually */ } }
    });
  });
})();
