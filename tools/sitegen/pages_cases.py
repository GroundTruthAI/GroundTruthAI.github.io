"""Business case pages and the business case explorer."""
import glob
import importlib.util
import os

from content import site as S
from .core import esc, md, paras, ul, page, breadcrumb, badge, button
from .diagrams import arch_figure, legend

CASES_DIR = os.path.join(os.path.dirname(__file__), "..", "content", "cases")

STATUS_LABEL = {"verified": "Verified in prototype", "proposed": "Proposed integration", "customer": "Customer system"}
CAT_LABEL = {"direct": "Direct cost", "operational": "Operational", "strategic": "Strategic", "quality": "Model quality"}
SCEN_LABEL = S.ROI_SCENARIOS


def load_cases():
    cases = []
    for f in sorted(glob.glob(os.path.join(CASES_DIR, "bc*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        cases.append(m.CASE)
    cases.sort(key=lambda c: c["rank"])
    return cases


def case_url(c):
    return f'/business-cases/{c["slug"]}/'


def _label(dim, key):
    return dict(S.FILTERS[dim][1])[key]


TOC = [
    ("challenge", "Business challenge"), ("gap", "Why existing approaches fall short"), ("solution", "Solution"),
    ("architecture", "Reference architecture"), ("outcomes", "Business outcomes"), ("metrics", "Metrics"),
    ("stakeholders", "Stakeholders"), ("implementation", "Implementation"), ("evidence", "Evidence"),
    ("pilot", "Pilot proposal"),
]


def _sec(id_, num, title, inner, cls=""):
    return (f'<section class="cs {cls}" id="{id_}" aria-labelledby="{id_}-h">'
            f'<h2 id="{id_}-h"><span class="cs-n" aria-hidden="true">{num:02d}</span>{esc(title)}</h2>{inner}</section>')


def render_case(c, cases, industries):
    by_id = {x["id"]: x for x in cases}
    ind = {i["slug"]: i for i in industries}
    a = c["architecture"]
    st = c["stakeholders"]
    imp = c["implementation"]
    ev = c["evidence"]
    p = c["pilot"]
    flag = c["tier"] == "flagship"
    pilot_href = f'/pilot/?case={c["id"]}'
    roi_href = f'/roi/?case={c["id"]}'

    inds = "".join(f'<li><a class="chip" href="/industries/{s_}/">{esc(ind[s_]["name"])}</a></li>' for s_ in c["industries"] if s_ in ind)
    facts = (
        '<div class="case-facts">'
        f'<div class="side-card"><p class="side-h">Relevant industries</p><ul class="chips">{inds}</ul></div>'
        f'<div class="side-card"><p class="side-h">Primary buyers</p><p class="small">'
        + " · ".join(esc(_label('buyers', b)) for b in c["filters"]["buyers"])
        + f'</p></div><div class="side-card"><p class="side-h">Value model</p><p class="small">{esc(SCEN_LABEL[c["roi_scenario"]])}</p>'
        f'<a class="link-arrow" href="{roi_href}">Open ROI scenario</a></div></div>')

    hero = (
        '<div class="case-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Business cases", "/business-cases/"), (c["title"], None)])
        + f'<p class="eyebrow"><span class="code">{c["id"]}</span> {esc(c["eyebrow"])}'
        + (' · <span class="flag">Flagship</span>' if flag else "") + "</p>"
        + f'<h1>{esc(c["title"])}</h1><p class="case-headline">{md(c["headline"])}</p>'
        + f'<p class="lead">{md(c["summary"])}</p>'
        + '<div class="case-pso">'
        + f'<div><p class="pso-k">Business problem</p><p>{md(c["problem_short"])}</p></div>'
        + f'<div><p class="pso-k">Proposed solution</p><p>{md(c["solution_short"])}</p></div>'
        + f'<div><p class="pso-k">Primary outcome</p><p>{md(c["outcome_short"])}</p></div></div>'
        + '<div class="cta-row">' + button(c["cta"], pilot_href) + button("Estimate the value", roi_href, "ghost")
        + '<button class="btn btn-ghost js-print" type="button" hidden>Print summary</button></div>'
        + facts
        + f'<p class="status-line">{badge("Proposed enterprise application", "proposed")} Not yet validated in production. '
          '<a href="#evidence">See the evidence and its limits</a>.</p>'
        + '</div></div>')

    toc = ('<div class="case-toc"><nav aria-label="On this page"><p class="toc-h">On this page</p><ol>' + "".join(
        f'<li><a href="#{i}">{t}</a></li>' for i, t in TOC) + "</ol></nav>"
        + button(c["cta"], pilot_href, "primary", ' data-block') + "</div>")

    s = []
    s.append(_sec("challenge", 1, "Business challenge", paras(c["challenge"])))
    s.append(_sec("gap", 2, "Why existing approaches are insufficient",
                  '<div class="approach-grid">' + "".join(
                      f'<div class="approach"><h3>{md(x["name"])}</h3><p>{md(x["limit"])}</p></div>' for x in c["approaches"])
                  + '</div><p class="note">Trade-offs describe generic architectural approaches, not specific products.</p>'))
    sol = c["solution"]
    steps = "".join(f'<li><h3>{md(t)}</h3><p>{md(d)}</p></li>' for t, d in sol["steps"])
    s.append(_sec("solution", 3, "GroundTruth AI solution",
                  f'<p class="lead-s">{md(sol["intro"])}</p><ol class="steps">{steps}</ol>'
                  f'<div class="callout callout-limit"><p class="callout-h">What this does not do</p>{ul(sol["not"])}</div>'))
    s.append(_sec("architecture", 4, "Reference architecture",
                  legend() + arch_figure(a["current"], f'{c["id"].lower()}-cur', "Existing")
                  + arch_figure(a["proposed"], f'{c["id"].lower()}-pro', "Proposed")
                  + (f'<div class="arch-notes">{ul(a["notes"])}</div>' if a.get("notes") else "")))
    o = c["outcomes"]
    s.append(_sec("outcomes", 5, "Business outcomes",
                  '<div class="outcome-grid">'
                  f'<div class="oc oc-direct"><h3>Direct cost reduction</h3>{ul(o["direct"])}</div>'
                  f'<div class="oc oc-ops"><h3>Operational efficiency</h3>{ul(o["operational"])}</div>'
                  f'<div class="oc oc-strat"><h3>Strategic enablement</h3>{ul(o["strategic"])}'
                  '<p class="oc-note">Strategic value is assessed qualitatively; no monetary value is assigned.</p></div></div>'
                  f'<p class="note">Direct savings apply only to the data-proportional share of each cost line and are net of the cost of distillation. '
                  f'<a href="{roi_href}">Model them with your own assumptions</a>.</p>'))
    rows = "".join(f'<tr><th scope="row">{md(m)}</th><td>{md(h)}</td><td><span class="cat cat-{k}">{CAT_LABEL[k]}</span></td></tr>'
                   for m, h, k in c["metrics"])
    s.append(_sec("metrics", 6, "Quantifiable business metrics",
                  '<p>Metrics a customer can use to evaluate the solution, measured before and after on the same workload.</p>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Metric</th><th scope="col">How it is measured</th>'
                  f'<th scope="col">Category</th></tr></thead><tbody>{rows}</tbody></table></div>'))
    ops = "".join(f'<li><strong>{md(r)}</strong> — {md(n)}</li>' for r, n in st["operational"])
    s.append(_sec("stakeholders", 7, "Target stakeholders",
                  '<dl class="stake">'
                  f'<div><dt>Business sponsor</dt><dd><strong>{md(st["sponsor"][0])}</strong><span>{md(st["sponsor"][1])}</span></dd></div>'
                  f'<div><dt>Economic buyer</dt><dd><strong>{md(st["economic"][0])}</strong><span>{md(st["economic"][1])}</span></dd></div>'
                  f'<div><dt>Technical buyer</dt><dd><strong>{md(st["technical"][0])}</strong><span>{md(st["technical"][1])}</span></dd></div>'
                  '</dl>'
                  f'<h3 class="h-s">Operational stakeholders</h3><ul class="plain">{ops}</ul>'))
    ip = "".join(f'<tr><th scope="row">{md(n)}</th><td><span class="st st-{k}">{STATUS_LABEL[k]}</span></td><td>{md(note)}</td></tr>'
                 for n, k, note in imp["integration_points"])
    s.append(_sec("implementation", 8, "Implementation approach",
                  f'<p>{md(imp["deployment"])}</p>'
                  '<h3 class="h-s">Integration points</h3>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Integration</th><th scope="col">Status</th>'
                  f'<th scope="col">Notes</th></tr></thead><tbody>{ip}</tbody></table></div>'
                  '<p class="note"><strong>Verified</strong> means exercised in the prototype used for internal experiments. '
                  '<strong>Proposed</strong> means designed but not yet built or tested. <strong>Customer system</strong> means owned and operated by the customer.</p>'
                  '<div class="two-col">'
                  f'<div><h3 class="h-s">Required infrastructure</h3>{ul(imp["infrastructure"])}</div>'
                  f'<div><h3 class="h-s">Operational constraints</h3>{ul(imp["constraints"])}</div></div>'))
    s.append(_sec("evidence", 9, "Evidence",
                  f'<p class="status-line">{badge(ev["status"], "proposed")}</p>'
                  f'<p>{md(ev["summary"])}</p>'
                  '<div class="ev-grid">'
                  f'<div class="ev ev-yes"><h3>What supports it</h3>{ul(ev["supports"])}</div>'
                  f'<div class="ev ev-gap"><h3>What is not yet validated</h3>{ul(ev["gaps"])}</div>'
                  f'<div class="ev ev-risk"><h3>Risks we manage in the pilot</h3>{ul(ev["risks"])}</div></div>'
                  '<p class="note"><a href="/evidence/">Benchmark data, measurement notes and the evidence classification</a>.</p>'))
    pilot = (
        f'<p class="pilot-meta"><strong>Indicative duration:</strong> {esc(p["duration"])} · '
        '<strong>Pricing:</strong> scoped per engagement, not published.</p>'
        '<dl class="pilot">'
        f'<div><dt>Customer problem</dt><dd>{md(p["problem"])}</dd></div>'
        f'<div><dt>Required inputs</dt><dd>{ul(p["inputs"])}</dd></div>'
        f'<div><dt>Existing baseline</dt><dd>{md(p["baseline"])}</dd></div>'
        f'<div><dt>Evaluation methodology</dt><dd>{ul(p["method"])}</dd></div>'
        f'<div><dt>Technical success criteria</dt><dd>{ul(p["technical_criteria"])}</dd></div>'
        f'<div><dt>Economic success criteria</dt><dd>{ul(p["economic_criteria"])}</dd></div>'
        f'<div><dt>Deliverables</dt><dd>{ul(p["deliverables"])}</dd></div>'
        f'<div><dt>Production adoption conditions</dt><dd>{ul(p["adoption"])}</dd></div>'
        '</dl>')
    s.append(_sec("pilot", 10, "Pilot proposal", pilot))

    caveats = ""
    if c.get("caveats"):
        caveats = f'<aside class="callout callout-legal" aria-label="Important qualification"><p class="callout-h">Important</p>{ul(c["caveats"])}</aside>'

    rel = "".join(
        f'<li><a class="rel" href="{case_url(by_id[r])}"><span class="code">{r}</span><strong>{esc(by_id[r]["title"])}</strong>'
        f'<span>{esc(by_id[r]["outcome_short"])}</span></a></li>' for r in c["related"] if r in by_id)

    close = (
        '<section class="case-close" aria-labelledby="close-h"><div class="wrap">'
        f'<h2 id="close-h">{esc(c["cta"])}</h2>'
        f'<p>A scoped, {esc(p["duration"].split(" (")[0])} evaluation on your data, in your environment, against your baseline, with acceptance thresholds you set before we start.</p>'
        f'<div class="cta-row">{button(c["cta"], pilot_href)}{button("Estimate the value first", roi_href, "ghost")}</div>'
        + (f'<h3 class="h-s">Related business cases</h3><ul class="rel-list">{rel}</ul>' if rel else "")
        + '</div></section>')

    print_head = (f'<div class="print-only print-head"><p><strong>GroundTruth AI · Business case summary</strong> · {c["id"]} · '
                  f'{esc(S.BASE_URL + case_url(c))}</p></div>')

    body = (hero + print_head + '<div class="wrap case-layout">' + toc
            + f'<div class="case-main">{caveats}{"".join(s)}</div></div>' + close)
    page(case_url(c), f'{c["title"]} — business case', f'{c["headline"]} {c["summary"]}'[:300], body,
         active="business-cases", cases=cases, priority="0.9" if flag else "0.8", body_class="pg-case")


def case_card(c, industries, size=""):
    ind = {i["slug"]: i["name"] for i in industries}
    data = " ".join(f'data-{dim}="{" ".join(c["filters"][dim])}"' for dim in S.FILTERS)
    data += f' data-industries="{" ".join(c["industries"])}"'
    flag = c["tier"] == "flagship"
    return (
        f'<li class="bc-card {size}{" is-flag" if flag else ""}" {data}>'
        f'<p class="bc-meta"><span class="code">{c["id"]}</span>{" · Flagship" if flag else ""}</p>'
        f'<h3><a href="{case_url(c)}">{esc(c["title"])}</a></h3>'
        f'<p class="bc-k">Problem</p><p>{md(c["problem_short"])}</p>'
        f'<p class="bc-k">Outcome</p><p class="bc-out">{md(c["outcome_short"])}</p>'
        f'<p class="bc-ind">{" · ".join(esc(ind[s]) for s in c["industries"][:3] if s in ind)}{" · …" if len(c["industries"]) > 3 else ""}</p>'
        '</li>')


def render_explorer(cases, industries):
    filters = []
    # Objective = primary filter as toggle chips
    obj_label, obj_opts = S.FILTERS["objectives"]
    chips = "".join(f'<li><button type="button" class="fchip" aria-pressed="false" data-dim="objectives" data-val="{k}">{esc(v)}</button></li>'
                    for k, v in obj_opts)
    filters.append(f'<fieldset class="f-obj"><legend>{obj_label}</legend><ul class="fchips">{chips}</ul></fieldset>')
    sel = []
    ind_opts = "".join(f'<option value="{i["slug"]}">{esc(i["name"])}</option>' for i in industries)
    sel.append(f'<div class="f-sel"><label for="f-industries">Industry</label><select id="f-industries" data-dim="industries"><option value="">All industries</option>{ind_opts}</select></div>')
    for dim in ("architecture", "deployment", "buyers", "problems"):
        lab, opts = S.FILTERS[dim]
        o = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in opts)
        sel.append(f'<div class="f-sel"><label for="f-{dim}">{lab}</label><select id="f-{dim}" data-dim="{dim}"><option value="">Any</option>{o}</select></div>')
    filters.append('<details class="f-more"><summary>More filters: industry, architecture, deployment, buyer, problem</summary>'
                   f'<div class="f-grid">{"".join(sel)}</div></details>')

    flag = [c for c in cases if c["tier"] == "flagship"]
    rest = [c for c in cases if c["tier"] != "flagship"]
    cards = "".join(case_card(c, industries, "bc-lg") for c in flag) + "".join(case_card(c, industries) for c in rest)

    table_rows = "".join(
        f'<tr><td><span class="code">{c["id"]}</span></td><th scope="row"><a href="{case_url(c)}">{esc(c["title"])}</a></th>'
        f'<td>{md(c["outcome_short"])}</td><td>{"Flagship" if c["tier"] == "flagship" else "Business case"}</td>'
        f'<td>{esc(SCEN_LABEL[c["roi_scenario"]])}</td></tr>' for c in cases)

    body = (
        '<div class="page-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Business cases", None)])
        + '<p class="eyebrow">Business case explorer</p>'
        '<h1>Start from the problem you need to solve</h1>'
        '<p class="lead">Eleven enterprise problems where task-aware dataset distillation can change the economics or the feasibility of AI. '
        'Filter by what you are trying to achieve, or by your industry, architecture and role.</p>'
        '<div class="cta-row"><a class="btn btn-primary" href="/pilot/">Request a Pilot</a><a class="btn btn-ghost" href="/roi/">Open the ROI calculator</a></div>'
        '</div></div>'
        '<section class="sec sec-tight" aria-labelledby="ex-h"><div class="wrap">'
        '<h2 id="ex-h" class="sr-only">Filter business cases</h2>'
        f'<form class="explorer" id="explorer" hidden aria-describedby="ex-help"><p id="ex-help" class="small">Filters combine: a case is shown when it matches every selected criterion. Any selected objective matches.</p>{"".join(filters)}'
        '<div class="f-foot"><p class="f-count" role="status" aria-live="polite"><span id="f-n">11</span> of 11 business cases shown</p>'
        '<button type="reset" class="btn btn-ghost btn-sm" id="f-reset">Reset filters</button></div></form>'
        f'<ul class="bc-grid" id="bc-grid">{cards}</ul>'
        '<p class="f-empty" id="f-empty" hidden>No business case matches every filter. Remove a filter, or <a href="/pilot/">describe your situation</a> and we will tell you honestly whether distillation fits.</p>'
        '</div></section>'
        '<section class="sec" aria-labelledby="idx-h"><div class="wrap">'
        '<h2 id="idx-h">Business case index</h2><p>Ordered by current commercial priority. Every case is a proposed enterprise application, '
        'designed to be validated in a pilot.</p>'
        '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">ID</th><th scope="col">Business case</th><th scope="col">Primary outcome</th>'
        f'<th scope="col">Tier</th><th scope="col">ROI scenario</th></tr></thead><tbody>{table_rows}</tbody></table></div>'
        '</div></section>')
    page("/business-cases/", "Business cases", "Eleven enterprise data problems GroundTruth AI addresses with task-aware dataset distillation: OT/IT segregation, cross-enterprise analytics, AI training costs, multi-site industrial AI and more.",
         body, active="business-cases", cases=cases, priority="0.9", extra_js=("/assets/js/explorer.js",))
