"""Executive commercial presentation (4 slides, EN + ES) at /resources/executive-brief/.

Single source of truth for the HTML viewer and the PDFs: tools/build_pdf.py prints these same pages with
headless Chrome (print styles in assets/css/brief.css give one 16:9 page per slide).
Content uses only information already published on the site; the 20-plant scenario is the site's
illustrative scenario (assumed 90% reduction) and is labelled as such.
"""
from content import site as S
from . import core
from .core import esc, asset, BRAND, CSP

DIR = "/resources/executive-brief/"
PDF = {"en": "GroundTruthAI_Executive_Brief_EN.pdf", "es": "GroundTruthAI_Resumen_Comercial_ES.pdf"}
URL = {"en": DIR, "es": DIR + "es.html"}
CONTACT = S.BASE_URL + "/pilot/"

T = {
    "en": {
        "title": "GroundTruth AI | Executive Business Overview",
        "desc": "GroundTruth AI in four slides: enterprise intelligence across distributed data, industrial AI without centralizing raw data, "
                "AI training efficiency and three business opportunities.",
        "deck": "GroundTruth AI executive overview", "skip": "Skip to the presentation",
        "prev": "Previous slide", "next": "Next slide", "of": "of", "slide": "Slide",
        "pdf": "Download PDF", "full": "Full screen", "back": "Website", "contact": "Discuss your use case",
        "other": "ES", "other_label": "Ver en español", "kicker": "Executive overview",
        "note": "Illustrative information for discussion. Figures and scenarios are estimates and have no contractual value.",
        "legal": [("Legal notice", "/legal-notice/"), ("Privacy policy", "/privacy/"), ("Cookie policy", "/cookie-policy/")],
        # slide 1
        "h1a": "Keep data distributed.", "h1b": "Centralize intelligence.",
        "lead": "Use information from industrial facilities, business units and distributed data environments to train AI models and "
                "perform analytics without centralizing entire raw datasets.",
        "benefits": ["Enable new AI and analytics projects", "Reduce unnecessary data movement", "Optimize AI infrastructure costs"],
        "d1_src": ["Industrial plants", "Business units", "Regions"], "d1_sub": "original data stays here",
        "d1_core": ["Enterprise", "intelligence"], "d1_cap": "ONLY OPTIMIZED, APPROVED DATASETS TRAVEL",
        "d1_title": "Original data stays in industrial plants, business units and regions; only optimized, approved datasets reach a common enterprise intelligence environment.",
        # slide 2
        "h2": "Three business opportunities. One technology.",
        "opps": [
            ("Unlock new AI projects", "Enable enterprise-wide analytics and AI training across industrial facilities, subsidiaries and segregated data environments.",
             ["Shared predictive maintenance models", "Cross-business analytics", "Intelligence across multiple industrial facilities"]),
            ("Reduce the cost of AI", "Optimize the datasets used to train and update AI models.",
             ["Lower computational requirements", "More efficient model retraining", "Reduced infrastructure expenditure"]),
            ("Move less data", "Optimize relevant information before transferring it between infrastructures.",
             ["Industrial data exchange between OT and IT", "Edge-to-cloud data transfer", "Multicloud data replication"]),
        ],
        "opp_tag": "Strategic priority",
        # slide 3
        "h3": "20 industrial plants. One AI model.",
        "s3_lead": "Imagine a global manufacturer that wants to anticipate equipment failures across all its facilities while keeping "
                   "original operational data within its existing industrial environments.",
        "s3_key": "Enterprise-wide predictive maintenance without complete raw data consolidation.",
        "s3_steps": ["Optimize the relevant information locally", "Keep original data in each plant",
                     "Transfer approved, task-specific datasets", "Train a common AI model centrally"],
        "s3_approach": "The GroundTruth AI approach",
        "figs": [("200 TB", "eligible data"), ("90%", "assumed reduction"), ("20 TB", "transferred"), ("180 TB", "potentially avoided")],
        "s3_qual": "Illustrative scenario, not a customer deployment. The reduction is an assumption that requires workload-specific validation.",
        "d3": {"trad": "Traditional approach", "gt": "With GroundTruth AI", "plant": "Plant", "central": ["Central data", "platform"],
               "model": ["AI", "model"], "stays": "data stays", "big": "200 TB copied", "small": "20 TB"},
        "d3_title": "Before: all historical data from the plants is copied to a central platform to train the AI model. After: each plant keeps its data, optimizes it locally and sends a much smaller approved dataset.",
        # slide 4
        "h4": "Tell us about your business challenge.",
        "s4_lead": "Identify an AI or analytics opportunity that is currently constrained by distributed data, data segregation, "
                   "infrastructure costs or excessive data movement.",
        "qs": ["What would you like to predict, analyze or improve?", "Where is the relevant information currently located?",
               "What prevents you from using it efficiently today?"],
        "cta": "Let's assess your use case", "nodata": "No data sharing is required for the initial discussion.",
    },
    "es": {
        "title": "GroundTruth AI | Resumen ejecutivo",
        "desc": "GroundTruth AI en cuatro diapositivas: inteligencia empresarial sobre datos distribuidos, IA industrial sin centralizar los datos "
                "originales, eficiencia en el entrenamiento de IA y tres oportunidades de negocio.",
        "deck": "Resumen ejecutivo de GroundTruth AI", "skip": "Ir a la presentación",
        "prev": "Diapositiva anterior", "next": "Diapositiva siguiente", "of": "de", "slide": "Diapositiva",
        "pdf": "Descargar PDF", "full": "Pantalla completa", "back": "Web", "contact": "Analicemos tu caso",
        "other": "EN", "other_label": "View in English", "kicker": "Resumen ejecutivo",
        "note": "Información orientativa para conversar. Las cifras y los escenarios son estimaciones y no tienen valor contractual.",
        "legal": [("Aviso legal", "/aviso-legal/"), ("Política de privacidad", "/privacidad/"), ("Política de cookies", "/cookies/")],
        "h1a": "Datos distribuidos.", "h1b": "Inteligencia centralizada.",
        "lead": "Aprovecha la información de plantas industriales, unidades de negocio y entornos de datos distribuidos para entrenar "
                "modelos de IA y realizar analítica sin centralizar todos los datos originales.",
        "benefits": ["Habilitar nuevos proyectos de IA y analítica", "Reducir el movimiento innecesario de datos", "Optimizar los costes de infraestructura de IA"],
        "d1_src": ["Plantas industriales", "Unidades de negocio", "Regiones"], "d1_sub": "datos originales en origen",
        "d1_core": ["Inteligencia", "empresarial"], "d1_cap": "SOLO VIAJAN DATOS OPTIMIZADOS Y APROBADOS",
        "d1_title": "Los datos originales se quedan en plantas, unidades de negocio y regiones; solo llegan a un entorno común de inteligencia empresarial conjuntos de datos optimizados y aprobados.",
        "h2": "Tres oportunidades de negocio. Una tecnología.",
        "opps": [
            ("Habilitar nuevos proyectos de IA", "Analítica y entrenamiento de IA a escala de empresa, con datos de plantas industriales, filiales y entornos segregados.",
             ["Modelos compartidos de mantenimiento predictivo", "Analítica entre unidades de negocio", "Inteligencia común a varias plantas"]),
            ("Reducir el coste de la IA", "Optimiza los datos con los que se entrenan y actualizan los modelos de IA.",
             ["Menos necesidades de computación", "Reentrenamientos más eficientes", "Menor gasto en infraestructura"]),
            ("Mover menos datos", "Optimiza la información relevante antes de transferirla entre infraestructuras.",
             ["Intercambio de datos entre sistemas industriales (OT) y corporativos (IT)", "Transferencia del edge a la nube", "Replicación entre nubes"]),
        ],
        "opp_tag": "Prioridad estratégica",
        "h3": "20 plantas industriales. Un modelo de IA común.",
        "s3_lead": "Una empresa industrial quiere anticipar fallos de equipos en todas sus instalaciones, manteniendo los datos operativos "
                   "originales dentro de sus entornos industriales.",
        "s3_key": "Mantenimiento predictivo global sin centralizar todos los datos industriales originales.",
        "s3_steps": ["Optimizar localmente la información relevante", "Mantener los datos originales en cada planta",
                     "Transferir solo datos aprobados y específicos para la tarea", "Entrenar un modelo de IA común de forma centralizada"],
        "s3_approach": "El enfoque de GroundTruth AI",
        "figs": [("200 TB", "datos elegibles"), ("90 %", "reducción supuesta"), ("20 TB", "transferidos"), ("180 TB", "que podrían no moverse")],
        "s3_qual": "Escenario ilustrativo, no un despliegue en cliente. La reducción es una hipótesis que debe validarse en cada caso.",
        "d3": {"trad": "Enfoque tradicional", "gt": "Con GroundTruth AI", "plant": "Planta", "central": ["Plataforma", "central"],
               "model": ["Modelo", "de IA"], "stays": "datos en planta", "big": "200 TB copiados", "small": "20 TB"},
        "d3_title": "Antes: todo el histórico de las plantas se copia a una plataforma central para entrenar el modelo. Después: cada planta conserva sus datos, los optimiza localmente y envía un conjunto aprobado mucho menor.",
        "h4": "Cuéntanos un reto de negocio.",
        "s4_lead": "Identifica una oportunidad de IA o analítica que actualmente esté limitada por la segregación de datos, "
                   "los costes de infraestructura o la dificultad de mover información.",
        "qs": ["¿Qué te gustaría predecir, analizar o mejorar?", "¿Dónde se encuentra actualmente la información relevante?",
               "¿Qué dificulta su aprovechamiento?"],
        "cta": "Analicemos tu caso", "nodata": "No es necesario compartir datos en la primera conversación.",
    },
}

GRAD = ('<defs><linearGradient id="{u}-g" x1="0" x2="1"><stop offset="0" stop-color="#2EE6A6"/><stop offset="1" stop-color="#3CC8F5"/></linearGradient>'
        '<marker id="{u}-ag" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="#2EE6A6"/></marker>'
        '<marker id="{u}-ar" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto"><path d="M0 0 10 5 0 10z" fill="#FF9466"/></marker></defs>')


def _svg(uid, vb, title, inner, cls):
    return (f'<svg class="{cls}" viewBox="{vb}" role="img" aria-labelledby="{uid}-t"><title id="{uid}-t">{esc(title)}</title>'
            + GRAD.format(u=uid) + inner + "</svg>")


def diagram_value(t, uid):
    g = []
    ys = [24, 140, 256]
    for name, y in zip(t["d1_src"], ys):
        g.append(f'<rect class="bd-box" x="6" y="{y}" width="252" height="92" rx="16"/>'
                 f'<text class="bd-t" x="24" y="{y + 40}">{esc(name)}</text>'
                 f'<text class="bd-s" x="24" y="{y + 66}">{esc(t["d1_sub"])}</text>'
                 + "".join(f'<rect class="bd-bar" x="{226 + k * 7}" y="{y + 52 + (k % 2) * 5}" width="4" height="{24 - (k % 2) * 5}" rx="1.5"/>' for k in range(3))
                 + f'<rect class="bd-gt" x="276" y="{y + 30}" width="32" height="32" rx="9"/><circle class="bd-gt2" cx="292" cy="{y + 46}" r="5"/>'
                 f'<path class="bd-flow" d="M308 {y + 46} C378 {y + 46} 390 194 436 194" marker-end="url(#{uid}-ag)"/>')
    g.append('<path class="bd-bound" d="M344 14 V354"/>')
    g.append(f'<circle class="bd-glow" cx="512" cy="194" r="86"/><circle class="bd-core" cx="512" cy="194" r="70"/>'
             f'<circle class="bd-ring" cx="512" cy="194" r="70" stroke="url(#{uid}-g)"/>'
             f'<text class="bd-ct" x="512" y="188" text-anchor="middle">{esc(t["d1_core"][0])}</text>'
             f'<text class="bd-ct" x="512" y="212" text-anchor="middle">{esc(t["d1_core"][1])}</text>')
    g.append(f'<text class="bd-cap" x="344" y="374" text-anchor="middle">{esc(t["d1_cap"])}</text>')
    return _svg(uid, "0 0 600 384", t["d1_title"], "".join(g), "bd bd-value")


def diagram_scenario(t, uid):
    d = t["d3"]
    g = []
    for row, y0, label in ((0, 8, d["trad"]), (1, 206, d["gt"])):
        g.append(f'<text class="bd-row" x="6" y="{y0 + 14}">{esc(label.upper())}</text>')
        ys = [y0 + 32, y0 + 78, y0 + 124]
        names = [f'{d["plant"]} 1', f'{d["plant"]} 2', f'{d["plant"]} 20']
        for i, (y, nm) in enumerate(zip(ys, names)):
            g.append(f'<rect class="bd-box" x="6" y="{y}" width="150" height="38" rx="10"/><text class="bd-p" x="20" y="{y + 25}">{esc(nm)}</text>')
            if i == 1:
                g.append(f'<text class="bd-dots" x="81" y="{y + 50}" text-anchor="middle">· · ·</text>')
            if row == 0:
                g.append(f'<path class="bd-raw" d="M156 {y + 19} C220 {y + 19} 228 {y0 + 97} 268 {y0 + 97}" marker-end="url(#{uid}-ar)"/>')
            else:
                g.append(f'<rect class="bd-gt" x="120" y="{y + 8}" width="24" height="22" rx="6"/>'
                         f'<path class="bd-flow bd-thin" d="M144 {y + 19} C300 {y + 19} 330 {y0 + 97} 432 {y0 + 97}" marker-end="url(#{uid}-ag)"/>')
        if row == 0:
            g.append(f'<rect class="bd-store" x="276" y="{y0 + 62}" width="128" height="70" rx="12"/>'
                     f'<text class="bd-p" x="340" y="{y0 + 92}" text-anchor="middle">{esc(d["central"][0])}</text>'
                     f'<text class="bd-p" x="340" y="{y0 + 112}" text-anchor="middle">{esc(d["central"][1])}</text>'
                     f'<path class="bd-raw" d="M404 {y0 + 97} H434" marker-end="url(#{uid}-ar)"/>'
                     f'<text class="bd-vol bd-vol-raw" x="210" y="{y0 + 190}" text-anchor="middle">{esc(d["big"])}</text>')
        else:
            g.append(f'<text class="bd-vol bd-vol-g" x="400" y="{y0 + 80}" text-anchor="middle">{esc(d["small"])}</text>'
                     f'<text class="bd-s" x="20" y="{y0 + 186}">{esc(d["stays"])}</text>')
        g.append(f'<circle class="bd-core" cx="488" cy="{y0 + 97}" r="50"/><circle class="bd-ring" cx="488" cy="{y0 + 97}" r="50" stroke="url(#{uid}-g)"/>'
                 f'<text class="bd-ct bd-ct-s" x="488" y="{y0 + 93}" text-anchor="middle">{esc(d["model"][0])}</text>'
                 f'<text class="bd-ct bd-ct-s" x="488" y="{y0 + 113}" text-anchor="middle">{esc(d["model"][1])}</text>')
    g.append('<path class="bd-div" d="M6 200 H574"/>')
    return _svg(uid, "0 0 580 408", t["d3_title"], "".join(g), "bd bd-scen")


ICONS = [
    # unlock new projects: distributed nodes joining a central node
    '<svg class="op-ic" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><circle cx="24" cy="24" r="7"/><circle cx="8" cy="10" r="4"/>'
    '<circle cx="40" cy="10" r="4"/><circle cx="8" cy="38" r="4"/><circle cx="40" cy="38" r="4"/><path d="M11 13 18 19M37 13 30 19M11 35 18 29M37 35 30 29"/></svg>',
    # reduce cost: descending bars
    '<svg class="op-ic" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><rect x="6" y="8" width="8" height="32" rx="2"/><rect x="20" y="18" width="8" height="22" rx="2"/>'
    '<rect x="34" y="28" width="8" height="12" rx="2"/><path d="M6 44 H42"/></svg>',
    # move less data: wide stream becoming a narrow one
    '<svg class="op-ic" viewBox="0 0 48 48" aria-hidden="true" focusable="false"><path d="M4 14 H18 M4 24 H18 M4 34 H18"/><path d="M18 10 V38 L30 24 Z"/><path d="M30 24 H44 M38 18 44 24 38 30"/></svg>',
]


def slides(t, lang):
    u = lambda n: f"b{lang}{n}"
    brand = f'<p class="sl-brand">{BRAND}</p>'
    def foot(n):
        return f'<p class="sl-foot"><span>groundtruthai.github.io</span><span>{n} / 4</span></p>'

    s1 = (f'<section class="slide s1" id="slide-1" aria-roledescription="slide" aria-label="{t["slide"]} 1 {t["of"]} 4">{brand}'
          f'<div class="s-grid"><div class="s-text"><p class="sl-kick">{esc(t["kicker"])}</p>'
          f'<h1 class="sl-h1">{esc(t["h1a"])} <span class="g">{esc(t["h1b"])}</span></h1>'
          f'<p class="sl-lead">{esc(t["lead"])}</p>'
          '<ul class="sl-ben">' + "".join(f'<li><span class="ben-n">{i}</span>{esc(b)}</li>' for i, b in enumerate(t["benefits"], 1)) + "</ul></div>"
          f'<div class="s-art">{diagram_value(t, u(1))}</div></div>{foot(1)}</section>')

    opps = "".join(
        f'<li class="op{" op-main" if i == 0 else ""}">{ICONS[i]}'
        + (f'<p class="op-tag">{esc(t["opp_tag"])}</p>' if i == 0 else "")
        + f'<h3>{esc(h)}</h3><p class="op-d">{esc(dsc)}</p><ul>' + "".join(f"<li>{esc(x)}</li>" for x in ex) + "</ul></li>"
        for i, (h, dsc, ex) in enumerate(t["opps"]))
    s2 = (f'<section class="slide s2" id="slide-2" aria-roledescription="slide" aria-label="{t["slide"]} 2 {t["of"]} 4">{brand}'
          f'<h2 class="sl-h2">{esc(t["h2"])}</h2><ol class="ops">{opps}</ol>{foot(2)}</section>')

    figs = "".join(f'<div><dt>{esc(lbl)}</dt><dd{" class=\"g\"" if k >= 2 else ""}>{esc(v)}</dd></div>' for k, (v, lbl) in enumerate(t["figs"]))
    s3 = (f'<section class="slide s3" id="slide-3" aria-roledescription="slide" aria-label="{t["slide"]} 3 {t["of"]} 4">{brand}'
          f'<div class="s-grid s-grid-3"><div class="s-text"><h2 class="sl-h2">{esc(t["h3"])}</h2>'
          f'<p class="sl-lead">{esc(t["s3_lead"])}</p><p class="sl-key">{esc(t["s3_key"])}</p>'
          f'<h3 class="sl-mini">{esc(t["s3_approach"])}</h3><ol class="sl-steps">' + "".join(f"<li>{esc(x)}</li>" for x in t["s3_steps"]) + "</ol></div>"
          f'<div class="s-art">{diagram_scenario(t, u(3))}<dl class="sl-figs">{figs}</dl>'
          f'<p class="sl-qual">{esc(t["s3_qual"])}</p></div></div>{foot(3)}</section>')

    mail = S.CONTACT_EMAIL
    s4 = (f'<section class="slide s4" id="slide-4" aria-roledescription="slide" aria-label="{t["slide"]} 4 {t["of"]} 4">{brand}'
          f'<div class="s-grid s-grid-4"><div class="s-text"><h2 class="sl-h2">{esc(t["h4"])}</h2><p class="sl-lead">{esc(t["s4_lead"])}</p>'
          '<ol class="sl-qs">' + "".join(f"<li>{esc(q)}</li>" for q in t["qs"]) + "</ol></div>"
          f'<div class="s-cta"><a class="sl-btn" href="{esc(CONTACT)}">{esc(t["cta"])}</a>'
          f'<p class="sl-nodata">{esc(t["nodata"])}</p>'
          f'<p class="sl-contact"><a href="{esc(CONTACT)}">groundtruthai.github.io/pilot</a>'
          + (f'<br><a href="mailto:{esc(mail)}">{esc(mail)}</a>' if mail else "") + '</p>'
          f'<p class="sl-legal">{esc(t["note"])}</p></div></div>{foot(4)}</section>')
    return s1 + s2 + s3 + s4


def render_brief():
    for lang in ("en", "es"):
        t = T[lang]
        other = "es" if lang == "en" else "en"
        canonical = S.BASE_URL + URL[lang]
        legal = " · ".join(f'<a href="{h}">{esc(n)}</a>' for n, h in t["legal"])
        doc = (
            '<!doctype html>\n'
            f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<meta http-equiv="Content-Security-Policy" content="{CSP.format(connect="'none'")}">\n'
            '<meta name="referrer" content="strict-origin-when-cross-origin">\n'
            f'<title>{esc(t["title"])}</title>\n'
            f'<meta name="description" content="{esc(t["desc"])}">\n<meta name="author" content="GroundTruth AI">\n'
            f'<link rel="canonical" href="{esc(canonical)}">\n'
            f'<link rel="alternate" hreflang="en" href="{S.BASE_URL + URL["en"]}">\n<link rel="alternate" hreflang="es" href="{S.BASE_URL + URL["es"]}">\n'
            f'<meta property="og:title" content="{esc(t["title"])}">\n<meta property="og:description" content="{esc(t["desc"])}">\n'
            f'<meta property="og:url" content="{esc(canonical)}">\n<meta property="og:type" content="website">\n'
            f'<meta property="og:locale" content="{"en_US" if lang == "en" else "es_ES"}">\n<meta property="og:site_name" content="GroundTruth AI">\n'
            f'<meta property="og:image" content="{S.BASE_URL}/assets/img/og-card.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n'
            '<meta name="color-scheme" content="dark">\n<meta name="theme-color" content="#05080F">\n'
            f'<link rel="icon" href="{asset("/assets/img/favicon.svg")}" type="image/svg+xml">\n'
            f'<link rel="icon" href="{asset("/assets/img/favicon.png")}" sizes="32x32" type="image/png">\n'
            f'<link rel="apple-touch-icon" href="{asset("/assets/img/apple-touch-icon.png")}">\n'
            '<link rel="preload" href="/assets/fonts/Inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
            f'<link rel="stylesheet" href="{asset("/assets/css/site.css")}">\n<link rel="stylesheet" href="{asset("/assets/css/brief.css")}">\n'
            f'<script src="{asset("/assets/js/brief.js")}" defer></script>\n'
            '</head>\n<body class="deck-body">\n'
            f'<a class="skip" href="#deck">{esc(t["skip"])}</a>\n'
            '<header class="deck-bar"><a class="brand" href="/" aria-label="GroundTruth AI home">' + BRAND + '</a>'
            '<nav class="deck-nav" aria-label="Presentation">'
            f'<a class="deck-lang" href="{URL[other]}" hreflang="{other}" lang="{other}" title="{esc(t["other_label"])}" data-keep-hash>'
            f'<span aria-hidden="true">{t["other"]}</span><span class="sr-only">{esc(t["other_label"])}</span></a>'
            f'<a class="deck-link" href="{DIR}{PDF[lang]}" download>{esc(t["pdf"])}</a>'
            f'<button class="deck-link deck-full" type="button" hidden>{esc(t["full"])}</button>'
            f'<a class="deck-link deck-site" href="/">{esc(t["back"])}</a>'
            f'<a class="btn btn-primary btn-sm" href="/pilot/">{esc(t["contact"])}</a></nav></header>\n'
            f'<main id="deck" class="deck" tabindex="-1" aria-roledescription="carousel" aria-label="{esc(t["deck"])}">'
            f'<div class="deck-stage">{slides(t, lang)}</div>'
            '<div class="deck-ui" hidden>'
            f'<button class="deck-btn deck-prev" type="button" aria-label="{esc(t["prev"])}"><span aria-hidden="true">←</span></button>'
            f'<p class="deck-count" aria-live="polite"><span class="sr-only">{esc(t["slide"])} </span><span class="deck-i">1</span> / 4</p>'
            f'<button class="deck-btn deck-next" type="button" aria-label="{esc(t["next"])}"><span aria-hidden="true">→</span></button></div>'
            '</main>\n'
            f'<footer class="deck-note"><p>{esc(t["note"])} {legal}</p></footer>\n'
            '</body>\n</html>\n')
        core.write(URL[lang], doc)
        core.PAGES.append((URL[lang], "0.7"))
