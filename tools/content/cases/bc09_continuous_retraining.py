"""BC09 — Continuous model retraining. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC09",
    "slug": "continuous-model-retraining",
    "rank": 5,
    "tier": "explorer",
    "title": "Continuous model retraining",
    "eyebrow": "MLOps economics",
    "headline": "Retrain production models on a validated distilled dataset instead of the full history every cycle.",
    "summary": (
        "Use a validated distilled dataset as the default training input for recurring retraining, "
        "and regenerate it when data or operating conditions change."
    ),
    "problem_short": "Production models are retrained on ever-growing full histories, so each cycle costs more compute, time and storage than the last.",
    "solution_short": "Retraining pipelines consume a validated distilled dataset; distillation is re-run on demand when the data shifts.",
    "outcome_short": "Lower recurring retraining cost and shorter model update cycles, with fidelity checked every cycle.",
    "cta": "Assess your retraining costs",
    "industries": ["financial-services", "retail-consumer", "telecommunications", "manufacturing"],
    "filters": {
        "objectives": ["training-cost", "operational-efficiency", "energy"],
        "architecture": ["centralized-ml", "multicloud"],
        "deployment": ["private-cloud", "public-cloud", "hybrid"],
        "buyers": ["ml-platform", "cdo", "cto", "cfo"],
        "problems": ["training-spend", "model-staleness", "storage-growth"],
    },
    "roi_scenario": "training",

    "challenge": [
        "Production machine learning models lose accuracy as customer behavior, markets, equipment "
        "and operating conditions change. Mature MLOps teams therefore retrain on a schedule "
        "(weekly, monthly or quarterly) or whenever monitoring flags degradation.",
        "Many retraining pipelines simply re-read the complete historical dataset each time, plus the "
        "newest data. Training volume grows with every cycle, so compute, run time and the storage "
        "of training snapshots grow with it. Across a portfolio of dozens or hundreds of models, "
        "historical reprocessing becomes a significant and recurring line in the ML platform budget.",
        "The cost also shows up as latency: when retraining takes days, models stay stale for longer "
        "and teams retrain less often than the data suggests they should.",
    ],

    "approaches": [
        {"name": "Retrain on the full history every cycle",
         "limit": "Simple and auditable, but cost and run time scale with accumulated data, much of "
                  "which adds little new information to the model."},
        {"name": "Sliding windows (train only on the most recent months)",
         "limit": "Caps volume but discards seasonal patterns and rare historical events the model may "
                  "still need; the window length is usually a guess rather than a validated choice."},
        {"name": "Random sub-sampling of the history",
         "limit": "Reduces volume without regard to the task, so minority classes and rare events are "
                  "thinned out at the same rate as redundant records."},
        {"name": "Incremental or online learning",
         "limit": "Avoids full retrains for some model families, but is not available for every model "
                  "type, complicates validation and can drift silently without a reference dataset."},
    ],

    "solution": {
        "intro": "GroundTruth AI turns the training history into a maintained asset: a task-specific "
                 "distilled dataset that is validated against the full data and used as the default "
                 "input for recurring retraining. Each cycle trains on the distilled history plus new "
                 "data; when the data shifts materially, distillation is re-run. **Available today:** "
                 "generating and re-generating a distilled dataset on demand. **Proposed:** adaptive "
                 "distillation that updates the distilled set incrementally, and automatic "
                 "regeneration triggered by drift monitoring.",
        "steps": [
            ("Baseline the model", "Select a production model, its retraining cadence, its evaluation "
             "metric and the tolerance the business accepts versus a full-history retrain."),
            ("Distill the history", "Generate a distilled training dataset for that task and validate "
             "it by training on full and distilled data side by side."),
            ("Retrain on distilled + new data", "The existing pipeline reads the distilled history and "
             "the latest data instead of the full archive; nothing else in the pipeline changes."),
            ("Check fidelity every cycle", "Each retrain is compared with periodic full-history "
             "reference runs to confirm the distilled set is still representative."),
            ("Regenerate when needed", "Distillation is re-run on a schedule or on request. Triggering "
             "it from drift alerts is a proposed integration, not an available feature."),
        ],
        "not": [
            "It does not decide when a model should be retrained; that remains the MLOps team's policy.",
            "It does not remove the need for periodic full-data reference evaluations.",
            "Drift detection is a prototype capability and has not been validated on customer data.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Payments provider with monthly retraining",
        "context": "A payments company retrains its fraud models every month on a growing transaction history.",
        "current": "Each retraining cycle processes the full history, so cost and duration grow every month.",
        "problem": "Retraining is becoming slower and more expensive, which delays model updates exactly when fraud patterns shift.",
        "proposed": "Each cycle, a distilled dataset is regenerated from the updated history, validated against the full-data model and used for retraining. Full-data retraining remains as a periodic control.",
        "assumptions": [],
        "constraints": [
            "Fraud is a minority class; positive examples must be preserved",
            "Drift-triggered regeneration is a proposed capability; the scenario assumes scheduled regeneration",
        ],
        "economic": [
            "Lower compute per retraining cycle",
            "Net of the cost of regenerating the distilled dataset each cycle",
        ],
        "strategic": [
            "Shorter update cycles when fraud patterns change",
        ],
        "validation": [
            "Minority-class recall in every cycle",
            "Stability of model quality over several consecutive cycles",
            "Cumulative cost including regeneration",
        ],
        "stakeholder": "Head of ML or MLOps, with the fraud risk owner",
    },

    "architecture": {
        "current": {
            "title": "Conventional: full history reprocessed every cycle",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["hist", "Full training history", "store"], ["new", "New production data", "system"]]},
                {"id": "ml", "label": "ML platform", "kind": "central",
                 "nodes": [["pipe", "Retraining pipeline", "system"], ["model", "Retrained model", "model"]]},
                {"id": "prod", "label": "Production", "kind": "external",
                 "nodes": [["serve", "Model serving", "system"], ["mon", "Performance monitoring", "system"]]},
            ],
            "flows": [
                ["new", "hist", "raw", "appended each cycle"],
                ["hist", "pipe", "raw", "full history, every cycle"],
                ["pipe", "model", "raw", ""],
                ["model", "serve", "model", "deploy"],
                ["mon", "pipe", "control", "scheduled retrain"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: retrain on a maintained distilled history",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["hist", "Full training history", "store"], ["new", "New production data", "system"]]},
                {"id": "gtz", "label": "Distillation layer", "kind": "boundary",
                 "nodes": [["gt", "GroundTruth distillation runtime", "gt"], ["ds", "Distilled history + report", "store"]]},
                {"id": "ml", "label": "ML platform", "kind": "central",
                 "nodes": [["pipe", "Retraining pipeline", "system"], ["model", "Retrained model", "model"]]},
                {"id": "prod", "label": "Production", "kind": "external",
                 "nodes": [["mon", "Performance / drift monitoring", "system"]]},
            ],
            "flows": [
                ["hist", "gt", "raw", "on regeneration only"],
                ["gt", "ds", "distilled", "validated set"],
                ["ds", "pipe", "distilled", "every cycle"],
                ["new", "pipe", "raw", "latest data"],
                ["pipe", "model", "distilled", ""],
                ["mon", "gt", "control", "regenerate (proposed)"],
            ],
        },
        "notes": [
            "The full history remains in place as the system of record and is read again only when the "
            "distilled set is regenerated or a reference evaluation is run.",
            "The monitoring-to-regeneration trigger is a proposed integration; in a pilot, regeneration "
            "is scheduled or requested manually.",
        ],
    },

    "outcomes": {
        "direct": [
            "Lower compute cost per retraining cycle, net of periodic distillation runs.",
            "Less historical data reprocessed and fewer large training snapshots stored.",
            "Lower energy per retraining cycle, measured including distillation.",
        ],
        "operational": [
            "Shorter retraining run times and faster model update cycles.",
            "Retraining frequency set by business need rather than by compute budget.",
            "A versioned, validated training dataset that simplifies reproducibility and audit.",
        ],
        "strategic": [
            "More models kept current with the same ML platform capacity.",
            "A foundation for adaptive, drift-aware retraining as that capability matures.",
        ],
    },

    "metrics": [
        ["Compute cost per retraining cycle", "GPU/CPU hours and cost per cycle, before vs. after", "direct"],
        ["Annual retraining expenditure", "Cycles per year × cost per cycle, including distillation runs", "direct"],
        ["Retraining run time", "Wall-clock time from trigger to validated model", "operational"],
        ["Historical data reprocessed", "TB read per cycle", "direct"],
        ["Model predictive performance", "Task metric vs. a full-history retrain on the same test set", "quality"],
        ["Rare-event and segment coverage", "Representation of minority classes and key segments in the distilled set", "quality"],
        ["Distillation overhead", "Compute, energy and time of each regeneration", "direct"],
        ["Model staleness", "Average age of production models since last retrain", "operational"],
        ["Models in scope", "Number of production models retrained on distilled data", "strategic"],
    ],

    "stakeholders": {
        "sponsor": ["CDO or head of analytics", "Wants more models kept current without a proportional budget increase."],
        "economic": ["CTO or CFO", "Owns ML platform and cloud compute spend; needs measurable recurring savings."],
        "technical": ["Head of ML / MLOps platform", "Must confirm the distilled set fits pipelines, versioning and validation gates."],
        "operational": [
            ["Model owners / data scientists", "Model quality and explainability after the change in training input."],
            ["Model risk management", "Validation evidence and reproducibility for regulated models."],
            ["FinOps team", "Attribution of compute savings and distillation overhead."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to compare full-data and distilled-data training."],
            ["Training data exports (Parquet / CSV) from the data platform", "proposed", "File-based hand-off for the pilot."],
            ["Pipeline orchestration and model registry (e.g. Airflow, MLflow, Kubeflow)", "proposed", "Candidate integration so the distilled set is a versioned pipeline input; not built or tested."],
            ["Drift-triggered regeneration", "proposed", "Would connect monitoring alerts to distillation runs; drift detection is a prototype."],
            ["Customer ML platform (e.g. Databricks, SageMaker, Vertex AI)", "customer", "Consumes the distilled dataset as ordinary training data."],
        ],
        "infrastructure": [
            "Compute in the customer's ML environment for distillation runs (CPU-first; sizing set in the pilot).",
            "Read access to the training history for the selected model.",
            "A storage location for versioned distilled datasets and fidelity reports.",
        ],
        "deployment": "For a pilot, distillation runs as a batch job in the customer's cloud account or "
                      "data center, and the pilot compares several retraining cycles on full and distilled "
                      "data. Packaging as a pipeline step with registry integration is a proposed roadmap "
                      "item, scoped with the customer's MLOps team.",
        "constraints": [
            "Fidelity across successive retraining cycles has not yet been measured; the pilot is the first measurement.",
            "Regulated models may require model-risk review before the training input changes.",
            "Savings depend on the share of retraining cost that scales with data volume.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "Internal experiments show large single-run data reductions with limited accuracy change "
                   "on public benchmarks, and lower training energy per run on a workstation. Repeated "
                   "retraining over shifting data, and adaptive or drift-triggered regeneration, have not "
                   "been tested.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "86% less energy per training run on a workstation after data reduction (internal measurement; distillation energy not separately reported).",
        ],
        "gaps": [
            "No multi-cycle retraining experiment on data that changes over time.",
            "Adaptive distillation and drift-triggered regeneration are proposed, not built.",
            "Drift detection has not been validated on customer data.",
            "No measurement of distillation overhead amortized across retraining cycles.",
        ],
        "risks": [
            "A distilled set can become unrepresentative after a regime change if regeneration lags behind drift.",
            "If distillation must be re-run almost every cycle, net savings shrink.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One production model with a regular retraining cadence and a material retraining cost.",
        "inputs": [
            "The model's full training history and the most recent data windows",
            "The current retraining pipeline, cadence and evaluation metric",
            "Cost and run-time records for recent retraining cycles",
            "Compute in the customer's ML environment for distillation",
        ],
        "baseline": "The current retraining process on the full history, replayed over several historical cycles.",
        "method": [
            "Replay at least three historical retraining cycles on full and on distilled-plus-new data.",
            "Evaluate each pair on the same held-out test set for that cycle.",
            "Measure compute, run time, data read and energy per cycle, including distillation runs.",
            "Test one scheduled regeneration of the distilled set and record its cost.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of the full-history retrain in every replayed cycle.",
            "Coverage of minority classes and key segments maintained.",
            "Retraining pipeline unchanged apart from its training input.",
        ],
        "economic_criteria": [
            "Cost and run time per cycle reduced by a customer-defined target.",
            "Net annual saving positive after distillation and regeneration overhead.",
        ],
        "deliverables": [
            "Cycle-by-cycle fidelity report (full vs. distilled)",
            "Measured cost, run-time and energy comparison per cycle",
            "Recommended regeneration policy for the model",
            "Integration design for the customer's pipeline and registry",
        ],
        "adoption": [
            "Technical and economic criteria met across replayed cycles",
            "Model-risk or validation sign-off where required",
            "Agreed regeneration policy and named owner",
            "Periodic full-history reference evaluation scheduled",
        ],
    },

    "caveats": [
        "Adaptive distillation and drift-triggered regeneration are proposed capabilities. Today, "
        "distilled datasets are regenerated on a schedule or on request.",
    ],
    "related": ["BC03", "BC06", "BC10"],
}
