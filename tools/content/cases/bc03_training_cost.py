"""BC03 — AI training cost optimization. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC03",
    "slug": "ai-training-cost-optimization",
    "rank": 3,
    "tier": "flagship",
    "title": "AI training cost optimization",
    "eyebrow": "ML economics",
    "headline": "Train on the data that matters, and stop paying to process the rest.",
    "summary": (
        "Reduce the data footprint of training workloads with task-aware distillation, while measuring "
        "and controlling the effect on downstream predictive performance."
    ),
    "problem_short": "Training and retraining on ever-larger datasets drives compute spend, slows experimentation and ties up shared infrastructure.",
    "solution_short": "Distill each training dataset to a compact, task-specific core and validate it against a full-data baseline before use.",
    "outcome_short": "Lower compute per training run and faster experimentation, within an agreed accuracy tolerance.",
    "cta": "Evaluate your AI training costs",
    "industries": ["financial-services", "telecommunications", "retail-consumer", "manufacturing", "ai-infrastructure"],
    "filters": {
        "objectives": ["training-cost", "operational-efficiency", "energy"],
        "architecture": ["centralized-ml", "multicloud"],
        "deployment": ["public-cloud", "private-cloud", "on-prem", "hybrid"],
        "buyers": ["cto", "ml-platform", "cio", "cfo"],
        "problems": ["training-spend", "storage-growth", "energy-footprint"],
    },
    "roi_scenario": "training",

    "challenge": [
        "Training cost scales with the data a model reads. Every experiment, hyperparameter sweep and "
        "scheduled retrain processes the full training set again, so GPU and CPU hours, data loading "
        "time and storage throughput grow with dataset size, not with the value the data adds.",
        "Much of that volume is redundant for a given task: near-duplicate records, over-represented "
        "routine cases and features of little predictive value. Teams know this, but reducing data by "
        "hand is risky, slow and hard to defend to model owners.",
        "The result is a recurring line item that grows faster than model quality, longer feedback loops "
        "for data scientists, and competition for shared accelerator capacity.",
    ],

    "approaches": [
        {"name": "Buy more or cheaper compute",
         "limit": "Reserved capacity, spot instances and newer accelerators lower the unit price, but every "
                  "run still processes the full dataset; spend keeps tracking data growth."},
        {"name": "Random sub-sampling",
         "limit": "Simple and fast, but task-agnostic: it can drop minority classes and edge cases, and "
                  "gives no guarantee about the impact on model quality."},
        {"name": "Manual data curation",
         "limit": "Can be effective for a single model but is labor-intensive, hard to repeat and rarely "
                  "kept up to date as data and tasks change."},
        {"name": "Model compression and efficient architectures",
         "limit": "Valuable and complementary, but it targets model size and inference cost rather than "
                  "the volume of data each training run must process."},
    ],

    "solution": {
        "intro": "GroundTruth AI inserts a distillation step in front of the training pipeline. For a "
                 "defined modeling task, it produces a compact dataset that retains the information the "
                 "model needs, then proves it with a side-by-side comparison against the full data. "
                 "Training jobs read the distilled dataset instead of the full one.",
        "steps": [
            ("Select the workload", "Identify training jobs with high recurring cost: frequent retrains, "
             "large sweeps or long-running experiments."),
            ("Set the tolerance", "Model owners define the acceptable change in the task metric and any "
             "mandatory coverage (for example, minority classes)."),
            ("Distill", "The runtime generates a task-specific distilled dataset from the full training data."),
            ("Validate", "An evaluation compares models trained on full and distilled data on the same "
             "held-out test set, including per-class results."),
            ("Train on the distilled set", "Approved distilled datasets feed experiments and retrains; "
             "the dataset is regenerated when data or task change materially."),
        ],
        "not": [
            "It does not guarantee identical accuracy: benchmark results show changes of up to −2.8 pp, and tolerance is set per task.",
            "It does not reduce the whole training bill one-for-one; only the data-proportional share of cost is affected, net of distillation cost.",
            "It does not replace model compression, efficient architectures or capacity planning; it complements them.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Retail ML platform team",
        "context": "A retailer's central ML platform trains demand, pricing and personalization models on several years of transaction and clickstream history.",
        "current": "Each experiment and each retraining run processes the full history on shared compute capacity.",
        "problem": "Training spend and queue times rise with data volume. Data scientists wait for capacity, and experimentation slows.",
        "proposed": "For selected models, GroundTruth AI produces a validated distilled training set. Experiments run on the distilled set; candidate models are validated against the full-data baseline before release.",
        "assumptions": [
            "Annual training compute for the selected models: 400,000 (in any currency)",
            "60% of that spend scales with data volume",
            "Assumed dataset reduction: 70%, an illustrative planning value",
            "Data-proportional spend reduced by about 168,000 before distillation and licensing costs",
        ],
        "constraints": [
            "Accuracy tolerance agreed per model before the evaluation",
            "Distilled sets are task-specific; a new target needs regeneration",
        ],
        "economic": [
            "Lower compute per training run and per experiment",
            "Net of the compute used for distillation",
        ],
        "strategic": [
            "More experiments on the same capacity",
            "Faster iteration from idea to validated model",
        ],
        "validation": [
            "Accuracy within tolerance on a full-data test set",
            "Measured compute and wall-clock time per run, including distillation",
            "How often the distilled set can be reused across experiments",
        ],
        "stakeholder": "Head of ML platform, with IT finance",
    },

    "architecture": {
        "current": {
            "title": "Conventional: every run reads the full training set",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["raw", "Full training dataset", "store"], ["fs", "Feature pipeline", "system"]]},
                {"id": "train", "label": "Training infrastructure", "kind": "central",
                 "nodes": [["exp", "Experiments + sweeps", "model"], ["re", "Scheduled retraining", "model"]]},
                {"id": "reg", "label": "Model lifecycle", "kind": "external",
                 "nodes": [["mr", "Model registry", "store"]]},
            ],
            "flows": [
                ["raw", "fs", "raw", "all records"],
                ["fs", "exp", "raw", "full set, every run"],
                ["fs", "re", "raw", "full set, every cycle"],
                ["exp", "mr", "model", "candidate models"],
                ["re", "mr", "model", "updated models"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill once, train many times",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["raw", "Full training dataset", "store"], ["gt", "GroundTruth distillation runtime", "gt"]]},
                {"id": "val", "label": "Validation", "kind": "boundary",
                 "nodes": [["fid", "Evaluation report vs. full data", "system"]]},
                {"id": "train", "label": "Training infrastructure", "kind": "central",
                 "nodes": [["ds", "Distilled training set", "store"], ["exp", "Experiments + retraining", "model"]]},
                {"id": "reg", "label": "Model lifecycle", "kind": "external",
                 "nodes": [["mr", "Model registry", "store"]]},
            ],
            "flows": [
                ["raw", "gt", "raw", "read once per regeneration"],
                ["gt", "fid", "distilled", "distilled candidate"],
                ["fid", "ds", "distilled", "approved within tolerance"],
                ["ds", "exp", "distilled", "compact set, every run"],
                ["exp", "mr", "model", "models"],
                ["mr", "gt", "control", "regenerate on task change"],
            ],
        },
        "notes": [
            "Distillation is a recurring cost of its own; savings appear when the distilled set is reused "
            "across many runs or retraining cycles.",
            "The full dataset remains the system of record and the reference for every fidelity check.",
        ],
    },

    "outcomes": {
        "direct": [
            "Lower compute per training run for workloads where cost scales with data volume.",
            "Lower recurring retraining spend when the distilled set is reused across cycles.",
            "Lower storage and data-loading throughput for training copies.",
        ],
        "operational": [
            "Shorter training times and faster experiment turnaround for data scientists.",
            "More experiments within the same accelerator budget.",
            "Better utilization of shared training infrastructure.",
        ],
        "strategic": [
            "Models that were deprioritized on cost grounds become viable to train and maintain.",
            "Training on workstations or smaller clusters becomes feasible for some workloads.",
            "A measurable lever on AI unit economics that finance and engineering can both track.",
        ],
    },

    "metrics": [
        ["Annual training expenditure", "Spend on compute for the selected workloads, before vs. after", "direct"],
        ["Training execution time", "Wall-clock time per run on the same hardware", "operational"],
        ["Compute per run", "GPU/CPU hours per training run", "direct"],
        ["Training data footprint", "Rows / GB read per run", "direct"],
        ["Model predictive performance", "Task metric on a held-out full-data test set", "quality"],
        ["Per-class / minority performance", "Recall and precision for under-represented classes", "quality"],
        ["Distillation overhead", "Compute, time and energy to generate and validate the distilled set", "direct"],
        ["Energy per training run", "kWh measured at the hardware, including distillation", "direct"],
        ["Experiments per budget period", "Number of training runs completed within the same budget", "operational"],
    ],

    "stakeholders": {
        "sponsor": ["CTO or head of AI", "Wants more model throughput per unit of compute budget."],
        "economic": ["CIO or CFO", "Owns the cloud and accelerator budget; needs a measurable reduction in recurring spend."],
        "technical": ["Head of ML platform / MLOps", "Must fit distillation into pipelines and keep model quality under control."],
        "operational": [
            ["Model owners and data scientists", "Accept or reject distilled data based on task metrics."],
            ["FinOps team", "Tracks training spend and attributes savings correctly."],
            ["Model risk / validation (regulated sectors)", "Reviews whether training-data changes affect model approval."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to train and compare full vs. distilled models."],
            ["CNN training on image data", "verified", "Exercised on the MNIST benchmark."],
            ["Python training pipelines (PyTorch / TensorFlow data loaders)", "proposed", "Distilled set delivered as files; native loaders not yet built."],
            ["MLflow / Kubeflow pipeline step", "proposed", "Candidate packaging as a pipeline component; not built or tested."],
            ["Cloud ML platforms and object stores", "customer", "Store and consume the distilled dataset as ordinary training data."],
        ],
        "infrastructure": [
            "A CPU or GPU host near the training data (sizing set during the pilot).",
            "Read access to the training dataset and the current training code.",
            "Storage for the distilled dataset and evaluation reports.",
        ],
        "deployment": "In a pilot, the runtime runs as an offline step against an export of the training "
                      "data, and the customer's existing training code is pointed at the distilled set. "
                      "Packaging as a reusable pipeline component and scheduled regeneration are proposed "
                      "roadmap items.",
        "constraints": [
            "Benefits depend on how much of the workload cost is data-proportional; fixed overheads are unaffected.",
            "Results so far are on classification tasks; regression, ranking and sequence models need measurement.",
            "Regulated model-validation processes may require re-approval when training data changes.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "This is the business case with the most direct experimental support. On four public "
                   "benchmarks, distillation reduced training data by 86–95% with accuracy changes between "
                   "−1.4 and −2.8 pp, and internal measurements show 86% less energy per training run on a "
                   "workstation. These are internal experiments on small, clean datasets; enterprise "
                   "workloads and cost structures have not yet been measured.",
        "supports": [
            "Iris (tabular, MLP): 95% reduction, 97.4% → 94.7% accuracy (−2.7 pp).",
            "Wine (tabular, MLP): 86% reduction, 97.8% → 95.6% (−2.2 pp).",
            "Breast Cancer (tabular, MLP): 95% reduction, 96.5% → 95.1% (−1.4 pp).",
            "MNIST (image, CNN): 93% reduction, 96.5% → 93.7% (−2.8 pp).",
            "86% less energy per training run on a workstation (internal measurement; the distillation step's own energy is not separately reported).",
        ],
        "gaps": [
            "No measurement on large enterprise datasets or distributed training clusters.",
            "No end-to-end cost measurement including distillation, storage and operations.",
            "Classification only; no regression, ranking, forecasting or language-model results.",
            "Experiments not independently replicated; energy methodology not yet published.",
        ],
        "risks": [
            "Accuracy loss beyond tolerance for some tasks, particularly with rare classes.",
            "Savings smaller than data reduction where cost is dominated by fixed overheads.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One recurring training or retraining workload with material compute cost and a clear evaluation metric.",
        "inputs": [
            "The training dataset (or a representative extract) and its held-out test set",
            "The current training code, hardware profile and run frequency",
            "Current cost per run or per month for the workload",
            "Model owner's acceptance tolerance and coverage requirements",
        ],
        "baseline": "The current model trained on the full dataset with the existing pipeline and hardware.",
        "method": [
            "Train the same model on full and distilled data; evaluate both on the same held-out test set.",
            "Measure compute hours, wall-clock time and energy per run for both paths.",
            "Measure the time, compute and energy to generate and validate the distilled set.",
            "Project annual impact from the customer's actual run frequency, with stated assumptions.",
        ],
        "technical_criteria": [
            "Task metric within the customer-defined tolerance of baseline.",
            "Agreed per-class or minority-class thresholds met.",
            "Distilled set reproducible from the same inputs.",
        ],
        "economic_criteria": [
            "Compute per run reduced by a customer-defined target.",
            "Net annual saving positive after distillation overhead at actual retraining frequency.",
        ],
        "deliverables": [
            "Evaluation report, overall and per class",
            "Measured cost, time and energy comparison per run, including overhead",
            "Annualized savings model using the customer's own assumptions",
            "Integration plan for the customer's training pipeline",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Model owner and, where applicable, model-risk sign-off",
            "Agreed regeneration policy and ownership",
            "Pipeline integration scoped and approved",
        ],
    },

    "caveats": [
        "Savings estimates apply only to the data-proportional share of training cost and are net of the "
        "cost of distillation. Benchmark figures are internal experiments, not enterprise measurements.",
    ],
    "related": ["BC09", "BC06", "BC10"],
}
