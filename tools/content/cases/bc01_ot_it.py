"""BC01 — OT/IT data segregation.

This file is also the schema exemplar for every business case. Rules:
- Plain strings only. Inline markup allowed: **bold** and *italic*. No HTML.
- Keep every key, in this order. Lists may vary in length within the stated ranges.
- Architecture diagrams use the small DSL documented under "architecture".
"""

CASE = {
    "id": "BC01",
    "slug": "ot-it-data-segregation",
    "rank": 1,                       # commercial priority (CONTENT_BRIEF §5)
    "tier": "flagship",              # "flagship" | "explorer"
    "title": "OT/IT data segregation",
    "eyebrow": "Industrial data architecture",
    "headline": "Train enterprise AI on plant data without replicating the plant into IT.",
    "summary": (
        "Distill task-relevant training data inside the authorized OT environment and move only "
        "approved, optimized datasets across the OT/IT boundary for central model training."
    ),
    # Card copy (one sentence each, <= 160 characters)
    "problem_short": "Central AI programs need plant data, but replicating full OT histories into IT erodes segregation and multiplies infrastructure.",
    "solution_short": "Task-aware distillation runs source-side, in the OT environment; only approved distilled datasets cross the boundary.",
    "outcome_short": "Centralized industrial AI training without centralizing all raw OT data.",
    "cta": "Request an OT/IT data efficiency pilot",
    "industries": ["manufacturing", "energy-utilities", "oil-gas-mining", "transportation-logistics"],
    "filters": {
        "objectives": ["segregated-analytics", "data-movement", "replication", "distributed-infra"],
        "architecture": ["ot-it", "multi-site", "centralized-ml"],
        "deployment": ["on-prem", "hybrid"],
        "buyers": ["cio", "coo", "ot-leader", "enterprise-architect"],
        "problems": ["raw-replication", "bandwidth", "storage-growth"],
    },
    "roi_scenario": "transfer",

    # 1. Business challenge — 2–3 paragraphs
    "challenge": [
        "Industrial enterprises keep Operational Technology (OT) and Information Technology (IT) "
        "environments apart for good reasons: safety, availability, cybersecurity, vendor support "
        "obligations and clear operational accountability. Plant historians, SCADA systems and "
        "control networks sit behind segmented zones, industrial DMZs and, in some sites, "
        "one-way gateways.",
        "Enterprise AI programs pull in the opposite direction. Predictive maintenance, quality "
        "and energy models are usually trained centrally, on IT or cloud platforms, and the "
        "conventional workflow asks for large volumes of raw sensor history to be copied across "
        "the boundary first. Each new use case adds another replication path, another landing "
        "zone and another copy to secure, store and govern.",
        "The result is a recurring trade-off between the architecture the plant needs and the "
        "data volume the central AI team asks for.",
    ],

    # 2. Why existing approaches are insufficient — 3–5 items (no named competitors)
    "approaches": [
        {"name": "Replicate full OT history into the data lake",
         "limit": "Maximizes data availability but multiplies boundary traffic, central storage and "
                  "the number of raw copies under governance. Much of the replicated volume is never "
                  "used by the models it was copied for."},
        {"name": "Rule-based down-sampling or aggregation at the edge",
         "limit": "Cheap and predictable, but task-agnostic: averaging and fixed sampling rates can "
                  "remove exactly the transients and rare operating states a predictive model needs."},
        {"name": "Train models locally at each site",
         "limit": "Keeps data in place but fragments the model estate, duplicates ML skills and "
                  "compute at every plant and makes cross-site learning difficult."},
        {"name": "Federated learning",
         "limit": "Avoids moving data but requires training infrastructure and orchestration inside "
                  "each OT environment and a sustained, bidirectional model-exchange channel across "
                  "the boundary, which many OT security policies do not allow."},
    ],

    # 3. GroundTruth AI solution
    "solution": {
        "intro": "GroundTruth AI moves the data-reduction step to the source. A distillation runtime "
                 "deployed in an authorized zone on the OT side builds a compact training dataset "
                 "for a specific modeling task, validates it against the full data, and hands it to "
                 "the existing, approved transfer path. Central teams train on the distilled dataset.",
        "steps": [
            ("Define the task", "The central AI team and plant engineering agree the target model, "
             "the variables and the acceptance thresholds (for example, maximum accuracy loss and "
             "minimum coverage of known failure modes)."),
            ("Distill at the source", "The runtime reads historian extracts inside the OT environment "
             "and generates a task-specific distilled dataset. Raw data never leaves its zone."),
            ("Validate fidelity", "A fidelity report compares models trained on full and distilled data "
             "and checks coverage of operating regimes and labeled events."),
            ("Approve and transfer", "OT and data owners approve the dataset; it crosses the boundary "
             "through the existing DMZ or gateway path, under existing controls."),
            ("Train centrally", "Data science teams train and iterate on central platforms with a "
             "fraction of the original volume, and request regeneration when the task changes."),
        ],
        "not": [
            "It does not replace network segmentation, firewalls, data diodes or OT security controls.",
            "It does not open new connections into control networks; it uses transfer paths the customer already authorizes.",
            "A distilled dataset is still plant data and stays under the customer's classification and transfer rules.",
        ],
    },

    # 4. Reference architecture — DSL
    #   zones: ordered left→right. kind: "source" | "boundary" | "central" | "external"
    #   nodes: [id, label, kind]  kind: "system" | "store" | "gt" (GroundTruth component) | "model" | "user"
    #   flows: [from_id, to_id, kind, label]  kind: "raw" | "distilled" | "model" | "control"
    "architecture": {
        "current": {
            "title": "Conventional: raw OT history replicated into IT",
            "zones": [
                {"id": "ot", "label": "OT zone · plant network", "kind": "source",
                 "nodes": [["hist", "Plant historian", "store"], ["scada", "SCADA / PLC signals", "system"]]},
                {"id": "dmz", "label": "Industrial DMZ", "kind": "boundary",
                 "nodes": [["rep", "Replication gateway", "system"]]},
                {"id": "it", "label": "Enterprise IT / cloud", "kind": "central",
                 "nodes": [["lake", "Raw data lake copy", "store"], ["ml", "Central ML training", "model"]]},
            ],
            "flows": [
                ["scada", "hist", "raw", "continuous"],
                ["hist", "rep", "raw", "full history"],
                ["rep", "lake", "raw", "TBs / month"],
                ["lake", "ml", "raw", "all features"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill in OT, transfer approved datasets",
            "zones": [
                {"id": "ot", "label": "OT zone · plant network", "kind": "source",
                 "nodes": [["hist", "Plant historian", "store"], ["gt", "GroundTruth distillation runtime", "gt"]]},
                {"id": "dmz", "label": "Industrial DMZ", "kind": "boundary",
                 "nodes": [["appr", "Approval + existing transfer path", "system"]]},
                {"id": "it", "label": "Enterprise IT / cloud", "kind": "central",
                 "nodes": [["ds", "Distilled dataset store", "store"], ["ml", "Central ML training", "model"]]},
            ],
            "flows": [
                ["hist", "gt", "raw", "stays in zone"],
                ["gt", "appr", "distilled", "distilled set + fidelity report"],
                ["appr", "ds", "distilled", "approved only"],
                ["ds", "ml", "distilled", ""],
                ["ml", "gt", "control", "task spec / regeneration request"],
            ],
        },
        "notes": [
            "The distillation runtime is deployed in a zone the OT owner authorizes (typically level 3 "
            "or the site operations zone), not on control-level devices.",
            "Only the distilled dataset and its fidelity report cross the boundary; task specifications "
            "flow inward through the customer's existing change process.",
        ],
    },

    # 5. Business outcomes — separate direct savings from new capabilities
    "outcomes": {
        "direct": [
            "Less data replicated across the OT/IT boundary for each modeling use case.",
            "Lower central storage and ingestion for training data.",
            "Lower central compute per training run, net of source-side distillation cost.",
        ],
        "operational": [
            "Existing segregation architecture preserved: no new raw data paths into IT.",
            "Fewer raw copies to secure, catalog and retire.",
            "Faster onboarding of new plant use cases, because datasets are smaller and task-specific.",
        ],
        "strategic": [
            "Central AI training on industrial data without centralizing all raw OT data.",
            "A repeatable pattern for enterprise-wide industrial intelligence across plants.",
            "Use cases previously blocked by data-transfer policy become candidates for evaluation.",
        ],
    },

    # 6. Quantifiable business metrics — 6–10: [metric, how it is measured, category]
    #    category: "direct" | "operational" | "strategic" | "quality"
    "metrics": [
        ["Boundary transfer volume per use case", "GB/TB crossing the DMZ per month, before vs. after", "direct"],
        ["Central storage for training data", "TB held in IT/cloud for the use case", "direct"],
        ["Training compute per run", "GPU/CPU hours and cost per training run", "direct"],
        ["Model predictive performance", "Task metric (e.g. F1, MAE) on a held-out full-data test set", "quality"],
        ["Rare-event coverage", "Share of labeled failure modes and operating regimes represented", "quality"],
        ["Source-side overhead", "CPU hours, memory and energy consumed by distillation in OT", "direct"],
        ["Raw data copies under governance", "Number of raw replicas of OT data outside the OT zone", "operational"],
        ["Time to first trained model", "Days from use-case approval to a validated model", "operational"],
        ["Participating plants / data domains", "Sites contributing approved datasets", "strategic"],
    ],

    # 7. Target stakeholders
    "stakeholders": {
        "sponsor": ["COO or industrial digitalization leader", "Wants plant AI at scale without new operational risk."],
        "economic": ["CIO", "Owns central data platform and transfer costs; needs a governed pattern that scales."],
        "technical": ["OT architect and enterprise architect", "Must confirm the runtime fits the zone model and transfer controls."],
        "operational": [
            ["Plant / site operations", "Availability of the OT environment; no load on control systems."],
            ["OT security (CISO office)", "Placement, hardening and change control of the runtime."],
            ["Central data science team", "Model quality on distilled data; regeneration turnaround."],
        ],
    },

    # 8. Implementation approach
    "implementation": {
        "integration_points": [
            # [name, status, note]  status: "verified" | "proposed" | "customer"
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to evaluate fidelity against a full-data baseline."],
            ["Historian extracts (CSV / Parquet export)", "proposed", "File-based hand-off from the historian; no direct historian connector exists yet."],
            ["Industrial historian APIs (e.g. AVEVA PI) and OPC UA", "proposed", "Candidate connectors; not built or tested."],
            ["Existing DMZ transfer tooling / data diode", "customer", "Customer-owned path; GroundTruth AI produces files it can carry."],
            ["Central ML platform (e.g. Databricks, Azure ML, SageMaker)", "customer", "Consumes the distilled dataset as ordinary training data."],
        ],
        "infrastructure": [
            "One server or VM in the authorized OT-side zone (CPU-first; sizing set during the pilot).",
            "Read access to historian extracts for the pilot variables.",
            "An approved outbound transfer path for files.",
        ],
        "deployment": "For a pilot, the runtime is installed on a customer-provided server in the OT-side "
                      "zone and operated offline from historian exports. Packaging as a hardened container "
                      "or appliance for production is a proposed roadmap item, scoped with the customer's "
                      "OT security team.",
        "constraints": [
            "Industrial time-series distillation has not yet been benchmarked; the pilot is the first measurement.",
            "Labels for failure modes are often sparse; coverage targets must be agreed up front.",
            "Change-control windows in OT can lengthen installation timelines.",
        ],
    },

    # 9. Evidence
    "evidence": {
        "status": "Proposed enterprise application — not yet validated in production",
        "summary": "Internal experiments show large data reductions with limited accuracy change on public "
                   "benchmarks. Whether the same holds for industrial sensor time series, and for "
                   "multi-variable failure prediction, is what an OT/IT pilot is designed to establish.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "Distillation runs as a software step on a standard Python runtime, which is compatible with an offline, file-based OT deployment.",
        ],
        "gaps": [
            "No benchmark yet on industrial time-series or historian data.",
            "No measurement yet of rare-failure coverage after distillation.",
            "No measured source-side compute and energy overhead on OT-zone hardware.",
            "No production deployment or OT security assessment completed.",
        ],
        "risks": [
            "Distillation may under-represent rare operating states unless coverage constraints are enforced.",
            "OT security approval of a new software component can delay or block deployment.",
        ],
    },

    # 10. Pilot proposal
    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One predictive-maintenance or quality model that today requires a raw historian copy in IT.",
        "inputs": [
            "6–24 months of historian data for the selected assets, exported in the OT zone",
            "Failure, maintenance or quality labels where available",
            "The current central training pipeline and its evaluation metric",
            "A server in the authorized OT-side zone",
        ],
        "baseline": "The existing model trained centrally on the full replicated dataset.",
        "method": [
            "Train the same model on full and distilled data; evaluate both on the same held-out full-data test set.",
            "Measure transfer volume, central storage and training compute for both paths.",
            "Measure source-side distillation time, compute and energy.",
            "Review placement and controls with OT security.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of baseline (agreed before the pilot).",
            "All labeled failure modes in the test window represented in the distilled set.",
            "No change to OT network paths or control-system load.",
        ],
        "economic_criteria": [
            "Boundary transfer and central training-data storage reduced by a customer-defined target.",
            "Net saving remains positive after source-side overhead.",
        ],
        "deliverables": [
            "Fidelity report (full vs. distilled), including coverage analysis",
            "Measured transfer, storage, compute and energy comparison",
            "Reference architecture for the customer's zone model",
            "Production adoption plan and risk register",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "OT security approval of runtime placement and packaging",
            "Data owner sign-off on the approval workflow",
            "Named owner for regeneration when the task or process changes",
        ],
    },

    # Highlighted qualifications shown as a callout
    "caveats": [
        "Distilled datasets derived from OT data remain subject to the customer's data classification, "
        "export-control and transfer policies.",
    ],
    "related": ["BC04", "BC05", "BC02"],
}
