"""Solution-family (commercial pillar) landing pages: /solutions/<slug>/."""
from content import site as S
from .core import esc, md, ul, page, breadcrumb, button
from .diagrams import viz_pillar_distributed, viz_pillar_efficiency, viz_pillar_mobility
from .pages_cases import case_url, scenario_block, engagement_block

VIZ = {"distributed-enterprise-intelligence": viz_pillar_distributed,
       "ai-infrastructure-efficiency": viz_pillar_efficiency,
       "intelligent-data-mobility": viz_pillar_mobility}

# Which business case's illustrative scenario is featured on each pillar page
FEATURED_SCENARIO = {"distributed-enterprise-intelligence": "BC01",
                     "ai-infrastructure-efficiency": "BC03",
                     "intelligent-data-mobility": "BC05"}


def render_pillar(p, cases):
    by = {c["id"]: c for c in cases}
    others = [o for o in S.PILLARS if o["slug"] != p["slug"]]
    items = "".join(
        f'<li class="pc{" is-flag" if by[cid]["tier"] == "flagship" else ""}"><h3><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></h3>'
        f'<p class="pc-head">{md(by[cid]["headline"])}</p>'
        f'<p class="bc-k">Problem</p><p>{md(by[cid]["problem_short"])}</p>'
        f'<p class="bc-k">Outcome</p><p class="bc-out">{md(by[cid]["outcome_short"])}</p>'
        f'<a class="link-arrow" href="{case_url(by[cid])}">Read the business case</a></li>'
        for cid in p["cases"] if cid in by)
    sc_case = by[FEATURED_SCENARIO[p["slug"]]]
    other_links = "".join(f'<li><a class="chip chip-lg" href="/solutions/{o["slug"]}/">{esc(o["name"])}</a></li>' for o in others)
    first = by[p["cases"][0]]
    body = (
        '<div class="page-hero pillar-hero"><div class="wrap">'
        + breadcrumb([("Home", "/"), ("Business cases", "/business-cases/"), (p["name"], None)])
        + f'<p class="eyebrow">Solution family{" · flagship" if p["flagship"] else ""}</p>'
        f'<h1>{esc(p["name"])}</h1><p class="case-headline">{esc(p["message"])}</p>'
        '<div class="two-col pillar-top"><div>'
        f'<p class="pso-k">The enterprise problem</p><p>{md(p["problem"])}</p>'
        f'<p class="pso-k">The business outcome</p><p class="pillar-out">{md(p["outcome"])}</p>'
        '<div class="cta-row">' + button(p["cta"], f'/pilot/?case={first["id"]}') + button("Model it in the simulator", "/simulator/", "ghost") + '</div>'
        f'</div><div class="fc-viz">{VIZ[p["slug"]]()}</div></div>'
        '</div></div>'
        '<section class="sec" aria-labelledby="pc-h"><div class="wrap">'
        f'<p class="eyebrow">Business cases</p><h2 id="pc-h">{len(p["cases"])} business cases in this solution family</h2>'
        f'<ul class="pc-grid">{items}</ul></div></section>'
        '<section class="sec sec-alt" aria-labelledby="pv-h"><div class="wrap two-col">'
        f'<div><h2 id="pv-h">What it changes</h2>{ul(p["points"])}</div>'
        '<div class="side-card"><p class="side-h">What it does not change</p>' + ul([
            "Distilled datasets are derived from source data and stay under the same classification, protection and transfer rules.",
            "Distillation is not anonymization, encryption or a security control, and grants no legal authorization for any transfer.",
            "Original data remains in its source environment under existing retention policies; nothing is deleted by default.",
        ]) + '<p class="small"><a href="/evidence/">Evidence and validation status</a></p></div></div></section>'
        '<section class="sec" aria-labelledby="ps-h"><div class="wrap">'
        '<p class="eyebrow">Illustrative enterprise scenario</p>'
        f'<h2 id="ps-h">{esc(sc_case["title"])}: how it could work</h2>'
        + scenario_block(sc_case) + '</div></section>'
        '<section class="sec sec-alt" aria-labelledby="pe-h"><div class="wrap">'
        '<p class="eyebrow">Commercial engagement</p><h2 id="pe-h">Start with a conversation, not a commitment</h2>'
        + engagement_block() +
        f'<h3 class="h-s">Other solution families</h3><ul class="chips">{other_links}</ul></div></section>')
    page(f'/solutions/{p["slug"]}/', f'{p["name"]} — enterprise solutions', p["seo"], body,
         active="business-cases", cases=cases, priority="0.9" if p["flagship"] else "0.8")
