"""BC02 — Cross-enterprise analytics. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC02",
    "slug": "cross-enterprise-analytics",
    "rank": 2,
    "tier": "flagship",
    "title": "Cross-enterprise analytics",
    "eyebrow": "Distributed data estates",
    "headline": "Build group-wide models without first consolidating every subsidiary's data.",
    "summary": (
        "Generate task-specific distilled datasets inside each authorized data domain and combine "
        "the approved datasets for central analytics and AI training, while data ownership stays distributed."
    ),
    "problem_short": "Group-wide analytics stall because subsidiaries, regions and business units hold data in separate, separately governed estates.",
    "solution_short": "Each domain distills a task-specific dataset in place; only approved distilled sets are combined centrally for training.",
    "outcome_short": "Enterprise-wide predictive models without a complete data consolidation program.",
    "cta": "Evaluate your distributed data environments",
    "industries": ["financial-services", "healthcare", "multinational-groups"],
    "filters": {
        "objectives": ["segregated-analytics", "replication", "data-movement", "operational-efficiency"],
        "architecture": ["multi-domain", "multi-jurisdiction", "centralized-ml"],
        "deployment": ["private-cloud", "hybrid", "on-prem"],
        "buyers": ["cdo", "cio", "enterprise-architect", "ml-platform"],
        "problems": ["consolidation-blocked", "raw-replication", "cross-border"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Large organizations rarely have one data estate. Subsidiaries, business units, regions and "
        "acquired companies each run their own platforms, with their own data owners, retention rules, "
        "security models and, often, their own regulators. That separation is usually deliberate: it "
        "reflects legal entities, accountability and risk boundaries.",
        "Yet the most valuable analytical questions are group-wide: customer behavior across brands, "
        "risk across portfolios, demand across regions, outcomes across clinical sites. The default "
        "answer is a consolidation program: replicate everything into a central lake or warehouse, "
        "harmonize it, then start modeling. Those programs are expensive, slow to approve and frequently "
        "constrained by governance policies that do not permit full replication in the first place.",
        "Analytical ambition ends up waiting for data architecture, and many cross-business use cases "
        "never reach the evaluation stage.",
    ],

    "approaches": [
        {"name": "Full consolidation into a central lake or warehouse",
         "limit": "Delivers one place to model, but requires replicating complete datasets, multi-year "
                  "integration effort and approvals from every data owner. Policy may simply not allow it."},
        {"name": "Data virtualization or federated query",
         "limit": "Avoids copies for reporting, but ML training needs repeated full scans of large "
                  "datasets across domains, which shifts cost and latency onto source systems."},
        {"name": "Separate models per subsidiary",
         "limit": "Respects ownership but produces many small models, duplicated effort and no "
                  "group-wide view of patterns that only appear across entities."},
        {"name": "Federated learning",
         "limit": "Keeps data in place but needs training infrastructure, orchestration and ML "
                  "operations inside every domain, plus a coordinated model-exchange process that "
                  "many organizations are not yet equipped to run."},
    ],

    "solution": {
        "intro": "GroundTruth AI changes what has to move. Within each authorized data domain, a "
                 "distillation runtime builds a compact dataset for one defined analytical task and "
                 "validates it against that domain's full data. Data owners approve what leaves; the "
                 "central team combines the approved distilled datasets and trains group-wide models.",
        "steps": [
            ("Agree the shared task", "Group analytics and domain data owners define the target model, "
             "a common feature contract and acceptance thresholds before any data moves."),
            ("Distill in each domain", "The runtime runs inside each subsidiary's or region's environment "
             "and produces a task-specific distilled dataset. Source data stays where it is owned."),
            ("Validate locally", "Each domain receives a fidelity report: a model trained on its distilled "
             "set compared with one trained on its full data."),
            ("Approve and combine", "Domain owners approve release under their own policies; approved "
             "datasets are combined in the central environment."),
            ("Train and evaluate centrally", "The central team trains the group-wide model and evaluates "
             "it on held-out data from each domain, so no domain is silently under-served."),
        ],
        "not": [
            "It does not harmonize schemas or master data: a shared feature contract is a prerequisite.",
            "It does not anonymize data or authorize any transfer; distilled sets keep the source data's obligations.",
            "It does not replace a data integration strategy where full integration is the right answer.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "International financial group",
        "context": "A financial group operates banks, an insurer and payment businesses in several jurisdictions, each with its own data environment, governance and supervisors.",
        "current": "Each entity trains its own fraud and risk models on its own data. Group analytics rely on aggregated reporting; complete data replication between entities is restricted by privacy law, contracts and internal policy.",
        "problem": "The group wants selected shared fraud-detection or risk models that learn from patterns visible across entities. Replicating complete transaction histories into a group platform is slow to authorize and often not permitted.",
        "proposed": "Each entity distills a task-specific training dataset inside its own environment. Legal and data protection teams decide, dataset by dataset, whether it may be shared. Where it may, the group trains a shared model and each entity validates it on its own data.",
        "assumptions": [],
        "constraints": [
            "Minority-class performance: fraud is rare, so positive cases must be preserved",
            "Privacy restrictions: distilled data derived from personal data must be treated as personal data unless shown otherwise",
            "Transfer authorization is decided by legal and data protection functions, case by case",
            "Each entity remains the owner of its source data and its distilled dataset",
            "Distributional heterogeneity between entities, products and countries",
        ],
        "economic": [
            "Less complete-data replication into group platforms for the selected models",
            "Lower central training compute",
        ],
        "strategic": [
            "Group-wide fraud and risk models that see cross-entity patterns",
            "A shorter path from analytical idea to an authorized dataset",
            "Entity-level data ownership preserved",
        ],
        "validation": [
            "Recall and precision on the minority class, per entity",
            "Performance under distribution differences between entities",
            "Privacy and re-identification risk review of each distilled dataset",
            "A documented legal basis for every transfer",
        ],
        "stakeholder": "Chief Data Officer, with the group CRO and the data protection officer",
    },

    "architecture": {
        "current": {
            "title": "Conventional: consolidate every domain before modeling",
            "zones": [
                {"id": "a", "label": "Subsidiary A", "kind": "source",
                 "nodes": [["dba", "Operational data A", "store"]]},
                {"id": "b", "label": "Subsidiary B / region B", "kind": "source",
                 "nodes": [["dbb", "Operational data B", "store"]]},
                {"id": "int", "label": "Consolidation program", "kind": "boundary",
                 "nodes": [["etl", "Full replication + ETL", "system"]]},
                {"id": "grp", "label": "Group data platform", "kind": "central",
                 "nodes": [["lake", "Consolidated raw copy", "store"], ["ml", "Group-wide model training", "model"]]},
            ],
            "flows": [
                ["dba", "etl", "raw", "complete dataset"],
                ["dbb", "etl", "raw", "complete dataset"],
                ["etl", "lake", "raw", "all records, all fields"],
                ["lake", "ml", "raw", ""],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill per domain, combine approved sets",
            "zones": [
                {"id": "a", "label": "Subsidiary A", "kind": "source",
                 "nodes": [["dba", "Operational data A", "store"], ["gta", "GroundTruth runtime A", "gt"]]},
                {"id": "b", "label": "Subsidiary B / region B", "kind": "source",
                 "nodes": [["dbb", "Operational data B", "store"], ["gtb", "GroundTruth runtime B", "gt"]]},
                {"id": "gov", "label": "Domain approval", "kind": "boundary",
                 "nodes": [["appr", "Data-owner approval", "system"]]},
                {"id": "grp", "label": "Group analytics environment", "kind": "central",
                 "nodes": [["ds", "Combined distilled datasets", "store"], ["ml", "Group-wide model training", "model"]]},
            ],
            "flows": [
                ["dba", "gta", "raw", "stays in domain"],
                ["dbb", "gtb", "raw", "stays in domain"],
                ["gta", "appr", "distilled", "distilled set A + report"],
                ["gtb", "appr", "distilled", "distilled set B + report"],
                ["appr", "ds", "distilled", "approved only"],
                ["ds", "ml", "distilled", ""],
                ["ml", "appr", "control", "shared task specification"],
            ],
        },
        "notes": [
            "Each runtime operates under the governance of the domain that hosts it; the central team "
            "never receives credentials to source systems.",
            "Combining distilled sets from heterogeneous domains is an *architectural hypothesis not yet "
            "benchmarked*: differences in populations and distributions between domains are measured "
            "explicitly in the pilot.",
        ],
    },

    "outcomes": {
        "direct": [
            "Less data replicated into central platforms for each group-wide use case.",
            "Lower central storage, ingestion and training compute for those use cases, net of in-domain distillation cost.",
            "Smaller transfers between domains and the central environment.",
        ],
        "operational": [
            "Analytical projects start before, or without, a full consolidation program.",
            "Fewer raw copies of subsidiary data to secure, catalog and retire.",
            "One repeatable release pattern that each data owner can approve under existing policy.",
        ],
        "strategic": [
            "Group-wide predictive models that reflect patterns across entities, not one entity at a time.",
            "Distributed data ownership preserved as a design principle rather than an obstacle.",
            "Analytical collaboration across organizational boundaries that was previously not attempted.",
        ],
    },

    "metrics": [
        ["Data replicated per use case", "Volume moved from domains to the central environment, before vs. after", "direct"],
        ["Central training-data storage", "TB held centrally for the use case", "direct"],
        ["Training compute per run", "CPU/GPU hours and cost per group-wide training run", "direct"],
        ["Group model performance", "Task metric on held-out full data, overall and per domain", "quality"],
        ["Per-domain performance gap", "Difference between group model and domain-only model in each domain", "quality"],
        ["In-domain distillation overhead", "Compute, time and energy consumed in each domain", "direct"],
        ["Participating data domains", "Number of domains contributing approved datasets", "strategic"],
        ["Time to first group-wide model", "Weeks from use-case approval to a validated model", "operational"],
        ["Approval cycle time", "Days for a domain owner to review and release a distilled set", "operational"],
    ],

    "stakeholders": {
        "sponsor": ["Chief Data Officer or group head of analytics", "Wants group-wide insight without waiting for full consolidation."],
        "economic": ["CIO or group CFO", "Funds the data platform and consolidation budget; needs a lower-cost route to cross-business value."],
        "technical": ["Enterprise architect and head of ML platform", "Must confirm the runtime fits each domain's environment and the feature contract is workable."],
        "operational": [
            ["Domain data owners", "Control what leaves their environment and under which conditions."],
            ["Data protection and compliance officers", "Assess legal basis and transfer rules for distilled sets."],
            ["Subsidiary IT teams", "Host and operate the runtime within local standards."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used for fidelity evaluation against each domain's full-data baseline."],
            ["Domain warehouse or lake extracts (CSV / Parquet)", "proposed", "File-based input per domain; no direct database connectors exist yet."],
            ["Spark / Databricks or Snowflake connectors", "proposed", "Candidate connectors; not built or tested."],
            ["Data catalog and approval workflow", "customer", "Customer-owned release process; GroundTruth AI supplies dataset and report."],
            ["Central ML platform", "customer", "Consumes combined distilled datasets as ordinary training data."],
        ],
        "infrastructure": [
            "One VM or container host inside each participating domain (CPU-first; sizing set in the pilot).",
            "Read access to an extract of the agreed features in each domain.",
            "A central environment authorized to receive the approved distilled datasets.",
        ],
        "deployment": "A pilot typically involves two or three domains. The runtime is installed in each "
                      "domain's environment and run against agreed extracts; distilled datasets are released "
                      "through the customer's existing approval and transfer process. Automated, scheduled "
                      "multi-domain orchestration is a proposed roadmap item.",
        "constraints": [
            "A common feature contract across domains is required; semantic differences are not resolved by distillation.",
            "Distribution differences between domains may require per-domain coverage targets.",
            "Legal review of each transfer remains necessary and can set the pilot's critical path.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "The single-dataset results are encouraging: large reductions with limited accuracy "
                   "change on public benchmarks. The cross-enterprise pattern adds an untested step, "
                   "combining distilled sets produced independently in heterogeneous domains, which is "
                   "an architectural hypothesis the pilot is designed to test.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "Distillation runs as a self-contained software step, so it can be executed separately inside each domain.",
        ],
        "gaps": [
            "Combining distilled sets from heterogeneous domains has not been benchmarked (non-IID data).",
            "No measurement yet of per-domain performance gaps in a combined model.",
            "No enterprise-scale or multi-domain deployment completed.",
            "No legal or privacy assessment of distilled datasets in a real governance setting.",
        ],
        "risks": [
            "A domain with a distinct population may be under-represented in the group model unless its performance is tracked separately.",
            "Approval processes across several data owners can extend timelines beyond the technical work.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One group-wide predictive or analytical model that today requires consolidating data from two or three domains.",
        "inputs": [
            "An extract of the agreed features in each participating domain",
            "A shared target definition and feature contract",
            "Where permitted, a consolidated full-data baseline or a per-domain baseline",
            "A host in each domain and a central environment for the combined set",
        ],
        "baseline": "The same model trained on consolidated full data where allowed; otherwise per-domain models trained on each domain's full data.",
        "method": [
            "Distill independently in each domain against the shared task.",
            "Train the group model on combined distilled sets; evaluate overall and per domain on held-out full data.",
            "Measure replicated volume, central storage and training compute against the baseline path.",
            "Record in-domain overhead and the approval cycle time for each release.",
        ],
        "technical_criteria": [
            "Group model performance within the customer-defined tolerance of baseline.",
            "No participating domain below its agreed per-domain threshold.",
            "Distilled releases approved by each data owner under existing policy.",
        ],
        "economic_criteria": [
            "Replicated volume and central storage reduced by a customer-defined target.",
            "Net saving positive after in-domain distillation overhead.",
        ],
        "deliverables": [
            "Per-domain fidelity reports and combined-model evaluation",
            "Measured comparison of replication, storage and compute",
            "Reference architecture and release workflow for the customer's domains",
            "Production adoption plan, including legal and governance checkpoints",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Legal and data-protection sign-off on the release pattern",
            "Data-owner agreement to a recurring approval workflow",
            "Feature contract owned and maintained by a named team",
        ],
    },

    "caveats": [
        "Distilled datasets remain subject to the data protection, residency, contractual and transfer "
        "rules that apply to the source data. Distillation is not anonymization and does not authorize transfers.",
    ],
    "related": ["BC07", "BC11", "BC01"],
}
