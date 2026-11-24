"""BC06 — AI infrastructure and data center efficiency. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC06",
    "slug": "ai-infrastructure-efficiency",
    "rank": 9,
    "tier": "explorer",
    "title": "AI infrastructure and data center efficiency",
    "eyebrow": "Infrastructure economics",
    "headline": "Do more AI work per server, per terabyte and per kilowatt-hour.",
    "summary": (
        "Reduce the volume of eligible training datasets and the compute they drive, so existing AI "
        "infrastructure supports more workloads, measured net of the cost of distillation itself."
    ),
    "problem_short": "Enterprise AI workloads consume growing storage, compute and energy, and much of that capacity is spent on redundant training data.",
    "solution_short": "Task-aware distillation shrinks eligible training datasets and the compute that scales with them.",
    "outcome_short": "Better utilization of AI infrastructure for eligible workloads, net of distillation overhead.",
    "cta": "Assess your AI infrastructure efficiency",
    "industries": ["ai-infrastructure", "telecommunications", "financial-services"],
    "filters": {
        "objectives": ["training-cost", "distributed-infra", "energy", "operational-efficiency"],
        "architecture": ["centralized-ml", "multicloud"],
        "deployment": ["on-prem", "private-cloud", "public-cloud"],
        "buyers": ["infra-leader", "cio", "cto", "cfo"],
        "problems": ["storage-growth", "training-spend", "energy-footprint"],
    },
    "roi_scenario": "infrastructure",

    "challenge": [
        "AI workloads are among the fastest-growing consumers of enterprise compute, storage and power. "
        "GPU clusters, high-performance storage tiers and the cooling that supports them are expensive to "
        "expand, and in many facilities power and rack capacity, not budget, set the ceiling.",
        "A large share of this capacity is consumed by training and retraining on datasets that contain "
        "substantial redundancy. Every redundant record is stored on fast tiers, read on every epoch and "
        "processed on every training run.",
        "Infrastructure leaders are asked to support more models with the same footprint, while finance "
        "and sustainability teams ask for clearer economics per workload.",
    ],

    "approaches": [
        {"name": "Add capacity",
         "limit": "Buys headroom but increases capital, power and cooling commitments, and is constrained "
                  "where facility power or hardware supply is the limit."},
        {"name": "Scheduling and utilization tuning",
         "limit": "Improves how capacity is shared but does not reduce the work each training job performs."},
        {"name": "Storage tiering and lifecycle policies",
         "limit": "Lowers the cost of cold data but does not reduce the data that active training jobs read repeatedly."},
        {"name": "Model compression and efficient architectures",
         "limit": "Reduces model size and inference cost; training data volume, and the compute it drives, often remains unchanged. "
                  "These techniques are complementary to dataset reduction."},
    ],

    "solution": {
        "intro": "GroundTruth AI reduces the data side of eligible AI workloads. For training and retraining "
                 "jobs where dataset volume drives compute and storage, the distillation engine produces a "
                 "validated, task-specific dataset that replaces the full dataset in the training pipeline. "
                 "The saving is assessed per workload, after subtracting the compute, energy and operational "
                 "cost of running distillation.",
        "steps": [
            ("Identify eligible workloads", "Select recurring training jobs where data volume is a material "
             "driver of compute, storage or energy."),
            ("Distill per task", "Generate a distilled dataset for each selected workload, with customer-defined "
             "accuracy tolerances."),
            ("Validate", "Compare models trained on full and distilled data on the same held-out test set."),
            ("Substitute in the pipeline", "Point the training job at the distilled dataset; keep the full dataset "
             "under existing retention policy."),
            ("Measure net effect", "Track storage, GPU/CPU hours and energy per workload, including distillation overhead."),
        ],
        "not": [
            "Dataset reduction does not translate into an equivalent reduction in total data center spend; only the data-proportional share of eligible workloads is affected.",
            "It does not reduce inference, networking or facility overhead costs that are independent of training data volume.",
            "It does not replace capacity planning, scheduling or hardware efficiency programs.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Enterprise private AI platform",
        "context": "An enterprise runs a private AI platform in its own data centers, shared by dozens of teams.",
        "current": "Training datasets are stored with backups and replicas, and training jobs compete for the same capacity.",
        "problem": "Storage, compute and energy demand grow with data volume, and capacity requests outpace budgets.",
        "proposed": "Eligible workloads train on validated distilled datasets, and the capacity they no longer use is reallocated. Source data is retained under existing policies.",
        "assumptions": [],
        "constraints": [
            "Only eligible, data-proportional workloads are affected",
            "Distillation itself consumes compute and energy",
        ],
        "economic": [
            "Less storage for eligible central training copies",
            "Less data-proportional compute for eligible workloads",
        ],
        "strategic": [
            "Capacity expansion deferred for eligible workloads",
        ],
        "validation": [
            "Utilization measured before and after on the same workloads",
            "Energy measured including distillation",
            "Model quality within tolerance",
        ],
        "stakeholder": "Head of infrastructure and data centers",
    },

    "architecture": {
        "current": {
            "title": "Conventional: every training run reads the full dataset",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["raw", "Full training datasets", "store"], ["hot", "High-performance storage tier", "store"]]},
                {"id": "compute", "label": "AI compute cluster", "kind": "central",
                 "nodes": [["train", "GPU training jobs", "model"], ["retrain", "Scheduled retraining", "model"]]},
                {"id": "fac", "label": "Facility", "kind": "external",
                 "nodes": [["power", "Power and cooling", "system"]]},
            ],
            "flows": [
                ["raw", "hot", "raw", "full copy staged"],
                ["hot", "train", "raw", "every epoch"],
                ["hot", "retrain", "raw", "every cycle"],
                ["train", "power", "control", "load scales with data"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: eligible jobs train on distilled datasets",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["raw", "Full training datasets", "store"], ["gt", "GroundTruth distillation engine", "gt"]]},
                {"id": "compute", "label": "AI compute cluster", "kind": "central",
                 "nodes": [["ds", "Distilled datasets (hot tier)", "store"], ["train", "Training and retraining jobs", "model"]]},
                {"id": "fac", "label": "Facility", "kind": "external",
                 "nodes": [["power", "Power and cooling", "system"]]},
            ],
            "flows": [
                ["raw", "gt", "raw", "periodic distillation"],
                ["gt", "ds", "distilled", "validated datasets"],
                ["ds", "train", "distilled", "smaller per epoch"],
                ["train", "power", "control", "net of distillation load"],
            ],
        },
        "notes": [
            "Distillation itself consumes compute and energy; it is scheduled and metered as a workload of its own.",
            "Full datasets remain under existing retention policy and can be used to regenerate distilled datasets.",
        ],
    },

    "outcomes": {
        "direct": [
            "Lower GPU/CPU hours per eligible training run, net of distillation compute.",
            "Less high-performance storage for active training datasets.",
            "Potentially lower energy per eligible training run, measured including distillation.",
        ],
        "operational": [
            "More training jobs supported on existing capacity.",
            "Shorter training queues and faster turnaround for data science teams.",
            "Clearer per-workload infrastructure economics.",
        ],
        "strategic": [
            "Capacity headroom where power or hardware supply constrains growth.",
            "An input to AI infrastructure planning that addresses data volume, not only hardware.",
            "Measured efficiency data that can support sustainability reporting once lifecycle measurement is in place.",
        ],
    },

    "metrics": [
        ["Compute per training run", "GPU/CPU hours per run, before vs. after, including distillation", "direct"],
        ["Active training storage", "TB on high-performance tiers for eligible workloads", "direct"],
        ["Energy per training run", "kWh metered per run, including distillation", "direct"],
        ["Distillation overhead", "Compute hours and kWh consumed by distillation per cycle", "direct"],
        ["Model predictive performance", "Task metric on a held-out full-data test set", "quality"],
        ["Cluster utilization", "Jobs completed per GPU-hour available", "operational"],
        ["Queue time", "Average wait time for training jobs", "operational"],
        ["Share of eligible workloads", "Fraction of training spend where data volume drives cost", "strategic"],
    ],

    "stakeholders": {
        "sponsor": ["CIO or CTO", "Needs AI growth without proportional infrastructure expansion."],
        "economic": ["Infrastructure and data center leader, with the CFO", "Owns capacity, power and hardware budgets."],
        "technical": ["Head of ML platform", "Must confirm distilled datasets integrate with training pipelines without quality loss."],
        "operational": [
            ["Data center operations", "Metering of power and utilization per workload."],
            ["Data science teams", "Model quality and turnaround on distilled data."],
            ["Sustainability office", "Methodology for energy reporting."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used for fidelity evaluation against full-data baselines."],
            ["CNN training on image data", "verified", "Exercised on the MNIST benchmark."],
            ["Spark / Databricks data pipelines", "proposed", "Candidate integration for large datasets; not built or tested."],
            ["MLflow / Kubeflow pipeline steps", "proposed", "Candidate packaging as a pipeline component; not built."],
            ["Cluster schedulers and power metering", "customer", "Customer systems used to measure compute and energy."],
        ],
        "infrastructure": [
            "Compute capacity for distillation jobs on the existing cluster or a dedicated node.",
            "Access to training datasets for the selected workloads.",
            "Per-job metering of compute and, where available, energy.",
        ],
        "deployment": "For a pilot, distillation runs as a batch job inside the customer's data platform on one or "
                      "two selected training workloads. Integration as a standard pipeline step is a proposed "
                      "roadmap item.",
        "constraints": [
            "Only workloads where data volume drives cost benefit; fixed overheads are unaffected.",
            "Energy measurement requires per-job metering, which many clusters lack.",
            "Distillation has been benchmarked on small public datasets; scaling to enterprise volumes is untested.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "Internal experiments show large data reductions with limited accuracy change on public "
                   "benchmarks, and an internal measurement indicates lower energy per training run on a "
                   "workstation. Effects at data center scale, and net of distillation overhead, have not yet "
                   "been measured.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "86% less energy per training run on a workstation after data reduction (internal measurement; distillation's own energy not separately reported).",
        ],
        "gaps": [
            "No measurement on GPU clusters or enterprise-scale datasets.",
            "No end-to-end accounting of distillation compute and energy against training savings.",
            "No data center or lifecycle energy measurement.",
            "No production deployment.",
        ],
        "risks": [
            "Savings may be small for workloads where data volume is not the main cost driver.",
            "Distillation overhead may offset savings for infrequently trained models.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One or two recurring training workloads with material compute, storage or energy consumption.",
        "inputs": [
            "Training datasets and pipelines for the selected workloads",
            "Current compute, storage and, where available, energy metering per job",
            "The evaluation metric and acceptance tolerance for each model",
            "Cluster capacity to run distillation jobs",
        ],
        "baseline": "The current training jobs on full datasets, metered over representative runs.",
        "method": [
            "Train each model on full and distilled data; evaluate both on the same held-out test set.",
            "Meter compute, storage and energy for training runs and for distillation separately.",
            "Calculate net effect per run and per year at the customer's retraining frequency.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of baseline.",
            "Distilled datasets integrate with existing pipelines without code changes beyond the data path.",
        ],
        "economic_criteria": [
            "Net reduction in compute hours and energy per run, including distillation, above a customer-defined target.",
            "Positive annualized net saving for the selected workloads.",
        ],
        "deliverables": [
            "Evaluation report per workload",
            "Metered compute, storage and energy comparison, including distillation overhead",
            "Workload eligibility assessment for the wider training portfolio",
            "Production adoption plan",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Agreed method for metering and reporting net effect",
            "ML platform owner approval of the pipeline integration",
        ],
    },

    "caveats": [
        "Dataset reduction is not equivalent to a reduction in total data center expenditure. Only the "
        "data-proportional share of eligible workloads is affected, net of the compute and energy used by distillation.",
    ],
    "related": ["BC03", "BC10", "BC09"],
}
