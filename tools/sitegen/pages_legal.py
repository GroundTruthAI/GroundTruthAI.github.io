"""Legal pages in Spanish (reference text) and English (translation):
Aviso legal / Legal notice (LSSI-CE art. 10), Política de privacidad / Privacy policy (GDPR art. 13, LOPDGDD)
and Política de cookies / Cookie policy (LSSI-CE art. 22.2).

Owner identification comes from content/site.py → LEGAL (Spanish values) and LEGAL_EN (English values).
Nothing is invented. Texts should be reviewed by the company's legal adviser.
"""
from content import site as S
from .core import esc, page, breadcrumb

UPDATED = {"es": "24 de noviembre de 2026", "en": "24 November 2026"}

PAGES = {  # key: (es path, en path)
    "notice": ("/aviso-legal/", "/legal-notice/"),
    "privacy": ("/privacidad/", "/privacy/"),
    "cookies": ("/cookies/", "/cookie-policy/"),
}
TITLES = {"es": {"notice": "Aviso legal", "privacy": "Política de privacidad", "cookies": "Política de cookies"},
          "en": {"notice": "Legal notice", "privacy": "Privacy policy", "cookies": "Cookie policy"}}

T = {
    "es": {"home": "Inicio", "eyebrow": "Información legal", "updated": "Última actualización", "other": "English version",
           "labels": ["Titular", "NIF", "Domicilio", "Correo electrónico", "Datos registrales", "Sitio web"],
           "prevails": ""},
    "en": {"home": "Home", "eyebrow": "Legal information", "updated": "Last updated", "other": "Versión en español",
           "labels": ["Owner", "Tax ID (NIF)", "Address", "Email", "Registry details", "Website"],
           "prevails": "This is an English translation provided for convenience. In case of discrepancy, the Spanish version prevails."},
}


def _url(key, lang):
    return PAGES[key][0 if lang == "es" else 1]


def _links(lang):
    return '<p class="small">' + " · ".join(f'<a href="{_url(k, lang)}">{TITLES[lang][k]}</a>' for k in PAGES) + "</p>"


def _owner(lang):
    L = dict(S.LEGAL)
    if lang == "en":
        L.update({k: v for k, v in S.LEGAL_EN.items() if v})
    vals = [L["owner"], L["nif"], L["address"], L["email"], L["registry"], S.BASE_URL]
    items = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in zip(T[lang]["labels"], vals) if v)
    return f'<dl class="legal-id">{items}</dl>'


def _mail(lang):
    e = S.LEGAL["email"]
    if e:
        return f'<a href="mailto:{esc(e)}">{esc(e)}</a>'
    return "la dirección de correo indicada en el aviso legal" if lang == "es" else "the email address given in the legal notice"


def _render(key, lang, lead, description, sections, cases):
    t = T[lang]
    title = TITLES[lang][key]
    other_lang = "en" if lang == "es" else "es"
    other = f'<p class="legal-lang"><a href="{_url(key, other_lang)}" hreflang="{other_lang}" lang="{other_lang}">{t["other"]}</a></p>'
    hero = ('<div class="page-hero"><div class="wrap">' + breadcrumb([(t["home"], "/"), (title, None)])
            + f'<p class="eyebrow">{t["eyebrow"]}</p><h1>{esc(title)}</h1><p class="lead">{lead}</p>{other}</div></div>')
    body = []
    if t["prevails"]:
        body.append(f'<p class="small legal-prev">{t["prevails"]}</p>')
    for h, paras in sections:
        body.append(f'<h2 class="h-m legal-h">{esc(h)}</h2>' + "".join(p if p.startswith("<") else f"<p>{p}</p>" for p in paras))
    doc = ('<section class="sec sec-tight"><div class="wrap legal">' + "".join(body)
           + f'<p class="small">{t["updated"]}: {UPDATED[lang]}.</p>{_links(lang)}</div></section>')
    alternates = {"es": S.BASE_URL + _url(key, "es"), "en": S.BASE_URL + _url(key, "en")}
    page(_url(key, lang), title, description, hero + doc, cases=cases, priority="0.2", lang=lang, alternates=alternates)


def render_legal(cases):
    owner_es = esc(S.LEGAL["owner"]) or "el titular"
    owner_en = esc(S.LEGAL_EN.get("owner") or S.LEGAL["owner"]) or "the owner"

    # ------------------------------------------------------------------ Aviso legal / Legal notice
    _render("notice", "es",
            "Información exigida por el artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE).",
            "Aviso legal de GroundTruth AI: identificación del titular, condiciones de uso, carácter no contractual de los contenidos, propiedad intelectual y legislación aplicable.",
            [("1. Datos identificativos del titular", [_owner("es")]),
             ("2. Objeto y ámbito", [
                 "Este sitio web informa sobre la tecnología de destilación de conjuntos de datos de GroundTruth AI, sus posibles aplicaciones empresariales "
                 "y las vías de contacto comercial. El acceso al sitio es gratuito y atribuye la condición de usuario, que acepta este aviso legal."]),
             ("3. Carácter informativo y no contractual de los contenidos", [
                 "Todas las cifras, escenarios, simulaciones y cálculos publicados en este sitio, incluidos el simulador de arquitectura, la calculadora "
                 "de retorno de la inversión (ROI), los escenarios empresariales ilustrativos y los resultados experimentales, son <strong>estimaciones "
                 "ilustrativas</strong> obtenidas a partir de experimentos internos sobre conjuntos de datos públicos y de hipótesis indicadas en cada página "
                 "o introducidas por el propio usuario.",
                 "Estos contenidos tienen carácter exclusivamente informativo: <strong>no constituyen una oferta, un compromiso ni una garantía de resultados "
                 "y carecen de valor contractual</strong>. Los resultados reales dependen de cada carga de trabajo, de los datos y del entorno técnico, y solo "
                 "pueden determinarse mediante una evaluación específica. Cualquier compromiso comercial o técnico requerirá un contrato escrito independiente.",
                 "Los casos de negocio y arquitecturas de referencia describen aplicaciones propuestas para su evaluación en proyectos piloto y no implican "
                 "despliegues existentes en clientes."]),
             ("4. Responsabilidad", [
                 f"En la medida permitida por la legislación aplicable, {owner_es} no será responsable de las decisiones adoptadas por el usuario sobre la base "
                 "de las estimaciones, simulaciones o cálculos de este sitio, ni de los daños derivados de su uso, de errores u omisiones en los contenidos o de "
                 "interrupciones del servicio. Lo anterior no limita los derechos que la normativa reconoce a los consumidores y usuarios."]),
             ("5. Propiedad intelectual e industrial", [
                 f"Los contenidos, textos, diagramas, diseño y código de este sitio, así como las marcas y signos distintivos, pertenecen a {owner_es} o se usan "
                 "con autorización. Queda prohibida su reproducción, distribución o transformación con fines comerciales sin autorización previa por escrito. "
                 "Los datos de terceros citados en el sitio pertenecen a sus respectivas fuentes."]),
             ("6. Enlaces a sitios de terceros", [
                 "El sitio incluye enlaces a fuentes y servicios de terceros. El titular no controla ni se responsabiliza de sus contenidos ni de sus políticas."]),
             ("7. Protección de datos y cookies", [
                 'El tratamiento de datos personales se rige por la <a href="/privacidad/">Política de privacidad</a>. '
                 'El uso de cookies se describe en la <a href="/cookies/">Política de cookies</a>.']),
             ("8. Legislación aplicable y jurisdicción", [
                 "Este aviso legal se rige por la legislación española. Las controversias se someterán a los juzgados y tribunales que resulten competentes "
                 "conforme a la normativa aplicable, incluida, en su caso, la de protección de consumidores y usuarios."])],
            cases)
    _render("notice", "en",
            "Information required by Article 10 of Spanish Law 34/2002 on information society services and electronic commerce (LSSI-CE).",
            "GroundTruth AI legal notice: owner identification, terms of use, non-contractual nature of the content, intellectual property and applicable law.",
            [("1. Owner identification", [_owner("en")]),
             ("2. Purpose and scope", [
                 "This website provides information about GroundTruth AI's dataset distillation technology, its potential enterprise applications and "
                 "how to start a commercial conversation. Access is free of charge and makes you a user who accepts this legal notice."]),
             ("3. Informative, non-contractual nature of the content", [
                 "All figures, scenarios, simulations and calculations published on this website, including the architecture simulator, the return on "
                 "investment (ROI) calculator, the illustrative enterprise scenarios and the experimental results, are <strong>illustrative estimates</strong> "
                 "derived from internal experiments on public datasets and from assumptions stated on each page or entered by the user.",
                 "This content is provided for information only: <strong>it is not an offer or a commitment, carries no guarantee of results and has no contractual "
                 "value</strong>. Actual results depend on each workload, the data and the technical environment, and can only be determined in a specific "
                 "evaluation. Any commercial or technical commitment requires a separate written contract.",
                 "Business cases and reference architectures describe applications proposed for evaluation in pilot projects and do not imply existing "
                 "customer deployments."]),
             ("4. Liability", [
                 f"To the extent permitted by applicable law, {owner_en} is not liable for decisions users make on the basis of the estimates, simulations or "
                 "calculations on this website, nor for damage arising from its use, from errors or omissions in the content or from service interruptions. "
                 "This does not limit the rights that the law grants to consumers and users."]),
             ("5. Intellectual and industrial property", [
                 f"The content, text, diagrams, design and code of this website, as well as trademarks and distinctive signs, belong to {owner_en} or are used "
                 "with permission. Reproduction, distribution or transformation for commercial purposes without prior written permission is prohibited. "
                 "Third-party data cited on the website belongs to its respective sources."]),
             ("6. Links to third-party websites", [
                 "The website contains links to third-party sources and services. The owner does not control and is not responsible for their content or policies."]),
             ("7. Data protection and cookies", [
                 'Personal data is processed as described in the <a href="/privacy/">Privacy policy</a>. '
                 'The use of cookies is described in the <a href="/cookie-policy/">Cookie policy</a>.']),
             ("8. Applicable law and jurisdiction", [
                 "This legal notice is governed by Spanish law. Disputes will be submitted to the courts that are competent under the applicable rules, "
                 "including, where relevant, consumer protection rules."])],
            cases)

    # ------------------------------------------------------------------ Privacidad / Privacy
    _render("privacy", "es",
            "Información sobre el tratamiento de datos personales conforme al Reglamento (UE) 2016/679 (RGPD) y a la Ley Orgánica 3/2018 (LOPDGDD).",
            "Política de privacidad de GroundTruth AI: responsable, datos tratados, finalidades, base jurídica, destinatarios, conservación y derechos.",
            [("1. Responsable del tratamiento", [_owner("es")]),
             ("2. Datos que tratamos", [
                 "Solo tratamos los datos que nos facilita a través del formulario de contacto: nombre, correo electrónico profesional, organización, cargo, "
                 "sector, caso de negocio de interés, plazo previsto y la descripción que decida incluir. Le rogamos que no incluya datos confidenciales ni "
                 "datos personales de terceros.",
                 "Este sitio no utiliza cookies ni herramientas de analítica. El proveedor de alojamiento puede registrar direcciones IP en sus registros "
                 "técnicos con fines de seguridad."]),
             ("3. Finalidad y base jurídica", [
                 "Atender su solicitud (conversación inicial, evaluación de viabilidad, piloto, colaboración tecnológica o revisión técnica) y, en su caso, "
                 "gestionar la relación precontractual. La base jurídica es su consentimiento (art. 6.1.a RGPD), que puede retirar en cualquier momento, y la "
                 "aplicación de medidas precontractuales a petición suya (art. 6.1.b RGPD). No elaboramos perfiles ni adoptamos decisiones automatizadas."]),
             ("4. Destinatarios y encargados del tratamiento", [
                 "No cedemos sus datos a terceros salvo obligación legal. Para prestar el servicio intervienen proveedores que actúan como encargados del "
                 "tratamiento: el servicio de envío de formularios FormSubmit, que entrega su solicitud por correo electrónico; el proveedor del correo "
                 "electrónico en el que se recibe; y GitHub Pages como alojamiento del sitio. Algunos de estos proveedores pueden tratar datos fuera del "
                 "Espacio Económico Europeo; en ese caso, la transferencia debe ampararse en las garantías previstas en el capítulo V del RGPD."]),
             ("5. Conservación", [
                 "Conservamos los datos durante el tiempo necesario para atender su solicitud y, después, bloqueados durante los plazos legalmente exigibles "
                 "para atender posibles responsabilidades."]),
             ("6. Sus derechos", [
                 f"Puede ejercer sus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad, así como retirar su "
                 f"consentimiento, escribiendo a {_mail('es')}. Si considera que el tratamiento no se ajusta a la normativa, puede presentar una reclamación ante "
                 f'la Agencia Española de Protección de Datos (<a href="https://www.aepd.es/" rel="noopener">www.aepd.es</a>).'])],
            cases)
    _render("privacy", "en",
            "How personal data is processed under Regulation (EU) 2016/679 (GDPR) and Spanish Organic Law 3/2018 (LOPDGDD).",
            "GroundTruth AI privacy policy: controller, data processed, purposes, legal basis, recipients, retention and your rights.",
            [("1. Data controller", [_owner("en")]),
             ("2. Data we process", [
                 "We only process the data you provide through the contact form: name, work email, organization, role, industry, business case of "
                 "interest, expected timeline and any description you choose to include. Please do not include confidential information or personal "
                 "data about other people.",
                 "This website uses no cookies and no analytics tools. The hosting provider may record IP addresses in its technical logs for security purposes."]),
             ("3. Purpose and legal basis", [
                 "To respond to your request (initial conversation, feasibility assessment, pilot, technology partnership or technical review) and, where "
                 "applicable, to manage the pre-contractual relationship. The legal basis is your consent (Art. 6(1)(a) GDPR), which you may withdraw at any "
                 "time, and steps taken at your request before entering into a contract (Art. 6(1)(b) GDPR). We do not profile you or make automated decisions."]),
             ("4. Recipients and processors", [
                 "We do not share your data with third parties unless required by law. The following providers act as processors to deliver the service: "
                 "the FormSubmit form service, which delivers your request by email; the email provider where it is received; and GitHub Pages, which hosts "
                 "the website. Some of these providers may process data outside the European Economic Area; any such transfer must rely on the safeguards "
                 "set out in Chapter V of the GDPR."]),
             ("5. Retention", [
                 "We keep your data for as long as needed to respond to your request and, afterwards, blocked for the periods required by law to handle "
                 "possible liabilities."]),
             ("6. Your rights", [
                 f"You may exercise your rights of access, rectification, erasure, objection, restriction of processing and data portability, and withdraw "
                 f"your consent, by writing to {_mail('en')}. If you believe the processing does not comply with the law, you may lodge a complaint with the "
                 f'Spanish Data Protection Agency (<a href="https://www.aepd.es/" rel="noopener">www.aepd.es</a>) or the supervisory authority of your country.'])],
            cases)

    # ------------------------------------------------------------------ Cookies
    _render("cookies", "es",
            "Información conforme al artículo 22.2 de la LSSI-CE.",
            "Política de cookies de GroundTruth AI: este sitio no utiliza cookies ni tecnologías de seguimiento.",
            [("1. Uso de cookies en este sitio", [
                "Este sitio web <strong>no utiliza cookies</strong> ni tecnologías similares de almacenamiento o seguimiento, propias ni de terceros: "
                "no hay herramientas de analítica, publicidad ni redes sociales integradas. Las fuentes tipográficas se sirven desde el propio sitio.",
                "El simulador y la calculadora de ROI funcionan íntegramente en su navegador y no guardan ni envían los datos que introduce. El formulario "
                'de contacto solo envía datos cuando usted lo remite, según se describe en la <a href="/privacidad/">Política de privacidad</a>.']),
             ("2. Cambios", [
                "Si en el futuro se incorporan cookies no necesarias, se actualizará esta política y se solicitará su consentimiento previo."])],
            cases)
    _render("cookies", "en",
            "Information under Article 22.2 of Spanish Law 34/2002 (LSSI-CE).",
            "GroundTruth AI cookie policy: this website uses no cookies or tracking technologies.",
            [("1. Use of cookies on this website", [
                "This website <strong>does not use cookies</strong> or similar storage or tracking technologies, first-party or third-party: there are no "
                "analytics, advertising or embedded social media tools. Fonts are served from the website itself.",
                "The simulator and the ROI calculator run entirely in your browser and do not store or send the data you enter. The contact form only "
                'sends data when you submit it, as described in the <a href="/privacy/">Privacy policy</a>.']),
             ("2. Changes", [
                "If non-essential cookies are introduced in the future, this policy will be updated and your prior consent will be requested."])],
            cases)
