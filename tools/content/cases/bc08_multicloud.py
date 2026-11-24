"""BC08 — Multicloud data optimization. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC08",
    "slug": "multicloud-data-optimization",
    "rank": 8,
    "tier": "explorer",
    "title": "Multicloud data optimization",
    "eyebrow": "Hybrid and multicloud estates",
    "headline": "Move training data between clouds by what the workload needs, not by the terabyte.",
    "summary": (
        "Generate workload-specific optimized datasets before authorized transfers between private "
        "infrastructure and cloud platforms, reducing duplication and transfer of large datasets."
    ),
    "problem_short": "AI workloads span private infrastructure and several clouds, forcing costly duplication and transfer of large training datasets.",
    "solution_short": "Distill at the source environment and transfer only the workload-specific dataset to the target platform.",
    "outcome_short": "Less data duplicated and moved between environments for AI workloads.",
    "cta": "Evaluate your intercloud data flows",
    "industries": ["financial-services", "retail-consumer", "ai-infrastructure", "multinational-groups"],
    "filters": {
        "objectives": ["data-movement", "replication", "distributed-infra", "training-cost"],
        "architecture": ["multicloud", "centralized-ml"],
        "deployment": ["private-cloud", "public-cloud", "hybrid"],
        "buyers": ["cio", "cto", "infra-leader", "enterprise-architect", "cfo"],
        "problems": ["raw-replication", "bandwidth", "storage-growth"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Enterprise data estates now span on-premises data centers, private clouds and several public "
        "cloud platforms. Data is often generated or held in one environment while the AI services, "
        "accelerators or teams that need it sit in another.",
        "The conventional answer is to replicate complete datasets to wherever training runs. Each copy "
        "incurs transfer and egress charges, ingestion and storage in the target platform, and another "
        "dataset to secure and keep in sync.",
        "As AI workloads move between providers for capacity, price or capability, the cost and "
        "complexity of moving data becomes a constraint on architectural choice.",
    ],

    "approaches": [
        {"name": "Replicate complete datasets to each platform",
         "limit": "Simplest for data science teams but multiplies egress, storage and synchronization effort for every copy."},
        {"name": "Query in place across clouds",
         "limit": "Avoids bulk copies for analytics, but training workloads read data repeatedly and cross-cloud reads "
                  "can be slow and charged per access."},
        {"name": "Consolidate on a single platform",
         "limit": "Removes cross-cloud movement but is a long migration program and reduces flexibility to use "
                  "capacity or services from other providers."},
        {"name": "Generic compression and deduplication",
         "limit": "Reduces bytes on the wire but is task-agnostic; most of the original volume still moves and must be stored."},
    ],

    "solution": {
        "intro": "GroundTruth AI inserts a distillation step before authorized transfers. In the environment where "
                 "the data resides, the engine produces a workload-specific training dataset and fidelity report. "
                 "Only that dataset is transferred to the target platform, through the customer's existing "
                 "transfer tooling. The full dataset stays in its home environment.",
        "steps": [
            ("Select the workload", "Identify a training workload that runs in a different environment from its data."),
            ("Distill at the source", "Run distillation in the source environment with customer-defined accuracy tolerances."),
            ("Validate", "Compare models trained on full and distilled data on the same held-out test set."),
            ("Transfer the distilled dataset", "Move only the approved dataset to the target platform through existing, authorized tooling."),
            ("Train and regenerate", "Train on the target platform; regenerate the dataset when the source data or task changes."),
        ],
        "not": [
            "It does not replace data integration, synchronization or master-data management between platforms.",
            "It does not change provider pricing; savings depend on the customer's actual transfer, storage and processing rates.",
            "Distilled datasets remain subject to the same security, residency and contractual controls as their source.",
        ],
    },

    "architecture": {
        "current": {
            "title": "Conventional: full datasets replicated to the training platform",
            "zones": [
                {"id": "src", "label": "Source environment", "kind": "source",
                 "nodes": [["data", "Enterprise datasets", "store"]]},
                {"id": "net", "label": "Intercloud transfer", "kind": "boundary",
                 "nodes": [["egress", "Egress / interconnect", "system"]]},
                {"id": "tgt", "label": "Target cloud platform", "kind": "central",
                 "nodes": [["copy", "Full replicated copy", "store"], ["ml", "Cloud ML training", "model"]]},
            ],
            "flows": [
                ["data", "egress", "raw", "complete dataset"],
                ["egress", "copy", "raw", "charged per GB"],
                ["copy", "ml", "raw", "kept in sync"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill before transfer, train on what the workload needs",
            "zones": [
                {"id": "src", "label": "Source environment", "kind": "source",
                 "nodes": [["data", "Enterprise datasets", "store"], ["gt", "GroundTruth distillation engine", "gt"]]},
                {"id": "net", "label": "Intercloud transfer", "kind": "boundary",
                 "nodes": [["egress", "Existing authorized transfer", "system"]]},
                {"id": "tgt", "label": "Target cloud platform", "kind": "central",
                 "nodes": [["ds", "Workload-specific dataset", "store"], ["ml", "Cloud ML training", "model"]]},
            ],
            "flows": [
                ["data", "gt", "raw", "stays at source"],
                ["gt", "egress", "distilled", "distilled + report"],
                ["egress", "ds", "distilled", "smaller transfer"],
                ["ds", "ml", "distilled", ""],
                ["ml", "gt", "control", "regeneration request"],
            ],
        },
        "notes": [
            "Distillation runs where the data resides, so its compute is billed in the source environment and "
            "must be included in the net calculation.",
            "The full dataset remains the system of record in its home environment.",
        ],
    },

    "outcomes": {
        "direct": [
            "Lower egress and interconnect charges for eligible training transfers.",
            "Less ingestion and storage in the target platform.",
            "Lower processing of training data in the target platform, net of source-side distillation cost.",
        ],
        "operational": [
            "Fewer full dataset replicas to secure and keep in sync.",
            "Faster provisioning of training data on a new platform.",
            "Simpler data lifecycle for cross-platform AI workloads.",
        ],
        "strategic": [
            "More freedom to place training workloads where capacity or services are best suited.",
            "Reduced dependence on large-scale migration programs for AI use cases.",
            "A consistent pattern for distributed AI infrastructure across providers.",
        ],
    },

    "metrics": [
        ["Intercloud transfer volume", "GB transferred per workload per cycle, before vs. after", "direct"],
        ["Egress and interconnect cost", "Charges attributable to training data transfers", "direct"],
        ["Target-platform storage", "TB stored for the workload in the target environment", "direct"],
        ["Source-side overhead", "Compute hours and cost of distillation in the source environment", "direct"],
        ["Model predictive performance", "Task metric on a held-out full-data test set", "quality"],
        ["Replicas under management", "Number of full dataset copies across environments", "operational"],
        ["Time to provision training data", "Hours from request to data available on target platform", "operational"],
        ["Workloads placed cross-platform", "Training workloads running outside their data's home environment", "strategic"],
    ],

    "stakeholders": {
        "sponsor": ["CIO or CTO", "Wants flexible AI placement without data duplication costs."],
        "economic": ["Infrastructure leader or cloud FinOps lead, with the CFO", "Owns egress, storage and cloud processing budgets."],
        "technical": ["Enterprise or cloud architect", "Must confirm placement of distillation and transfer paths."],
        "operational": [
            ["ML platform team", "Pipeline changes and model quality on distilled data."],
            ["Security and compliance", "Controls on each environment and transfer."],
            ["Data owners", "Approval of datasets leaving their home environment."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used for fidelity evaluation against full-data baselines."],
            ["Cloud object storage (e.g. S3, Azure Blob, GCS)", "proposed", "Candidate read/write connectors; not built or tested."],
            ["Spark / Databricks pipelines", "proposed", "Candidate integration for large datasets; not built."],
            ["Transfer and replication tooling", "customer", "Customer-owned; carries distilled datasets as files."],
            ["Target ML platforms", "customer", "Consume distilled datasets as ordinary training data."],
        ],
        "infrastructure": [
            "Compute in the source environment for distillation jobs.",
            "Read access to the source dataset for the selected workload.",
            "The existing authorized transfer path to the target platform.",
        ],
        "deployment": "For a pilot, distillation runs as a batch job in the source environment on exports of one "
                      "workload's training data. Native connectors for cloud storage and data platforms are "
                      "proposed roadmap items.",
        "constraints": [
            "Savings depend on the customer's negotiated transfer, storage and compute rates.",
            "Workloads that need the full dataset, such as exploratory analysis, are out of scope.",
            "Scaling to enterprise data volumes has not yet been benchmarked.",
        ],
    },

    "evidence": {
        "status": "Proposed enterprise application — not yet validated in production",
        "summary": "Internal experiments show large data reductions with limited accuracy change on public "
                   "benchmarks. The effect on intercloud transfer, storage and processing costs has not yet been "
                   "measured on a customer estate.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
        ],
        "gaps": [
            "No measurement of transfer or storage cost on customer multicloud infrastructure.",
            "No benchmark at enterprise data volumes.",
            "No native connectors for cloud storage or data platforms built yet.",
            "No production deployment.",
        ],
        "risks": [
            "Distillation compute in the source environment may offset transfer savings for infrequent transfers.",
            "Workloads may require regeneration more often than expected if source data changes rapidly.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One training workload whose data is replicated from its home environment to another platform.",
        "inputs": [
            "The source dataset and the current replication process",
            "Current transfer, storage and processing costs for the workload",
            "The training pipeline and evaluation metric on the target platform",
            "Compute in the source environment",
        ],
        "baseline": "The current workload trained on the full replicated dataset.",
        "method": [
            "Train on full and distilled data; evaluate both on the same held-out test set.",
            "Measure transfer volume, egress cost, target storage and processing for both paths.",
            "Measure source-side distillation compute and cost.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of baseline.",
            "Distilled datasets transfer through existing tooling without changes to controls.",
        ],
        "economic_criteria": [
            "Transfer and target-platform storage reduced by a customer-defined target.",
            "Net saving positive after source-side overhead at the customer's transfer frequency.",
        ],
        "deliverables": [
            "Fidelity report",
            "Transfer, storage, processing and overhead comparison at the customer's rates",
            "Assessment of other eligible cross-platform workloads",
            "Production adoption plan",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Security and data owner approval",
            "Agreed regeneration policy",
        ],
    },

    "caveats": [
        "Savings estimates use the customer's own transfer, storage and compute rates; GroundTruth AI does not "
        "assume provider pricing.",
    ],
    "related": ["BC06", "BC07", "BC03"],
}
