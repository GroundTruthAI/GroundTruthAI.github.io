"""Home, Platform, Technology, Evidence, ROI, Simulator, Partners, Company, Engagement form and 404 pages."""
from content import site as S
from .core import esc, md, ul, page, breadcrumb, button, badge, section, write
from .diagrams import (hero_visual, viz_bc03, viz_pillar_distributed, viz_pillar_efficiency, viz_pillar_mobility,
                       arch_figure, legend, SCENARIO_A, OEM_EMBED)
from .pages_cases import case_url, engagement_block

# Technical support available for each case (public summary of the evidence matrix)
SUPPORT = {
    "BC03": ("Direct", "Benchmark data reduction and accuracy; 86% workstation training-energy measurement."),
    "BC09": ("Partial", "Benchmarks cover single training runs; repeated retraining cycles have not been evaluated."),
    "BC05": ("Partial", "39% edge energy measurement; no device characterization yet."),
    "BC06": ("Partial", "Per-run training energy measurement; no data-center-level measurement."),
    "BC10": ("Partial", "Per-run training energy measurement; no lifecycle assessment."),
}
DEFAULT_SUPPORT = ("Indirect", "Single-domain benchmarks only; multi-domain combination not yet benchmarked.")
PILLAR_VIZ = {"distributed-enterprise-intelligence": viz_pillar_distributed,
              "ai-infrastructure-efficiency": viz_pillar_efficiency,
              "intelligent-data-mobility": viz_pillar_mobility}

# Status vocabulary for what exists today (platform, deployment, integrations)
STATUS = {"available": ("Available for evaluation", "proto"), "experimental": ("Experimental", "proto"),
          "reference": ("Reference architecture", "ref"),
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
def _volume_bars():
    """Numeric comparison for the featured scenario (illustrative figures, drawn to scale)."""
    rows = [("Conventional: eligible history replicated", 200, "bv-full", "200 TB"),
            ("With source-side distillation (assumed 90%)", 20, "bv-dist", "20 TB")]
    out = []
    for i, (label, v, cls, txt) in enumerate(rows):
        y = 8 + i * 46
        w = round(360 * v / 200)
        out.append(f'<text class="bv-n" x="0" y="{y + 10}">{esc(label)}</text>'
                   f'<rect class="{cls}" x="0" y="{y + 18}" width="{w}" height="14" rx="4"' + (' fill="url(#UID-g)"' if cls == "bv-dist" else "") + '/>'
                   f'<text class="bv-v" x="{w + 8}" y="{y + 30}">{txt}</text>')
    inner = ('<defs><linearGradient id="UID-g" x1="0" x2="1"><stop offset="0" stop-color="#2EE6A6"/><stop offset="1" stop-color="#3CC8F5"/></linearGradient></defs>'
             + "".join(out))
    from .diagrams import _svg
    return _svg("0 0 460 100", "Illustrative scenario: 200 TB of eligible history replicated conventionally versus 20 TB of approved distilled datasets, 180 TB of transfer avoided.", inner, "viz sc-bars")


def render_home(cases, industries):
    by = {c["id"]: c for c in cases}

    def pillar_panel(p, layout):
        apps = "".join(f'<li><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></li>' for cid in p["cases"])
        viz = f'<div class="fc-viz">{PILLAR_VIZ[p["slug"]]()}</div>' if p["flagship"] else ""
        return (
            f'<article class="pl pl-{layout}" aria-labelledby="pl-{p["slug"]}">'
            f'<div class="pl-text"><p class="pl-k">{"Flagship solution" if p["flagship"] else "Solution"}</p>'
            f'<h3 id="pl-{p["slug"]}"><a href="/solutions/{p["slug"]}/">{esc(p["name"])}</a></h3>'
            f'<p class="pl-msg">{esc(p["message"])}</p>'
            '<dl class="fc-dl">'
            f'<div><dt>Challenge</dt><dd>{md(p["challenge_short"])}</dd></div>'
            f'<div class="fc-outcome"><dt>Outcome</dt><dd>{md(p["outcome_short"])}</dd></div></dl>'
            f'<ul class="pl-apps" aria-label="Business cases">{apps}</ul>'
            f'<a class="link-arrow" href="/solutions/{p["slug"]}/">Explore {esc(p["name"].lower())}</a></div>'
            f'{viz}</article>')

    p1, p2, p3 = S.PILLARS
    pillars = pillar_panel(p1, "wide") + '<div class="pl-pair">' + pillar_panel(p2, "half") + pillar_panel(p3, "half") + '</div>'

    rows = "".join(
        f'<li class="fl-row"><div class="fl-t"><p class="fl-p">{esc(S.PILLAR_OF[cid]["name"])}</p>'
        f'<h3><a href="{case_url(by[cid])}">{esc(by[cid]["title"])}</a></h3><p>{md(by[cid]["headline"])}</p></div>'
        f'<div class="fl-po"><p><span class="fl-k">Problem</span>{md(by[cid]["problem_short"])}</p>'
        f'<p class="fl-out"><span class="fl-k">Outcome</span>{md(by[cid]["outcome_short"])}</p></div>'
        f'<div class="fl-a"><a class="link-arrow" href="{case_url(by[cid])}">Business case</a>'
        f'<a class="link-arrow link-muted" href="/pilot/?case={cid}">{esc(by[cid]["cta"])}</a></div></li>'
        for cid in ("BC01", "BC04", "BC02", "BC03"))

    flow = [
        ("Access authorized source datasets", "Read-only access, granted by the data owner, inside the source environment.", "reference"),
        ("Generate a task-specific optimized dataset", "The runtime builds a compact training dataset for a defined model and task.", "experimental"),
        ("Evaluate downstream predictive performance", "The same model is trained on full and optimized data and compared on the same test data.", "experimental"),
        ("Transfer approved datasets where required", "Through the DMZ, gateway or pipeline you already control.", "reference"),
        ("Train centrally or run the validated workload", "On your existing ML and analytics platforms.", "customer"),
    ]
    flow_html = "".join(f'<li><span class="fs-n">{i}</span>{status_badge(k)}<h3>{esc(t)}</h3><p>{esc(d)}</p></li>'
                        for i, (t, d, k) in enumerate(flow, 1))
    deploy = [("Customer server, VM or private cloud", "available"), ("Multi-domain and industrial edge deployments", "reference"),
              ("Embedding in partner products (OEM)", "proposed")]
    dep_html = "".join(f'<li>{status_badge(k)} {esc(n)}</li>' for n, k in deploy)

    body = (
        '<section class="hero" aria-labelledby="hero-h"><div class="wrap"><div class="hero-grid"><div class="hero-copy">'
        '<p class="eyebrow">Enterprise AI across distributed and segregated data</p>'
        '<h1 id="hero-h">Keep data distributed. <span class="hl g">Centralize intelligence.</span></h1>'
        '<p class="hero-sub">Train AI models across industrial plants, business units and segregated data environments '
        'without centralizing entire raw datasets.</p>'
        '<p class="lead">Enable enterprise-wide analytics, reduce unnecessary data movement and optimize AI infrastructure efficiency.</p>'
        '<div class="cta-row"><a class="btn btn-primary btn-lg" href="/pilot/">Discuss your use case</a>'
        '<a class="btn btn-ghost btn-lg" href="/business-cases/">Explore business cases</a></div>'
        '<p class="hero-brief"><a href="/resources/executive-brief/">Executive overview — GroundTruth AI in 4 slides</a>'
        ' <span aria-hidden="true">·</span> <a href="/resources/executive-brief/es.html" hreflang="es" lang="es">Resumen ejecutivo en español</a></p>'
        f'</div><div class="hero-art">{hero_visual()}</div></div></div></section>'

        '<section class="sec sec-pillars" id="solutions" aria-labelledby="sol-h"><div class="wrap">'
        '<p class="eyebrow">Three strategic solutions</p>'
        '<h2 id="sol-h">One capability, three enterprise problems it solves</h2>'
        f'{pillars}</div></section>'

        '<section class="sec sec-scen" id="scenario" aria-labelledby="sc-h"><div class="wrap">'
        '<p class="eyebrow">Featured industrial scenario</p>'
        '<h2 id="sc-h">Train one predictive-maintenance model across 20 facilities without centralizing raw OT data</h2>'
        '<p class="sc-label"><span class="badge badge-illus">Illustrative enterprise scenario</span> Assumptions for discussion, not contractual; results depend on workload-specific validation.</p>'
        '<div class="two-col sc-intro"><div><p class="lead-s">A manufacturer wants centralized predictive-maintenance training on data from all '
        '20 of its facilities, while each facility keeps its original OT data in its authorized environment.</p>'
        '<p>Each facility distills a task-specific dataset on site. After evaluation and owner approval, only that dataset crosses the existing DMZ.</p>'
        + _volume_bars() + '</div>'
        '<dl class="sc-figs">'
        '<div><dt>Eligible training data</dt><dd>200 TB</dd><dd class="sc-sub">20 facilities × 10 TB</dd></div>'
        '<div><dt>Assumed reduction</dt><dd>90%</dd><dd class="sc-sub">to be validated per workload</dd></div>'
        '<div><dt>Optimized transfer</dt><dd class="g">20 TB</dd><dd class="sc-sub">approved datasets</dd></div>'
        '<div><dt>Potentially avoided</dt><dd class="g">180 TB</dd><dd class="sc-sub">original data stays on site</dd></div></dl></div>'
        + legend() + arch_figure(SCENARIO_A["proposed"], "sca-pro", "Reference architecture") +
        '<p class="note">To be validated per workload: predictive performance against a full-data baseline, rare-failure coverage at every facility, '
        'generalization to a facility held out from training, and the compute cost of distillation on site hardware.</p>'
        '<div class="cta-row"><a class="btn btn-primary" href="/business-cases/ot-it-data-segregation/">See the OT/IT data segregation case</a>'
        '<a class="btn btn-ghost" href="/simulator/">Change the assumptions in the simulator</a></div>'
        '</div></section>'

        '<section class="sec sec-alt" id="challenges" aria-labelledby="ch-h"><div class="wrap">'
        '<p class="eyebrow">Flagship business cases</p>'
        '<h2 id="ch-h">Solve your most critical data challenges</h2>'
        f'<ol class="fl-list">{rows}</ol>'
        '<div class="sec-head sec-foot"><a class="link-arrow" href="/business-cases/">All 11 business cases</a>'
        '<a class="link-arrow link-muted" href="/industries/">Business cases by industry</a></div>'
        '</div></section>'

        + section("how", "How it works",
                  f'<ol class="flow-steps flow-5">{flow_html}</ol>'
                  '<p class="note"><strong>Experimental</strong>: implemented in the prototype used in internal experiments. '
                  '<strong>Reference architecture</strong>: the deployment pattern a pilot implements with your teams. '
                  '<strong>Customer system</strong>: your existing platforms. '
                  '<a href="/technology/">How dataset distillation works</a></p>',
                  eyebrow="Technology")

        + '<section class="sec sec-alt" id="evidence" aria-labelledby="ev-h"><div class="wrap">'
        '<p class="eyebrow">Evidence and deployment</p><h2 id="ev-h">What has been measured, and where it runs</h2>'
        '<div class="two-col ev-home2"><div>'
        '<div class="ev-pair"><div class="ev-stat"><p class="big g">86–95<span>%</span></p><p>less training data on four public classification benchmarks</p></div>'
        '<div class="ev-stat"><p class="big g">1.4–2.8<span> pp</span></p><p>lower accuracy than the full-data model, in percentage points</p></div></div>'
        f'<div class="fc-viz">{viz_bc03(S.BENCHMARKS)}</div>'
        '<p><a class="link-arrow" href="/evidence/">Results, methodology and validation roadmap</a></p></div>'
        f'<div><ul class="dep-mini">{dep_html}</ul>'
        '<p><a class="link-arrow" href="/platform/">What is available for evaluation today</a></p></div></div>'
        '</div></section>'

        + '<section class="sec sec-cta" id="engage" aria-labelledby="cta-h"><div class="wrap">'
        '<p class="eyebrow">Commercial engagement</p><h2 id="cta-h">Start with a conversation about your architecture</h2>'
        + engagement_block(compact=True) +
        '<div class="cta-band eng-final"><div><h3 class="h-m">Have a distributed-data problem in mind?</h3>'
        '<p>Tell us where your data lives and what you want to train. <a href="/technology/#faq">Read the FAQ</a> first if you prefer.</p></div>'
        '<div class="cta-stack"><a class="btn btn-primary btn-lg" href="/pilot/">Discuss your use case</a></div></div>'
        '</div></section>')

    page("/", "GroundTruth AI — Keep data distributed. Centralize intelligence.",
         "Train enterprise AI across industrial plants, business units and segregated data environments without centralizing entire raw datasets: OT/IT data segregation, distributed industrial intelligence and AI infrastructure efficiency.",
         body, active="", cases=cases, priority="1.0", body_class="pg-home")


# ---------------------------------------------------------------------------- PLATFORM
PRODUCT_DIAGRAM = {
    "title": "Available for evaluation: the GroundTruth AI runtime and its outputs",
    "zones": [
        {"id": "in", "label": "Your environment · inputs", "kind": "source",
         "nodes": [["data", "Customer dataset (tabular or image arrays)", "store"], ["task", "Task specification: target, model, metric", "user"]]},
        {"id": "rt", "label": "GroundTruth AI runtime · Python prototype", "kind": "external",
         "nodes": [["gt", "Task-aware distillation", "gt"], ["ev", "Evaluation: same model on full vs. distilled data", "system"]]},
        {"id": "out", "label": "Outputs · stay in your environment", "kind": "central",
         "nodes": [["ds", "Distilled training dataset", "store"], ["res", "Evaluation results (task metrics)", "system"]]},
    ],
    "flows": [["data", "gt", "raw", "read access"], ["task", "gt", "control", ""], ["gt", "ev", "distilled", ""],
              ["gt", "ds", "distilled", ""], ["ev", "res", "model", ""]],
}


def render_platform(cases):
    comps = [
        ("Distillation runtime", "experimental",
         "Builds a compact, task-specific training dataset from source data. Python runtime; tabular data via pandas / NumPy and image arrays; classification tasks."),
        ("Performance evaluation", "experimental",
         "The evaluation method used in internal experiments: the same model is trained on full and distilled data and compared on the same test data, through a scikit-learn-compatible adapter."),
        ("Rare-event and regime coverage checks", "proposed",
         "Checks that labeled events, rare classes and operating regimes remain represented. Today coverage is an evaluation requirement agreed per pilot, not an automated check."),
        ("Approval, lineage and export package", "proposed",
         "Packaging each dataset with its evaluation results and derivation record for review by data owners."),
        ("Multi-domain coordination", "reference",
         "One runtime per plant, subsidiary or region with a shared task specification."),
        ("Edge gateway deployment", "reference",
         "Distillation close to sensors and devices. No specific device has been validated; no real-time execution is claimed."),
        ("Drift-triggered regeneration", "proposed",
         "Re-running distillation when data or conditions change. Drift detection exists as a separate prototype capability."),
    ]
    comp_html = "".join(f'<li class="comp"><div class="comp-h"><h3>{esc(n)}</h3>{status_badge(k)}</div><p>{esc(d)}</p></li>' for n, k, d in comps)

    deploy = [
        ("Workstation", "experimental", "Internal benchmarks and energy measurements were run on workstation-class hardware."),
        ("Customer server or VM", "available", "In the authorized zone (for example an OT-side operations zone or a subsidiary data center), operating on file exports."),
        ("Private cloud or customer VPC", "available", "Inside the customer's own cloud account, next to the data domain it serves."),
        ("Edge gateway", "reference", "Distillation close to sensors and devices. No specific device validated."),
        ("Embedded / OEM", "proposed", "Runtime embedded in a partner's product. See Partners."),
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

    avail = [
        ("Runtime", ["Experimental Python prototype used in the internal experiments",
                     "Tabular data via pandas / NumPy; image arrays (MNIST benchmark)",
                     "Classification tasks with scikit-learn-compatible models"]),
        ("Inputs and outputs", ["**In:** a dataset in your environment and a task specification (target, model family, metric)",
                                "**Out:** a distilled training dataset for that task",
                                "**Out:** evaluation results comparing the same model trained on full and on distilled data"]),
        ("Evaluation workflow", ["Agree the task and the acceptance tolerance",
                                 "Distill, then train the same model on both datasets",
                                 "Compare task metrics on the same test data; the full-data reference training also consumes compute"]),
        ("Current limitations", ["Classification only; industrial time series, regression and forecasting not yet evaluated",
                                 "No connectors or packaging: data is exchanged as files or arrays",
                                 "Each dataset is task-specific; new objectives need a new dataset",
                                 "Compute and energy of distillation itself not yet reported"]),
    ]
    av_html = "".join(f'<div class="acq"><h3>{esc(t)}</h3>{ul(items)}</div>' for t, items in avail)

    body = (
        _hero("A distillation runtime that runs where your data lives",
              "What is available for technical evaluation today, what each component's status is, and how it fits the platforms you already operate.",
              [("Home", "/"), ("Platform", None)], "Platform",
              button("Request a feasibility assessment", "/pilot/?type=assessment") + button("See the business cases", "/business-cases/", "ghost"))
        + section("available", "Available for technical evaluation",
                  legend() + arch_figure(PRODUCT_DIAGRAM, "prod", "Available")
                  + f'<div class="acq-grid acq-grid-2">{av_html}</div>'
                  '<p class="note">How an optimized dataset is constructed is part of the proprietary method and is not published; it is available for technical due diligence under NDA.</p>')
        + section("components", "Components and their status",
                  '<p><strong>Experimental</strong>: implemented and used in internal experiments; available for evaluation. '
                  '<strong>Reference architecture</strong>: a documented deployment pattern, implemented with a customer. '
                  '<strong>Proposed</strong>: designed, not built.</p>'
                  f'<ul class="comp-list">{comp_html}</ul>', cls="sec-alt")
        + section("deployment", "Execution environments",
                  f'<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Environment</th><th scope="col">Status</th><th scope="col">Description</th></tr></thead><tbody>{dep_html}</tbody></table></div>')
        + section("integrations", "Integration status",
                  '<p>What has been exercised, what is proposed and what stays a customer system. Proposed integrations are built with the first customer that needs them.</p>'
                  f'<div class="table-wrap"><table class="tbl tbl-narrow"><thead><tr><th scope="col">Integration</th><th scope="col">Status</th></tr></thead><tbody>{int_html}</tbody></table></div>',
                  cls="sec-alt")
        + section("security", "Data governance in the reference architecture",
                  '<div class="two-col"><div>' + ul([
                      "**Customer-controlled execution.** The runtime operates inside your environment, under your access controls.",
                      "**No data sent to GroundTruth AI.** Customer data, distilled or raw, stays with you.",
                      "**Owner approval before transfer.** Data owners review each distilled dataset and its evaluation results before it moves.",
                      "**Least-privilege access.** Read access limited to the variables and period in scope.",
                  ]) + '</div><div class="callout callout-legal"><p class="callout-h">What distillation does not change</p>' + ul([
                      "Distilled data is derived from source data and is classified like it; it may still contain sensitive information.",
                      "It is not anonymization, differential privacy or encryption, and grants no legal authorization for any transfer.",
                      "It does not replace network segmentation, OT security controls, data integration or compliance processes.",
                      "GroundTruth AI holds no security certifications today.",
                  ]) + '</div></div>')
        + section("next", "Evaluate it on your architecture",
                  '<p>A feasibility assessment starts with an architecture review: where the runtime would sit, which data it reads, which path the dataset takes and who approves it. '
                  '<a href="/technology/#faq">Frequently asked questions</a></p>'
                  '<div class="cta-row">' + button("Request a feasibility assessment", "/pilot/?type=assessment") + button("Read the technology", "/technology/", "ghost") + '</div>',
                  cls="sec-alt"))
    page("/platform/", "Platform: what is available for evaluation", "The GroundTruth AI distillation runtime available for technical evaluation: inputs, outputs, evaluation workflow, component status, execution environments and integrations.",
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
                  '<p>That is why distillation can run at the source: the task specification travels to the data, and only the result travels back.</p>'
                  '<h3 class="h-s">What this means for enterprise analytics</h3>' + ul([
                      "Each optimized dataset serves a defined analytical or machine learning objective; different objectives may need different datasets.",
                      "A dataset optimized for one prediction task may not be suitable for another.",
                      "Optimized datasets complement original data repositories; they do not replace them.",
                      "New analytical requirements may need a new optimized dataset, generated from the original data.",
                      "Downstream performance is evaluated for each workload before the dataset is used.",
                  ]) + '</div>'
                  '<div class="side-card"><p class="side-h">Inputs and outputs</p>' + ul([
                      "**In:** source data in its home environment, plus a task specification",
                      "**Out:** a distilled training dataset",
                      "**Out:** evaluation results comparing models trained on full and on distilled data",
                  ]) + '<p class="small">Evaluation trains a reference model on the full data (or reuses an existing baseline), which consumes compute; it is part of the cost of an evaluation.</p></div></div>')
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
                  '<li><span class="fs-n">4</span><h3>Performance evaluation</h3><p>Full vs. distilled models compared on the same test data.</p></li>'
                  '<li><span class="fs-n">5</span><h3>Approval and regeneration</h3><p>In the reference architecture, owners approve; datasets are regenerated when the task or data change.</p></li></ol>'
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
        + section("faq", "Frequently asked questions",
                  f'<div class="faq"><div class="faq-i"><h3>Does GroundTruth AI replace our data lake?</h3><p>No. Original data stays in its repositories under your retention policies. GroundTruth AI produces task-specific training datasets from it; it does not replace data lakes, historians or warehouses.</p></div><div class="faq-i"><h3>Can original industrial data remain within OT?</h3><p>In the source-side reference architecture, yes. Distillation runs in an approved OT-side computing environment, and only approved optimized datasets cross the boundary through existing exchange mechanisms such as the industrial DMZ. The OT and data owners decide what may cross.</p></div><div class="faq-i"><h3>Is GroundTruth AI equivalent to conventional data compression?</h3><p>No. Compression encodes every byte more compactly and is decompressed before use, so the training volume is unchanged. Distillation builds a smaller training dataset for a defined task; it is not designed to reproduce the original data.</p></div><div class="faq-i"><h3>Is GroundTruth AI equivalent to federated learning?</h3><p>No. Federated learning trains models inside every domain and exchanges model updates repeatedly. Source-side distillation sends approved optimized datasets to a central environment, where training can stay centralized. It does not provide the privacy guarantees of privacy-preserving federated learning, and the two approaches can be combined.</p></div><div class="faq-i"><h3>Does dataset distillation guarantee privacy or anonymization?</h3><p>No. Distillation is not anonymization, differential privacy or encryption. Optimized datasets are derived from the source data, may still contain sensitive information and remain subject to the same classification, protection and transfer rules.</p></div><div class="faq-i"><h3>Can the same optimized dataset support multiple analytical tasks?</h3><p>Not by default. An optimized dataset is built and evaluated for a defined target, model family and metric. Using it for another task requires evaluating it for that task, and often generating a new dataset.</p></div><div class="faq-i"><h3>What happens when analytical requirements change?</h3><p>A new or changed objective generally needs a new optimized dataset, generated from the original data that remains in its source environment, and evaluated for the new workload.</p></div><div class="faq-i"><h3>How can an enterprise evaluate the technology?</h3><p>In three stages: an architecture discovery conversation, a technical feasibility assessment on one representative workload, and an enterprise pilot with success criteria agreed in advance.</p></div></div>'
                  '<p><a class="link-arrow" href="/pilot/">Discuss your use case</a></p>')
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
    bm = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{esc(S.BENCHMARK_META[n][0])}</td><td>{esc(t)}</td><td class="num">{r}%</td>'
                 f'<td class="num">{100 - r}%</td><td class="num">{b:.1f}%</td><td class="num">{d:.1f}%</td><td class="num">{delta:+.1f} pp</td></tr>'
                 for n, t, r, b, d, delta in S.BENCHMARKS)
    per = []
    for p in S.PILLARS:
        for cid in p["cases"]:
            c = next(x for x in cases if x["id"] == cid)
            lvl, note = SUPPORT.get(cid, DEFAULT_SUPPORT)
            per.append(f'<tr><th scope="row"><a href="{case_url(c)}#evidence">{esc(c["title"])}</a></th><td>{esc(p["name"])}</td>'
                       f'<td><span class="sup sup-{lvl.lower()}">{lvl}</span></td><td>{esc(note)}</td></tr>')
    rm = "".join(f'<tr><td><span class="prio prio-{pr.lower()}">{pr}</span></td><th scope="row">{esc(n)}</th><td>{esc(d)}</td><td>{esc(m)}</td>'
                 f'<td>{esc(_names(cases, ids))}</td><td>Proposed</td></tr>' for pr, n, d, m, ids in ROADMAP)
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
        _hero("Experimental validation and technical evidence",
              "Results from internal experiments on public benchmarks, how to read them, how each claim on this site is classified, "
              "and the validation work that pilots are designed to complete.",
              [("Home", "/"), ("Evidence", None)], "Evidence",
              button("Discuss your use case", "/pilot/") + button("Validation roadmap", "#roadmap", "ghost"))
        + section("benchmarks", "Results on public benchmarks",
                  '<p>The same model architecture was trained on the full training data and on the distilled training data, and both were evaluated on the same test data.</p>'
                  '<div class="table-wrap"><table class="tbl tbl-bm"><caption class="sr-only">Benchmark results</caption><thead><tr><th scope="col">Dataset</th><th scope="col">Public dataset</th>'
                  '<th scope="col">Model</th><th scope="col" class="num">Training data removed</th><th scope="col" class="num">Training data kept</th>'
                  '<th scope="col" class="num">Full-data accuracy</th><th scope="col" class="num">Distilled accuracy</th>'
                  f'<th scope="col" class="num">Difference</th></tr></thead><tbody>{bm}</tbody></table></div>'
                  '<div class="two-col"><div><h3 class="h-s">How to read the results</h3>' + ul([
                      "**Training data removed** is a relative share of training records: 95% removed means the model trained on 5% of the records.",
                      "**Difference** is in percentage points: the absolute gap between two accuracies. Iris: 97.4% → 94.7% is −2.7 pp.",
                      "Absolute sizes of the distilled training sets, distillation runtime and memory are not yet reported.",
                      "Four results do not define a reduction-versus-accuracy curve; no trade-off curve is inferred from them.",
                  ]) + '<h3 class="h-s">Scope and limitations</h3>' + ul([
                      "Small, public, classification datasets; workstation-class hardware.",
                      "Not yet independently replicated.",
                      "Not extrapolated to industrial time series, multi-domain data or industrial scale.",
                      "The OT/IT, multi-domain and edge architectures on this site are reference architectures that have not been validated experimentally.",
                  ]) + f'</div><div class="fc-viz">{viz_bc03(S.BENCHMARKS)}</div></div>')
        + section("energy", "Energy measurements",
                  '<p>Two internal measurements, energy estimated with Schneider Electric reference data. The methodology is not yet published.</p>'
                  '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Measurement</th><th scope="col">What it covers</th><th scope="col">Not included</th></tr></thead><tbody>'
                  '<tr><th scope="row">86% less energy per training run</th><td>Model training on a workstation, after data reduction</td>'
                  '<td>Energy of the distillation step; total end-to-end or lifecycle energy; financial savings</td></tr>'
                  '<tr><th scope="row">39% less energy on IoT / edge devices</th><td>Processing at the point of capture</td>'
                  '<td>Energy of the distillation step; network and central infrastructure; financial savings</td></tr>'
                  '</tbody></table></div>'
                  '<p class="note">Net, end-to-end energy (training saved minus distillation used) is measured per workload in pilots.</p>', cls="sec-alt")
        + section("levels", "How every claim is classified", f'<ul class="lvl-list">{lv}</ul>')
        + section("by-case", "Evidence by business case",
                  '<p><strong>Direct</strong>: the experiments measure the outcome the case depends on. <strong>Partial</strong>: related measurements exist. '
                  '<strong>Indirect</strong>: the case relies on an architectural hypothesis that has not yet been benchmarked.</p>'
                  '<div class="table-wrap"><table class="tbl"><thead><tr><th scope="col">Business case</th><th scope="col">Solution family</th>'
                  f'<th scope="col">Technical support</th><th scope="col">Notes</th></tr></thead><tbody>{"".join(per)}</tbody></table></div>', cls="sec-alt")
        + section("roadmap", "Technical validation roadmap",
                  '<p>Proposed experiments, prioritized by commercial relevance; none has been run yet and no dates are published. '
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
        '<p class="disc-note"><strong>Not contractual.</strong> Illustrative estimates based on internal experiments and on the assumptions entered here; no warranty or guarantee of results. Actual results require a workload-specific evaluation. <a href="#site-disclaimer">Full disclaimer</a>.</p>'
        '</div></form></div></section>'
        + section("method", "Method and limits",
                  ul([
                      "Only the **eligible, data-proportional share** of each cost line is reduced. A reduction in dataset records is not an equivalent reduction in total infrastructure spend.",
                      "Transfer, ingestion, processing, storage, training compute and energy are separate lines; energy already paid inside compute spend is not counted again.",
                      "Unit costs per TB are treated as **variable** costs; leave fixed costs (committed contracts, reserved capacity, licenses) out of them.",
                      "**ROI** is first-year net value divided by the costs entered (recurring costs plus implementation); it is not shown when no costs are entered.",
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
        + _num("s_vol", "Training-relevant source data per domain", 10, "TB", hint="Data a central model would need, per training cycle.", mx=100000)
        + _num("s_tx", "Share of that data transferred centrally today", 100, "%", hint="Baseline: what a conventional architecture would move.", mx=100)
        + _num("s_el", "Share of transferred data eligible for distillation", 100, "%", hint="Data used only for model training.", mx=100)
        + _num("s_red", "Assumed dataset reduction", 90, "%", hint="Illustrative. Must be validated per workload.", mx=99)
        + _num("s_ctr", "Transfer cost (optional)", 0, "per TB")
        + _num("s_cproc", "Central ingestion and processing cost (optional)", 0, "per TB"))
    body = (
        _hero("Distributed intelligence simulator",
              "See how source-side distillation changes what crosses your authorized boundaries when central teams train AI on data from many plants, "
              "subsidiaries or regions. This is an architectural simulation of your assumptions: it does not run the GroundTruth AI algorithm and is not an experimental result.",
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
        '<div><dt>Total source data in scope</dt><dd id="k-orig">—</dd><dd class="sc-sub">stays at source in both architectures</dd></div>'
        '<div><dt>Baseline transfer</dt><dd id="k-base">—</dd><dd class="sc-sub">conventional centralization</dd></div>'
        '<div><dt>Eligible for distillation</dt><dd id="k-elig">—</dd><dd class="sc-sub" id="k-elig-s"></dd></div>'
        '<div><dt>Estimated optimized transfer</dt><dd id="k-opt" class="g">—</dd><dd class="sc-sub" id="k-opt-s"></dd></div>'
        '<div><dt>Potential avoided data movement</dt><dd id="k-avoid" class="g">—</dd><dd class="sc-sub" id="k-rel"></dd></div>'
        '<div class="sim-money" id="k-money-w" hidden><dt>Illustrative gross saving</dt><dd id="k-money">—</dd><dd class="sc-sub">per training cycle, before distillation, validation and license costs</dd></div>'
        '</dl>'
        '<details class="sim-calc"><summary>How the numbers are calculated</summary><ol>'
        '<li>Baseline transfer = <span id="f-n"></span> domains × <span id="f-vol"></span> × <span id="f-tx"></span> transferred = <strong id="f-base"></strong></li>'
        '<li>Eligible for distillation = baseline × <span id="f-el"></span> = <strong id="f-elig"></strong></li>'
        '<li>Optimized transfer = non-eligible raw data <span id="f-raw"></span> + eligible data reduced by <span id="f-red"></span> '
        '<span id="f-dist"></span> = <strong id="f-opt"></strong></li>'
        '<li>Avoided transfer = eligible × reduction = <strong id="f-avoid"></strong></li>'
        '<li>Illustrative gross saving = avoided × <span id="f-cost"></span> per TB = <strong id="f-money"></strong></li></ol>'
        '<p class="small">Volumes per training cycle. The non-eligible share is still transferred raw. Costs of distillation, evaluation and licensing are not deducted here; the ROI calculator deducts them.</p></details>'
        '<p class="disc-note"><strong>Not contractual.</strong> Illustrative estimates based on internal experiments and on the assumptions entered here; no warranty or guarantee of results. Actual results require a workload-specific evaluation. <a href="#site-disclaimer">Full disclaimer</a>.</p>'
        '</div></form>'
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
    targets = [("Industrial data platforms and historians", "Distill where plant data is already collected, before it is exported."),
               ("Industrial edge environments", "Reduce what leaves the site for central training."),
               ("Data integration architectures", "Move task-specific datasets instead of full replicas between domains."),
               ("Enterprise AI infrastructure and MLOps", "Train and retrain on validated distilled datasets."),
               ("Distributed analytical systems", "Enable central models across domains that keep their data.")]
    t_html = "".join(f'<li class="dep"><h3>{esc(n)}</h3><p>{esc(d)}</p></li>' for n, d in targets)
    body = (
        _hero("Embed source-side distillation in your product",
              "For platforms that already run next to industrial, edge or enterprise data, GroundTruth AI can add a differentiated capability: "
              "task-specific training datasets produced where the data lives.",
              [("Home", "/"), ("Partners", None)], "Partners and OEM",
              button("Discuss a technology integration", "/pilot/?type=partnership"))
        + section("where", "Where it could be embedded",
                  f'<ul class="dep-list">{t_html}</ul>'
                  '<p class="note">GroundTruth AI complements automation, historians, data integration and security infrastructure; it does not replace them.</p>')
        + section("pattern", "Proposed integration pattern",
                  legend() + arch_figure(OEM_EMBED, "oem", "Proposed")
                  + '<p class="note">Today GroundTruth AI is an experimental Python runtime available for evaluation. No integration with a third-party product has been built, '
                    'and none is claimed until it has been built and tested together. No partnerships have been announced.</p>', cls="sec-alt")
        + section("models", "How we work with technology partners",
                  ul(["**Joint technical validation** on your target data, before any joint claim.",
                      "**OEM, embedded or technology licensing** for a defined field of use, discussed per partnership. No prices are published.",
                      "**Joint solutions** for a business case such as OT/IT data segregation or edge-to-cloud optimization.",
                      "**Delivery partnerships** with systems integrators for assessments and pilots."])
                  + '<div class="cta-row">' + button("Discuss a technology integration", "/pilot/?type=partnership")
                  + button("Review the business cases", "/business-cases/", "ghost") + '</div>'))
    page("/partners/", "Partners and OEM", "Embed source-side dataset distillation in industrial data platforms, edge environments, data integration and enterprise AI infrastructure: joint validation, OEM and technology licensing.",
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
        '<p class="small">Sharing this internally first? <a href="/resources/executive-brief/">Executive overview in 4 slides</a> '
        '(<a href="/resources/executive-brief/GroundTruthAI_Executive_Brief_EN.pdf">PDF</a> · '
        '<a href="/resources/executive-brief/GroundTruthAI_Resumen_Comercial_ES.pdf" hreflang="es">PDF en español</a>)</p>'
        + ul(["Which data, where it lives, and why it cannot simply be centralized", "The model or analytics you want to build", "The baseline you would compare against"])
        + '<p class="small"><strong>No proprietary data needed.</strong> Please do not include confidential data, files or credentials in this form.</p>'
        '<div class="privacy" id="privacy"><h3 class="h-s">Privacy</h3>'
        '<p class="small">We collect the details you enter here only to reply to your request and to prepare the conversation. Your request is delivered by email to the '
        'GroundTruth AI team through <a href="https://formsubmit.co/" rel="noopener">FormSubmit</a>, a third-party form delivery service, which processes it to deliver it. '
        'Full details and your rights: <a href="/privacy/">Privacy policy</a> (<a href="/privacidad/" lang="es">español</a>). '
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
        '<div class="fld fld-check"><input type="checkbox" id="p-consent" name="consent" required><label for="p-consent">I have read the privacy policy and agree that GroundTruth AI may use these details to respond to this request, sent by email through FormSubmit. <span class="req">(required)</span></label></div>'
        '<p class="small consent-link"><a href="/privacy/">Read the privacy policy</a> · <a href="/privacidad/" lang="es">Política de privacidad (español)</a></p>'
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
