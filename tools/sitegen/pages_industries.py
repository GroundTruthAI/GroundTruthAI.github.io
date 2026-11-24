"""Industry pages and the business-case × industry matrix."""
from .core import esc, md, paras, ul, page, breadcrumb, button
from .pages_cases import case_url

SHORT = {"manufacturing": "Manufacturing", "energy-utilities": "Energy & utilities", "oil-gas-mining": "Oil, gas & mining",
         "transportation-logistics": "Transport & logistics", "financial-services": "Financial services", "healthcare": "Healthcare",
         "telecommunications": "Telecom", "retail-consumer": "Retail", "multinational-groups": "Multinationals",
         "ai-infrastructure": "AI infrastructure"}


def render_industry(i, cases, industries):
    by_id = {c["id"]: c for c in cases}
    con = i["constraints"]
    rel = "".join(
        f'<li class="ind-case"><a href="{case_url(by_id[cid])}"><span class="code">{cid}</span>'
        f'<strong>{esc(by_id[cid]["title"])}</strong>{" <em class=\"flag-s\">Flagship</em>" if by_id[cid]["tier"] == "flagship" else ""}</a>'
        f'<p>{md(why)}</p><p class="ind-out"><span class="bc-k">Primary outcome</span> {md(by_id[cid]["outcome_short"])}</p></li>'
        for cid, why in i["cases"] if cid in by_id)
    first = i["cases"][0][0]
    others = "".join(f'<li><a class="chip" href="/industries/{o["slug"]}/">{esc(o["name"])}</a></li>' for o in industries if o["slug"] != i["slug"])
    body = (
        '<div class="page-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Industries", "/industries/"), (i["name"], None)])
        + '<p class="eyebrow">Industry</p>'
        f'<h1>{esc(i["name"])}</h1><p class="lead">{md(i["short"])}</p>'
        f'<div class="cta-row">{button("Request a Pilot", "/pilot/?industry=" + i["slug"])}'
        f'{button("Most relevant business case", case_url(by_id[first]), "ghost")}</div></div></div>'
        '<section class="sec" aria-labelledby="ib-h"><div class="wrap">'
        '<h2 id="ib-h">Business cases that matter most in this sector</h2>'
        '<p>Ordered by relevance. Each links to the full business case with architecture, metrics and pilot design.</p>'
        f'<ol class="ind-cases">{rel}</ol></div></section>'
        '<section class="sec sec-alt" aria-labelledby="ic-h"><div class="wrap">'
        '<h2 id="ic-h">Sector context</h2><div class="two-col">'
        f'<div>{paras(i["context"])}</div>'
        f'<div class="side-card"><p class="side-h">Typical data estate</p>{ul(i["data_estate"])}</div></div></div></section>'
        '<section class="sec" aria-labelledby="ik-h"><div class="wrap">'
        '<h2 id="ik-h">Constraints a solution must respect</h2>'
        '<div class="con-grid">'
        f'<div class="con"><h3>Technical</h3>{ul(con["technical"])}</div>'
        f'<div class="con"><h3>Operational</h3>{ul(con["operational"])}</div>'
        f'<div class="con"><h3>Governance</h3>{ul(con["governance"])}</div></div>'
        '<p class="note">Distilled datasets remain subject to the same sector regulation, data protection and security controls as their source data.</p>'
        '</div></section>'
        '<section class="sec sec-alt" aria-labelledby="ip-h"><div class="wrap two-col">'
        f'<div><h2 id="ip-h">A sensible first pilot</h2><p class="lead-s">{md(i["pilot_hint"])}</p>'
        f'<div class="cta-row">{button("Request a Pilot", "/pilot/?industry=" + i["slug"])}{button("Estimate the value", "/roi/?case=" + first, "ghost")}</div></div>'
        f'<div class="side-card"><p class="side-h">Who is usually involved</p>{ul(i["buyers"])}</div>'
        '</div></section>'
        f'<section class="sec sec-tight" aria-labelledby="io-h"><div class="wrap"><h2 id="io-h" class="h-s">Other industries</h2><ul class="chips">{others}</ul></div></section>')
    page(f'/industries/{i["slug"]}/', f'{i["name"]} — industry', f'{i["short"]} Relevant GroundTruth AI business cases, sector constraints and a first pilot.',
         body, active="industries", cases=cases, priority="0.7")


def render_industries_index(cases, industries):
    cards = "".join(
        f'<li class="ind-card"><h3><a href="/industries/{i["slug"]}/">{esc(i["name"])}</a></h3><p>{md(i["short"])}</p>'
        f'<p class="bc-ind">{len(i["cases"])} relevant business cases</p></li>' for i in industries)
    head = "".join(f'<th scope="col"><a href="/industries/{i["slug"]}/">{esc(SHORT.get(i["slug"], i["name"]))}</a></th>' for i in industries)
    rows = []
    for c in cases:
        cells = "".join(
            '<td class="m-yes"><span aria-hidden="true">●</span><span class="sr-only">Relevant</span></td>' if i["slug"] in c["industries"]
            else '<td class="m-no"><span class="sr-only">Not primary</span></td>' for i in industries)
        rows.append(f'<tr><th scope="row"><a href="{case_url(c)}">{c["id"]} · {esc(c["title"])}</a></th>{cells}</tr>')
    body = (
        '<div class="page-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Industries", None)])
        + '<p class="eyebrow">Industries</p><h1>The same problem looks different in every sector</h1>'
        '<p class="lead">A business case describes a problem we can help solve. An industry describes where it occurs, '
        'with its own data estate, operating constraints and governance. Each industry page explains which cases matter most and why.</p>'
        '</div></div>'
        f'<section class="sec sec-tight" aria-labelledby="il-h"><div class="wrap"><h2 id="il-h" class="sr-only">Industries</h2><ul class="ind-grid">{"".join(cards)}</ul></div></section>'
        '<section class="sec" aria-labelledby="mx-h"><div class="wrap"><h2 id="mx-h">Business cases by industry</h2>'
        '<p>Where each business case is most relevant. A blank cell means the case is not a primary fit for that sector, not that it cannot apply.</p>'
        f'<div class="table-wrap matrix-wrap" tabindex="0" role="group" aria-label="Business case by industry matrix (scrollable)"><table class="tbl matrix"><thead><tr><th scope="col">Business case</th>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></div></section>')
    page("/industries/", "Industries", "How GroundTruth AI business cases apply in manufacturing, energy, oil and gas, transportation, financial services, healthcare, telecom, retail, multinationals and AI infrastructure.",
         body, active="industries", cases=cases, priority="0.8")
