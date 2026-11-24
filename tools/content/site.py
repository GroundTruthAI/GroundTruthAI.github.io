"""Site-wide configuration and shared vocabularies (mirror of CONTENT_BRIEF.md §5)."""

BASE_URL = "https://groundtruthai.github.io"
SITE_NAME = "GroundTruth AI"

# Pilot / partnership intake address (also the mailto: fallback).
CONTACT_EMAIL = "ingenieros.informatica@gmail.com"

# Form delivery service (GitHub Pages is static). FormSubmit AJAX endpoint.
# After activation, FormSubmit issues a random alias: replace the address in the URL with it
# to keep the mailbox out of the page source.
FORM_ORIGIN = "https://formsubmit.co"
FORM_ENDPOINT = FORM_ORIGIN + "/ajax/" + CONTACT_EMAIL

# Owner identification for the Spanish legal pages (LSSI-CE art. 10, RGPD art. 13).
# Fill in with verified data only. verify.py fails while owner, nif and address are empty.
LEGAL = {
    # Company in formation (no NIF or registered address yet). Replace the pending values as soon as they exist.
    "owner": "GroundTruth AI (sociedad en constitución)",
    "nif": "Pendiente de asignación",
    "address": "Pendiente de asignación; mientras tanto, contacto por correo electrónico",
    "email": CONTACT_EMAIL,
    "registry": "Pendiente de inscripción en el Registro Mercantil",
}
# English rendering of the same values for the English legal pages (empty = use LEGAL as is).
LEGAL_EN = {
    "owner": "GroundTruth AI (company in formation)",
    "nif": "Pending assignment",
    "address": "Pending assignment; in the meantime, contact us by email",
    "registry": "Pending registration in the Spanish Commercial Registry",
}

NAV = [
    # (label, href, key)
    ("Business Cases", "/business-cases/", "business-cases"),
    ("Industries", "/industries/", "industries"),
    ("Platform", "/platform/", "platform"),
    ("Technology", "/technology/", "technology"),
    ("Evidence", "/evidence/", "evidence"),
    ("Partners", "/partners/", "partners"),
    ("Company", "/company/", "company"),
]

FILTERS = {
    "objectives": ("Business objective", [
        ("segregated-analytics", "Enable analytics across segregated data"),
        ("training-cost", "Reduce AI training costs"),
        ("data-movement", "Reduce data movement"),
        ("distributed-infra", "Optimize distributed infrastructure"),
        ("replication", "Reduce data replication"),
        ("operational-efficiency", "Improve operational efficiency"),
        ("residency", "Support data residency objectives"),
        ("energy", "Reduce energy consumption"),
    ]),
    "architecture": ("Data architecture", [
        ("ot-it", "Segregated OT/IT networks"),
        ("multi-domain", "Multiple data domains or subsidiaries"),
        ("multi-site", "Multi-site or multi-facility"),
        ("edge", "Edge and device fleets"),
        ("multicloud", "Hybrid and multicloud"),
        ("centralized-ml", "Centralized ML platform"),
        ("multi-jurisdiction", "Multi-jurisdiction data estate"),
    ]),
    "deployment": ("Deployment environment", [
        ("on-prem", "On-premises or plant"),
        ("private-cloud", "Private cloud or VPC"),
        ("public-cloud", "Public cloud"),
        ("edge-gateway", "Edge gateway"),
        ("hybrid", "Hybrid"),
    ]),
    "buyers": ("Primary buyer", [
        ("cio", "CIO"),
        ("cto", "CTO"),
        ("cdo", "CDO / Chief Data Officer"),
        ("coo", "COO"),
        ("ot-leader", "Industrial / OT technology leader"),
        ("enterprise-architect", "Enterprise architect"),
        ("ml-platform", "Head of ML / MLOps platform"),
        ("infra-leader", "Infrastructure & data center leader"),
        ("sustainability", "Chief Sustainability Officer"),
        ("corp-dev", "M&A integration lead"),
        ("cfo", "CFO"),
    ]),
    "problems": ("Operational problem", [
        ("raw-replication", "Raw data replicated only to train models"),
        ("training-spend", "Rising training and retraining spend"),
        ("bandwidth", "Constrained bandwidth or transfer cost"),
        ("consolidation-blocked", "Data consolidation blocked or too slow"),
        ("rare-events", "Rare failures scattered across sites"),
        ("storage-growth", "Growing storage footprint"),
        ("cross-border", "Cross-border transfer restrictions"),
        ("model-staleness", "Models going stale between retrains"),
        ("energy-footprint", "AI energy footprint"),
        ("integration-backlog", "Post-merger integration backlog"),
    ]),
}

# Calculation models used by the ROI calculator (and by each case's "roi_scenario").
ROI_SCENARIOS = {
    "transfer": "Data movement & replication",
    "training": "Training & retraining spend",
    "infrastructure": "Storage, compute & energy",
}

# Commercial scenarios offered in the ROI calculator: (key, label, calculation model, label for a domain)
ROI_PRESETS = [
    ("ot-it", "Industrial OT/IT data movement", "transfer", "Plants or OT zones"),
    ("distributed", "Distributed enterprise analytics", "transfer", "Subsidiaries or data domains"),
    ("edge", "Edge-to-cloud optimization", "transfer", "Edge sites or device fleets"),
    ("multicloud", "Multicloud optimization", "transfer", "Source clouds or environments"),
    ("training", "AI training efficiency", "training", ""),
    ("infrastructure", "AI infrastructure efficiency", "infrastructure", ""),
]
# Default commercial scenario per business case
CASE_PRESET = {"BC01": "ot-it", "BC02": "distributed", "BC03": "training", "BC04": "ot-it", "BC05": "edge",
               "BC06": "infrastructure", "BC07": "distributed", "BC08": "multicloud", "BC09": "training",
               "BC10": "infrastructure", "BC11": "distributed"}

# Three commercial solution families. Every business case belongs to exactly one.
PILLARS = [
    {"slug": "distributed-enterprise-intelligence", "name": "Distributed enterprise intelligence", "flagship": True,
     "message": "Enable enterprise-wide intelligence without centralizing all your raw data.",
     "problem": "Plants, subsidiaries, regions and acquired companies keep their data in separate, separately governed "
                "environments. Central AI and analytics programs that first require a complete raw copy in one place "
                "collide with segregation, ownership and transfer rules, and many initiatives never start.",
     "outcome": "Central model training and analytics on approved, locally distilled datasets, while original data stays "
                "in its authorized environment.",
     "points": ["Analytical collaboration across segregated data domains",
                "Centralized model training on approved, locally distilled datasets",
                "Source data environments preserved as they are",
                "Multi-site industrial intelligence",
                "Less dependency on complete data consolidation",
                "New analytical initiatives that data architecture would otherwise hold back"],
     "cases": ["BC01", "BC02", "BC04", "BC07", "BC11"],
     "challenge_short": "Plants, subsidiaries and regions keep data in separately governed environments; central AI stalls when it needs a complete raw copy.",
     "outcome_short": "Central training and analytics on approved, locally distilled datasets.",
     "cta": "Assess your distributed data environments",
     "seo": "Enterprise analytics and AI training across data silos, OT/IT segregation and distributed industrial sites, without centralizing all raw data."},
    {"slug": "ai-infrastructure-efficiency", "name": "AI infrastructure efficiency", "flagship": False,
     "message": "Reduce the cost of developing, training and maintaining AI models.",
     "problem": "Every training and retraining cycle reprocesses growing data histories. Compute, storage, energy and "
                "wall-clock time scale with volume, while much of that volume adds little to the model.",
     "outcome": "Lower data-proportional training and retraining cost and faster experimentation, net of the cost of distillation.",
     "points": ["Training efficiency on task-specific datasets",
                "Better use of shared compute capacity",
                "Lower recurring processing costs",
                "Faster experimentation cycles",
                "More efficient retraining",
                "Potential energy savings, measured per workload"],
     "cases": ["BC03", "BC09", "BC06", "BC10"],
     "challenge_short": "Every training and retraining cycle reprocesses growing data histories.",
     "outcome_short": "Lower data-proportional training cost and faster experimentation, net of distillation.",
     "cta": "Evaluate your AI training costs",
     "seo": "Reduce enterprise AI training, retraining and infrastructure cost with task-aware dataset distillation, net of distillation overhead."},
    {"slug": "intelligent-data-mobility", "name": "Intelligent data mobility", "flagship": False,
     "message": "Move the information your AI needs, not every raw data record.",
     "problem": "Edge devices, sites and clouds produce more data than networks, ingestion pipelines and central storage can "
                "economically absorb. Large datasets are duplicated between environments simply to feed model training.",
     "outcome": "Less raw data transferred and replicated for AI workloads, with distillation performed at the source.",
     "points": ["Source-side dataset distillation",
                "Less unnecessary data transfer",
                "Less data replication between environments",
                "Leaner distributed infrastructure",
                "More efficient cloud ingestion",
                "Lower dependence on high-bandwidth connectivity"],
     "cases": ["BC05", "BC08"],
     "challenge_short": "Edge sites and clouds produce more data than networks and ingestion pipelines can economically move.",
     "outcome_short": "Less raw data transferred and replicated to feed AI workloads.",
     "cta": "Evaluate your edge-to-cloud data flows",
     "seo": "Source-side dataset optimization for edge-to-cloud and multicloud AI: move the information models need, not every raw record."},
]
PILLAR_OF = {cid: p for p in PILLARS for cid in p["cases"]}

# Three-stage commercial engagement. (type key used by the request form, label, call to action, description)
ENGAGEMENT = [
    ("discovery", "Architecture discovery", "Contact",
     "A short conversation about your business problem, data architecture, segregation requirements, current AI workloads "
     "and constraints, and whether GroundTruth AI is a plausible fit. No data is shared.",
     ["Business problem and current AI workloads", "Existing data architecture and segregation requirements",
      "Economic and operational constraints", "Initial view on applicability"]),
    ("assessment", "Technical feasibility assessment", "Request a feasibility assessment",
     "A scoped technical evaluation of one representative workload: data characteristics, existing baseline, integration "
     "requirements, the dataset reduction worth testing, quality constraints and preliminary economics.",
     ["Representative workload and baseline", "Data characteristics and quality constraints",
      "Integration requirements", "Preliminary economic feasibility"]),
    ("pilot", "Enterprise pilot", "Request an enterprise pilot",
     "A structured evaluation in your environment with agreed business objectives and technical success criteria, ending "
     "with an architecture assessment, an economic evaluation and deployment recommendations.",
     ["Agreed business objectives and success criteria", "Experimental validation on your data",
      "Architecture and economic evaluation", "Deployment recommendations"]),
]

EVIDENCE_LEVELS = [
    ("demonstrated", "Demonstrated business outcome",
     "Measured in a customer production environment.", "Reported here once a pilot or deployment produces it"),
    ("experimental", "Experimentally supported technical outcome",
     "Measured in internal experiments on public benchmark datasets.", "Data reduction and accuracy on 4 benchmarks; internal energy measurements"),
    ("proposed", "Enterprise application for pilot evaluation",
     "Architecture and value hypothesis, designed to be tested in a pilot.", "All 11 business cases"),
    ("illustrative", "Illustrative financial scenario",
     "Arithmetic on stated, editable assumptions. Not a forecast or a quote.", "ROI calculator"),
]

# Public facts about the benchmark datasets (total samples in the public release, features).
BENCHMARK_META = {
    "Iris": ("150 samples · 4 features · 3 classes", "UCI / scikit-learn"),
    "Wine": ("178 samples · 13 features · 3 classes", "UCI / scikit-learn"),
    "Breast Cancer": ("569 samples · 30 features · 2 classes", "UCI Wisconsin Diagnostic / scikit-learn"),
    "MNIST": ("70,000 images (60,000 train / 10,000 test) · 28×28 · 10 classes", "LeCun et al."),
}

BENCHMARKS = [
    # dataset, type, reduction %, baseline acc, distilled acc, delta pp
    ("Iris", "Tabular · deep learning (MLP)", 95, 97.4, 94.7, -2.7),
    ("Wine", "Tabular · deep learning (MLP)", 86, 97.8, 95.6, -2.2),
    ("Breast Cancer", "Tabular · deep learning (MLP)", 95, 96.5, 95.1, -1.4),
    ("MNIST", "Image · CNN", 93, 96.5, 93.7, -2.8),
]
