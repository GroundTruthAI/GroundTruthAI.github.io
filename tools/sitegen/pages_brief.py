"""Executive commercial presentation (EN + ES) at /executive/ and /executive/es/.

Single source of truth for the HTML viewer and the PDFs: tools/build_pdf.py prints these same pages with
headless Chrome (print styles in assets/css/brief.css give one 16:9 page per slide).
Content uses only information already published on the site; the 20-plant scenario is the site's
illustrative scenario (assumed 90% reduction) and is labelled as such.
"""
import os

from content import site as S
from . import core
from .core import esc, asset, BRAND, CSP

DIR = "/executive/"
OLD_DIR = "/resources/executive-brief/"   # previous location: page redirects + PDF copies kept for shared links
PDF = {"en": "GroundTruthAI_Executive_Brief_EN.pdf", "es": "GroundTruthAI_Resumen_Comercial_ES.pdf"}
URL = {"en": DIR, "es": DIR + "es/"}


def pdf_version():
    """Cache-busting version for the PDF links: hash of the presentation source (content, layout, print styles).
    It changes whenever the slides change, so browsers fetch the regenerated PDF instead of a cached copy."""
    import hashlib
    h = hashlib.sha256()
    for f in (__file__, os.path.join(core.ROOT, "assets/css/brief.css")):
        with open(f, "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:10]


def pdf_url(lang):
    return f"{DIR}{PDF[lang]}?v={pdf_version()}"
CONTACT = S.BASE_URL + "/pilot/"

N_SLIDES = 7

# Slide 6 economics: the shared savings model (content/site.py → SAVINGS_LINES), i.e. the ROI calculator's defaults.
def economics():
    return S.savings_example()


def _calc_text(key, spend, red, lang):
    if key == "storage":
        return ("500 TB × $40/TB·month · −{r}%" if lang == "en" else "500 TB × 40 €/TB·mes · −{r} %").format(r=red)
    amount = _k(spend, lang)
    return (f"{amount} a year · −{red}%" if lang == "en" else f"{amount} al año · −{red}\u00a0%")


def _k(v, lang):
    neg = v < 0
    v = abs(v)
    if v >= 1_000_000:
        m = f"{v / 1_000_000:.1f}".rstrip("0").rstrip(".")
        txt = f"${m}M" if lang == "en" else f"{m.replace('.', ',')}\u00a0M€"
    else:
        k = round(v / 1000)
        txt = f"${k}k" if lang == "en" else f"{k}\u00a0k€"
    return ("−" if neg else "") + txt

# Business cases shown on slide 4, by solution family: (site slug, EN title, EN one-liner, ES title, ES one-liner)
CASES = [
    ("Unlock new AI projects", "Habilitar nuevos proyectos de IA", [
        ("ot-it-data-segregation", "OT/IT data segregation", "Train AI on plant data without copying the plant's full history to corporate IT.",
         "Segregación de datos OT/IT", "Entrenar IA con datos de planta sin copiar todo su histórico a la informática corporativa."),
        ("distributed-industrial-intelligence", "Distributed industrial intelligence", "One maintenance model that learns from failures in every facility.",
         "Inteligencia industrial distribuida", "Un modelo de mantenimiento que aprende de las averías de todas las plantas."),
        ("cross-enterprise-analytics", "Cross-enterprise analytics", "Group-wide models without first merging every subsidiary's data.",
         "Analítica a nivel de grupo", "Modelos para todo el grupo sin fusionar antes los datos de cada filial."),
        ("data-residency-and-sovereignty", "Data residency", "Shared analytics while original data stays in its country.",
         "Residencia de datos", "Analítica compartida mientras los datos originales se quedan en su país."),
        ("post-merger-analytical-integration", "Post-merger analytics", "Joint analytics before the merged companies' systems are integrated.",
         "Analítica tras una fusión", "Analítica conjunta antes de integrar los sistemas de las empresas fusionadas."),
    ]),
    ("Reduce the cost of AI", "Reducir el coste de la IA", [
        ("ai-training-cost-optimization", "AI training cost optimization", "Train on the data that matters and stop paying to process the rest.",
         "Coste de entrenamiento de IA", "Entrenar con los datos que importan y dejar de pagar por procesar el resto."),
        ("continuous-model-retraining", "Continuous model retraining", "Update models regularly without reprocessing the full history each time.",
         "Reentrenamiento continuo", "Actualizar modelos con frecuencia sin reprocesar todo el histórico cada vez."),
        ("ai-infrastructure-efficiency", "AI infrastructure efficiency", "More AI work from the same servers and storage.",
         "Eficiencia de la infraestructura", "Más trabajo de IA con los mismos servidores y almacenamiento."),
        ("sustainable-ai-infrastructure", "Sustainable AI", "Lower, measured energy use for AI training.",
         "IA sostenible", "Menor consumo energético del entrenamiento de IA, medido."),
    ]),
    ("Move less data", "Mover menos datos", [
        ("edge-to-cloud-data-optimization", "Edge-to-cloud optimization", "Send what models need, not everything devices and remote sites produce.",
         "Del edge a la nube", "Enviar lo que necesitan los modelos, no todo lo que generan sensores y sitios remotos."),
        ("multicloud-data-optimization", "Multicloud optimization", "Stop copying large training datasets between cloud providers.",
         "Multicloud", "Dejar de copiar grandes conjuntos de datos entre proveedores de nube."),
    ]),
]

T = {
    "en": {
        "title": "GroundTruth AI | Executive Business Overview",
        "desc": "GroundTruth AI in six slides: AI that learns from data spread across plants, subsidiaries and countries without "
                "centralizing it, three business opportunities, eleven business cases and a 20-plant example.",
        "deck": "GroundTruth AI executive overview", "skip": "Skip to the presentation",
        "prev": "Previous slide", "next": "Next slide", "of": "of", "slide": "Slide",
        "pdf": "Download PDF", "full": "Full screen", "back": "Website", "contact": "Contact",
        "other": "ES", "other_label": "Ver en español", "kicker": "Dataset distillation for the enterprise",
        "note": "Illustrative information for discussion. Figures and scenarios are estimates and have no contractual value.",
        "legal": [("Legal notice", "/legal-notice/"), ("Privacy policy", "/privacy/"), ("Cookie policy", "/cookie-policy/")],
        # 1 value proposition
        "h1a": "Keep data distributed.", "h1b": "Centralize intelligence.",
        "how": "We make it possible with dataset distillation.",
        "what_k": "What we do:",
        "lead": "Our software runs inside each plant, business unit or region and "
                "distills the data into a much smaller training dataset that contains what an AI model needs for a specific purpose. "
                "Only that distilled dataset is shared; the original data stays where it is.",
        "benefits": ["Enable new AI and analytics projects", "Reduce unnecessary data movement", "Optimize AI infrastructure costs"],
        "notc_k": "Dataset distillation, not compression",
        "notc": "Compression shrinks the same data, which must be unpacked before use, so the AI still processes all of it. "
                "Distillation builds a much smaller dataset that the AI uses directly to learn.",
        "stats": [("86–95%", "less training data"), ("86%", "less energy per training run"), ("≈{net}", "saved a year by one AI system, 20-plant example · illustrative*")],
        "stats_note": "Internal tests on four public datasets: models trained on 5–14% of the data came within 1.4–2.8 accuracy points of "
                      "models trained on all of it. Energy: internal measurement, excluding the distillation step. *Illustrative estimate based on "
                      "planning assumptions, detailed on slide 6; before license costs. Results vary by use case; not contractual.",
        "d1_src": ["Industrial plants", "Business units", "Regions"], "d1_sub": "original data stays here",
        "d1_core": ["Enterprise", "intelligence"], "d1_cap": "ONLY DISTILLED, APPROVED DATASETS TRAVEL",
        "d1_title": "Original data stays in industrial plants, business units and regions; only small, approved datasets reach a common enterprise intelligence environment.",
        # 2 why it matters
        "hw": "Your data is spread out. Your AI needs all of it.",
        "w_lead": "Large companies want AI that learns from every plant, subsidiary and country. But their data lives in separate "
                  "systems, and copying all of it to one place is often slow, expensive or not allowed.",
        "obstacles": [
            ("Security boundaries", "Industrial control systems are kept apart from corporate IT, so plant data cannot simply be copied out."),
            ("Data protection and residency", "Customer and personal data often has to stay in its country or company."),
            ("Cost and volume", "Moving and storing terabytes again and again costs money, network capacity and time."),
            ("Constant retraining", "AI models need regular updates, and each update reprocesses an ever-larger history."),
        ],
        "w_key": "The result: valuable AI projects are delayed, scaled down or never started.",
        # how it works
        "hh": "How it works, in four steps.",
        "h_def_k": "Dataset distillation",
        "h_def": "is a technique that creates a much smaller training dataset from the original data, designed so that an AI model "
                 "trained on it performs close to one trained on all the data.",
        "h_steps": [
            ("Define the goal", "Agree what the AI must predict or analyze, and the quality it must reach."),
            ("Distill at the source", "Our software, installed where the data lives, builds a much smaller dataset for that goal. The original data does not move."),
            ("Check the quality", "The same model is trained on the full and on the distilled data, and the results are compared."),
            ("Share and train", "Once approved, only the distilled dataset travels through your existing channels, and the AI is trained centrally."),
        ],
        "h_where": "Where it runs: on your own servers or private cloud, next to the data. Your data is not sent to GroundTruth AI.",
        # opportunities
        "h2": "Three business opportunities. One technology.",
        "h2_sub": "All three rest on the same technology: dataset distillation.",
        "opps": [
            ("Unlock new AI projects", "Train AI and run analytics with data from all your plants, subsidiaries and countries, even when that data cannot be centralized.",
             ["One predictive maintenance model for all plants", "Analytics across business units and countries", "AI on industrial data that cannot leave the plant network"]),
            ("Reduce the cost of AI", "Train and update AI models with much less data, so each training run needs less computing power.",
             ["Lower computing costs", "Cheaper, faster model updates", "Less storage and server capacity"]),
            ("Move less data", "Send only the information a model needs, instead of copying everything between systems.",
             ["From industrial systems (OT) to corporate IT", "From sensors and remote sites to the cloud", "Between different cloud providers"]),
        ],
        "opp_tag": "Strategic priority",
        # 4 business cases
        "hc": "Eleven business cases you can evaluate.",
        "c_lead": "Each one describes a concrete problem, the proposed solution and how to measure the result.",
        "c_more": "Full details at groundtruthai.github.io/business-cases",
        "inds": "Industries: manufacturing · energy and utilities · oil, gas and mining · transport and logistics · financial services · healthcare · telecom · retail · multinational groups · AI infrastructure",
        # 5 scenario
        "h3": "20 industrial plants. One AI model.",
        "h3m": "One AI system. ≈{net} saved every year.",
        "money_k": "Estimated net saving per year · ONE AI system (predictive maintenance) across 20 plants",
        "scale_k": "Each additional AI system adds its own savings",
        "scale": [("1 system", "{s1}"), ("3 systems", "{s3}"), ("5 systems", "{s5}")],
        "scale_n": "Other AI systems on the same plants (quality, energy, anomaly detection…), assuming similar data and compute spend per system. More plants also increase the saving.",
        "money_s": "≈{net3} over three years · before license costs",
        "break_d": ("Distillation and validation", "compute at the plants + dataset checks"),
        "break_t": "Net saving per year",
        "s6_qual": "Illustrative estimate for a 20-plant AI program, not a customer deployment and not contractual. Spend levels and "
                   "reduction rates are GroundTruth AI planning assumptions to be validated in a pilot; they are the defaults of the ROI calculator. "
                   "Calculate yours at groundtruthai.github.io/roi",
        "s3_lead": "Imagine a global manufacturer that wants to anticipate equipment failures across all its facilities while keeping "
                   "original operational data within its existing industrial environments.",
        "s3_key": "Enterprise-wide predictive maintenance without complete raw data consolidation.",
        "s3_steps": ["Each plant keeps its historical data where it is", "GroundTruth AI, installed in each plant, distills the data into a much smaller dataset for the maintenance model",
                     "After review and approval, only that dataset travels through the existing connection", "The central team trains one model with data from all 20 plants"],
        "s3_approach": "How it works, step by step",
        "figs": [("200 TB", "eligible data"), ("90%", "assumed reduction"), ("20 TB", "transferred"), ("180 TB", "potentially avoided")],
        "s3_qual": "Illustrative scenario, not a customer deployment. The reduction is an assumption that requires workload-specific validation.",
        "d3": {"trad": "Traditional approach", "gt": "With GroundTruth AI", "plant": "Plant", "central": ["Central data", "platform"],
               "model": ["AI", "model"], "stays": "data stays", "big": "200 TB copied", "small": "20 TB"},
        "d3_title": "Before: all historical data from the plants is copied to a central platform to train the AI model. After: each plant keeps its data, prepares a much smaller dataset locally and sends only that.",
        # 6 call to action
        "h4": "Tell us about your business challenge.",
        "s4_lead": "Identify an AI or analytics opportunity that is currently constrained by distributed data, data segregation, "
                   "infrastructure costs or excessive data movement.",
        "qs": ["What would you like to predict, analyze or improve?", "Where is the relevant information currently located?",
               "What prevents you from using it efficiently today?"],
        "cta": "Let's assess your use case", "nodata": "No data sharing is required for the initial discussion.",
        "roi": "Estimate your own savings with the ROI calculator",
        "next_k": "What happens next",
        "next": "A short conversation about your case. If there is a fit, a scoped feasibility assessment on one use case.",
    },
    "es": {
        "title": "GroundTruth AI | Resumen ejecutivo",
        "desc": "GroundTruth AI en seis diapositivas: IA que aprende de datos repartidos entre plantas, filiales y países sin "
                "centralizarlos, tres oportunidades de negocio, once casos de negocio y un ejemplo con 20 plantas.",
        "deck": "Resumen ejecutivo de GroundTruth AI", "skip": "Ir a la presentación",
        "prev": "Diapositiva anterior", "next": "Diapositiva siguiente", "of": "de", "slide": "Diapositiva",
        "pdf": "Descargar PDF", "full": "Pantalla completa", "back": "Web", "contact": "Contacto",
        "other": "EN", "other_label": "View in English", "kicker": "Destilación de datos para la empresa",
        "note": "Información orientativa para conversar. Las cifras y los escenarios son estimaciones y no tienen valor contractual.",
        "legal": [("Aviso legal", "/aviso-legal/"), ("Política de privacidad", "/privacidad/"), ("Política de cookies", "/cookies/")],
        "h1a": "Datos distribuidos.", "h1b": "Inteligencia centralizada.",
        "how": "Lo conseguimos con destilación de datos.",
        "what_k": "Qué hacemos:",
        "lead": "Nuestro software funciona dentro de cada planta, unidad de negocio "
                "o región y destila los datos en un conjunto de entrenamiento mucho más pequeño, con lo que un modelo de IA necesita "
                "para un objetivo concreto. Solo se comparte ese conjunto destilado; los datos originales se quedan donde están.",
        "benefits": ["Habilitar nuevos proyectos de IA y analítica", "Reducir el movimiento innecesario de datos", "Optimizar los costes de infraestructura de IA"],
        "notc_k": "Destilación de datos, no compresión",
        "notc": "La compresión reduce el tamaño de los mismos datos, que hay que descomprimir para usarlos: la IA sigue procesándolos "
                "todos. La destilación crea un conjunto de datos mucho más pequeño que la IA usa directamente para aprender.",
        "stats": [("86–95\u00a0%", "menos datos de entrenamiento"), ("86\u00a0%", "menos energía por entrenamiento"), ("≈{net}", "de ahorro al año con un solo sistema de IA, ejemplo de 20 plantas · ilustrativo*")],
        "stats_note": "Ensayos internos con cuatro conjuntos de datos públicos: con el 5–14 % de los datos, los modelos quedaron a 1,4–2,8 "
                      "puntos de precisión de los entrenados con todos. Energía: medición interna, sin incluir el paso de destilación. "
                      "*Estimación ilustrativa basada en supuestos de planificación, detallados en la diapositiva 6; antes del coste de "
                      "licencia. Los resultados varían según el caso; sin valor contractual.",
        "d1_src": ["Plantas industriales", "Unidades de negocio", "Regiones"], "d1_sub": "datos originales en origen",
        "d1_core": ["Inteligencia", "empresarial"], "d1_cap": "SOLO VIAJAN DATOS DESTILADOS Y APROBADOS",
        "d1_title": "Los datos originales se quedan en plantas, unidades de negocio y regiones; solo llegan a un entorno común de inteligencia empresarial conjuntos de datos reducidos y aprobados.",
        "hw": "Tus datos están repartidos. Tu IA los necesita todos.",
        "w_lead": "Las grandes empresas quieren una IA que aprenda de todas sus plantas, filiales y países. Pero sus datos están en "
                  "sistemas separados, y copiarlos todos a un único lugar suele ser lento, caro o no estar permitido.",
        "obstacles": [
            ("Barreras de seguridad", "Los sistemas de control industrial están separados de la informática corporativa: los datos de planta no se pueden copiar sin más."),
            ("Protección y residencia de datos", "Los datos de clientes y personales a menudo deben quedarse en su país o en su empresa."),
            ("Coste y volumen", "Mover y almacenar terabytes una y otra vez cuesta dinero, capacidad de red y tiempo."),
            ("Reentrenamiento constante", "Los modelos de IA deben actualizarse con frecuencia, y cada actualización reprocesa un histórico cada vez mayor."),
        ],
        "w_key": "Resultado: proyectos de IA valiosos se retrasan, se recortan o nunca empiezan.",
        "hh": "Cómo funciona, en cuatro pasos.",
        "h_def_k": "La destilación de datos",
        "h_def": "es una técnica que crea, a partir de los datos originales, un conjunto de entrenamiento mucho más pequeño, diseñado "
                 "para que un modelo de IA entrenado con él funcione de forma parecida a uno entrenado con todos los datos.",
        "h_steps": [
            ("Definir el objetivo", "Se acuerda qué debe predecir o analizar la IA y qué calidad debe alcanzar."),
            ("Destilar en origen", "Nuestro software, instalado donde están los datos, crea un conjunto mucho más pequeño para ese objetivo. Los datos originales no se mueven."),
            ("Comprobar la calidad", "Se entrena el mismo modelo con los datos completos y con los destilados, y se comparan los resultados."),
            ("Compartir y entrenar", "Una vez aprobado, solo el conjunto destilado viaja por los canales que ya existen y la IA se entrena de forma centralizada."),
        ],
        "h_where": "Dónde funciona: en tus propios servidores o nube privada, junto a los datos. Tus datos no se envían a GroundTruth AI.",
        "h2": "Tres oportunidades de negocio. Una tecnología.",
        "h2_sub": "Las tres se apoyan en la misma tecnología: la destilación de datos.",
        "opps": [
            ("Habilitar nuevos proyectos de IA", "Entrena IA y haz analítica con datos de todas tus plantas, filiales y países, aunque esos datos no se puedan centralizar.",
             ["Un modelo de mantenimiento predictivo para todas las plantas", "Analítica entre unidades de negocio y países", "IA con datos industriales que no pueden salir de la red de planta"]),
            ("Reducir el coste de la IA", "Entrena y actualiza modelos de IA con muchos menos datos, de modo que cada entrenamiento necesita menos capacidad de cálculo.",
             ["Menores costes de computación", "Actualizaciones de modelos más rápidas y baratas", "Menos almacenamiento y servidores"]),
            ("Mover menos datos", "Envía solo la información que necesita el modelo, en lugar de copiarlo todo entre sistemas.",
             ["De los sistemas industriales (OT) a la informática corporativa (IT)", "De sensores y sitios remotos a la nube", "Entre distintos proveedores de nube"]),
        ],
        "opp_tag": "Prioridad estratégica",
        "hc": "Once casos de negocio para evaluar.",
        "c_lead": "Cada uno describe un problema concreto, la solución propuesta y cómo medir el resultado.",
        "c_more": "Detalle completo en groundtruthai.github.io/business-cases (en inglés)",
        "inds": "Sectores: industria · energía y utilities · petróleo, gas y minería · transporte y logística · servicios financieros · salud · telecomunicaciones · retail · grupos multinacionales · infraestructura de IA",
        "h3": "20 plantas industriales. Un modelo de IA común.",
        "h3m": "Un solo sistema de IA. ≈{net} de ahorro al año.",
        "money_k": "Ahorro neto estimado al año · UN solo sistema de IA (mantenimiento predictivo) en 20 plantas",
        "scale_k": "Cada sistema de IA adicional suma sus propios ahorros",
        "scale": [("1 sistema", "{s1}"), ("3 sistemas", "{s3}"), ("5 sistemas", "{s5}")],
        "scale_n": "Otros sistemas de IA en las mismas plantas (calidad, energía, detección de anomalías…), suponiendo un gasto en datos y cómputo similar por sistema. Con más plantas, el ahorro también crece.",
        "money_s": "≈{net3} en tres años · antes del coste de licencia",
        "break_d": ("Destilación y validación", "cómputo en planta + revisión de los datos"),
        "break_t": "Ahorro neto al año",
        "s6_qual": "Estimación ilustrativa para un programa de IA en 20 plantas, no un despliegue en cliente ni con valor contractual. "
                   "Los niveles de gasto y los porcentajes de reducción son supuestos de planificación de GroundTruth AI que deben "
                   "validarse en un piloto; son los valores por defecto de la calculadora ROI. Calcula el tuyo en groundtruthai.github.io/roi",
        "s3_lead": "Una empresa industrial quiere anticipar fallos de equipos en todas sus instalaciones, manteniendo los datos operativos "
                   "originales dentro de sus entornos industriales.",
        "s3_key": "Mantenimiento predictivo global sin centralizar todos los datos industriales originales.",
        "s3_steps": ["Cada planta conserva su histórico de datos donde está", "GroundTruth AI, instalado en cada planta, destila los datos en un conjunto mucho menor para el modelo de mantenimiento",
                     "Tras revisarlo y aprobarlo, solo ese conjunto viaja por la conexión ya existente", "El equipo central entrena un único modelo con datos de las 20 plantas"],
        "s3_approach": "Cómo funciona, paso a paso",
        "figs": [("200 TB", "datos elegibles"), ("90 %", "reducción supuesta"), ("20 TB", "transferidos"), ("180 TB", "que podrían no moverse")],
        "s3_qual": "Escenario ilustrativo, no un despliegue en cliente. La reducción es una hipótesis que debe validarse en cada caso.",
        "d3": {"trad": "Enfoque tradicional", "gt": "Con GroundTruth AI", "plant": "Planta", "central": ["Plataforma", "central"],
               "model": ["Modelo", "de IA"], "stays": "datos en planta", "big": "200 TB copiados", "small": "20 TB"},
        "d3_title": "Antes: todo el histórico de las plantas se copia a una plataforma central para entrenar el modelo. Después: cada planta conserva sus datos, prepara localmente un conjunto mucho menor y solo envía ese.",
        "h4": "Cuéntanos un reto de negocio.",
        "s4_lead": "Identifica una oportunidad de IA o analítica que actualmente esté limitada por la segregación de datos, "
                   "los costes de infraestructura o la dificultad de mover información.",
        "qs": ["¿Qué te gustaría predecir, analizar o mejorar?", "¿Dónde se encuentra actualmente la información relevante?",
               "¿Qué dificulta su aprovechamiento?"],
        "cta": "Analicemos tu caso", "nodata": "No es necesario compartir datos en la primera conversación.",
        "roi": "Calcula tu ahorro con la calculadora ROI",
        "next_k": "Qué pasa después",
        "next": "Una conversación breve sobre tu caso. Si encaja, una evaluación de viabilidad acotada sobre un caso de uso.",
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
        ys = [y0 + 28, y0 + 72, y0 + 132]
        names = [f'{d["plant"]} 1', f'{d["plant"]} 2', f'{d["plant"]} 20']
        for i, (y, nm) in enumerate(zip(ys, names)):
            g.append(f'<rect class="bd-box" x="6" y="{y}" width="150" height="36" rx="10"/><text class="bd-p" x="20" y="{y + 24}">{esc(nm)}</text>')
            if i == 1:
                g.append(f'<text class="bd-dots" x="81" y="{y + 54}" text-anchor="middle">⋮</text>')
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
            g.append(f'<text class="bd-vol bd-vol-g" x="372" y="{y0 + 54}" text-anchor="middle">{esc(d["small"])}</text>'
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


HOW_ICONS = [
    '<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="10"/><circle cx="24" cy="24" r="3"/>',
    '<path d="M8 8 H40 L28 24 V38 L20 42 V24 Z"/>',
    '<path d="M24 6 V42 M10 14 H38 M10 14 4 28 H16 Z M38 14 32 28 H44 Z"/>',
    '<path d="M6 24 H34 M26 16 34 24 26 32"/><rect x="36" y="12" width="8" height="24" rx="2"/>',
]

WHY_ICONS = [
    '<path d="M24 5 40 11 V23 C40 33 33 40 24 43 15 40 8 33 8 23 V11 Z"/><path d="M17 24 22 29 31 19"/>',
    '<circle cx="24" cy="24" r="17"/><path d="M7 24 H41 M24 7 C17 14 17 34 24 41 M24 7 C31 14 31 34 24 41"/>',
    '<path d="M6 34 H42 M10 34 V24 M20 34 V16 M30 34 V20 M40 34 V10"/>',
    '<path d="M38 18 A15 15 0 1 0 39 30"/><path d="M38 8 V18 H28"/>',
]


def slides(t, lang):
    u = lambda n: f"b{lang}{n}"
    brand = f'<p class="sl-brand">{BRAND}</p>'
    out = []

    def sec(n, cls, inner):
        out.append(f'<section class="slide {cls}" id="slide-{n}" aria-roledescription="slide" aria-label="{t["slide"]} {n} {t["of"]} {N_SLIDES}">'
                   f'{brand}{inner}<p class="sl-foot"><span>groundtruthai.github.io</span><span>{n} / {N_SLIDES}</span></p></section>')

    # 1 — value proposition
    sec(1, "s1",
        f'<div class="s-grid"><div class="s-text"><p class="sl-kick">{esc(t["kicker"])}</p>'
        f'<h1 class="sl-h1">{esc(t["h1a"])} <span class="g">{esc(t["h1b"])}</span></h1>'
        f'<p class="sl-how">{esc(t["how"])}</p>'
        f'<p class="sl-lead"><strong class="sl-what">{esc(t["what_k"])}</strong> {esc(t["lead"])}</p>'
        '<ul class="sl-ben">' + "".join(f'<li><span class="ben-n">{i}</span>{esc(b)}</li>' for i, b in enumerate(t["benefits"], 1)) + "</ul>"
        '<dl class="sl-stats">' + "".join(f'<div><dd class="g">{esc(v.format(net=_k(economics()["net"], lang)))}</dd><dt>{esc(k)}</dt></div>' for v, k in t["stats"]) + '</dl>'
        f'<p class="sl-stats-note">{esc(t["stats_note"])}</p></div>'
        f'<div class="s-art">{diagram_value(t, u(1))}</div></div>')

    # 2 — why it matters
    obs = "".join(f'<li class="ob"><svg class="op-ic" viewBox="0 0 48 48" aria-hidden="true" focusable="false">{WHY_ICONS[i]}</svg>'
                  f'<h3>{esc(h)}</h3><p>{esc(d)}</p></li>' for i, (h, d) in enumerate(t["obstacles"]))
    sec(2, "s-why",
        f'<h2 class="sl-h2">{esc(t["hw"])}</h2><p class="sl-lead sl-lead-w">{esc(t["w_lead"])}</p>'
        f'<ul class="obs">{obs}</ul><p class="sl-key sl-key-w">{esc(t["w_key"])}</p>')

    # 3 — how it works
    steps = "".join(f'<li class="hw"><span class="hw-n">{i}</span><svg class="op-ic" viewBox="0 0 48 48" aria-hidden="true" focusable="false">{HOW_ICONS[i - 1]}</svg>'
                    f'<h3>{esc(h)}</h3><p>{esc(d)}</p></li>' for i, (h, d) in enumerate(t["h_steps"], 1))
    sec(3, "s-how",
        f'<h2 class="sl-h2">{esc(t["hh"])}</h2>'
        f'<p class="sl-def"><strong>{esc(t["h_def_k"])}</strong> {esc(t["h_def"])}</p>'
        f'<ol class="hws">{steps}</ol><p class="sl-proof sl-notc sl-notc-how"><strong>{esc(t["notc_k"])}.</strong> {esc(t["notc"])}</p>'
        f'<p class="sl-where">{esc(t["h_where"])}</p>')

    # 4 — three opportunities
    opps = "".join(
        f'<li class="op{" op-main" if i == 0 else ""}">{ICONS[i]}'
        + (f'<p class="op-tag">{esc(t["opp_tag"])}</p>' if i == 0 else "")
        + f'<h3>{esc(h)}</h3><p class="op-d">{esc(dsc)}</p><ul>' + "".join(f"<li>{esc(x)}</li>" for x in ex) + "</ul></li>"
        for i, (h, dsc, ex) in enumerate(t["opps"]))
    sec(4, "s2", f'<h2 class="sl-h2">{esc(t["h2"])}</h2><p class="sl-sub">{esc(t["h2_sub"])}</p><ol class="ops">{opps}</ol>')

    # 5 — business cases
    cols = []
    for i, (gen, ges, items) in enumerate(CASES):
        lis = "".join(
            f'<li><a href="{S.BASE_URL}/business-cases/{slug}/">{esc(ten if lang == "en" else tes)}</a>'
            f'<span>{esc(den if lang == "en" else des)}</span></li>' for slug, ten, den, tes, des in items)
        cols.append(f'<div class="cs-col{" cs-main" if i == 0 else ""}"><h3>{ICONS[i]}{esc(gen if lang == "en" else ges)}</h3><ul>{lis}</ul></div>')
    sec(5, "s-cases",
        f'<h2 class="sl-h2">{esc(t["hc"])}</h2><p class="sl-lead sl-lead-c">{esc(t["c_lead"])} '
        f'<a href="{S.BASE_URL}/business-cases/">{esc(t["c_more"])}</a></p>'
        f'<div class="cs-grid">{"".join(cols)}</div><p class="sl-inds">{esc(t["inds"])}</p>')

    # 6 — scenario, focused on money
    ec = economics()
    net = _k(ec["net"], lang)
    sc = {"net": net, "s1": _k(ec["net"], lang), "s3": _k(ec["net"] * 3, lang), "s5": _k(ec["net"] * 5, lang)}
    rows = "".join(f'<tr><th scope="row">{esc(en if lang == "en" else es)}<span>{esc(_calc_text(key, spend, red, lang))}</span></th>'
                   f'<td>{esc(_k(ec["lines"][key], lang))}</td></tr>'
                   for key, en, es, spend, red, _h1, _h2 in S.SAVINGS_LINES)
    rows += (f'<tr class="neg"><th scope="row">{esc(t["break_d"][0])}<span>{esc(t["break_d"][1])}</span></th>'
             f'<td>{esc(_k(-ec["costs"], lang))}</td></tr>'
             f'<tr class="tot"><th scope="row">{esc(t["break_t"])}</th><td>{esc(net)}</td></tr>')
    figs = "".join(f'<div><dt>{esc(lbl)}</dt><dd{" class=\"g\"" if k >= 2 else ""}>{esc(v)}</dd></div>' for k, (v, lbl) in enumerate(t["figs"]))
    sec(6, "s3 s-money",
        f'<div class="s-grid s-grid-3"><div class="s-text"><h2 class="sl-h2">{esc(t["h3m"].format(**sc))}</h2>'
        f'<p class="sl-lead">{esc(t["s3_lead"])}</p>'
        f'<div class="sl-money"><p class="mk">{esc(t["money_k"])}</p><p class="mv g">≈{esc(net)}</p><p class="ms">{esc(t["money_s"].format(net3=_k(ec["net3"], lang)))}</p></div>'
        f'<table class="sl-break"><tbody>{rows}</tbody></table></div>'
        f'<div class="s-art"><div class="sl-scale"><p class="mk">{esc(t["scale_k"])}</p><dl>'
        + "".join(f'<div><dt>{esc(k)}</dt><dd class="g">≈{esc(v.format(**sc))}</dd></div>' for k, v in t["scale"])
        + f'</dl><p class="sl-scale-n">{esc(t["scale_n"])}</p></div>'
        f'{diagram_scenario(t, u(6))}<dl class="sl-figs">{figs}</dl>'
        f'<p class="sl-qual">{esc(t["s6_qual"])}</p></div></div>')

    # 7 — call to action
    mail = S.CONTACT_EMAIL
    sec(7, "s4",
        f'<div class="s-grid s-grid-4"><div class="s-text"><h2 class="sl-h2">{esc(t["h4"])}</h2><p class="sl-lead">{esc(t["s4_lead"])}</p>'
        '<ol class="sl-qs">' + "".join(f"<li>{esc(q)}</li>" for q in t["qs"]) + "</ol></div>"
        f'<div class="s-cta"><a class="sl-btn" href="{esc(CONTACT)}">{esc(t["cta"])}</a>'
        f'<p class="sl-nodata">{esc(t["nodata"])}</p>'
        f'<p class="sl-next"><strong>{esc(t["next_k"])}:</strong> {esc(t["next"])}</p>'
        f'<p class="sl-roi"><a href="{S.BASE_URL}/roi/">{esc(t["roi"])} →</a></p>'
        f'<p class="sl-contact"><a href="{esc(CONTACT)}">groundtruthai.github.io/pilot</a>'
        + (f'<br><a href="mailto:{esc(mail)}">{esc(mail)}</a>' if mail else "") + '</p>'
        f'<p class="sl-legal">{esc(t["note"])}</p></div></div>')
    return "".join(out)


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
            f'<a class="deck-link" href="{pdf_url(lang)}" download="{PDF[lang]}">{esc(t["pdf"])}</a>'
            f'<button class="deck-link deck-full" type="button" hidden>{esc(t["full"])}</button>'
            f'<a class="deck-link deck-site" href="/">{esc(t["back"])}</a>'
            f'<a class="btn btn-primary btn-sm" href="/pilot/">{esc(t["contact"])}</a></nav></header>\n'
            f'<main id="deck" class="deck" tabindex="-1" aria-roledescription="carousel" aria-label="{esc(t["deck"])}">'
            f'<div class="deck-stage">{slides(t, lang)}</div>'
            '<div class="deck-ui" hidden>'
            f'<button class="deck-btn deck-prev" type="button" aria-label="{esc(t["prev"])}"><span aria-hidden="true">←</span></button>'
            f'<p class="deck-count" aria-live="polite"><span class="sr-only">{esc(t["slide"])} </span><span class="deck-i">1</span> / {N_SLIDES}</p>'
            f'<button class="deck-btn deck-next" type="button" aria-label="{esc(t["next"])}"><span aria-hidden="true">→</span></button></div>'
            '</main>\n'
            f'<footer class="deck-note"><p>{esc(t["note"])} {legal}</p></footer>\n'
            '</body>\n</html>\n')
        core.write(URL[lang], doc)
        core.PAGES.append((URL[lang], "0.7"))
