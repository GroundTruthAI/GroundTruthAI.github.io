"""Spanish legal pages: Aviso legal (LSSI-CE art. 10), Política de privacidad (RGPD art. 13 / LOPDGDD)
and Política de cookies (LSSI-CE art. 22.2). Written in Spanish (lang="es").

Owner identification comes from content/site.py → LEGAL. Nothing is invented: empty fields are not
rendered, and tools/verify.py fails until the mandatory ones are filled, so the site cannot be released
without them. Texts should be reviewed by the company's legal adviser.
"""
from content import site as S
from .core import esc, page, breadcrumb

UPDATED = "24 de noviembre de 2026"
LINKS = '<p class="small"><a href="/aviso-legal/">Aviso legal</a> · <a href="/privacidad/">Política de privacidad</a> · <a href="/cookies/">Política de cookies</a></p>'


def _hero(title, lead):
    return ('<div class="page-hero"><div class="wrap">' + breadcrumb([("Inicio", "/"), (title, None)])
            + f'<p class="eyebrow">Información legal</p><h1>{esc(title)}</h1><p class="lead">{lead}</p></div></div>')


def _doc(sections):
    out = []
    for h, paras in sections:
        out.append(f'<h2 class="h-m legal-h">{esc(h)}</h2>' + "".join(f"<p>{p}</p>" if not p.startswith("<") else p for p in paras))
    return '<section class="sec sec-tight"><div class="wrap legal">' + "".join(out) + f'<p class="small">Última actualización: {UPDATED}.</p>{LINKS}</div></section>'


def _owner():
    L = S.LEGAL
    rows = [("Titular", L["owner"]), ("NIF", L["nif"]), ("Domicilio", L["address"]),
            ("Correo electrónico", L["email"]), ("Datos registrales", L["registry"]), ("Sitio web", S.BASE_URL)]
    items = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in rows if v)
    return f'<dl class="legal-id">{items}</dl>'


def _mail():
    e = S.LEGAL["email"]
    return f'<a href="mailto:{esc(e)}">{esc(e)}</a>' if e else "la dirección de correo indicada en el aviso legal"


def render_legal(cases):
    owner = esc(S.LEGAL["owner"]) or "el titular"
    # ------------------------------------------------------------ Aviso legal
    page("/aviso-legal/", "Aviso legal",
         "Aviso legal de GroundTruth AI: identificación del titular, condiciones de uso, carácter no contractual de los contenidos, propiedad intelectual y legislación aplicable.",
         _hero("Aviso legal", "Información exigida por el artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE).")
         + _doc([
             ("1. Datos identificativos del titular", [_owner()]),
             ("2. Objeto y ámbito", [
                 f"Este sitio web informa sobre la tecnología de destilación de conjuntos de datos de GroundTruth AI, sus posibles aplicaciones empresariales "
                 f"y las vías de contacto comercial. El acceso al sitio es gratuito y atribuye la condición de usuario, que acepta este aviso legal."]),
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
                 f"En la medida permitida por la legislación aplicable, {owner} no será responsable de las decisiones adoptadas por el usuario sobre la base "
                 "de las estimaciones, simulaciones o cálculos de este sitio, ni de los daños derivados de su uso, de errores u omisiones en los contenidos o de "
                 "interrupciones del servicio. Lo anterior no limita los derechos que la normativa reconoce a los consumidores y usuarios."]),
             ("5. Propiedad intelectual e industrial", [
                 f"Los contenidos, textos, diagramas, diseño y código de este sitio, así como las marcas y signos distintivos, pertenecen a {owner} o se usan "
                 "con autorización. Queda prohibida su reproducción, distribución o transformación con fines comerciales sin autorización previa por escrito. "
                 "Los datos de terceros citados en el sitio pertenecen a sus respectivas fuentes."]),
             ("6. Enlaces a sitios de terceros", [
                 "El sitio incluye enlaces a fuentes y servicios de terceros. El titular no controla ni se responsabiliza de sus contenidos ni de sus políticas."]),
             ("7. Protección de datos y cookies", [
                 'El tratamiento de datos personales se rige por la <a href="/privacidad/">Política de privacidad</a>. '
                 'El uso de cookies se describe en la <a href="/cookies/">Política de cookies</a>.']),
             ("8. Legislación aplicable y jurisdicción", [
                 "Este aviso legal se rige por la legislación española. Las controversias se someterán a los juzgados y tribunales que resulten competentes "
                 "conforme a la normativa aplicable, incluida, en su caso, la de protección de consumidores y usuarios."]),
         ]),
         cases=cases, priority="0.2", lang="es")

    # ------------------------------------------------------------ Política de privacidad
    page("/privacidad/", "Política de privacidad",
         "Política de privacidad de GroundTruth AI: responsable, datos tratados, finalidades, base jurídica, destinatarios, conservación y derechos.",
         _hero("Política de privacidad", "Información sobre el tratamiento de datos personales conforme al Reglamento (UE) 2016/679 (RGPD) "
               "y a la Ley Orgánica 3/2018 (LOPDGDD).")
         + _doc([
             ("1. Responsable del tratamiento", [_owner()]),
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
                 f"consentimiento, escribiendo a {_mail()}. Si considera que el tratamiento no se ajusta a la normativa, puede presentar una reclamación ante "
                 f'la Agencia Española de Protección de Datos (<a href="https://www.aepd.es/" rel="noopener">www.aepd.es</a>).']),
         ]),
         cases=cases, priority="0.2", lang="es")

    # ------------------------------------------------------------ Política de cookies
    page("/cookies/", "Política de cookies",
         "Política de cookies de GroundTruth AI: este sitio no utiliza cookies ni tecnologías de seguimiento.",
         _hero("Política de cookies", "Información conforme al artículo 22.2 de la LSSI-CE.")
         + _doc([
             ("1. Uso de cookies en este sitio", [
                 "Este sitio web <strong>no utiliza cookies</strong> ni tecnologías similares de almacenamiento o seguimiento, propias ni de terceros: "
                 "no hay herramientas de analítica, publicidad ni redes sociales integradas. Las fuentes tipográficas se sirven desde el propio sitio.",
                 "El simulador y la calculadora de ROI funcionan íntegramente en su navegador y no guardan ni envían los datos que introduce. El formulario "
                 "de contacto solo envía datos cuando usted lo remite, según se describe en la <a href=\"/privacidad/\">Política de privacidad</a>."]),
             ("2. Cambios", [
                 "Si en el futuro se incorporan cookies no necesarias, se actualizará esta política y se solicitará su consentimiento previo."]),
         ]),
         cases=cases, priority="0.2", lang="es")
