"""Home, Platform, Technology, Evidence, ROI, Partners, Company, Pilot and 404 pages."""
from content import site as S
from .core import esc, md, ul, page, breadcrumb, button, badge, section, write
from .diagrams import hero_visual, viz_bc01, viz_bc02, viz_bc03, viz_bc04
from .pages_cases import case_url

# Technical support available for each case (public summary of the evidence matrix)
SUPPORT = {
    "BC03": ("Direct", "Benchmark data reduction and accuracy; 86% workstation training-energy measurement."),
    "BC09": ("Direct", "Same benchmark evidence as BC03; repeated retraining cycles not yet measured."),
    "BC05": ("Partial", "39% edge energy measurement; no device characterization yet."),
    "BC06": ("Partial", "Per-run training energy measurement; no data-center-level measurement."),
    "BC10": ("Partial", "Per-run training energy measurement; no lifecycle assessment."),
}
DEFAULT_SUPPORT = ("Indirect", "Single-domain benchmarks only; multi-domain combination not yet benchmarked.")


def _hero(title, lead, crumbs, eyebrow, ctas=""):
    return ('<div class="page-hero"><div class="wrap">' + breadcrumb(crumbs) + f'<p class="eyebrow">{esc(eyebrow)}</p>'
            f'<h1>{esc(title)}</h1><p class="lead">{md(lead)}</p>' + (f'<div class="cta-row">{ctas}</div>' if ctas else "") + '</div></div>')


# ---------------------------------------------------------------------------- HOME
def render_home(cases, industries):
    by = {c["id"]: c for c in cases}

    def flag_block(c, viz, layout):
        return (
            f'<article class="fc fc-{layout}" aria-labelledby="fc-{c["id"]}">'
            f'<div class="fc-text"><p class="eyebrow"><span class="code">{c["id"]}</span> {esc(c["eyebrow"])}</p>'
            f'<h3 id="fc-{c["id"]}"><a href="{case_url(c)}">{esc(c["title"])}</a></h3>'
            f'<p class="fc-head">{md(c["headline"])}</p>'
            '<dl class="fc-dl">'
            f'<div><dt>Problem</dt><dd>{md(c["problem_short"])}</dd></div>'
            f'<div><dt>Solution</dt><dd>{md(c["solution_short"])}</dd></div>'
            f'<div class="fc-outcome"><dt>Primary outcome</dt><dd>{md(c["outcome_short"])}</dd></div></dl>'
            f'<div class="cta-row cta-row-s"><a class="link-arrow" href="{case_url(c)}">Explore the business case</a>'
            f'<a class="link-arrow link-muted" href="/pilot/?case={c["id"]}">{esc(c["cta"])}</a></div></div>'
            f'<div class="fc-viz">{viz}</div></article>')

    flag = (
        flag_block(by["BC01"], viz_bc01(), "wide")
        + '<div class="fc-pair">' + flag_block(by["BC02"], viz_bc02(), "half") + flag_block(by["BC03"], viz_bc03(S.BENCHMARKS), "half") + '</div>'
        + flag_block(by["BC04"], viz_bc04(), "wide fc-rev"))

    more = "".join(
        f'<li><a href="{case_url(c)}"><span class="code">{c["id"]}</span><strong>{esc(c["title"])}</strong>'
        f'<span>{md(c["outcome_short"])}</span></a></li>' for c in cases if c["tier"] != "flagship")

    inds = "".join(f'<li><a class="chip chip-lg" href="/industries/{i["slug"]}/">{esc(i["name"])}</a></li>' for i in industries)

    body = (
        '<section class="hero" aria-labelledby="hero-h"><div class="wrap hero-grid"><div class="hero-copy">'
        '<p class="eyebrow">Task-aware dataset distillation for distributed enterprises</p>'
        '<h1 id="hero-h">Keep data distributed. <span class="hl g">Centralize intelligence.</span></h1>'
        '<p class="lead">Enable enterprise analytics across segregated data environments, optimize AI training costs and reduce unnecessary '
        'data movement through intelligent dataset distillation.</p>'
        '<div class="cta-row"><a class="btn btn-primary btn-lg" href="/pilot/">Request a Pilot</a>'
        '<a class="btn btn-ghost btn-lg" href="#challenges">See the business cases</a></div>'
        '<div class="hero-stats">'
        '<div class="stat"><p class="num g">86–95<span class="u">%</span></p><p class="lbl">less training data across four public benchmarks</p></div>'
        '<div class="stat"><p class="num g">≤2.8<span class="u">pp</span></p><p class="lbl">maximum accuracy change vs. full-data baseline</p></div>'
        '<div class="stat"><p class="num g">8–12<span class="u">wk</span></p><p class="lbl">indicative pilot to a measured decision</p></div></div>'
        '<p class="hero-note">Pilot-stage technology. Every claim on this site carries its <a href="/evidence/">evidence level</a>.</p>'
        f'</div><div class="hero-art">{hero_visual()}</div></div></section>'

        '<section class="sec sec-flag" id="challenges" aria-labelledby="ch-h"><div class="wrap">'
        '<p class="eyebrow">Flagship business cases</p>'
        '<h2 id="ch-h">Solve your most critical data challenges</h2>'
        '<p class="lead">Four enterprise problems where moving less data changes what is possible, not just what it costs.</p>'
        f'{flag}</div></section>'

        '<section class="sec sec-tight" aria-labelledby="more-h"><div class="wrap">'
        '<div class="sec-head"><h2 id="more-h" class="h-m">Seven more business cases from the same capability</h2>'
        '<a class="link-arrow" href="/business-cases/">Open the business case explorer</a></div>'
        f'<ul class="more-list">{more}</ul></div></section>'

        + section("opportunity", "The centralize-everything pattern is breaking",
                  '<div class="tension-grid">'
                  '<div class="tension"><h3>Segregation is deliberate</h3><p>OT networks, subsidiaries, regions and clouds are separated for '
                  'safety, security, ownership and regulation. AI programs that require a full raw copy in one place collide with those decisions.</p></div>'
                  '<div class="tension"><h3>Consolidation is slow and expensive</h3><p>Migrating and harmonizing entire data estates takes years. '
                  'Valuable analytics wait for programs whose scope is far larger than any single model needs.</p></div>'
                  '<div class="tension"><h3>Training cost scales with data</h3><p>Every retraining cycle reprocesses history. Storage, transfer, '
                  'compute and energy grow with volume, while much of that volume adds little to the model.</p></div></div>'
                  '<p class="lead-s">The opportunity: prepare the data a model actually needs <strong>where the data lives</strong>, and move '
                  'only that, under the controls you already have.</p>',
                  eyebrow="The opportunity", cls="sec-alt")

        + section("how", "How it works",
                  '<ol class="flow-steps">'
                  '<li><span class="fs-n">1</span><h3>Define the task</h3><p>Target model, variables and acceptance thresholds agreed with data owners.</p></li>'
                  '<li><span class="fs-n">2</span><h3>Distill at the source</h3><p>A runtime inside the authorized environment builds a compact, task-specific training set.</p></li>'
                  '<li><span class="fs-n">3</span><h3>Validate fidelity</h3><p>Models trained on full and distilled data are compared on the same test set.</p></li>'
                  '<li><span class="fs-n">4</span><h3>Approve and transfer</h3><p>Owners approve; the dataset moves through existing, governed paths.</p></li>'
                  '<li><span class="fs-n">5</span><h3>Train centrally</h3><p>Central teams train and iterate on a fraction of the volume.</p></li></ol>'
                  '<p><a class="link-arrow" href="/technology/">How dataset distillation works</a></p>',
                  eyebrow="Proposed solution")

        + section("value", "Three kinds of business value — measured separately",
                  '<div class="value-grid">'
                  '<div class="vg vg-direct"><h3>Direct cost reduction</h3>' + ul([
                      "Training and retraining compute", "Eligible storage and replicas", "Data transfer and ingestion",
                      "Processing and energy, net of distillation overhead"]) + '</div>'
                  '<div class="vg vg-ops"><h3>Operational efficiency</h3>' + ul([
                      "Faster model development and retraining", "Fewer raw copies to secure and govern",
                      "Simpler distributed AI workflows"]) + '</div>'
                  '<div class="vg vg-strat"><h3>Strategic enablement</h3>' + ul([
                      "Analytics across segregated environments", "Multi-facility and cross-subsidiary models",
                      "Initiatives that were blocked by data architecture"]) + '<p class="oc-note">Assessed qualitatively. We do not put a price on it.</p></div></div>'
                  '<div class="cta-row"><a class="btn btn-ghost" href="/roi/">Estimate value with your own assumptions</a></div>',
                  eyebrow="Business outcomes", cls="sec-alt")

        + section("evidence", "What we have shown, and what we have not",
                  '<div class="ev-home">'
                  '<div class="ev-stat"><p class="big g">86–95<span>%</span></p><p>less training data across four public benchmarks</p></div>'
                  '<div class="ev-stat"><p class="big g">≤2.8<span> pp</span></p><p>maximum accuracy change versus full-data baseline</p></div>'
                  '<div class="ev-stat ev-none"><p class="big">0</p><p>production deployments to date. Every business case is a proposed application, designed to be proven in a pilot.</p></div></div>'
                  '<p class="note">Internal experiments on Iris, Wine, Breast Cancer (tabular, MLP) and MNIST (image, CNN). Not yet independently replicated; '
                  'industrial time-series and multi-domain experiments are in the validation backlog.</p>'
                  '<p><a class="link-arrow" href="/evidence/">Full evidence and limitations</a></p>',
                  eyebrow="Evidence")

        + section("integration", "Fits the architecture you already run",
                  '<div class="int-grid">'
                  '<div><h3>Runs in your environment</h3><p>Deployed on a server, VM or private-cloud instance you control. Pilot design principle: no customer data is sent to GroundTruth AI.</p></div>'
                  '<div><h3>Uses your transfer paths</h3><p>Produces ordinary dataset files that move through your existing DMZ, gateway or pipeline controls.</p></div>'
                  '<div><h3>Feeds your ML platform</h3><p>Central teams consume distilled data as standard training data in the tools they already use.</p></div></div>'
                  '<p><a class="link-arrow" href="/platform/">Platform, deployment options and integration status</a></p>',
                  eyebrow="Integration and deployment", cls="sec-alt")

        + section("industries", "Built for complex, regulated, distributed enterprises",
                  f'<ul class="chips chips-lg">{inds}</ul>', eyebrow="Industries")

        + '<section class="sec sec-cta" aria-labelledby="cta-h"><div class="wrap cta-band">'
        '<div><p class="eyebrow">Commercial engagement</p><h2 id="cta-h">Prove it on one workload, with your data and your thresholds</h2>'
        '<p>An 8–12 week pilot, in your environment, against your current baseline. You define success before we start; you keep the measurements.</p></div>'
        '<div class="cta-stack"><a class="btn btn-primary btn-lg" href="/pilot/">Request a Pilot</a>'
        '<a class="btn btn-ghost" href="/business-cases/">Find your business case</a></div></div></section>')

    page("/", "GroundTruth AI — Keep data distributed. Centralize intelligence.",
         "Enable enterprise analytics across segregated data environments, optimize AI training costs and reduce unnecessary data movement through task-aware dataset distillation.",
         body, active="", cases=cases, priority="1.0", body_class="pg-home")


# ---------------------------------------------------------------------------- PLATFORM
def render_platform(cases):
    comps = [
        ("Distillation runtime", "Prototype", "proto",
         "Builds a compact, task-specific training dataset from source data inside the customer environment. Python runtime; tabular and image data exercised in internal experiments."),
        ("Fidelity validation", "Prototype", "proto",
         "Trains the same model on full and distilled data and compares task metrics on the same test set. Uses a scikit-learn-compatible model adapter."),
        ("Coverage and regime checks", "Proposed", "prop",
         "Confirms labeled events, rare classes and operating regimes remain represented. Designed for industrial and multi-domain cases; to be built and tested in pilots."),
        ("Approval and export workflow", "Proposed", "prop",
         "Packages the dataset with its fidelity report and lineage for review by data owners before transfer."),
        ("Regeneration and drift-triggered refresh", "Proposed", "prop",
         "Re-runs distillation when the task, data distribution or operating conditions change. Drift detection exists as a separate prototype capability."),
    ]
    comp_html = "".join(f'<li class="comp"><div class="comp-h"><h3>{esc(n)}</h3>{badge(s, k)}</div><p>{esc(d)}</p></li>' for n, s, k, d in comps)

    deploy = [
        ("Source-side server or VM", "Pilot mode", "Installed on customer hardware in the authorized zone (for example, the OT-side operations zone or a subsidiary data center). Operates on file exports."),
        ("Private cloud or customer VPC", "Pilot mode", "Runs inside the customer's own cloud account, next to the data domain it serves."),
        ("Workstation", "Used in experiments", "Internal benchmarks and energy measurements were run on workstation-class hardware."),
        ("Edge gateway", "Proposed", "Distillation close to sensors and devices. No specific device has been validated; no real-time execution is claimed."),
        ("Embedded / OEM", "Proposed", "Runtime embedded in a partner's appliance, historian or platform. See Partners."),
    ]
    dep_html = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{esc(s)}</td><td>{esc(d)}</td></tr>' for n, s, d in deploy)

    integ = [
        ("Python runtime", "verified"), ("Tabular data via pandas / NumPy", "verified"), ("scikit-learn-compatible model adapter", "verified"),
        ("Image arrays for CNN training (benchmark)", "verified"), ("CSV / Parquet file exchange", "proposed"),
        ("Industrial historian connectors (e.g. AVEVA PI)", "proposed"), ("OPC UA / MQTT", "proposed"), ("Kafka and event streams", "proposed"),
        ("Object storage (S3, ADLS, GCS)", "proposed"), ("Spark / Databricks", "proposed"), ("MLflow / model registries", "proposed"),
        ("Container and Kubernetes packaging", "proposed"), ("DMZ transfer tooling and data diodes", "customer"),
        ("Central ML platforms (Azure ML, SageMaker, Vertex AI, Databricks)", "customer"), ("Data catalogs and lineage tools", "customer"),
    ]
    lab = {"verified": "Verified in prototype", "proposed": "Proposed integration", "customer": "Customer system"}
    int_html = "".join(f'<tr><th scope="row">{esc(n)}</th><td><span class="st st-{k}">{lab[k]}</span></td></tr>' for n, k in integ)

    body = (
        _hero("A distillation layer that runs where your data lives",
              "GroundTruth AI is deployed inside the environment that owns the data. It produces task-specific training datasets, "
              "proves their fidelity against the full data, and hands them to the transfer paths and ML platforms you already operate.",
              [("Home", "/"), ("Platform", None)], "Platform",
              button("Request a Pilot", "/pilot/") + button("See the business cases", "/business-cases/", "ghost"))
        + section("components", "Platform components",
                  f'<p>Status is stated for every component. <strong>Prototype</strong> means implemented and used in internal experiments; '
                  f'<strong>Proposed</strong> means designed and scoped, not yet built.</p><ul class="comp-list">{comp_html}</ul>')
        + section("deployment", "Deployment options",
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Option</th><th scope="col">Status</th><th scope="col">Description</th></tr></thead><tbody>{dep_html}</tbody></table></div>',
                  cls="sec-alt")
        + section("integrations", "Integration status",
                  '<p>We distinguish what has been exercised from what is planned. Proposed integrations are built with the first customer that needs them.</p>'
                  f'<div class="table-wrap"><table class="tbl tbl-narrow"><thead><tr><th scope="col">Integration</th><th scope="col">Status</th></tr></thead><tbody>{int_html}</tbody></table></div>')
        + section("security", "Security and data governance",
                  '<div class="two-col"><div>' + ul([
                      "**Customer-controlled execution.** The runtime operates inside your environment, under your access controls.",
                      "**No data egress to GroundTruth AI.** Pilot design principle: customer data, distilled or raw, is not sent to us.",
                      "**Owner approval before transfer.** Every distilled dataset is reviewed with its fidelity report before it moves.",
                      "**Least-privilege access.** Read access limited to the variables and period in scope.",
                      "**Lineage.** Each dataset records its source scope, task specification and generation parameters.",
                  ]) + '</div><div class="callout callout-legal"><p class="callout-h">What distillation does not change</p>' + ul([
                      "Distilled data is derived from source data and is classified like it.",
                      "It is not anonymization and grants no legal authorization for any transfer.",
                      "It does not replace network segmentation, OT security controls or data integration.",
                      "GroundTruth AI holds no security certifications today.",
                  ]) + '</div></div>', cls="sec-alt")
        + section("next", "Evaluate the platform on your architecture",
                  '<p>A pilot starts with an architecture review: where the runtime would sit, which data it reads, which path the dataset takes and who approves it.</p>'
                  '<div class="cta-row">' + button("Request a Pilot", "/pilot/") + button("Read the technology", "/technology/", "ghost") + '</div>'))
    page("/platform/", "Platform", "GroundTruth AI platform components, deployment options, integration status and data governance — with verified and proposed capabilities stated separately.",
         body, active="platform", cases=cases, priority="0.7")


# ---------------------------------------------------------------------------- TECHNOLOGY
def render_technology(cases):
    comp = [
        ("Compression", "Every byte, encoded smaller", "Must be decompressed to be used; volume for training is unchanged."),
        ("Random or fixed-rate sampling", "A uniform fraction of records", "Task-agnostic; can drop rare classes, transients and edge regimes."),
        ("Aggregation and down-sampling", "Averages over time or groups", "Removes the variability many predictive models rely on."),
        ("Feature selection", "Fewer columns", "Reduces width, not volume; complementary to distillation."),
        ("Federated learning", "Data stays put; models travel", "Needs training infrastructure in every domain and an ongoing model-exchange channel."),
        ("Task-aware dataset distillation", "A compact dataset built for a defined model and task", "Fidelity must be validated per task; regenerated when the task changes."),
    ]
    rows = "".join(f'<tr{" class=\"tr-hl\"" if i == len(comp) - 1 else ""}><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td></tr>' for i, (a, b, c) in enumerate(comp))
    body = (
        _hero("Dataset distillation, explained for architects",
              "Dataset distillation builds a much smaller training dataset for a specific modeling task, such that models trained on it perform "
              "close to models trained on the full data. It is the enabling technology behind every GroundTruth AI business case.",
              [("Home", "/"), ("Technology", None)], "Technology",
              button("See what it enables", "/business-cases/") + button("Evidence", "/evidence/", "ghost"))
        + section("what", "What makes it task-aware",
                  '<div class="two-col"><div>'
                  '<p>A distilled dataset is not a general-purpose summary. What is kept depends on the <strong>task</strong>: the target variable, the model family and the '
                  'acceptance metric. The same source data can produce different distilled sets for a failure-prediction model and for a quality model.</p>'
                  '<p>That is why distillation can run at the source: the task specification travels to the data, and only the result travels back.</p></div>'
                  '<div class="side-card"><p class="side-h">Inputs and outputs</p>' + ul([
                      "**In:** source data in its home environment, plus a task specification",
                      "**Out:** a distilled training dataset",
                      "**Out:** a fidelity report comparing full-data and distilled-data models",
                      "**Out:** lineage metadata for governance",
                  ]) + '</div></div>')
        + section("compare", "How it differs from familiar techniques",
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Technique</th><th scope="col">What it keeps</th><th scope="col">Trade-off</th></tr></thead><tbody>{rows}</tbody></table></div>',
                  cls="sec-alt")
        + section("pipeline", "The distillation pipeline",
                  '<ol class="flow-steps">'
                  '<li><span class="fs-n">1</span><h3>Task specification</h3><p>Target, features, model family, metric and tolerance.</p></li>'
                  '<li><span class="fs-n">2</span><h3>Profiling</h3><p>Distributions, classes, regimes and labeled events in scope.</p></li>'
                  '<li><span class="fs-n">3</span><h3>Distillation</h3><p>The engine constructs the compact training set for the task.</p></li>'
                  '<li><span class="fs-n">4</span><h3>Fidelity validation</h3><p>Full vs. distilled models compared on the same test data.</p></li>'
                  '<li><span class="fs-n">5</span><h3>Approval and regeneration</h3><p>Owners approve; datasets are regenerated when the task or data change.</p></li></ol>'
                  '<p class="note">Proprietary method details are not published. They are available for technical due diligence under NDA.</p>')
        + section("scope", "Current scope and limits",
                  '<div class="ev-grid">'
                  '<div class="ev ev-yes"><h3>Exercised today</h3>' + ul([
                      "Classification tasks", "Tabular data with deep learning (MLP)", "Image data with a CNN (MNIST)",
                      "Python runtime and scikit-learn-compatible models"]) + '</div>'
                  '<div class="ev ev-gap"><h3>In the validation backlog</h3>' + ul([
                      "Industrial sensor time series and historian data", "Regression and forecasting tasks",
                      "Distilling separately in several domains and combining the results", "Rare-event and minority-class coverage",
                      "Measured energy and compute overhead of distillation itself"]) + '</div>'
                  '<div class="ev ev-risk"><h3>Known trade-offs</h3>' + ul([
                      "Accuracy can drop (up to −2.8 pp in benchmarks); tolerance is set per task",
                      "A distilled set is task-specific; new tasks need regeneration",
                      "Distillation has its own compute and energy cost"]) + '</div></div>', cls="sec-alt")
        + section("adjacent", "The wider engine and adjacent capabilities",
                  '<p>Distillation is part of a multimodal intelligence engine designed to fuse tabular, image, behavioral and time-series signals. '
                  'The same engine supports capabilities that are <strong>prototypes</strong>, not validated on customer data and outside the scope of the business cases on this site:</p>'
                  + ul(["**Data drift detection** — monitoring changes in input distributions and model behavior (proposed as a trigger for regeneration in BC09).",
                        "**Anomaly detection** — multimodal anomaly signals, including fraud-style patterns.",
                        "**Behavioral segmentation and recommendation** — earlier product explorations."])
                  + '<p><a class="link-arrow" href="/business-cases/continuous-model-retraining/">See how drift detection relates to continuous retraining</a></p>'))
    page("/technology/", "Technology", "How task-aware dataset distillation works, how it differs from compression, sampling and federated learning, and its current scope and limits.",
         body, active="technology", cases=cases, priority="0.7")


# ---------------------------------------------------------------------------- EVIDENCE
def render_evidence(cases):
    lv = "".join(f'<li class="lvl lvl-{k}"><h3>{esc(n)}</h3><p>{esc(d)}</p><p class="lvl-now"><span>Today:</span> {esc(now)}</p></li>'
                 for k, n, d, now in S.EVIDENCE_LEVELS)
    bm = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{esc(t)}</td><td class="num">{r}%</td><td class="num">{b:.1f}%</td>'
                 f'<td class="num">{d:.1f}%</td><td class="num">{delta:+.1f} pp</td></tr>' for n, t, r, b, d, delta in S.BENCHMARKS)
    per = []
    for c in cases:
        lvl, note = SUPPORT.get(c["id"], DEFAULT_SUPPORT)
        per.append(f'<tr><td><span class="code">{c["id"]}</span></td><th scope="row"><a href="{case_url(c)}#evidence">{esc(c["title"])}</a></th>'
                   f'<td>Proposed application</td><td><span class="sup sup-{lvl.lower()}">{lvl}</span></td><td>{esc(note)}</td></tr>')
    ctx = [
        ("95.6% of enterprise file data inactive or redundant, obsolete or trivial", "CTERA, Cold Data Report (2026), 16 PB across 856 NAS scans; vendor-commissioned",
         "https://www.blocksandfiles.com/"),
        ("Storage, backup and DR exceed 30% of IT budget for 55% of large U.S. enterprises", "Komprise, State of Unstructured Data Management (2026), survey of 300 IT leaders",
         "https://www.komprise.com/"),
        ("Temporal quality degradation in 91% of 128 model–dataset pairs", "Vela et al., Scientific Reports 12, 11654 (2022)", "https://doi.org/10.1038/s41598-022-15245-z"),
        ("U.S. data centers used 4.4% of national electricity in 2023", "LBNL / U.S. DOE, 2024 United States Data Center Energy Usage Report",
         "https://www.energy.gov/"),
        ("Global data-center electricity ≈415 TWh in 2024", "IEA, Energy and AI (2025)", "https://www.iea.org/reports/energy-and-ai"),
    ]
    ctx_html = "".join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)} · <a href="{esc(u)}" rel="noopener">source</a></td></tr>' for a, b, u in ctx)
    body = (
        _hero("Evidence, stated plainly",
              "Business-led positioning must not become exaggerated claims. Every statement on this site is classified by the kind of evidence behind it, "
              "and every business case states what has not yet been proven.",
              [("Home", "/"), ("Evidence", None)], "Evidence",
              button("Request a Pilot", "/pilot/") + button("ROI calculator", "/roi/", "ghost"))
        + section("levels", "How we classify evidence", f'<ul class="lvl-list">{lv}</ul>')
        + section("benchmarks", "Experimentally supported technical outcomes",
                  '<p>Internal experiments on public benchmark datasets. Accuracy compares models trained on the full training data and on the distilled training data.</p>'
                  '<div class="table-wrap"><table class="tbl"><caption class="sr-only">Benchmark results</caption><thead><tr><th scope="col">Dataset</th><th scope="col">Data and model</th>'
                  '<th scope="col" class="num">Data reduction</th><th scope="col" class="num">Full-data accuracy</th><th scope="col" class="num">Distilled accuracy</th>'
                  f'<th scope="col" class="num">Change</th></tr></thead><tbody>{bm}</tbody></table></div>'
                  '<div class="two-col"><div><h3 class="h-s">Energy measurements</h3>' + ul([
                      "**86%** less energy per model training run on a workstation after data reduction.",
                      "**39%** less energy on IoT / edge devices at the point of capture.",
                      "Internal measurements; energy estimated with Schneider Electric reference data. Methodology not yet published.",
                      "The figures do not separately report the energy consumed by the distillation step. Pilots measure it explicitly.",
                  ]) + '</div><div><h3 class="h-s">Read these results carefully</h3>' + ul([
                      "Small, clean, public datasets; classification only.",
                      "Not yet independently replicated.",
                      "Results do not transfer automatically to industrial time series, logs or multi-domain data.",
                      "No customer production deployment exists today.",
                  ]) + '</div></div>', cls="sec-alt")
        + section("by-case", "Evidence by business case",
                  '<p><strong>Direct</strong>: the experiments measure the outcome the case depends on. <strong>Partial</strong>: related measurements exist. '
                  '<strong>Indirect</strong>: the case relies on an architectural hypothesis that has not yet been benchmarked.</p>'
                  '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">ID</th><th scope="col">Business case</th><th scope="col">Status</th>'
                  f'<th scope="col">Technical support</th><th scope="col">Notes</th></tr></thead><tbody>{"".join(per)}</tbody></table></div>')
        + section("backlog", "Validation backlog",
                  '<p>The experiments that would most strengthen the business cases. Planned; no dates are published.</p><ol class="num-list">'
                  '<li><strong>Industrial time-series benchmark</strong> — historian-style sensor data, failure prediction. Supports BC01, BC04, BC05.</li>'
                  '<li><strong>Multi-domain combination experiment</strong> — distill separately in heterogeneous domains, combine, compare with centralized training. Supports BC01, BC02, BC04, BC07, BC08, BC11.</li>'
                  '<li><strong>Rare-event coverage study</strong> — minority classes and failure modes after distillation. Supports BC01, BC04.</li>'
                  '<li><strong>Distillation overhead measurement</strong> — compute and energy of the distillation step itself. Supports every direct-cost claim.</li>'
                  '<li><strong>Retraining-cycle study</strong> — repeated distillation and retraining under drift. Supports BC09.</li>'
                  '<li><strong>Edge device characterization</strong> — footprint and throughput on representative gateways. Supports BC05.</li></ol>'
                  '<p>Pilots are designed to generate exactly this evidence, on customer data, with measurements the customer keeps.</p>', cls="sec-alt")
        + section("context", "Market context (third-party sources)",
                  '<p>Context for why data volume matters. These figures describe the market, not GroundTruth AI results.</p>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Finding</th><th scope="col">Source</th></tr></thead><tbody>{ctx_html}</tbody></table></div>'
                  '<h3 class="h-s">Earlier briefing material</h3><p>The <a href="/resources/smart-data-savings/">Smart Data Savings briefing deck</a> uses internal planning rates '
                  '(for example storage and cloud processing reductions) that have <strong>not</strong> been validated in production. Treat them as illustrative assumptions.</p>'))
    page("/evidence/", "Evidence", "GroundTruth AI evidence classification, benchmark results, energy measurements, evidence by business case and the validation backlog.",
         body, active="evidence", cases=cases, priority="0.8")


# ---------------------------------------------------------------------------- ROI
def _num(id_, label, value, unit="", step="any", hint="", cls=""):
    h = f'<span class="hint" id="{id_}-h">{esc(hint)}</span>' if hint else ""
    d = f' aria-describedby="{id_}-h"' if hint else ""
    return (f'<div class="fld {cls}"><label for="{id_}">{esc(label)}</label>'
            f'<div class="inp"><input type="number" id="{id_}" name="{id_}" value="{value}" min="0" step="{step}" inputmode="decimal"{d}>'
            f'{f"<span class=unit>{esc(unit)}</span>" if unit else ""}</div>{h}</div>')


def render_roi(cases):
    opts = "".join(f'<option value="{c["id"]}" data-scenario="{c["roi_scenario"]}">{c["id"]} · {esc(c["title"])}</option>' for c in cases)
    strat = {c["id"]: c["outcomes"]["strategic"] for c in cases}
    strat_html = "".join(f'<ul class="strat-list" data-case="{cid}" hidden>' + "".join(
        f'<li><label><input type="checkbox"> {md(s)}</label></li>' for s in items) + "</ul>" for cid, items in strat.items())

    transfer = (
        '<fieldset class="scen" data-scen="transfer"><legend>Data movement & replication</legend><div class="fld-grid">'
        + _num("t_dom", "Data domains or sites", 4, "", "1")
        + _num("t_vol", "Raw data moved per domain per month", 20, "TB")
        + _num("t_elig", "Share moved only to feed model training", 50, "%", hint="Only this eligible share is affected.")
        + _num("t_ctr", "Transfer / network cost", 20, "per TB", hint="Egress, WAN or gateway cost. Use your contract rates.")
        + _num("t_cproc", "Central ingestion & processing cost", 30, "per TB")
        + _num("t_cst", "Central storage cost incl. replicas", 25, "per TB·month")
        + _num("t_ret", "Average retention of training copies", 12, "months", "1")
        + _num("t_over", "Source-side distillation cost", 5, "per TB distilled", hint="Compute and operations at the source. Measured in a pilot.")
        + '</div></fieldset>')
    training = (
        '<fieldset class="scen" data-scen="training" hidden><legend>Training & retraining spend</legend><div class="fld-grid">'
        + _num("r_spend", "Annual training and retraining compute spend", 400000, "per year")
        + _num("r_share", "Share of that spend that scales with data volume", 60, "%", hint="Fixed costs (reserved capacity, tooling) are not reduced.")
        + _num("r_runs", "Distillation runs per year", 12, "", "1", hint="One per retraining cycle, or less if datasets are reused.")
        + _num("r_rcost", "Cost per distillation run", 1500, "per run")
        + _num("r_kwh", "Annual training energy (optional)", 0, "kWh")
        + _num("r_dkwh", "Energy per distillation run (optional)", 0, "kWh")
        + _num("r_price", "Electricity price", 0.15, "per kWh")
        + _num("r_hours", "Training wall-clock hours per year (optional)", 0, "hours")
        + '</div></fieldset>')
    infra = (
        '<fieldset class="scen" data-scen="infrastructure" hidden><legend>Storage, compute & energy</legend><div class="fld-grid">'
        + _num("i_tb", "Eligible stored training data", 500, "TB", hint="Only datasets that could be replaced by distilled versions.")
        + _num("i_cst", "Storage cost incl. backup and replicas", 25, "per TB·month")
        + _num("i_comp", "Eligible annual compute spend", 300000, "per year")
        + _num("i_share", "Share of compute that scales with data", 60, "%")
        + _num("i_kwh", "Eligible annual energy", 0, "kWh", hint="Only energy not already paid inside the compute spend above.")
        + _num("i_price", "Electricity price", 0.15, "per kWh")
        + _num("i_ocost", "Annual distillation compute cost", 20000, "per year")
        + _num("i_okwh", "Annual distillation energy", 0, "kWh")
        + _num("i_grid", "Grid emission factor (optional)", 0, "kg CO₂e/kWh", hint="Location-based. Operational emissions only; not a lifecycle assessment.")
        + '</div></fieldset>')
    common = (
        '<fieldset class="scen-common"><legend>Assumptions that apply to every scenario</legend><div class="fld-grid">'
        + _num("c_red", "Assumed data reduction on eligible data", 70, "%", hint="Benchmarks: 86–95% on public datasets. Your pilot measures yours.")
        + _num("c_sol", "GroundTruth AI annual subscription", 0, "per year", hint="Enter a quoted figure. Pricing is not published.")
        + _num("c_impl", "One-time implementation cost", 0, "one-time")
        + _num("c_hrs", "Team hours on data preparation and transfer per year (optional)", 0, "hours")
        + _num("c_hsave", "Share of those hours avoidable (optional)", 0, "%")
        + _num("c_rate", "Loaded hourly cost (optional)", 0, "per hour")
        + '</div></fieldset>')

    body = (
        _hero("Estimate the value for your business case",
              "An illustrative financial scenario built only on assumptions you enter. It separates direct cost reduction, operational efficiency and strategic "
              "enablement, deducts the cost of distillation itself, and never puts a price on strategic value.",
              [("Home", "/"), ("Business cases", "/business-cases/"), ("ROI calculator", None)], "ROI calculator")
        + '<section class="sec sec-tight" aria-labelledby="roi-h"><div class="wrap">'
        '<h2 id="roi-h" class="sr-only">Calculator</h2>'
        '<noscript><div class="callout"><p>The calculator needs JavaScript. The method: savings = eligible volume or spend × assumed reduction × unit cost, minus distillation cost, '
        'minus solution cost. Strategic value is listed, never priced.</p></div></noscript>'
        '<form class="roi" id="roi" hidden><div class="roi-in">'
        '<div class="fld-row"><div class="fld"><label for="roi-case">Business case</label>'
        f'<select id="roi-case"><option value="">Choose a business case (optional)</option>{opts}</select></div>'
        '<div class="fld"><label for="roi-scen">Value scenario</label><select id="roi-scen">'
        + "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in S.ROI_SCENARIOS.items())
        + '</select></div><div class="fld fld-s"><label for="roi-cur">Currency</label><select id="roi-cur"><option value="$">USD $</option><option value="€">EUR €</option><option value="£">GBP £</option></select></div></div>'
        + transfer + training + infra + common
        + '<p class="note">Defaults are placeholders for illustration only, not benchmarks, quotes or forecasts. Replace them with your own figures.</p>'
        '</div><div class="roi-out" aria-live="polite">'
        '<div class="out-card out-main"><p class="out-k">Net annual direct value</p><p class="out-big" id="o-net">—</p>'
        '<p class="out-s" id="o-net-s"></p></div>'
        '<div class="out-card"><p class="out-k">Direct cost reduction</p><ul class="out-lines" id="o-lines"></ul></div>'
        '<div class="out-card"><p class="out-k">Operational efficiency</p><ul class="out-lines" id="o-ops"></ul></div>'
        '<div class="out-card"><p class="out-k">Energy and emissions</p><ul class="out-lines" id="o-energy"></ul></div>'
        '<div class="out-card out-strat"><p class="out-k">Strategic enablement · not priced</p>'
        '<p class="small" id="o-strat-empty">Choose a business case to list its strategic outcomes. Tick those that matter to you; they are not converted into money.</p>'
        f'{strat_html}</div>'
        '<div class="cta-row"><button class="btn btn-ghost btn-sm js-print" type="button" hidden>Print scenario</button>'
        '<a class="btn btn-primary btn-sm" id="o-pilot" href="/pilot/">Validate these assumptions in a pilot</a></div>'
        '</div></form></div></section>'
        + section("method", "Method and limits",
                  ul([
                      "Only the **eligible, data-proportional share** of each cost line is reduced. Dataset reduction is not an equivalent reduction of total infrastructure or data-center spend.",
                      "**Distillation overhead** (compute, energy) and the **solution cost** are deducted from gross savings.",
                      "Energy results are operational estimates. Environmental claims require lifecycle measurement.",
                      "Operational efficiency is only computed from hours you enter; strategic enablement is never priced.",
                      "All calculation happens in your browser. Nothing you enter is sent anywhere.",
                  ]), cls="sec-alt"))
    page("/roi/", "ROI calculator", "Estimate the direct, operational and strategic value of dataset distillation for a specific business case, using your own assumptions and net of distillation overhead.",
         body, active="business-cases", cases=cases, priority="0.8", extra_js=("/assets/js/roi.js",))


# ---------------------------------------------------------------------------- PARTNERS
def render_partners(cases):
    models = [
        ("Systems integrators and consultancies", "Co-deliver pilots and production rollouts inside OT, data platform and MLOps programs.",
         "Reference architectures, pilot methodology and technical enablement."),
        ("Industrial automation and OT vendors", "Embed source-side distillation in historians, edge gateways or industrial data platforms (OEM).",
         "Embedded runtime licensing and joint validation on industrial data."),
        ("Cloud and data platforms", "Integrate distilled datasets into data, ML and marketplace offerings for multicloud and residency scenarios.",
         "Integration design for object stores, pipelines and registries."),
        ("Infrastructure and hardware providers", "Pair efficient training-data pipelines with workstation, server and data-center offerings.",
         "Joint measurement of training time and energy on partner hardware."),
        ("Research and validation partners", "Independent replication and new benchmarks: time series, multi-domain, rare events.",
         "Access to the method under NDA for structured evaluation."),
    ]
    cards = "".join(f'<li class="pm"><h3>{esc(n)}</h3><p>{esc(d)}</p><p class="pm-k">We bring</p><p>{esc(b)}</p></li>' for n, d, b in models)
    body = (
        _hero("Build, deliver and embed distillation with us",
              "GroundTruth AI is a software layer designed to sit inside other people's architectures. We are looking for partners who own those architectures.",
              [("Home", "/"), ("Partners", None)], "Partners",
              button("Discuss a partnership", "/pilot/?type=partnership"))
        + section("models", "Partnership models", f'<p class="note">GroundTruth AI has no announced partnerships today. The models below describe what we are seeking.</p><ul class="pm-grid">{cards}</ul>')
        + section("oem", "OEM and embedded licensing",
                  '<div class="two-col"><div><p>Several business cases (OT/IT segregation, edge-to-cloud, distributed industrial intelligence) are strongest when distillation ships '
                  'inside a platform the customer already trusts. We offer the runtime for embedding, with joint validation on the partner\'s target data.</p></div><div>'
                  + ul(["Licensing models are discussed per partnership; no prices are published.",
                        "Joint validation plan before any co-marketing claim.",
                        "No claim of compatibility with a partner product until it has been tested."]) + '</div></div>', cls="sec-alt")
        + section("start", "Start a conversation",
                  '<p>Tell us which business case your customers face and where your platform sits in their architecture.</p>'
                  '<div class="cta-row">' + button("Discuss a partnership", "/pilot/?type=partnership") + button("Review the business cases", "/business-cases/", "ghost") + '</div>'))
    page("/partners/", "Partners", "Partnership models for systems integrators, OT vendors, cloud platforms, infrastructure providers and research partners, including OEM licensing.",
         body, active="partners", cases=cases, priority="0.6")


# ---------------------------------------------------------------------------- COMPANY
def render_company(cases):
    body = (
        _hero("Keep data distributed. Centralize intelligence.",
              "GroundTruth AI develops task-aware dataset distillation so enterprises can build central AI on data that stays where it belongs.",
              [("Home", "/"), ("Company", None)], "Company",
              button("Request a Pilot", "/pilot/"))
        + section("why", "Why we exist",
                  '<p class="lead-s">Enterprise data is distributed for good reasons: safety, ownership, regulation, cost. The default AI workflow ignores those reasons and asks for everything in one place. '
                  'We think the better answer is to move less, and to move only what a model actually needs.</p>')
        + section("stage", "Where we are",
                  '<div class="two-col"><div>' + ul([
                      "Proof-of-concept-ready technology, validated in internal experiments on public benchmarks.",
                      "Seeking structured enterprise pilots and design partners.",
                      "No production deployments, customer references or certifications yet. We say so on every business case.",
                  ]) + '</div><div class="side-card"><p class="side-h">Founded by</p><p>Applied machine-learning researchers with backgrounds in data-efficient learning, '
                  'decision systems and industrial and enterprise AI.</p></div></div>', cls="sec-alt")
        + section("principles", "How we work",
                  '<div class="tension-grid">'
                  '<div class="tension"><h3>Evidence before claims</h3><p>Every statement is labeled as demonstrated, experimental, proposed or illustrative.</p></div>'
                  '<div class="tension"><h3>Your data, your environment</h3><p>Pilots run inside your environment. Your data is not sent to us.</p></div>'
                  '<div class="tension"><h3>Your thresholds</h3><p>You define acceptable model performance and economic targets before a pilot starts.</p></div></div>')
        + section("contact", "Contact",
                  '<p>For pilots, partnerships and technical due diligence, use the request form. We reply with a short scoping call proposal.</p>'
                  '<div class="cta-row">' + button("Request a Pilot", "/pilot/") + button("Discuss a partnership", "/pilot/?type=partnership", "ghost") + '</div>', cls="sec-alt"))
    page("/company/", "Company", "About GroundTruth AI: mission, stage, principles and how to get in touch.", body, active="company", cases=cases, priority="0.5")


# ---------------------------------------------------------------------------- PILOT
def render_pilot(cases, industries):
    case_opts = "".join(f'<option value="{c["id"]}" data-cta="{esc(c["cta"])}">{c["id"]} · {esc(c["title"])}</option>' for c in cases)
    ind_opts = "".join(f'<option value="{i["slug"]}">{esc(i["name"])}</option>' for i in industries)
    configured = bool(S.CONTACT_EMAIL)
    body = (
        _hero("Request a Pilot",
              "A bounded evaluation on one workload, in your environment, against your baseline, with success criteria you set before we start.",
              [("Home", "/"), ("Request a Pilot", None)], "Commercial engagement")
        + section("structure", "How a pilot runs",
                  '<ol class="flow-steps flow-4">'
                  '<li><span class="fs-n">1</span><h3>Scope</h3><p>Pick one workload and baseline. Agree technical and economic acceptance thresholds.</p></li>'
                  '<li><span class="fs-n">2</span><h3>Deploy</h3><p>Install the runtime in the authorized environment. Review placement with security.</p></li>'
                  '<li><span class="fs-n">3</span><h3>Distill and validate</h3><p>Compare full-data and distilled-data models on the same test set.</p></li>'
                  '<li><span class="fs-n">4</span><h3>Measure and decide</h3><p>Transfer, storage, compute, energy and accuracy, including distillation overhead.</p></li></ol>'
                  '<p class="note">Indicative duration 8–12 weeks. Pilot pricing is scoped per engagement and not published.</p>')
        + '<section class="sec sec-alt" aria-labelledby="form-h"><div class="wrap two-col two-col-form">'
        '<div><h2 id="form-h">Tell us about your situation</h2>'
        '<p>We reply with a scoping call proposal and the pilot design for your business case. If distillation is not a good fit, we will say so.</p>'
        + ul(["Which data, where it lives, and why it cannot simply be centralized", "The model or analytics you want to build", "The baseline you would compare against"])
        + '<p class="small">This form does not send data to any server. '
        + ("Submitting opens your email client with the request pre-filled." if configured else
           "Submitting prepares a structured request you can copy and send to your GroundTruth AI contact.")
        + '</p></div>'
        '<noscript><p class="callout">The request form needs JavaScript. Please contact your GroundTruth AI representative directly.</p></noscript>'
        f'<form class="pilot-form" id="pilot-form" novalidate data-to="{esc(S.CONTACT_EMAIL)}">'
        '<div class="fld"><label for="p-type">Request type</label><select id="p-type" name="type">'
        '<option value="pilot">Pilot</option><option value="assessment">Architecture assessment</option>'
        '<option value="partnership">Partnership</option><option value="diligence">Technical due diligence</option></select></div>'
        f'<div class="fld"><label for="p-case">Business case</label><select id="p-case" name="case"><option value="">Not sure yet</option>{case_opts}</select></div>'
        f'<div class="fld"><label for="p-ind">Industry</label><select id="p-ind" name="industry"><option value="">Select</option>{ind_opts}</select></div>'
        '<div class="fld-2"><div class="fld"><label for="p-name">Name <span class="req">(required)</span></label><input id="p-name" name="name" autocomplete="name" required></div>'
        '<div class="fld"><label for="p-email">Work email <span class="req">(required)</span></label><input id="p-email" name="email" type="email" autocomplete="email" required></div></div>'
        '<div class="fld-2"><div class="fld"><label for="p-org">Organization <span class="req">(required)</span></label><input id="p-org" name="org" autocomplete="organization" required></div>'
        '<div class="fld"><label for="p-role">Role</label><input id="p-role" name="role" autocomplete="organization-title"></div></div>'
        '<div class="fld"><label for="p-env">Data environment and constraint</label><textarea id="p-env" name="env" rows="4" '
        'placeholder="For example: historian data in 6 plants behind an industrial DMZ; central ML team on Azure; transfer policy limits raw replication."></textarea></div>'
        '<div class="fld"><label for="p-time">Timeline</label><select id="p-time" name="timeline"><option value="">Select</option>'
        '<option>Exploring</option><option>Within 3 months</option><option>3–6 months</option><option>Budgeted this year</option></select></div>'
        '<div class="fld fld-check"><label><input type="checkbox" id="p-consent" name="consent" required> I agree that GroundTruth AI may use these details to respond to this request. <span class="req">(required)</span></label></div>'
        '<p class="form-err" id="p-err" role="alert" hidden></p>'
        '<button class="btn btn-primary" type="submit" id="p-submit">Request a Pilot</button>'
        '<div class="form-out" id="p-out" hidden><p class="callout-h" id="p-out-h" tabindex="-1">Your request is ready</p>'
        '<p id="p-out-msg"></p><label for="p-text" class="sr-only">Prepared request</label><textarea id="p-text" rows="10" readonly></textarea>'
        '<button class="btn btn-ghost btn-sm" type="button" id="p-copy">Copy request</button></div>'
        '</form></div></section>')
    page("/pilot/", "Request a Pilot", "Request a scoped GroundTruth AI pilot: one workload, your environment, your baseline and your acceptance thresholds.",
         body, active="", cases=cases, priority="0.9", extra_js=("/assets/js/pilot.js",))


def render_404(cases):
    body = (_hero("Page not found", "The page you were looking for has moved or does not exist.",
                  [("Home", "/"), ("Not found", None)], "404",
                  button("Business cases", "/business-cases/") + button("Home", "/", "ghost")))
    # 404 is served at any path by GitHub Pages: absolute URLs keep it working.
    page("/404.html", "Page not found", "Page not found.", body, cases=cases, priority=None)


LEGACY = {
    "distillation.html": "/technology/",
    "data-drift.html": "/technology/#adjacent",
    "customer-segmentation.html": "/technology/#adjacent",
    "recommender-systems.html": "/technology/#adjacent",
    "fraud-detection.html": "/technology/#adjacent",
    "portfolio-details.html": "/",
    "service-details.html": "/",
    "starter-page.html": "/",
}


def render_legacy():
    for old, new in LEGACY.items():
        write("/" + old, (
            '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{S.BASE_URL}{new}">'
            '<meta name="robots" content="noindex"><title>Moved · GroundTruth AI</title></head>'
            f'<body><p>This page has moved to <a href="{new}">{S.BASE_URL}{new}</a>.</p></body></html>\n'))
