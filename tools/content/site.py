"""Site-wide configuration and shared vocabularies (mirror of CONTENT_BRIEF.md §5)."""

BASE_URL = "https://groundtruthai.github.io"
SITE_NAME = "GroundTruth AI"

# Pilot / partnership intake address (also the mailto: fallback).
CONTACT_EMAIL = "joseluis.salmeron@gmail.com"

# Form delivery service (GitHub Pages is static). FormSubmit AJAX endpoint.
# After activation, FormSubmit issues a random alias: replace the address in the URL with it
# to keep the mailbox out of the page source.
FORM_ORIGIN = "https://formsubmit.co"
FORM_ENDPOINT = FORM_ORIGIN + "/ajax/" + CONTACT_EMAIL

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

ROI_SCENARIOS = {
    "transfer": "Data movement & replication",
    "training": "Training & retraining spend",
    "infrastructure": "Storage, compute & energy",
}

EVIDENCE_LEVELS = [
    ("demonstrated", "Demonstrated business outcome",
     "Measured in a customer production environment.", "None yet"),
    ("experimental", "Experimentally supported technical outcome",
     "Measured in internal experiments on public benchmark datasets.", "Data reduction and accuracy on 4 benchmarks; internal energy measurements"),
    ("proposed", "Proposed enterprise application",
     "Architecture and value hypothesis, designed to be tested in a pilot.", "All 11 business cases"),
    ("illustrative", "Illustrative financial scenario",
     "Arithmetic on stated, editable assumptions. Not a forecast or a quote.", "ROI calculator"),
]

BENCHMARKS = [
    # dataset, type, reduction %, baseline acc, distilled acc, delta pp
    ("Iris", "Tabular · deep learning (MLP)", 95, 97.4, 94.7, -2.7),
    ("Wine", "Tabular · deep learning (MLP)", 86, 97.8, 95.6, -2.2),
    ("Breast Cancer", "Tabular · deep learning (MLP)", 95, 96.5, 95.1, -1.4),
    ("MNIST", "Image · CNN", 93, 96.5, 93.7, -2.8),
]
