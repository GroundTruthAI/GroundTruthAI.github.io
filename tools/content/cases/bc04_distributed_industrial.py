"""BC04 — Distributed industrial intelligence. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC04",
    "slug": "distributed-industrial-intelligence",
    "rank": 4,
    "tier": "flagship",
    "title": "Distributed industrial intelligence",
    "eyebrow": "Multi-site operations",
    "headline": "Learn from every facility without centralizing every facility's history.",
    "summary": (
        "Distill locally at each facility and use the approved distilled datasets to train centralized "
        "or cross-facility models for maintenance, anomaly detection and equipment health."
    ),
    "problem_short": "Failure patterns are scattered across plants with different equipment and conditions, and centralizing all their history is impractical.",
    "solution_short": "Each facility distills a task-specific dataset locally; approved sets train shared cross-site models centrally.",
    "outcome_short": "Multi-site predictive models built from distributed data preparation.",
    "cta": "Explore multi-site industrial intelligence",
    "industries": ["manufacturing", "energy-utilities", "oil-gas-mining", "transportation-logistics"],
    "filters": {
        "objectives": ["segregated-analytics", "data-movement", "distributed-infra", "operational-efficiency"],
        "architecture": ["multi-site", "ot-it", "centralized-ml"],
        "deployment": ["on-prem", "edge-gateway", "hybrid"],
        "buyers": ["coo", "ot-leader", "cio", "enterprise-architect"],
        "problems": ["rare-events", "bandwidth", "consolidation-blocked", "raw-replication"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Industrial organizations run many facilities: plants, substations, mines, depots, pumping "
        "stations. Each has its own data collection systems, equipment generations, control "
        "configurations and operating conditions, and each holds years of sensor history.",
        "The most valuable failure knowledge is spread thin. A given failure mode may occur a handful of "
        "times per site per year, so no single facility has enough examples to train a reliable model. "
        "Learning across sites means pooling data, but shipping complete historian archives from every "
        "facility to a central platform is often impractical: limited site connectivity, high transfer "
        "and storage cost, local data ownership and OT security policies all stand in the way.",
        "Organizations end up with either isolated site models of uneven quality or a stalled "
        "centralization project.",
    ],

    "approaches": [
        {"name": "Centralize all historian data",
         "limit": "Gives data scientists everything, but moves and stores complete archives from every "
                  "site, most of which is steady-state operation of little value to the model."},
        {"name": "Independent models per facility",
         "limit": "Respects local ownership but each model sees only its own rare events, so performance "
                  "is weakest exactly where failures are scarcest."},
        {"name": "Fixed down-sampling or aggregation at each site",
         "limit": "Reduces volume predictably, but averages away transients and rare regimes that drive "
                  "failure prediction."},
        {"name": "Federated learning across sites",
         "limit": "Avoids moving data but needs training infrastructure at every site and continuous "
                  "model exchange, which strains site IT capacity and OT change control."},
    ],

    "solution": {
        "intro": "GroundTruth AI distributes data preparation and centralizes learning. A distillation "
                 "runtime at each facility builds a task-specific distilled dataset from local history, "
                 "with explicit targets for rare-event and operating-regime coverage. Approved datasets "
                 "from all sites are combined to train shared models centrally.",
        "steps": [
            ("Define the shared model", "Reliability engineering and the central AI team agree the target "
             "(for example, a failure mode on a common asset class), the feature contract and coverage targets."),
            ("Distill at each facility", "The runtime processes local history on site and keeps every "
             "labeled failure event and each operating regime represented, while compressing routine operation."),
            ("Validate per site", "Each site receives a fidelity report against its own full data, including "
             "rare-event and regime coverage."),
            ("Approve and combine", "Site and OT owners approve release through existing transfer paths; "
             "approved sets are combined centrally."),
            ("Train and evaluate across sites", "Shared models are trained centrally and evaluated on "
             "held-out data from each site, so differences between facilities are visible, not averaged away."),
        ],
        "not": [
            "It does not harmonize tag names, units or asset hierarchies across sites; that mapping is a prerequisite.",
            "It does not create failure labels; where labels are sparse, coverage targets must reflect that.",
            "It does not bypass site OT security controls or connectivity limits; it reduces what has to travel.",
        ],
    },

    "architecture": {
        "current": {
            "title": "Conventional: ship complete site histories to the center",
            "zones": [
                {"id": "s1", "label": "Facility 1", "kind": "source",
                 "nodes": [["h1", "Site historian 1", "store"]]},
                {"id": "s2", "label": "Facility 2", "kind": "source",
                 "nodes": [["h2", "Site historian 2", "store"]]},
                {"id": "s3", "label": "Facility 3", "kind": "source",
                 "nodes": [["h3", "Site historian 3", "store"]]},
                {"id": "c", "label": "Central AI platform", "kind": "central",
                 "nodes": [["lake", "Pooled raw archives", "store"], ["ml", "Cross-site model training", "model"]]},
            ],
            "flows": [
                ["h1", "lake", "raw", "full archive"],
                ["h2", "lake", "raw", "full archive"],
                ["h3", "lake", "raw", "full archive"],
                ["lake", "ml", "raw", "mostly steady state"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill at each site, learn centrally",
            "zones": [
                {"id": "s1", "label": "Facility 1", "kind": "source",
                 "nodes": [["h1", "Site historian 1", "store"], ["g1", "GroundTruth runtime 1", "gt"]]},
                {"id": "s2", "label": "Facility 2", "kind": "source",
                 "nodes": [["h2", "Site historian 2", "store"], ["g2", "GroundTruth runtime 2", "gt"]]},
                {"id": "s3", "label": "Facility 3", "kind": "source",
                 "nodes": [["h3", "Site historian 3", "store"], ["g3", "GroundTruth runtime 3", "gt"]]},
                {"id": "c", "label": "Central AI platform", "kind": "central",
                 "nodes": [["ds", "Approved distilled sets", "store"], ["ml", "Cross-site model training", "model"]]},
            ],
            "flows": [
                ["h1", "g1", "raw", "stays on site"],
                ["h2", "g2", "raw", "stays on site"],
                ["h3", "g3", "raw", "stays on site"],
                ["g1", "ds", "distilled", "events + regimes kept"],
                ["g2", "ds", "distilled", "approved set"],
                ["g3", "ds", "distilled", "approved set"],
                ["ds", "ml", "distilled", ""],
                ["ml", "g2", "control", "shared task + coverage"],
            ],
        },
        "notes": [
            "Coverage targets are set per site: every labeled failure event and each identified operating "
            "regime is retained, so rare events are concentrated rather than diluted.",
            "Combining distilled sets from heterogeneous sites is an *architectural hypothesis not yet "
            "benchmarked*: distribution differences between facilities are measured explicitly in the pilot.",
        ],
    },

    "outcomes": {
        "direct": [
            "Less data transferred from facilities to the central platform per use case.",
            "Lower central storage and training compute for cross-site models, net of on-site distillation cost.",
            "Lower dependence on high-bandwidth links from remote facilities.",
        ],
        "operational": [
            "Data preparation runs where the data and the process knowledge are.",
            "New facilities join a shared model by adding a runtime, not a full archive migration.",
            "Fewer raw archive copies to secure and govern centrally.",
        ],
        "strategic": [
            "Multi-site predictive maintenance and shared equipment health models.",
            "Cross-facility anomaly detection that learns from failures wherever they occur.",
            "Centralized AI development without complete industrial data consolidation.",
        ],
    },

    "metrics": [
        ["Inter-site data transfer", "Volume moved from facilities to the center per month, before vs. after", "direct"],
        ["Central storage for training data", "TB held centrally for the use case", "direct"],
        ["Cross-site model performance", "Task metric overall and per facility on held-out full data", "quality"],
        ["Rare-event coverage", "Share of labeled failure events per site retained in distilled sets", "quality"],
        ["Operating-regime coverage", "Share of identified regimes per site represented", "quality"],
        ["Per-site performance gap", "Shared model vs. site-only model at each facility", "quality"],
        ["On-site distillation overhead", "Compute, time and energy per facility", "direct"],
        ["Participating facilities", "Number of sites contributing approved datasets", "strategic"],
        ["Time to onboard a new site", "Days from approval to first contributed dataset", "operational"],
    ],

    "stakeholders": {
        "sponsor": ["COO or VP of operations / reliability", "Wants fewer unplanned outages across the fleet of facilities."],
        "economic": ["CIO or head of industrial digitalization", "Owns central platform and connectivity costs across sites."],
        "technical": ["OT architect and enterprise architect", "Must validate on-site placement, transfer paths and the feature contract."],
        "operational": [
            ["Site managers and site OT teams", "Host the runtime; protect plant availability."],
            ["Reliability and maintenance engineering", "Define failure modes, labels and acceptance."],
            ["Central data science team", "Train and maintain the shared models."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used for per-site fidelity evaluation."],
            ["Historian extracts per site (CSV / Parquet)", "proposed", "File-based input; no direct historian connector exists yet."],
            ["Historian APIs (e.g. AVEVA PI), OPC UA, MQTT", "proposed", "Candidate connectors; not built or tested."],
            ["Site-to-center transfer (existing WAN, gateways)", "customer", "Customer-owned path; carries distilled files."],
            ["Central ML platform", "customer", "Trains shared models on combined distilled sets."],
        ],
        "infrastructure": [
            "One server or VM per participating facility in an authorized zone (CPU-first; sizing set in the pilot).",
            "Read access to historian extracts and maintenance or failure labels at each site.",
            "A central environment authorized to receive approved datasets.",
        ],
        "deployment": "A pilot typically covers two or three facilities with a common asset class. The "
                      "runtime runs offline against site exports; distilled datasets travel through existing "
                      "transfer paths. Fleet-wide orchestration and remote management of site runtimes are "
                      "proposed roadmap items.",
        "constraints": [
            "Tag, unit and asset-hierarchy mapping across sites must exist or be built for the pilot assets.",
            "Failure labels are sparse and inconsistent between sites; label quality bounds model quality.",
            "Industrial time-series distillation has not yet been benchmarked; the pilot is the first measurement.",
        ],
    },

    "evidence": {
        "status": "Proposed enterprise application — not yet validated in production",
        "summary": "Single-dataset benchmarks show large reductions with limited accuracy change. This "
                   "business case adds three untested elements: industrial time-series data, explicit "
                   "rare-event and regime coverage, and the combination of distilled sets from "
                   "heterogeneous sites, which is an architectural hypothesis not yet benchmarked.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "Distillation runs as a self-contained software step that can be executed independently at each site.",
        ],
        "gaps": [
            "No benchmark on industrial time-series or historian data.",
            "No study yet of rare-failure coverage after distillation.",
            "No experiment combining distilled sets from sites with different distributions (non-IID).",
            "No multi-site or production deployment completed.",
        ],
        "risks": [
            "A facility with unusual equipment or conditions may be poorly served by a shared model; per-site evaluation is mandatory.",
            "Rare failure modes may be lost if coverage constraints are not enforced.",
            "Site-by-site OT approvals can extend timelines.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One failure mode or anomaly-detection task on an asset class present at two or three facilities.",
        "inputs": [
            "12–36 months of historian data for the selected assets at each facility",
            "Maintenance, failure or event labels per site",
            "A mapping of tags and units across sites for the pilot assets",
            "A server per facility in an authorized zone",
        ],
        "baseline": "A cross-site model trained on pooled full data where feasible, and each site's own model trained on its full data.",
        "method": [
            "Distill at each site with agreed rare-event and regime coverage targets.",
            "Train the shared model on combined distilled sets; evaluate overall and per site on held-out full data.",
            "Compare against site-only models and, where available, a pooled full-data model.",
            "Measure transfer volume, central storage, training compute and on-site overhead.",
        ],
        "technical_criteria": [
            "Shared-model performance within the customer-defined tolerance of baseline at every site.",
            "All labeled failure events in the evaluation window retained in distilled sets.",
            "No change to OT network paths or control-system load at any site.",
        ],
        "economic_criteria": [
            "Inter-site transfer and central storage reduced by a customer-defined target.",
            "Net saving positive after on-site distillation overhead.",
        ],
        "deliverables": [
            "Per-site fidelity and coverage reports",
            "Shared-model evaluation, overall and per facility",
            "Measured transfer, storage, compute and energy comparison",
            "Fleet roll-out plan and risk register",
        ],
        "adoption": [
            "Technical and economic criteria met at every pilot site",
            "OT security approval of the site runtime pattern",
            "Tag-mapping and label ownership assigned",
            "Regeneration policy for process and equipment changes",
        ],
    },

    "caveats": [
        "Shared models must be evaluated per facility; an improvement on average can hide a degradation at one site.",
    ],
    "related": ["BC01", "BC05", "BC09"],
}
