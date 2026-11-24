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
    ("challenge", "Business challenge"), ("opportunity", "Business opportunity"), ("solution", "GroundTruth AI approach"),
    ("scenario", "Illustrative scenario"), ("architecture", "Reference architecture"), ("outcomes", "Business outcomes"),
    ("metrics", "Evaluation metrics"), ("considerations", "Technical considerations"), ("evidence", "Available evidence"),
    ("engage", "Commercial engagement"),
]
PRINT_SKIP = {"opportunity", "scenario", "considerations"}


def _sec(id_, num, title, inner, cls=""):
    if id_ in PRINT_SKIP:
        cls = (cls + " no-print").strip()
    return (f'<section class="cs {cls}" id="{id_}" aria-labelledby="{id_}-h">'
            f'<h2 id="{id_}-h"><span class="cs-n" aria-hidden="true">{num:02d}</span>{esc(title)}</h2>{inner}</section>')


def pilot_href(c, kind=""):
    return f'/pilot/?case={c["id"]}' + (f"&type={kind}" if kind else "")


def scenario_block(c, heading="h3"):
    """Illustrative enterprise scenario. Always labelled; never presented as a customer story."""
    sc = c["scenario"]
    rows = [("Enterprise context", md(sc["context"])), ("Current architecture", md(sc["current"])),
            ("Business problem", md(sc["problem"])), ("Proposed GroundTruth AI architecture", md(sc["proposed"]))]
    dl = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    assum = ""
    if sc["assumptions"]:
        assum = ('<div class="sc-assume"><p class="sc-k">Illustrative assumptions</p>' + ul(sc["assumptions"])
                 + '<p class="sc-fine">Planning values, not measurements. The achievable reduction and model quality are validated per workload.</p></div>')
    cols = (
        '<div class="sc-grid">'
        f'<div><p class="sc-k">Technical constraints</p>{ul(sc["constraints"])}</div>'
        f'<div><p class="sc-k">Potential economic outcomes</p>{ul(sc["economic"])}</div>'
        f'<div><p class="sc-k">Potential strategic outcomes</p>{ul(sc["strategic"])}</div>'
        f'<div><p class="sc-k">Technical validation requirements</p>{ul(sc["validation"])}</div></div>')
    return (
        '<div class="scenario">'
        '<p class="sc-label"><span class="badge badge-illus">Illustrative enterprise scenario</span> Hypothetical organization; assumptions are for discussion and not contractual.</p>'
        f'<{heading} class="sc-name">{esc(sc["name"])}</{heading}>'
        f'<dl class="sc-dl">{dl}</dl>{assum}{cols}'
        f'<p class="sc-stake"><span class="sc-k">Relevant stakeholder</span> {esc(sc["stakeholder"])}</p>'
        f'<div class="cta-row cta-row-s">{button(c["cta"], pilot_href(c))}'
        f'<a class="link-arrow" href="/simulator/">Model this architecture in the simulator</a></div></div>')


STAGE_SHORT = {
    "discovery": "A short conversation about your problem, data architecture and constraints, and whether GroundTruth AI fits. No data is shared.",
    "assessment": "A scoped evaluation of one representative workload: data, baseline, integration, quality constraints and preliminary economics.",
    "pilot": "A structured evaluation in your environment against agreed technical and economic success criteria.",
}


def engagement_block(c=None, compact=False):
    """Three-stage engagement: discovery → feasibility assessment → enterprise pilot."""
    items = []
    for i, (key, name, cta, desc, points) in enumerate(S.ENGAGEMENT, 1):
        label = c["cta"] if (c and key == "discovery") else cta
        href = (pilot_href(c, "" if key == "discovery" else key) if c else f"/pilot/?type={key}")
        kind = "primary" if i == 1 else "ghost"
        pts = "" if compact else ul(points)
        text = STAGE_SHORT[key] if compact else desc
        items.append(f'<li class="eng eng-{key}"><p class="eng-n">Stage {i}</p><h3>{esc(name)}</h3><p>{esc(text)}</p>{pts}'
                     f'{button(label, href, kind)}</li>')
    return f'<ol class="eng-list">{"".join(items)}</ol>'


def render_case(c, cases, industries):
    by_id = {x["id"]: x for x in cases}
    ind = {i["slug"]: i for i in industries}
    a = c["architecture"]
    st = c["stakeholders"]
    imp = c["implementation"]
    ev = c["evidence"]
    p = c["pilot"]
    flag = c["tier"] == "flagship"
    pil = S.PILLAR_OF[c["id"]]
    roi_href = f'/roi/?case={c["id"]}'

    inds = "".join(f'<li><a class="chip" href="/industries/{s_}/">{esc(ind[s_]["name"])}</a></li>' for s_ in c["industries"] if s_ in ind)
    facts = (
        '<div class="case-facts">'
        f'<div class="side-card"><p class="side-h">Relevant industries</p><ul class="chips">{inds}</ul></div>'
        f'<div class="side-card"><p class="side-h">Primary buyers</p><p class="small">'
        + " · ".join(esc(_label('buyers', b)) for b in c["filters"]["buyers"])
        + f'</p></div><div class="side-card"><p class="side-h">Solution family</p><p class="small"><a href="/solutions/{pil["slug"]}/">{esc(pil["name"])}</a></p>'
        f'<a class="link-arrow" href="{roi_href}">Estimate the value</a></div></div>')

    hero = (
        '<div class="case-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Business cases", "/business-cases/"), (c["title"], None)])
        + f'<p class="eyebrow">{esc(pil["name"])} · {esc(c["eyebrow"])}'
        + (' · <span class="flag">Flagship</span>' if flag else "") + "</p>"
        + f'<h1>{esc(c["title"])}</h1><p class="case-headline">{md(c["headline"])}</p>'
        + f'<p class="lead">{md(c["summary"])}</p>'
        + '<div class="case-pso">'
        + f'<div><p class="pso-k">Business problem</p><p>{md(c["problem_short"])}</p></div>'
        + f'<div><p class="pso-k">GroundTruth AI solution</p><p>{md(c["solution_short"])}</p></div>'
        + f'<div><p class="pso-k">Primary outcome</p><p>{md(c["outcome_short"])}</p></div></div>'
        + '<div class="cta-row">' + button(c["cta"], pilot_href(c)) + button("Estimate the value", roi_href, "ghost")
        + '<button class="btn btn-ghost js-print" type="button" hidden>Print summary</button></div>'
        + facts
        + f'<p class="status-line">{badge("Enterprise application for pilot evaluation", "proposed")} '
          '<a href="#evidence">Evidence and validation status</a></p>'
        + '</div></div>')

    toc = ('<div class="case-toc"><nav aria-label="On this page"><p class="toc-h">On this page</p><ol>' + "".join(
        f'<li><a href="#{i}">{t}</a></li>' for i, t in TOC) + "</ol></nav>"
        + button(c["cta"], pilot_href(c), "primary", ' data-block') + "</div>")

    s = []
    s.append(_sec("challenge", 1, "Business challenge", paras(c["challenge"])))
    s.append(_sec("opportunity", 2, "Business opportunity",
                  f'<p class="lead-s">{md(c["outcome_short"])}</p>'
                  '<h3 class="h-s">Where conventional architectures fall short</h3>'
                  '<div class="approach-grid">' + "".join(
                      f'<div class="approach"><h4>{md(x["name"])}</h4><p>{md(x["limit"])}</p></div>' for x in c["approaches"])
                  + '</div><p class="note">Generic architectural approaches, not specific products. '
                    '<a href="/technology/#compare">How distillation compares with other techniques</a>.</p>'))
    sol = c["solution"]
    steps = "".join(f'<li><h3>{md(t)}</h3><p>{md(d)}</p></li>' for t, d in sol["steps"])
    s.append(_sec("solution", 3, "GroundTruth AI approach",
                  f'<p class="lead-s">{md(sol["intro"])}</p><ol class="steps">{steps}</ol>'
                  f'<div class="callout callout-limit"><p class="callout-h">What this does not do</p>{ul(sol["not"])}</div>'
                  '<p class="note"><a href="/technology/">How task-aware dataset distillation works</a> · '
                  '<a href="/platform/">What is available for evaluation today</a></p>'))
    s.append(_sec("scenario", 4, "Illustrative enterprise scenario", scenario_block(c)))
    s.append(_sec("architecture", 5, "Reference architecture",
                  '<p class="small">Reference architecture for pilot evaluation: it shows how the components would be placed, not an existing deployment.</p>'
                  + legend() + arch_figure(a["current"], f'{c["id"].lower()}-cur', "Before")
                  + arch_figure(a["proposed"], f'{c["id"].lower()}-pro', "After")
                  + (f'<div class="arch-notes">{ul(a["notes"])}</div>' if a.get("notes") else "")))
    o = c["outcomes"]
    rows = "".join(f'<tr><th scope="row">{md(m)}</th><td>{md(h)}</td><td><span class="cat cat-{k}">{CAT_LABEL[k]}</span></td></tr>'
                   for m, h, k in c["metrics"])
    s.append(_sec("outcomes", 6, "Business outcomes",
                  '<p>Potential outcomes; their size depends on the workload and is established in an evaluation.</p>'
                  '<div class="outcome-grid">'
                  f'<div class="oc oc-strat"><h3>Strategic business enablement</h3>{ul(o["strategic"])}'
                  '<p class="oc-note">Assessed qualitatively; no monetary value is assigned.</p></div>'
                  f'<div class="oc oc-direct"><h3>Direct cost reduction</h3>{ul(o["direct"])}</div>'
                  f'<div class="oc oc-ops"><h3>Operational efficiency</h3>{ul(o["operational"])}</div></div>'
                  f'<p class="note">Direct savings apply only to the data-proportional share of eligible cost lines, net of distillation and evaluation. '
                  f'<a href="{roi_href}">Model them with your own assumptions</a>.</p>'))
    s.append(_sec("metrics", 7, "Evaluation metrics",
                  '<p>Measured before and after on the same workload.</p>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Metric</th><th scope="col">How it is measured</th>'
                  f'<th scope="col">Category</th></tr></thead><tbody>{rows}</tbody></table></div>'))
    ip = "".join(f'<tr><th scope="row">{md(n)}</th><td><span class="st st-{k}">{STATUS_LABEL[k]}</span></td><td>{md(note)}</td></tr>'
                 for n, k, note in imp["integration_points"])
    caveats = ""
    if c.get("caveats"):
        caveats = f'<aside class="callout callout-legal" aria-label="Data governance"><p class="callout-h">Data governance</p>{ul(c["caveats"])}</aside>'
    s.append(_sec("considerations", 8, "Technical considerations",
                  f'<p>{md(imp["deployment"])}</p>'
                  '<div class="two-col">'
                  f'<div><h3 class="h-s">Required infrastructure</h3>{ul(imp["infrastructure"])}</div>'
                  f'<div><h3 class="h-s">Operational constraints</h3>{ul(imp["constraints"])}</div></div>'
                  '<h3 class="h-s">To be validated in an evaluation</h3>'
                  '<div class="ev-grid ev-grid-2">'
                  f'<div class="ev ev-gap"><h4>Open questions</h4>{ul(ev["gaps"])}</div>'
                  f'<div class="ev ev-risk"><h4>Risks managed in the pilot</h4>{ul(ev["risks"])}</div></div>'
                  + caveats +
                  '<h3 class="h-s">Integration points</h3>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Integration</th><th scope="col">Status</th>'
                  f'<th scope="col">Notes</th></tr></thead><tbody>{ip}</tbody></table></div>'
                  '<p class="note"><strong>Verified in prototype</strong>: exercised in the prototype used for internal experiments. '
                  '<strong>Proposed</strong>: designed, not built or tested. <strong>Customer system</strong>: owned and operated by the customer.</p>'))
    s.append(_sec("evidence", 9, "Available evidence",
                  f'<p class="status-line">{badge(ev["status"], "proposed")}</p>'
                  f'<p>{md(ev["summary"])}</p>'
                  f'<div class="ev ev-yes ev-wide"><h3>What supports it today</h3>{ul(ev["supports"])}</div>'
                  '<p class="note"><a href="/evidence/">Benchmark results, methodology and evidence classification</a> · '
                  '<a href="/evidence/#roadmap">Validation roadmap</a></p>'))
    ops = "".join(f'<li><strong>{md(r)}</strong> — {md(n)}</li>' for r, n in st["operational"])
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
    s.append(_sec("engage", 10, "Commercial engagement",
                  '<div class="no-print"><p>Start with a conversation. Commit to a pilot only once feasibility is clear.</p>'
                  + engagement_block(c, compact=True) + '</div>'
                  '<h3 class="h-s no-print">Who is usually involved</h3>'
                  '<dl class="stake no-print">'
                  f'<div><dt>Business sponsor</dt><dd><strong>{md(st["sponsor"][0])}</strong><span>{md(st["sponsor"][1])}</span></dd></div>'
                  f'<div><dt>Economic buyer</dt><dd><strong>{md(st["economic"][0])}</strong><span>{md(st["economic"][1])}</span></dd></div>'
                  f'<div><dt>Technical buyer</dt><dd><strong>{md(st["technical"][0])}</strong><span>{md(st["technical"][1])}</span></dd></div>'
                  '</dl>'
                  f'<ul class="plain no-print">{ops}</ul>'
                  '<h3 class="h-s" id="pilot">Enterprise pilot design</h3>' + pilot))

    rel = "".join(
        f'<li><a class="rel" href="{case_url(by_id[r])}"><span class="rel-p">{esc(S.PILLAR_OF[r]["name"])}</span><strong>{esc(by_id[r]["title"])}</strong>'
        f'<span>{esc(by_id[r]["outcome_short"])}</span></a></li>' for r in c["related"] if r in by_id)

    close = (
        '<section class="case-close" aria-labelledby="close-h"><div class="wrap">'
        f'<h2 id="close-h">{esc(c["cta"])}</h2>'
        '<p>A short architecture discovery conversation about your environment. No data is shared, and there is no commitment to a pilot.</p>'
        f'<div class="cta-row">{button(c["cta"], pilot_href(c))}{button("Request a feasibility assessment", pilot_href(c, "assessment"), "ghost")}'
        f'{button("Estimate the value first", roi_href, "ghost")}</div>'
        + (f'<h3 class="h-s">Related business cases</h3><ul class="rel-list">{rel}</ul>' if rel else "")
        + '</div></section>')

    print_head = (f'<div class="print-only print-head"><p><strong>GroundTruth AI · Business case summary</strong> · {esc(c["title"])} · '
                  f'{esc(S.BASE_URL + case_url(c))}</p></div>')
    print_foot = (f'<div class="print-only print-foot"><p><strong>Next step:</strong> {esc(c["cta"])} — '
                  f'{esc(S.BASE_URL)}/pilot/. Business case for pilot evaluation; not yet validated in production.</p></div>')

    body = (hero + print_head + '<div class="wrap case-layout">' + toc
            + f'<div class="case-main">{"".join(s)}{print_foot}</div></div>' + close)
    title = f'{c["title"]} — {pil["name"]}'
    page(case_url(c), title, f'{c["headline"]} {c["summary"]}'[:300], body,
         active="business-cases", cases=cases, priority="0.9" if flag else "0.8", body_class="pg-case")


def case_card(c, industries, size=""):
    ind = {i["slug"]: i["name"] for i in industries}
    data = " ".join(f'data-{dim}="{" ".join(c["filters"][dim])}"' for dim in S.FILTERS)
    data += f' data-industries="{" ".join(c["industries"])}" data-pillar="{S.PILLAR_OF[c["id"]]["slug"]}"'
    flag = c["tier"] == "flagship"
    return (
        f'<li class="bc-card {size}{" is-flag" if flag else ""}" {data}>'
        f'<p class="bc-meta">{esc(S.PILLAR_OF[c["id"]]["name"])}{" · Flagship" if flag else ""}</p>'
        f'<h3><a href="{case_url(c)}">{esc(c["title"])}</a></h3>'
        f'<p class="bc-k">Problem</p><p>{md(c["problem_short"])}</p>'
        f'<p class="bc-k">Outcome</p><p class="bc-out">{md(c["outcome_short"])}</p>'
        f'<p class="bc-ind">{" · ".join(esc(ind[s]) for s in c["industries"][:3] if s in ind)}{" · …" if len(c["industries"]) > 3 else ""}</p>'
        '</li>')


def render_explorer(cases, industries):
    by = {c["id"]: c for c in cases}
    filters = []
    pil_opts = "".join(f'<option value="{p["slug"]}">{esc(p["name"])}</option>' for p in S.PILLARS)
    ind_opts = "".join(f'<option value="{i["slug"]}">{esc(i["name"])}</option>' for i in industries)
    filters.append('<div class="f-top">'
                   f'<div class="f-sel"><label for="f-pillar">Solution family</label><select id="f-pillar" data-dim="pillar"><option value="">All solution families</option>{pil_opts}</select></div>'
                   f'<div class="f-sel"><label for="f-industries">Industry</label><select id="f-industries" data-dim="industries"><option value="">All industries</option>{ind_opts}</select></div></div>')
    obj_label, obj_opts = S.FILTERS["objectives"]
    chips = "".join(f'<li><button type="button" class="fchip" aria-pressed="false" data-dim="objectives" data-val="{k}">{esc(v)}</button></li>'
                    for k, v in obj_opts)
    filters.append(f'<fieldset class="f-obj"><legend>{obj_label}</legend><ul class="fchips">{chips}</ul></fieldset>')
    sel = []
    for dim in ("architecture", "deployment", "buyers", "problems"):
        lab, opts = S.FILTERS[dim]
        o = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in opts)
        sel.append(f'<div class="f-sel"><label for="f-{dim}">{lab}</label><select id="f-{dim}" data-dim="{dim}"><option value="">Any</option>{o}</select></div>')
    filters.append('<details class="f-more"><summary>More filters: architecture, deployment, buyer, problem</summary>'
                   f'<div class="f-grid">{"".join(sel)}</div></details>')

    order = [cid for p in S.PILLARS for cid in p["cases"]]
    flag = [c for c in cases if c["tier"] == "flagship"]
    rest = [by[cid] for cid in order if by[cid]["tier"] != "flagship"]
    cards = "".join(case_card(c, industries, "bc-lg") for c in flag) + "".join(case_card(c, industries) for c in rest)

    pillars = "".join(
        f'<li class="pl-mini{" is-flag" if p["flagship"] else ""}"><a href="/solutions/{p["slug"]}/"><strong>{esc(p["name"])}</strong>'
        f'<span>{esc(p["message"])}</span><span class="pl-n">{len(p["cases"])} business cases</span></a></li>' for p in S.PILLARS)

    table_rows = "".join(
        f'<tr><th scope="row"><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></th>'
        f'<td>{esc(p["name"])}</td><td>{md(by[cid]["outcome_short"])}</td></tr>' for p in S.PILLARS for cid in p["cases"])

    body = (
        '<div class="page-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Business cases", None)])
        + '<p class="eyebrow">Business case explorer</p>'
        '<h1>Start from the problem you need to solve</h1>'
        '<p class="lead">Eleven enterprise problems in three solution families, where task-aware dataset distillation can change the economics '
        'or the feasibility of AI. Filter by what you are trying to achieve, or by your industry, architecture and role.</p>'
        f'<ul class="pl-minis">{pillars}</ul>'
        '</div></div>'
        '<section class="sec sec-tight" aria-labelledby="ex-h"><div class="wrap">'
        '<h2 id="ex-h" class="sr-only">Filter business cases</h2>'
        f'<form class="explorer" id="explorer" hidden aria-describedby="ex-help"><p id="ex-help" class="small">Filters combine: a case is shown when it matches every selected criterion. Any selected objective matches.</p>{"".join(filters)}'
        '<div class="f-foot"><p class="f-count" role="status" aria-live="polite"><span id="f-n">11</span> of 11 business cases shown</p>'
        '<button type="reset" class="btn btn-ghost btn-sm" id="f-reset">Reset filters</button></div></form>'
        f'<ul class="bc-grid" id="bc-grid">{cards}</ul>'
        '<p class="f-empty" id="f-empty" hidden>No business case matches every filter. Remove a filter, or <a href="/pilot/">describe your situation</a> and we will tell you plainly whether distillation fits.</p>'
        '</div></section>'
        '<section class="sec" aria-labelledby="idx-h"><div class="wrap">'
        '<h2 id="idx-h">Business case index</h2><p>Grouped by solution family. Every case is an enterprise application for pilot evaluation.</p>'
        '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Business case</th><th scope="col">Solution family</th>'
        f'<th scope="col">Primary outcome</th></tr></thead><tbody>{table_rows}</tbody></table></div>'
        '<div class="cta-row">' + button("Contact", "/pilot/") + button("Try the architecture simulator", "/simulator/", "ghost")
        + button("Open the ROI calculator", "/roi/", "ghost") + button("Executive overview (7 slides)", "/resources/executive-brief/", "ghost") + '</div>'
        '</div></section>')
    page("/business-cases/", "Business cases by solution family",
         "Eleven enterprise business cases in three solution families: distributed enterprise intelligence (OT/IT segregation, cross-enterprise analytics, multi-site industrial AI), AI infrastructure efficiency and intelligent data mobility.",
         body, active="business-cases", cases=cases, priority="0.9", extra_js=("/assets/js/explorer.js",))
