"""Home, Platform, Technology, Evidence, ROI, Simulator, Partners, Company, Engagement form and 404 pages."""
from content import site as S
from .core import esc, md, ul, page, breadcrumb, button, badge, section, write
from .diagrams import (hero_visual, viz_bc03, viz_pillar_distributed, viz_pillar_efficiency, viz_pillar_mobility,
                       arch_figure, legend, SCENARIO_A, OEM_EMBED)
from .pages_cases import case_url, engagement_block

# Technical support available for each case (public summary of the evidence matrix)
SUPPORT = {
    "BC03": ("Direct", "Benchmark data reduction and accuracy; 86% workstation training-energy measurement."),
    "BC09": ("Direct", "Same benchmark evidence as AI training cost optimization; repeated retraining cycles not yet measured."),
    "BC05": ("Partial", "39% edge energy measurement; no device characterization yet."),
    "BC06": ("Partial", "Per-run training energy measurement; no data-center-level measurement."),
    "BC10": ("Partial", "Per-run training energy measurement; no lifecycle assessment."),
}
DEFAULT_SUPPORT = ("Indirect", "Single-domain benchmarks only; multi-domain combination not yet benchmarked.")
PILLAR_VIZ = {"distributed-enterprise-intelligence": viz_pillar_distributed,
              "ai-infrastructure-efficiency": viz_pillar_efficiency,
              "intelligent-data-mobility": viz_pillar_mobility}

# Status vocabulary for what exists today (platform, deployment, integrations)
STATUS = {"available": ("Available for pilots", "proto"), "experimental": ("Experimental", "proto"),
          "reference": ("Reference architecture", "ref"), "planned": ("Planned", "prop"),
          "proposed": ("Proposed", "prop"), "customer": ("Customer system", "cust")}


def status_badge(key):
    label, kind = STATUS[key]
    return badge(label, kind)


def _hero(title, lead, crumbs, eyebrow, ctas=""):
    return ('<div class="page-hero"><div class="wrap">' + breadcrumb(crumbs) + f'<p class="eyebrow">{esc(eyebrow)}</p>'
            f'<h1>{esc(title)}</h1><p class="lead">{md(lead)}</p>' + (f'<div class="cta-row">{ctas}</div>' if ctas else "") + '</div></div>')


def _names(cases, ids):
    by = {c["id"]: c for c in cases}
    return ", ".join(by[i]["title"] for i in ids if i in by)


# ---------------------------------------------------------------------------- HOME
def render_home(cases, industries):
    by = {c["id"]: c for c in cases}

    # Section 2 — three strategic solutions
    def pillar_panel(p, layout):
        apps = "".join(f'<li><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></li>' for cid in p["cases"])
        return (
            f'<article class="pl pl-{layout}" aria-labelledby="pl-{p["slug"]}">'
            f'<div class="pl-text"><p class="pl-k">{"Flagship solution" if p["flagship"] else "Solution"}</p>'
            f'<h3 id="pl-{p["slug"]}"><a href="/solutions/{p["slug"]}/">{esc(p["name"])}</a></h3>'
            f'<p class="pl-msg">{esc(p["message"])}</p>'
            '<dl class="fc-dl">'
            f'<div><dt>Enterprise problem</dt><dd>{md(p["problem"])}</dd></div>'
            f'<div class="fc-outcome"><dt>Business outcome</dt><dd>{md(p["outcome"])}</dd></div></dl>'
            f'<p class="pl-apps-h">Applications</p><ul class="pl-apps">{apps}</ul>'
            f'<a class="link-arrow" href="/solutions/{p["slug"]}/">Explore {esc(p["name"].lower())}</a></div>'
            f'<div class="fc-viz">{PILLAR_VIZ[p["slug"]]()}</div></article>')

    p1, p2, p3 = S.PILLARS
    pillars = pillar_panel(p1, "wide") + '<div class="pl-pair">' + pillar_panel(p2, "half") + pillar_panel(p3, "half") + '</div>'

    # Section 3 — flagship business cases (rows, not another card grid)
    rows = "".join(
        f'<li class="fl-row"><div class="fl-t"><p class="fl-p">{esc(S.PILLAR_OF[cid]["name"])}</p>'
        f'<h3><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></h3><p>{md(by[cid]["headline"])}</p></div>'
        f'<div class="fl-po"><p><span class="fl-k">Problem</span>{md(by[cid]["problem_short"])}</p>'
        f'<p class="fl-out"><span class="fl-k">Outcome</span>{md(by[cid]["outcome_short"])}</p></div>'
        f'<div class="fl-a"><a class="link-arrow" href="{case_url(by[cid])}">Business case</a>'
        f'<a class="link-arrow link-muted" href="/pilot/?case={cid}">{esc(by[cid]["cta"])}</a></div></li>'
        for cid in ("BC01", "BC02", "BC03", "BC04"))
    inds = "".join(f'<li><a class="chip" href="/industries/{i["slug"]}/">{esc(i["name"])}</a></li>' for i in industries)

    # Section 5 — workflow with implementation status per step
    flow = [
        ("Data remains in its authorized source environment", "Original data stays where it is, under existing access, retention and operating policies.", "reference"),
        ("GroundTruth AI generates a task-specific optimized dataset", "The distillation runtime builds a compact training dataset for a defined model and task.", "experimental"),
        ("The dataset is evaluated against agreed quality requirements", "Models trained on full and distilled data are compared on the same test set.", "experimental"),
        ("Approved datasets move through existing authorized mechanisms", "Data owners approve; transfer uses the DMZ, gateway or pipeline you already control.", "reference"),
        ("Enterprise analytics and AI training run centrally", "Central teams use the datasets as ordinary training data on their existing platforms.", "customer"),
        ("Downstream performance is validated", "Model performance is checked against the full-data baseline and the agreed tolerance.", "reference"),
    ]
    flow_html = "".join(f'<li><span class="fs-n">{i}</span>{status_badge(k)}<h3>{esc(t)}</h3><p>{esc(d)}</p></li>'
                        for i, (t, d, k) in enumerate(flow, 1))

    # Section 7 — deployment architectures
    deploy = [
        ("Private infrastructure", "Server or VM you control, next to the data domain it serves.", "available"),
        ("On-premises environments", "Plant, data center or OT-side operations zone, operated offline on file exports.", "available"),
        ("Private cloud", "Inside your own cloud account or VPC.", "available"),
        ("Enterprise IT", "Distilled datasets are consumed as ordinary training data by your existing ML and analytics platforms.", "customer"),
        ("Distributed enterprise data environments", "One runtime per domain, coordinated across plants, subsidiaries or regions.", "reference"),
        ("Industrial edge", "Distillation on gateways close to sensors and devices. No specific device validated yet.", "reference"),
        ("OEM integration", "Runtime embedded in a partner's historian, gateway or data platform.", "proposed"),
    ]
    dep_html = "".join(f'<li class="dep"><div class="comp-h"><h3>{esc(n)}</h3>{status_badge(k)}</div><p>{esc(d)}</p></li>' for n, d, k in deploy)

    body = (
        # 1 — hero
        '<section class="hero" aria-labelledby="hero-h"><div class="wrap"><div class="hero-grid"><div class="hero-copy">'
        '<p class="eyebrow">Enterprise AI across distributed and segregated data</p>'
        '<h1 id="hero-h">Keep data distributed. <span class="hl g">Centralize intelligence.</span></h1>'
        '<p class="hero-sub">Train AI models across industrial plants, business units and segregated data environments '
        'without centralizing entire raw datasets.</p>'
        '<p class="lead">Enable enterprise-wide analytics, reduce unnecessary data movement and lower AI training costs '
        'while respecting existing data boundaries.</p>'
        '<div class="cta-row"><a class="btn btn-primary btn-lg" href="/pilot/">Discuss your use case</a>'
        '<a class="btn btn-ghost btn-lg" href="/business-cases/">Explore business cases</a></div>'
        f'</div><div class="hero-art">{hero_visual()}</div></div></div></section>'

        # 2 — three strategic solutions
        '<section class="sec sec-pillars" id="solutions" aria-labelledby="sol-h"><div class="wrap">'
        '<p class="eyebrow">Three strategic solutions</p>'
        '<h2 id="sol-h">One capability, three enterprise problems it solves</h2>'
        f'{pillars}</div></section>'

        # 3 — flagship business cases
        '<section class="sec sec-alt" id="challenges" aria-labelledby="ch-h"><div class="wrap">'
        '<p class="eyebrow">Flagship business cases</p>'
        '<h2 id="ch-h">Solve your most critical data challenges</h2>'
        '<p class="lead">Four enterprise problems where moving less data changes what is possible, not only what it costs.</p>'
        f'<ol class="fl-list">{rows}</ol>'
        '<div class="sec-head sec-foot"><a class="link-arrow" href="/business-cases/">All 11 business cases in the explorer</a>'
        f'<ul class="chips chips-s" aria-label="Business cases by industry">{inds}</ul></div>'
        '</div></section>'

        # 4 — featured enterprise scenario
        '<section class="sec" id="scenario" aria-labelledby="sc-h"><div class="wrap">'
        '<p class="eyebrow">Featured enterprise scenario</p>'
        '<h2 id="sc-h">One predictive-maintenance model, 20 facilities, no central copy of every historian</h2>'
        '<p class="sc-label"><span class="badge badge-illus">Illustrative enterprise scenario</span> Hypothetical; numbers are planning assumptions, not results.</p>'
        '<div class="two-col sc-intro"><div><p class="lead-s">A manufacturing group runs 20 facilities, each with its own authorized OT environment. '
        'Its central AI team wants one predictive-maintenance model trained on data from every facility. Replicating the eligible '
        'history would mean moving about 200 TB into enterprise IT.</p>'
        '<p>With GroundTruth AI, each facility distills a task-specific dataset on site, validates it and sends it, once approved, '
        'through the DMZ path it already uses. Raw historian data never leaves the plant.</p></div>'
        '<dl class="sc-figs">'
        '<div><dt>Eligible training data</dt><dd>200 TB</dd><dd class="sc-sub">20 facilities × 10 TB</dd></div>'
        '<div><dt>Assumed reduction</dt><dd>90%</dd><dd class="sc-sub">planning value, to be validated</dd></div>'
        '<div><dt>Optimized transfer</dt><dd class="g">20 TB</dd><dd class="sc-sub">approved datasets</dd></div>'
        '<div><dt>Potential avoided transfer</dt><dd class="g">180 TB</dd><dd class="sc-sub">raw data stays on site</dd></div></dl></div>'
        + legend() + '<div class="arch-pair">' + arch_figure(SCENARIO_A["current"], "sca-cur", "Before")
        + arch_figure(SCENARIO_A["proposed"], "sca-pro", "After") + '</div>'
        '<p class="note">What must be validated: predictive performance against a full-data baseline, rare-failure coverage in every facility, '
        'cross-site generalization including a facility held out from training, and the compute cost of distillation on site hardware.</p>'
        '<div class="cta-row"><a class="btn btn-primary" href="/simulator/">Try it in the architecture simulator</a>'
        f'<a class="btn btn-ghost" href="{case_url(by["BC01"])}">OT/IT data segregation business case</a></div>'
        '</div></section>'

        # 5 — how the technology works
        + section("how", "How the technology works",
                  '<p class="lead-s">Prepare the data a model needs where the data lives, and move only that, under the controls you already have.</p>'
                  f'<ol class="flow-steps flow-6">{flow_html}</ol>'
                  '<p class="note"><strong>Experimental</strong>: implemented in the prototype used for internal experiments. '
                  '<strong>Reference architecture</strong>: the deployment pattern a pilot implements with your teams. '
                  '<strong>Customer system</strong>: your existing platforms.</p>'
                  '<p><a class="link-arrow" href="/technology/">How dataset distillation works</a></p>',
                  eyebrow="Technology", cls="sec-alt")

        # 6 — technical evidence
        + section("evidence", "Experimental validation and technical evidence",
                  '<div class="two-col ev-home2"><div>'
                  '<div class="ev-pair"><div class="ev-stat"><p class="big g">86–95<span>%</span></p><p>less training data across four public benchmarks</p></div>'
                  '<div class="ev-stat"><p class="big g">≤2.8<span> pp</span></p><p>largest accuracy change versus the full-data model</p></div></div>'
                  '<p class="note">Internal experiments on Iris, Wine and Breast Cancer (tabular, MLP) and MNIST (image, CNN), classification tasks. '
                  'Industrial time-series and multi-domain experiments are on the <a href="/evidence/#roadmap">technical validation roadmap</a>.</p>'
                  '<p><a class="link-arrow" href="/evidence/">Methodology, results and evidence classification</a></p></div>'
                  f'<div class="fc-viz">{viz_bc03(S.BENCHMARKS)}</div></div>',
                  eyebrow="Evidence")

        # 7 — enterprise deployment
        + section("deployment", "Deploys inside the architecture you already run",
                  f'<ul class="dep-list">{dep_html}</ul>'
                  '<p class="note"><strong>Available for pilots</strong>: the prototype runtime can be installed there for an evaluation today. '
                  '<strong>Reference architecture</strong>: designed and documented, implemented with the first customer that needs it. '
                  '<strong>Proposed</strong>: a commercial and technical opportunity, not yet built.</p>'
                  '<p><a class="link-arrow" href="/platform/">What an enterprise customer acquires today</a></p>',
                  eyebrow="Enterprise deployment", cls="sec-alt")

        # 8 — commercial engagement
        + '<section class="sec sec-cta" id="engage" aria-labelledby="cta-h"><div class="wrap">'
        '<p class="eyebrow">Commercial engagement</p><h2 id="cta-h">Start with a conversation about your architecture</h2>'
        '<p class="lead">Begin with a short discovery call. Move to a scoped feasibility assessment, and only then to a pilot, when the case is clear.</p>'
        + engagement_block() + '</div></section>')

    page("/", "GroundTruth AI — Keep data distributed. Centralize intelligence.",
         "Train enterprise AI and run analytics across industrial plants, business units and segregated data environments without centralizing entire raw datasets. Reduce data movement and AI training costs.",
         body, active="", cases=cases, priority="1.0", body_class="pg-home")


# ---------------------------------------------------------------------------- PLATFORM
def render_platform(cases):
    comps = [
        ("Distillation runtime", "experimental",
         "Builds a compact, task-specific training dataset from source data inside the customer environment. Python runtime; tabular and image data exercised in internal experiments. Available for installation in pilot evaluations."),
        ("Fidelity validation", "experimental",
         "Trains the same model on full and distilled data and compares task metrics on the same test set. Uses a scikit-learn-compatible model adapter."),
        ("Coverage and regime checks", "planned",
         "Confirms labeled events, rare classes and operating regimes remain represented. Designed for industrial and multi-domain cases."),
        ("Approval, provenance and export package", "planned",
         "Packages the dataset with its validation report and lineage for review by data owners before transfer."),
        ("Multi-domain coordination", "reference",
         "One runtime per plant, subsidiary or region with a shared task specification. Documented as a reference architecture."),
        ("Edge gateway deployment", "reference",
         "Distillation close to sensors and devices. No specific device has been validated; no real-time execution is claimed."),
        ("Regeneration and drift-triggered refresh", "planned",
         "Re-runs distillation when the task, data distribution or operating conditions change. Drift detection exists as a separate prototype capability."),
    ]
    comp_html = "".join(f'<li class="comp"><div class="comp-h"><h3>{esc(n)}</h3>{status_badge(k)}</div><p>{esc(d)}</p></li>' for n, k, d in comps)

    deploy = [
        ("Source-side server or VM", "available", "Customer hardware in the authorized zone (for example, the OT-side operations zone or a subsidiary data center). Operates on file exports."),
        ("Private cloud or customer VPC", "available", "Runs inside the customer's own cloud account, next to the data domain it serves."),
        ("Workstation", "experimental", "Internal benchmarks and energy measurements were run on workstation-class hardware."),
        ("Edge gateway", "reference", "Distillation close to sensors and devices. No specific device validated."),
        ("Embedded / OEM", "proposed", "Runtime embedded in a partner's appliance, historian or platform. See Partners and OEM."),
    ]
    dep_html = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{status_badge(k)}</td><td>{esc(d)}</td></tr>' for n, k, d in deploy)

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

    acquire = [
        ("What you get in an evaluation", ["The GroundTruth AI distillation runtime (prototype), installed in your environment",
                                           "Fidelity validation reports comparing full-data and distilled-data models",
                                           "A reference architecture for your zone model and transfer paths",
                                           "Direct engineering support from the GroundTruth AI team"]),
        ("Inputs and outputs", ["**In:** source data in its home environment, as files or arrays, plus a task specification",
                                "**Out:** a distilled training dataset in standard formats",
                                "**Out:** a validation report and lineage metadata"]),
        ("Data and models exercised", ["Tabular data with deep learning (MLP) and image data with a CNN, on classification tasks",
                                       "scikit-learn-compatible model adapters",
                                       "Industrial time series, regression and forecasting: on the validation roadmap"]),
        ("Operating requirements", ["CPU-first runtime on a server or VM you provide; sizing set during the evaluation",
                                    "Read access to the data in scope; no inbound connection from GroundTruth AI",
                                    "No customer data is sent to GroundTruth AI"]),
        ("Your responsibilities", ["Data access and approvals by data owners",
                                   "Transfer through your existing DMZ, gateway or pipeline",
                                   "Training on your own ML and analytics platforms"]),
        ("Licensing and support", ["Evaluations are scoped per engagement",
                                   "Production subscription, embedded and OEM licensing are discussed per customer or partner",
                                   "Support terms are defined at production adoption; no prices are published"]),
    ]
    acq_html = "".join(f'<div class="acq"><h3>{esc(t)}</h3>{ul(items)}</div>' for t, items in acquire)

    body = (
        _hero("A distillation layer that runs where your data lives",
              "GroundTruth AI is deployed inside the environment that owns the data. It produces task-specific training datasets, "
              "validates them against the full data, and hands them to the transfer paths and ML platforms you already operate.",
              [("Home", "/"), ("Platform", None)], "Platform",
              button("Discuss your use case", "/pilot/") + button("See the business cases", "/business-cases/", "ghost"))
        + section("acquire", "What an enterprise customer acquires today", f'<div class="acq-grid">{acq_html}</div>')
        + section("components", "Platform components and their status",
                  '<p><strong>Experimental</strong>: implemented and used in internal experiments, available for pilot evaluation. '
                  '<strong>Reference architecture</strong>: designed and documented, implemented with a customer. '
                  '<strong>Planned</strong>: scoped, not yet built.</p>'
                  f'<ul class="comp-list">{comp_html}</ul>', cls="sec-alt")
        + section("deployment", "Deployment options",
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Option</th><th scope="col">Status</th><th scope="col">Description</th></tr></thead><tbody>{dep_html}</tbody></table></div>')
        + section("integrations", "Integration status",
                  '<p>What has been exercised, what is planned and what stays a customer system. Proposed integrations are built with the first customer that needs them.</p>'
                  f'<div class="table-wrap"><table class="tbl tbl-narrow"><thead><tr><th scope="col">Integration</th><th scope="col">Status</th></tr></thead><tbody>{int_html}</tbody></table></div>',
                  cls="sec-alt")
        + section("security", "Security and data governance",
                  '<div class="two-col"><div>' + ul([
                      "**Customer-controlled execution.** The runtime operates inside your environment, under your access controls.",
                      "**No data egress to GroundTruth AI.** Customer data, distilled or raw, is not sent to us.",
                      "**Owner approval before transfer.** Every distilled dataset is reviewed with its validation report before it moves.",
                      "**Least-privilege access.** Read access limited to the variables and period in scope.",
                      "**Lineage.** Each dataset records its source scope, task specification and generation parameters.",
                  ]) + '</div><div class="callout callout-legal"><p class="callout-h">What distillation does not change</p>' + ul([
                      "Distilled data is derived from source data and is classified like it; it may still contain sensitive information.",
                      "It is not anonymization, differential privacy or encryption, and grants no legal authorization for any transfer.",
                      "It does not replace network segmentation, OT security controls, data integration or compliance processes.",
                      "GroundTruth AI holds no security certifications today.",
                  ]) + '</div></div>')
        + section("next", "Evaluate the platform on your architecture",
                  '<p>A feasibility assessment starts with an architecture review: where the runtime would sit, which data it reads, which path the dataset takes and who approves it.</p>'
                  '<div class="cta-row">' + button("Request a feasibility assessment", "/pilot/?type=assessment") + button("Read the technology", "/technology/", "ghost") + '</div>',
                  cls="sec-alt"))
    page("/platform/", "Platform and availability", "What an enterprise customer acquires from GroundTruth AI today: components and their status, deployment options, integration status and data governance.",
         body, active="platform", cases=cases, priority="0.7")


# ---------------------------------------------------------------------------- TECHNOLOGY
def render_technology(cases):
    comp = [
        ("Conventional data centralization", "Complete raw copies move to a central platform", "Central",
         "Maximum flexibility, with the largest transfer, storage, governance and authorization burden.", "Still right for many workloads; distillation targets those where full replication is undesirable or blocked."),
        ("Data compression", "Every byte, encoded smaller", "Source and destination",
         "Must be decompressed to be used; the training volume is unchanged.", "Complementary: distilled datasets can also be compressed."),
        ("Industrial downsampling and aggregation", "Averages or fixed-rate samples over time", "Historian or edge",
         "Task-agnostic; can remove transients and rare states that predictive models need.", "Often already in place; distillation is task-aware."),
        ("Random or stratified sampling", "A fraction of the records", "Source",
         "Simple and cheap; rare classes and unusual regimes can be lost. Stratification helps only for known strata.", "A baseline every pilot compares against."),
        ("Coreset selection", "A weighted subset of real records chosen for an objective", "Source or central",
         "Keeps real records; the subset needed for a given accuracy depends on the task.", "A closely related family; compared against on the validation roadmap."),
        ("Data pruning", "Real records minus those scored as redundant", "Usually central",
         "Typically needs the full dataset in one place to score records.", "Complementary when data is already central."),
        ("Data virtualization", "Queries; data is accessed in place", "Source systems serve queries",
         "Well suited to analytical queries; model training still pulls large volumes across the network.", "Complementary for BI and reporting."),
        ("Federated analytics", "Aggregate statistics computed locally", "Every domain",
         "Strong for metrics and reporting; limited for training complex models.", "Complementary."),
        ("Federated learning", "Model updates, exchanged iteratively; raw data stays", "Training in every domain",
         "Needs training infrastructure in every domain and a sustained model-exchange channel. Can be combined with privacy techniques such as secure aggregation or differential privacy.",
         "An alternative or a complement. GroundTruth AI does not claim equivalent privacy guarantees."),
        ("Synthetic data generation", "Artificial records sampled from a generative model", "Where the generator is trained, often central",
         "Useful for testing and augmentation; fidelity and privacy must be assessed, and the generator is usually trained on the full data.", "A different goal; can be complementary."),
        ("Data clean rooms", "Joint computation under contractual and technical controls", "A controlled shared environment",
         "Designed for multi-party analysis with strict output controls; data is still brought into the clean room.", "Complementary for cross-company analytics."),
        ("Task-aware dataset distillation", "A compact training dataset built for a defined task; only approved datasets move", "Distillation at the source; training central",
         "Fidelity is validated per task, datasets are regenerated when the task changes, and distillation needs compute at the source.", "An intermediate position between full centralization and distributed training."),
    ]
    rows = "".join(f'<tr{" class=\"tr-hl\"" if i == len(comp) - 1 else ""}><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(w)}</td><td>{esc(c)}</td><td>{esc(r)}</td></tr>'
                   for i, (a, b, w, c, r) in enumerate(comp))
    spectrum = [
        ("Centralize all raw data", "Complete raw datasets", "Central", "Storage and governance for every copy", "One-off or continuous bulk replication"),
        ("Source-side distillation", "Approved, task-specific datasets", "Central", "Compute for distillation at each source", "A dataset per task, regenerated when the task changes"),
        ("Federated learning", "Model updates only", "In every domain", "Training infrastructure in every domain", "Iterative, bidirectional model exchange"),
    ]
    sp = "".join(f'<div class="sp sp-{i}"><h3>{esc(n)}</h3><dl>'
                 f'<div><dt>What leaves each domain</dt><dd>{esc(a)}</dd></div><div><dt>Where training runs</dt><dd>{esc(b)}</dd></div>'
                 f'<div><dt>What each domain needs</dt><dd>{esc(c)}</dd></div><div><dt>Exchange pattern</dt><dd>{esc(d)}</dd></div></dl></div>'
                 for i, (n, a, b, c, d) in enumerate(spectrum))
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
                      "**Out:** a validation report comparing full-data and distilled-data models",
                      "**Out:** lineage metadata for governance",
                  ]) + '</div></div>')
        + section("position", "Between centralizing everything and training everywhere",
                  f'<div class="sp-grid">{sp}</div>' + ul([
                      "Original datasets remain distributed; distillation runs inside authorized source environments.",
                      "Only approved, optimized datasets are transferred, and model training can stay centralized.",
                      "Unlike typical federated learning, it does not require iterative exchange of model parameters or training infrastructure in every domain.",
                      "Local distillation still requires compute at each source.",
                      "It does not provide the privacy guarantees of privacy-preserving federated learning, and the approaches are not mutually exclusive.",
                  ]), cls="sec-alt")
        + section("compare", "How it differs from familiar techniques",
                  '<p>Architectural and business trade-offs, not a ranking. Several of these techniques are complementary.</p>'
                  f'<div class="table-wrap"><table class="tbl tbl-cmp"><thead><tr><th scope="col">Technique</th><th scope="col">What moves or is kept</th>'
                  f'<th scope="col">Where computation happens</th><th scope="col">Trade-off</th><th scope="col">Relationship</th></tr></thead><tbody>{rows}</tbody></table></div>')
        + section("pipeline", "The distillation pipeline",
                  '<ol class="flow-steps">'
                  '<li><span class="fs-n">1</span><h3>Task specification</h3><p>Target, features, model family, metric and tolerance.</p></li>'
                  '<li><span class="fs-n">2</span><h3>Profiling</h3><p>Distributions, classes, regimes and labeled events in scope.</p></li>'
                  '<li><span class="fs-n">3</span><h3>Distillation</h3><p>The engine constructs the compact training set for the task.</p></li>'
                  '<li><span class="fs-n">4</span><h3>Fidelity validation</h3><p>Full vs. distilled models compared on the same test data.</p></li>'
                  '<li><span class="fs-n">5</span><h3>Approval and regeneration</h3><p>Owners approve; datasets are regenerated when the task or data change.</p></li></ol>'
                  '<p class="note">Proprietary method details are not published. They are available for technical due diligence under NDA.</p>', cls="sec-alt")
        + section("scope", "Current scope",
                  '<div class="ev-grid">'
                  '<div class="ev ev-yes"><h3>Exercised today</h3>' + ul([
                      "Classification tasks", "Tabular data with deep learning (MLP)", "Image data with a CNN (MNIST)",
                      "Python runtime and scikit-learn-compatible models"]) + '</div>'
                  '<div class="ev ev-gap"><h3>On the validation roadmap</h3>' + ul([
                      "Industrial sensor time series and historian data", "Regression and forecasting tasks",
                      "Distilling separately in several domains and combining the results", "Rare-event and minority-class coverage",
                      "Measured compute and energy of distillation itself"]) + '</div>'
                  '<div class="ev ev-risk"><h3>Known trade-offs</h3>' + ul([
                      "Accuracy can drop (up to −2.8 pp in benchmarks); tolerance is set per task",
                      "A distilled set is task-specific; new tasks need regeneration",
                      "Distillation has its own compute and energy cost"]) + '</div></div>'
                  '<p><a class="link-arrow" href="/evidence/#roadmap">Technical validation roadmap</a></p>')
        + section("adjacent", "The wider engine and adjacent capabilities",
                  '<p>Distillation is part of a multimodal intelligence engine designed to fuse tabular, image, behavioral and time-series signals. '
                  'The same engine supports capabilities that are <strong>prototypes</strong>, not validated on customer data and outside the scope of the business cases on this site:</p>'
                  + ul(["**Data drift detection** — monitoring changes in input distributions and model behavior (proposed as a regeneration trigger for continuous retraining).",
                        "**Anomaly detection** — multimodal anomaly signals, including fraud-style patterns.",
                        "**Behavioral segmentation and recommendation** — earlier product explorations."])
                  + '<p><a class="link-arrow" href="/business-cases/continuous-model-retraining/">See how drift detection relates to continuous retraining</a></p>', cls="sec-alt"))
    page("/technology/", "Enterprise dataset distillation technology",
         "How task-aware, source-side dataset distillation works and how it compares with centralization, compression, sampling, coresets, data virtualization, federated learning, synthetic data and clean rooms.",
         body, active="technology", cases=cases, priority="0.7")


# ---------------------------------------------------------------------------- EVIDENCE
ROADMAP = [
    ("P0", "Multi-domain dataset distillation",
     "Independently distilled datasets from heterogeneous, non-IID domains, trained centrally. Compared with full data, random local samples, stratified local samples and local coresets.",
     "Global and per-domain performance, reduction, transfer volume, source-side and total compute, minority-event preservation, heterogeneity",
     ["BC01", "BC02", "BC04", "BC07", "BC08", "BC11"]),
    ("P0", "Industrial time-series validation",
     "Predictive maintenance, fault detection, anomaly detection and equipment-health workloads.",
     "Temporal information, rare events, operating-regime changes, predictive performance",
     ["BC01", "BC04", "BC05"]),
    ("P0", "Computational cost and economic efficiency",
     "End-to-end cost of distillation and training compared with full-data training.",
     "Distillation time, peak memory, hardware, training time, total compute, break-even point, reuse across repeated training",
     ["BC03", "BC06", "BC09", "BC10"]),
    ("P1", "Cross-facility generalization",
     "Models trained on distilled data from several facilities, evaluated per facility and on facilities not seen in training.",
     "Per-facility performance, degradation on unseen facilities",
     ["BC04", "BC01"]),
    ("P1", "Federated learning comparison",
     "Source-side distillation against federated learning under equivalent objectives and data access assumptions, where methodologically appropriate.",
     "Model quality, communication volume, infrastructure needed per domain, total compute",
     ["BC02", "BC07", "BC04"]),
    ("P1", "Industrial edge deployment",
     "Distillation in resource-constrained source environments.",
     "Throughput, CPU and memory footprint, execution time under industrial constraints",
     ["BC05", "BC01"]),
    ("P2", "Retraining-cycle study",
     "Repeated distillation and retraining under drift.",
     "Quality stability across cycles, cumulative cost including regeneration",
     ["BC09"]),
]


def render_evidence(cases):
    lv = "".join(f'<li class="lvl lvl-{k}"><h3>{esc(n)}</h3><p>{esc(d)}</p><p class="lvl-now"><span>Today:</span> {esc(now)}</p></li>'
                 for k, n, d, now in S.EVIDENCE_LEVELS)
    bm = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{esc(S.BENCHMARK_META[n][0])}</td><td>{esc(t)}</td><td class="num">{r}%</td><td class="num">{b:.1f}%</td>'
                 f'<td class="num">{d:.1f}%</td><td class="num">{delta:+.1f} pp</td></tr>' for n, t, r, b, d, delta in S.BENCHMARKS)
    per = []
    for p in S.PILLARS:
        for cid in p["cases"]:
            c = next(x for x in cases if x["id"] == cid)
            lvl, note = SUPPORT.get(cid, DEFAULT_SUPPORT)
            per.append(f'<tr><th scope="row"><a href="{case_url(c)}#evidence">{esc(c["title"])}</a></th><td>{esc(p["name"])}</td>'
                       f'<td><span class="sup sup-{lvl.lower()}">{lvl}</span></td><td>{esc(note)}</td></tr>')
    rm = "".join(f'<tr><td><span class="prio prio-{pr.lower()}">{pr}</span></td><th scope="row">{esc(n)}</th><td>{esc(d)}</td><td>{esc(m)}</td>'
                 f'<td>{esc(_names(cases, ids))}</td><td>Planned</td></tr>' for pr, n, d, m, ids in ROADMAP)
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
    scope = [
        ("Dataset-level experimental results", "Measured", "Data reduction and accuracy on four public classification benchmarks; internal energy measurements.", "experimental"),
        ("Industrial application hypotheses", "To be tested", "Industrial time series, rare failures and operating regimes: designed into the OT/IT and multi-site pilots.", "proposed"),
        ("Multi-domain architecture proposals", "To be tested", "Distilling separately in several domains and training centrally: the P0 experiment on the roadmap.", "proposed"),
        ("Validated customer outcomes", "Reported when available", "Results from enterprise pilots will be published here, with the customer's permission.", "demonstrated"),
    ]
    sc_html = "".join(f'<li class="lvl lvl-{k}"><h3>{esc(n)}</h3><p class="lvl-now"><span>Status:</span> {esc(s)}</p><p>{esc(d)}</p></li>' for n, s, d, k in scope)
    body = (
        _hero("Experimental validation and technical evidence",
              "Every statement on this site is classified by the evidence behind it. This page shows the experimental results, how to read them, "
              "and the validation roadmap that pilots are designed to complete.",
              [("Home", "/"), ("Evidence", None)], "Evidence",
              button("Discuss your use case", "/pilot/") + button("ROI calculator", "/roi/", "ghost"))
        + section("levels", "How we classify evidence", f'<ul class="lvl-list">{lv}</ul>')
        + section("scope-ev", "What the evidence covers", f'<ul class="lvl-list">{sc_html}</ul>'
                  '<p class="note">Results on small public datasets are not extrapolated to industrial-scale deployments, and independently distilled datasets '
                  'are not assumed to combine successfully without validation.</p>', cls="sec-alt")
        + section("benchmarks", "Experimentally supported technical outcomes",
                  '<p>Internal experiments on public benchmark datasets. Accuracy compares models trained on the full training data and on the distilled training data, '
                  'evaluated on the same test data.</p>'
                  '<div class="table-wrap"><table class="tbl"><caption class="sr-only">Benchmark results</caption><thead><tr><th scope="col">Dataset</th><th scope="col">Public dataset</th>'
                  '<th scope="col">Model</th><th scope="col" class="num">Data reduction</th><th scope="col" class="num">Full-data accuracy</th><th scope="col" class="num">Distilled accuracy</th>'
                  f'<th scope="col" class="num">Change</th></tr></thead><tbody>{bm}</tbody></table></div>'
                  '<div class="two-col"><div><h3 class="h-s">Methodology and reporting</h3>' + ul([
                      "Classification tasks; the same model architecture is trained on full and distilled data.",
                      "Data reduction is the share of training records removed by distillation.",
                      "Absolute distilled-set sizes, distillation runtime, peak memory and compute cost are not yet published; they are part of the P0 cost study.",
                      "Hardware: workstation-class machines.",
                      "Not yet independently replicated.",
                  ]) + '<h3 class="h-s">Energy measurements</h3>' + ul([
                      "**86%** less energy per model training run on a workstation after data reduction.",
                      "**39%** less energy on IoT / edge devices at the point of capture.",
                      "Internal measurements; energy estimated with Schneider Electric reference data. Methodology not yet published.",
                      "The figures do not separately report the energy consumed by the distillation step; pilots measure it explicitly.",
                  ]) + f'</div><div><div class="fc-viz">{viz_bc03(S.BENCHMARKS)}</div><h3 class="h-s">Limitations</h3>' + ul([
                      "Small, clean, public datasets; classification only.",
                      "Results do not transfer automatically to industrial time series, logs or multi-domain data.",
                      "No enterprise production deployment has been measured yet.",
                  ]) + '</div></div>')
        + section("by-case", "Evidence by business case",
                  '<p><strong>Direct</strong>: the experiments measure the outcome the case depends on. <strong>Partial</strong>: related measurements exist. '
                  '<strong>Indirect</strong>: the case relies on an architectural hypothesis that has not yet been benchmarked.</p>'
                  '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Business case</th><th scope="col">Solution family</th>'
                  f'<th scope="col">Technical support</th><th scope="col">Notes</th></tr></thead><tbody>{"".join(per)}</tbody></table></div>', cls="sec-alt")
        + section("roadmap", "Technical validation roadmap",
                  '<p>Prioritized by commercial relevance. These are planned experiments, not completed work; no dates are published. '
                  'Enterprise pilots are designed to generate this evidence on customer data, with measurements the customer keeps.</p>'
                  '<div class="table-wrap"><table class="tbl tbl-rm"><thead><tr><th scope="col">Priority</th><th scope="col">Experiment</th><th scope="col">Design</th>'
                  f'<th scope="col">Measures</th><th scope="col">Supports</th><th scope="col">Status</th></tr></thead><tbody>{rm}</tbody></table></div>')
        + section("context", "Market context (third-party sources)",
                  '<p>Context for why data volume matters. These figures describe the market, not GroundTruth AI results.</p>'
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Finding</th><th scope="col">Source</th></tr></thead><tbody>{ctx_html}</tbody></table></div>',
                  cls="sec-alt"))
    page("/evidence/", "Evidence and validation roadmap", "GroundTruth AI experimental results on public benchmarks, methodology and limitations, evidence by business case and the prioritized technical validation roadmap.",
         body, active="evidence", cases=cases, priority="0.8")


# ---------------------------------------------------------------------------- ROI
def _num(id_, label, value, unit="", step="any", hint="", cls="", mx=None):
    h = f'<span class="hint" id="{id_}-h">{esc(hint)}</span>' if hint else ""
    d = f' aria-describedby="{id_}-h"' if hint else ""
    m = f' max="{mx}"' if mx is not None else ""
    return (f'<div class="fld {cls}"><label for="{id_}">{esc(label)}</label>'
            f'<div class="inp"><input type="number" id="{id_}" name="{id_}" value="{value}" min="0"{m} step="{step}" inputmode="decimal"{d}>'
            f'{f"<span class=unit>{esc(unit)}</span>" if unit else ""}</div>{h}</div>')


def render_roi(cases):
    opts = "".join(f'<option value="{c["id"]}" data-preset="{S.CASE_PRESET[c["id"]]}">{esc(c["title"])}</option>' for c in cases)
    presets = "".join(f'<option value="{k}" data-model="{m}" data-domain="{esc(d)}">{esc(lbl)}</option>' for k, lbl, m, d in S.ROI_PRESETS)
    strat = {c["id"]: c["outcomes"]["strategic"] for c in cases}
    strat_html = "".join(f'<ul class="strat-list" data-case="{cid}" hidden>' + "".join(
        f'<li><label><input type="checkbox"> {md(s)}</label></li>' for s in items) + "</ul>" for cid, items in strat.items())

    transfer = (
        '<fieldset class="scen" data-scen="transfer"><legend>Data movement & replication</legend><div class="fld-grid">'
        + _num("t_dom", "Plants or OT zones", 4, "", "1")
        + _num("t_vol", "Raw data moved per domain per month", 20, "TB")
        + _num("t_elig", "Share moved only to feed model training", 50, "%", hint="Only this eligible share is affected.", mx=100)
        + _num("t_ctr", "Data transfer cost", 20, "per TB", hint="Egress, WAN or gateway cost. Use your contract rates.")
        + _num("t_cing", "Central ingestion cost", 10, "per TB", hint="Pipelines and landing-zone processing on arrival.")
        + _num("t_cproc", "Central processing cost", 20, "per TB", hint="Data preparation before training.")
        + _num("t_cst", "Central storage cost incl. replicas", 25, "per TB·month", hint="Central training copies only. Source data is retained.")
        + _num("t_ret", "Average retention of central training copies", 12, "months", "1")
        + _num("t_over", "Source-side distillation compute", 5, "per TB distilled", hint="Compute and operations at the source. Measured in a pilot.")
        + '</div></fieldset>')
    training = (
        '<fieldset class="scen" data-scen="training" hidden><legend>Training & retraining spend</legend><div class="fld-grid">'
        + _num("r_spend", "Annual training and retraining compute spend", 400000, "per year")
        + _num("r_share", "Share of that spend that scales with data volume", 60, "%", hint="Fixed costs (reserved capacity, tooling) are not reduced.", mx=100)
        + _num("r_runs", "Distillation runs per year", 12, "", "1", hint="One per retraining cycle, or fewer if datasets are reused.")
        + _num("r_rcost", "Compute cost per distillation run", 1500, "per run")
        + _num("r_kwh", "Annual training energy (optional)", 0, "kWh", hint="Informational: energy cost is already inside compute spend.")
        + _num("r_dkwh", "Energy per distillation run (optional)", 0, "kWh")
        + _num("r_price", "Electricity price", 0.15, "per kWh")
        + _num("r_hours", "Training wall-clock hours per year (optional)", 0, "hours")
        + '</div></fieldset>')
    infra = (
        '<fieldset class="scen" data-scen="infrastructure" hidden><legend>Storage, compute & energy</legend><div class="fld-grid">'
        + _num("i_tb", "Eligible stored training copies", 500, "TB", hint="Central training copies that a distilled version could replace. Source data is retained.")
        + _num("i_cst", "Storage cost incl. backup and replicas", 25, "per TB·month")
        + _num("i_comp", "Eligible annual processing and training compute", 300000, "per year")
        + _num("i_share", "Share of compute that scales with data", 60, "%", mx=100)
        + _num("i_kwh", "Eligible annual energy not included in compute", 0, "kWh", hint="Only energy not already paid inside the compute spend above.")
        + _num("i_price", "Electricity price", 0.15, "per kWh")
        + _num("i_ocost", "Annual distillation compute cost", 20000, "per year")
        + _num("i_okwh", "Annual distillation energy", 0, "kWh")
        + _num("i_grid", "Grid emission factor (optional)", 0, "kg CO₂e/kWh", hint="Location-based. Operational emissions only; not a lifecycle assessment.")
        + '</div></fieldset>')
    common = (
        '<fieldset class="scen-common"><legend>Assumptions that apply to every scenario</legend><div class="fld-grid">'
        + _num("c_red", "Assumed data reduction on eligible data", 70, "%", hint="Benchmarks: 86–95% on public datasets. Your workload must be measured.", mx=99)
        + _num("c_val", "Annual validation and dataset maintenance", 15000, "per year", hint="Fidelity checks, regeneration and approvals.")
        + _num("c_sol", "GroundTruth AI annual license", 0, "per year", hint="Enter a quoted figure. Pricing is not published.")
        + _num("c_impl", "One-time implementation cost", 0, "one-time")
        + _num("c_hrs", "Team hours on data preparation and transfer per year (optional)", 0, "hours")
        + _num("c_hsave", "Share of those hours avoidable (optional)", 0, "%", mx=100)
        + _num("c_rate", "Loaded hourly cost (optional)", 0, "per hour")
        + '</div></fieldset>')

    body = (
        _hero("Estimate the value for your business case",
              "An illustrative financial scenario built only on assumptions you enter. Savings apply only to eligible, data-proportional cost lines; "
              "distillation, validation, licensing and implementation are deducted; strategic enablement is listed, never priced.",
              [("Home", "/"), ("Business cases", "/business-cases/"), ("ROI calculator", None)], "ROI calculator")
        + '<section class="sec sec-tight" aria-labelledby="roi-h"><div class="wrap">'
        '<h2 id="roi-h" class="sr-only">Calculator</h2>'
        '<noscript><div class="callout"><p>The calculator needs JavaScript. The method: savings = eligible volume or spend × assumed reduction × unit cost, minus distillation, '
        'validation, license and implementation costs. Strategic value is listed, never priced.</p></div></noscript>'
        '<form class="roi" id="roi" hidden><div class="roi-in">'
        '<div class="fld-row"><div class="fld"><label for="roi-case">Business case</label>'
        f'<select id="roi-case"><option value="">Choose a business case (optional)</option>{opts}</select></div>'
        f'<div class="fld"><label for="roi-scen">Commercial scenario</label><select id="roi-scen">{presets}</select></div>'
        '<div class="fld fld-s"><label for="roi-cur">Currency</label><select id="roi-cur"><option value="$">USD $</option><option value="€">EUR €</option><option value="£">GBP £</option></select></div></div>'
        + transfer + training + infra + common
        + '<p class="note">Defaults are placeholders for illustration only, not benchmarks, quotes or forecasts. Replace them with your own figures.</p>'
        '<p class="form-err" id="roi-err" role="alert" hidden></p>'
        '</div><div class="roi-out" aria-live="polite">'
        '<div class="out-card out-main"><p class="out-k">Net annual direct value</p><p class="out-big" id="o-net">—</p>'
        '<p class="out-s" id="o-net-s"></p></div>'
        '<div class="out-card"><p class="out-k">1 · Direct financial savings</p><ul class="out-lines" id="o-lines"></ul></div>'
        '<div class="out-card"><p class="out-k">2 · Operational efficiency</p><ul class="out-lines" id="o-ops"></ul></div>'
        '<div class="out-card"><p class="out-k">Energy and emissions</p><ul class="out-lines" id="o-energy"></ul></div>'
        '<div class="out-card out-strat"><p class="out-k">3 · Strategic business enablement · not priced</p>'
        '<p class="small" id="o-strat-empty">Choose a business case to list its strategic outcomes. Tick those that matter to you; they are not converted into money.</p>'
        f'{strat_html}</div>'
        '<div class="cta-row"><button class="btn btn-ghost btn-sm js-print" type="button" hidden>Print scenario</button>'
        '<button class="btn btn-ghost btn-sm" type="button" id="o-copy" hidden>Copy summary</button>'
        '<a class="btn btn-primary btn-sm" id="o-pilot" href="/pilot/?type=assessment">Validate these assumptions</a></div>'
        '<p class="small" id="o-copy-s" role="status"></p>'
        '</div></form></div></section>'
        + section("method", "Method and limits",
                  ul([
                      "Only the **eligible, data-proportional share** of each cost line is reduced. A reduction in dataset records is not an equivalent reduction in total infrastructure spend.",
                      "Transfer, ingestion, processing, storage, training compute and energy are separate lines; energy already paid inside compute spend is not counted again.",
                      "**Distillation compute**, **validation and dataset maintenance**, the **license** and **implementation** are deducted from gross savings.",
                      "Original source data is assumed to be **retained**; only central training copies are affected.",
                      "Energy results are operational estimates. Environmental claims require lifecycle measurement.",
                      "Operational efficiency is only computed from hours you enter; strategic enablement is never priced.",
                      "All calculation happens in your browser. Nothing you enter is sent anywhere.",
                  ]) + '<p><a class="link-arrow" href="/simulator/">Prefer to start from the architecture? Use the simulator</a></p>', cls="sec-alt"))
    page("/roi/", "ROI calculator", "Estimate the direct, operational and strategic value of dataset distillation for a business case with your own assumptions, net of distillation, validation, license and implementation costs.",
         body, active="business-cases", cases=cases, priority="0.8", extra_js=("/assets/js/roi.js",))


# ---------------------------------------------------------------------------- SIMULATOR
def render_simulator(cases):
    fields = (
        _num("s_n", "Industrial facilities or data domains", 20, "", "1", hint="1 to 200.", mx=200)
        + _num("s_vol", "Eligible training data per domain", 10, "TB", hint="Data a central model would need, per training cycle.", mx=100000)
        + _num("s_tx", "Share of that data transferred centrally today", 100, "%", hint="Baseline: what a conventional architecture would move.", mx=100)
        + _num("s_el", "Share of transferred data eligible for distillation", 100, "%", hint="Data used only for model training.", mx=100)
        + _num("s_red", "Assumed dataset reduction", 90, "%", hint="Illustrative. Must be validated per workload.", mx=99)
        + _num("s_ctr", "Transfer cost (optional)", 0, "per TB")
        + _num("s_cproc", "Central ingestion and processing cost (optional)", 0, "per TB"))
    body = (
        _hero("Distributed intelligence simulator",
              "See how source-side distillation changes what crosses your authorized boundaries when central teams train AI on data from many plants, "
              "subsidiaries or regions. Adjust the assumptions; the architecture updates as you type.",
              [("Home", "/"), ("Business cases", "/business-cases/"), ("Architecture simulator", None)], "Illustrative architecture simulator")
        + '<section class="sec sec-tight" aria-labelledby="sim-h"><div class="wrap">'
        '<h2 id="sim-h" class="sr-only">Simulator</h2>'
        '<noscript><div class="callout"><p>The simulator needs JavaScript. The method: baseline transfer = domains × eligible data × share transferred; '
        'optimized transfer = baseline × (1 − eligible share × reduction); avoided transfer = baseline − optimized.</p></div></noscript>'
        '<form class="sim" id="sim" hidden>'
        '<div class="sim-in"><fieldset><legend>Assumptions</legend>'
        '<div class="cta-row cta-row-s sim-presets"><button class="btn btn-ghost btn-sm" type="button" data-preset="manufacturing">Manufacturing preset: 20 facilities × 10 TB, 90%</button></div>'
        f'<div class="fld-grid">{fields}</div></fieldset>'
        '<p class="form-err" id="sim-err" role="alert" hidden></p></div>'
        '<div class="sim-out">'
        '<figure class="sim-fig"><figcaption><span class="badge badge-illus">Illustrative architecture simulator</span></figcaption>'
        '<div class="sim-svg" id="sim-svg"></div>'
        '<ul class="arch-legend sim-legend"><li><span class="lg-line lg-raw" aria-hidden="true"></span>Raw data (baseline)</li>'
        '<li><span class="lg-line lg-distilled" aria-hidden="true"></span>Optimized dataset</li>'
        '<li><span class="lg-node" aria-hidden="true"></span>GroundTruth AI component</li><li><span class="lg-bound" aria-hidden="true"></span>Authorized transfer boundary</li></ul></figure>'
        '<dl class="sim-kpis" aria-live="polite">'
        '<div><dt>Original eligible data</dt><dd id="k-orig">—</dd><dd class="sc-sub">retained at source in both architectures</dd></div>'
        '<div><dt>Baseline transfer</dt><dd id="k-base">—</dd><dd class="sc-sub">conventional centralization</dd></div>'
        '<div><dt>Estimated optimized transfer</dt><dd id="k-opt" class="g">—</dd><dd class="sc-sub" id="k-opt-s"></dd></div>'
        '<div><dt>Potential avoided data movement</dt><dd id="k-avoid" class="g">—</dd><dd class="sc-sub" id="k-rel"></dd></div>'
        '<div class="sim-money" id="k-money-w" hidden><dt>Illustrative gross saving</dt><dd id="k-money">—</dd><dd class="sc-sub">per training cycle, before distillation, validation and license costs</dd></div>'
        '</dl></div></form>'
        '<div class="callout callout-limit sim-qual"><p class="callout-h">Read this before using the numbers</p>' + ul([
            "The dataset reduction is an assumption. The achievable reduction and the downstream model performance must be validated for each workload.",
            "Data retained at source stays subject to your normal retention policies; nothing here implies it is unaffected by them or that it is deleted.",
            "A reduced dataset is not automatically authorized for transfer. Data owners, security and legal functions decide.",
            "Distillation itself needs compute at each source. Use the ROI calculator for a net financial view.",
        ]) + '</div>'
        '<div class="cta-band sim-cta"><div><h2 class="h-m">Evaluate this architecture using your own data environments.</h2>'
        '<p>A feasibility assessment tests one representative workload: real reduction, model quality, transfer volumes and cost.</p></div>'
        '<div class="cta-stack"><a class="btn btn-primary btn-lg" href="/pilot/?type=assessment">Request a feasibility assessment</a>'
        '<a class="btn btn-ghost" href="/roi/">Build a net financial view</a></div></div>'
        '</div></section>')
    page("/simulator/", "Distributed intelligence simulator",
         "Illustrative architecture simulator: see how source-side dataset distillation changes data movement when training enterprise AI across many facilities or data domains.",
         body, active="business-cases", cases=cases, priority="0.8", extra_js=("/assets/js/simulator.js",))


# ---------------------------------------------------------------------------- PARTNERS
def render_partners(cases):
    targets = ["Industrial automation platforms", "Industrial historians", "OT/IT integration platforms", "Industrial gateways",
               "Edge computing platforms", "Enterprise data integration products", "Cloud infrastructure platforms", "MLOps platforms",
               "AI development infrastructure"]
    models = [
        ("Embedded software licensing", "The runtime ships inside your product and runs where your product already runs."),
        ("OEM licensing", "Source-side distillation offered under your brand as a feature or module of your platform."),
        ("Technology licensing", "Access to the method for a defined field of use, under NDA and license terms."),
        ("Joint technical validation", "A shared experiment plan on your target data before any co-marketing claim."),
        ("Joint enterprise solutions", "A combined offer for a business case such as OT/IT data segregation or edge-to-cloud."),
        ("Distribution partnerships", "Systems integrators and resellers delivering assessments, pilots and rollouts."),
    ]
    m_html = "".join(f'<li class="pm"><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for n, d in models)
    status = [("Python runtime for evaluation", "available"), ("Packaging for embedding (container, library, SDK)", "planned"),
              ("Integration with any specific third-party product", "proposed"), ("Joint validation on partner data", "proposed")]
    st_html = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{status_badge(k)}</td></tr>' for n, k in status)
    body = (
        _hero("Embed source-side distillation in your product",
              "GroundTruth AI is a software component designed to sit inside other architectures. For platforms that already run next to "
              "industrial, edge or enterprise data, it adds a differentiated capability: task-specific training datasets produced at the source.",
              [("Home", "/"), ("Partners and OEM", None)], "Partners and OEM",
              button("Discuss a technology integration", "/pilot/?type=partnership"))
        + section("why", "Why it adds value to an existing product",
                  '<div class="two-col"><div>' + ul([
                      "Your customers want central AI on data your product already holds or moves, without replicating all of it.",
                      "Source-side distillation turns that data into approved, task-specific training datasets inside your product's footprint.",
                      "It complements, rather than replaces, automation, historians, data integration and security infrastructure.",
                      "It creates a new reason to keep data processing in your platform rather than exporting raw data elsewhere.",
                  ]) + '</div><div class="side-card"><p class="side-h">Where it can be embedded</p>' + ul(targets) + '</div></div>')
        + section("pattern", "Where GroundTruth AI sits inside a partner product",
                  legend() + arch_figure(OEM_EMBED, "oem", "Proposed")
                  + '<p class="note">A proposed integration pattern, not an existing integration. Compatibility with a partner product is claimed only after it has been built and tested together.</p>',
                  cls="sec-alt")
        + section("status", "What exists and what is proposed",
                  f'<div class="table-wrap"><table class="tbl tbl-narrow"><thead><tr><th scope="col">Capability</th><th scope="col">Status</th></tr></thead><tbody>{st_html}</tbody></table></div>'
                  '<p class="note">The partnership models below describe what we are seeking; no partnerships have been announced.</p>')
        + section("models", "Commercial models", f'<ul class="pm-grid">{m_html}</ul>'
                  '<p class="note">Licensing terms are discussed per partnership; no prices are published.</p>', cls="sec-alt")
        + section("start", "Discuss a technology integration",
                  '<p>Tell us where your product sits in your customers\' architecture and which business case they face. We will propose a joint validation plan.</p>'
                  '<div class="cta-row">' + button("Discuss a technology integration", "/pilot/?type=partnership") + button("Review the business cases", "/business-cases/", "ghost") + '</div>'))
    page("/partners/", "Partners and OEM licensing", "Embed source-side dataset distillation in industrial platforms, historians, gateways, edge, data integration, cloud and MLOps products: OEM, embedded and technology licensing.",
         body, active="partners", cases=cases, priority="0.7")


# ---------------------------------------------------------------------------- COMPANY
def render_company(cases):
    pil = "".join(f'<li><a href="/solutions/{p["slug"]}/"><strong>{esc(p["name"])}</strong></a> — {esc(p["message"])}</li>' for p in S.PILLARS)
    body = (
        _hero("Keep data distributed. Centralize intelligence.",
              "GroundTruth AI enables enterprise intelligence across distributed and segregated data environments while reducing unnecessary data movement "
              "and optimizing AI infrastructure efficiency.",
              [("Home", "/"), ("Company", None)], "Company",
              button("Discuss your use case", "/pilot/"))
        + section("why", "Why we exist",
                  '<p class="lead-s">Enterprise data is distributed for good reasons: safety, ownership, regulation, cost. The default AI workflow ignores those reasons and asks for everything in one place. '
                  'We think the better answer is to move less, and to move only what a model actually needs.</p>'
                  f'<ul class="plain">{pil}</ul>')
        + section("stage", "Where we are",
                  '<div class="two-col"><div>' + ul([
                      "Technology validated in internal experiments on public benchmarks.",
                      "A prototype runtime available for evaluation in customer environments.",
                      "An enterprise pilot program open to organizations with a concrete distributed-data problem.",
                      "Production deployments, customer references and certifications will be published here once they exist.",
                  ]) + '</div><div class="side-card"><p class="side-h">Expertise</p><p>Founded by applied machine-learning researchers with backgrounds in data-efficient learning, '
                  'decision systems and industrial and enterprise AI.</p><p class="small">Technical due diligence, including method details under NDA, is available on request.</p></div></div>', cls="sec-alt")
        + section("principles", "How we work",
                  '<div class="tension-grid">'
                  '<div class="tension"><h3>Evidence before claims</h3><p>Every statement is labeled as demonstrated, experimental, for pilot evaluation or illustrative.</p></div>'
                  '<div class="tension"><h3>Your data, your environment</h3><p>Evaluations run inside your environment. Your data is not sent to us.</p></div>'
                  '<div class="tension"><h3>Your thresholds</h3><p>You define acceptable model performance and economic targets before a pilot starts.</p></div></div>')
        + section("contact", "Contact",
                  '<p>For use-case discussions, feasibility assessments, pilots, technology integrations and technical due diligence, use the request form. We reply with a proposal for a short call.</p>'
                  '<div class="cta-row">' + button("Discuss your use case", "/pilot/") + button("Discuss a technology integration", "/pilot/?type=partnership", "ghost") + '</div>', cls="sec-alt"))
    page("/company/", "Company", "About GroundTruth AI: mission, solution families, current stage, principles and how to get in touch.", body, active="company", cases=cases, priority="0.5")


# ---------------------------------------------------------------------------- ENGAGEMENT FORM (/pilot/)
REQUEST_TYPES = [("discovery", "Architecture discovery: discuss your use case"), ("assessment", "Technical feasibility assessment"),
                 ("pilot", "Enterprise pilot"), ("partnership", "Technology integration or OEM partnership"),
                 ("diligence", "Technical due diligence")]


def render_pilot(cases, industries):
    case_opts = "".join(f'<option value="{c["id"]}" data-cta="{esc(c["cta"])}">{esc(c["title"])}</option>' for c in cases)
    ind_opts = "".join(f'<option value="{i["slug"]}">{esc(i["name"])}</option>' for i in industries)
    type_opts = "".join(f'<option value="{k}">{esc(v)}</option>' for k, v in REQUEST_TYPES)
    stages = "".join(f'<li class="eng eng-{key}"><p class="eng-n">Stage {i}</p><h3>{esc(name)}</h3><p>{esc(desc)}</p>'
                     f'<a class="link-arrow" href="/pilot/?type={key}#request">{esc(cta)}</a></li>'
                     for i, (key, name, cta, desc, _p) in enumerate(S.ENGAGEMENT, 1))
    body = (
        _hero("Discuss your use case",
              "Start with a short conversation about your architecture. Move to a feasibility assessment and an enterprise pilot only when the case is clear.",
              [("Home", "/"), ("Discuss your use case", None)], "Commercial engagement")
        + section("stages", "Three steps, each with a clear decision",
                  f'<ol class="eng-list">{stages}</ol>'
                  '<p class="note">Pilots run in your environment, against your baseline, with success criteria you set before they start. Pricing is scoped per engagement and not published.</p>')
        + '<section class="sec sec-alt" id="request" aria-labelledby="form-h"><div class="wrap two-col two-col-form">'
        '<div><h2 id="form-h">Tell us about your situation</h2>'
        '<p>We reply with a proposal for a short call. If distillation is not a good fit, we will say so.</p>'
        + ul(["Which data, where it lives, and why it cannot simply be centralized", "The model or analytics you want to build", "The baseline you would compare against"])
        + '<p class="small"><strong>No proprietary data needed.</strong> Please do not include confidential data, files or credentials in this form.</p>'
        '<div class="privacy" id="privacy"><h3 class="h-s">Privacy</h3>'
        '<p class="small">We collect the details you enter here only to reply to your request and to prepare the conversation. Your request is delivered by email to the '
        'GroundTruth AI team through <a href="https://formsubmit.co/" rel="noopener">FormSubmit</a>, a third-party form delivery service, which processes it to deliver it. '
        'To ask for access to or deletion of your details, reply to our email. '
        'No cookies or analytics are used on this site. If online delivery fails, the page offers to open your own email client instead.</p></div></div>'
        '<noscript><p class="callout">The request form needs JavaScript. Please contact your GroundTruth AI representative directly.</p></noscript>'
        f'<form class="pilot-form" id="pilot-form" novalidate data-to="{esc(S.CONTACT_EMAIL)}" data-endpoint="{esc(S.FORM_ENDPOINT)}">'
        '<div class="hp" aria-hidden="true"><label for="p-hp">Leave this field empty</label><input id="p-hp" name="_honey" tabindex="-1" autocomplete="off"></div>'
        f'<div class="fld"><label for="p-type">What would you like to do?</label><select id="p-type" name="type">{type_opts}</select></div>'
        f'<div class="fld-2"><div class="fld"><label for="p-case">Business case</label><select id="p-case" name="case"><option value="">Not sure yet</option>{case_opts}</select></div>'
        f'<div class="fld"><label for="p-ind">Industry</label><select id="p-ind" name="industry"><option value="">Select</option>{ind_opts}</select></div></div>'
        '<div class="fld-2"><div class="fld"><label for="p-name">Name <span class="req">(required)</span></label><input id="p-name" name="name" autocomplete="name" required></div>'
        '<div class="fld"><label for="p-email">Work email <span class="req">(required)</span></label><input id="p-email" name="email" type="email" autocomplete="email" required></div></div>'
        '<div class="fld-2"><div class="fld"><label for="p-org">Organization <span class="req">(required)</span></label><input id="p-org" name="org" autocomplete="organization" required></div>'
        '<div class="fld"><label for="p-role">Role</label><input id="p-role" name="role" autocomplete="organization-title"></div></div>'
        '<div class="fld"><label for="p-env">Your data environment and constraint (optional)</label><textarea id="p-env" name="env" rows="4" maxlength="3000" '
        'placeholder="For example: historian data in 6 plants behind an industrial DMZ; central ML team on Azure; transfer policy limits raw replication."></textarea></div>'
        '<div class="fld"><label for="p-time">Timeline</label><select id="p-time" name="timeline"><option value="">Select</option>'
        '<option>Exploring</option><option>Within 3 months</option><option>3–6 months</option><option>Budgeted this year</option></select></div>'
        '<div class="fld fld-check"><label><input type="checkbox" id="p-consent" name="consent" required> I agree that GroundTruth AI may use these details to respond to this request, and that they are transmitted by email through FormSubmit. <span class="req">(required)</span></label></div>'
        '<p class="form-err" id="p-err" role="alert" hidden></p>'
        '<p class="form-status" id="p-status" role="status" aria-live="polite"></p>'
        '<button class="btn btn-primary" type="submit" id="p-submit">Discuss your use case</button>'
        '<div class="form-out" id="p-out" hidden><p class="callout-h" id="p-out-h" tabindex="-1">Your request</p>'
        '<p id="p-out-msg"></p><label for="p-text" class="sr-only">Prepared request</label><textarea id="p-text" rows="10" readonly></textarea>'
        '<button class="btn btn-ghost btn-sm" type="button" id="p-copy">Copy request</button></div>'
        '</form></div></section>')
    page("/pilot/", "Discuss your use case", "Start a conversation with GroundTruth AI: architecture discovery, a technical feasibility assessment or an enterprise pilot on one workload in your environment.",
         body, active="", cases=cases, priority="0.9", extra_js=("/assets/js/pilot.js",), connect=S.FORM_ORIGIN)


def render_404(cases):
    body = (_hero("Page not found", "The page you were looking for has moved or does not exist.",
                  [("Home", "/"), ("Not found", None)], "404",
                  button("Business cases", "/business-cases/") + button("Home", "/", "ghost")))
    # 404 is served at any path by GitHub Pages: absolute URLs keep it working.
    page("/404.html", "Page not found", "Page not found.", body, cases=cases, priority=None)


LEGACY = {
    "distillation.html": "/technology/",
    "data-drift.html": "/technology/#adjacent",
    "data_drift.html": "/technology/#adjacent",
    "anomaly_detection.html": "/technology/#adjacent",
    "efficient_data_size_reduction.html": "/technology/",
    "customer-segmentation.html": "/technology/#adjacent",
    "recommender-systems.html": "/technology/#adjacent",
    "fraud-detection.html": "/technology/#adjacent",
    "iris.html": "/evidence/#benchmarks",
    "wine.html": "/evidence/#benchmarks",
    "breast.html": "/evidence/#benchmarks",
    "mnist.html": "/evidence/#benchmarks",
    "portfolio-details.html": "/",
    "service-details.html": "/",
    "starter-page.html": "/",
    # Retired Smart Data Savings briefing deck (claims superseded; original kept in internal/legacy/)
    "resources/smart-data-savings/index.html": "/evidence/",
}


def render_legacy():
    for old, new in LEGACY.items():
        write("/" + old, (
            '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={new}"><link rel="canonical" href="{S.BASE_URL}{new}">'
            '<meta name="robots" content="noindex"><title>Moved · GroundTruth AI</title></head>'
            f'<body><p>This page has moved to <a href="{new}">{S.BASE_URL}{new}</a>.</p></body></html>\n'))
