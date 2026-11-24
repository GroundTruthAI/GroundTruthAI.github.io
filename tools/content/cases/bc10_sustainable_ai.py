"""BC10 — Sustainable AI infrastructure. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC10",
    "slug": "sustainable-ai-infrastructure",
    "rank": 11,
    "tier": "explorer",
    "title": "Sustainable AI infrastructure",
    "eyebrow": "Energy and resource efficiency",
    "headline": "Cut the energy of eligible AI workloads by processing less data, and prove it with measurements.",
    "summary": (
        "Reduce the computational work of eligible training workloads through task-aware dataset "
        "optimization, with energy measured end to end, including the distillation step itself."
    ),
    "problem_short": "AI workloads add energy demand that sustainability teams must account for, but few levers reduce it without reducing AI ambitions.",
    "solution_short": "Train eligible models on validated distilled datasets and measure net energy, distillation included, per workload.",
    "outcome_short": "A measurable, workload-level reduction in training energy that can feed sustainability reporting once verified.",
    "cta": "Discuss your AI energy footprint",
    "industries": ["ai-infrastructure", "multinational-groups", "energy-utilities"],
    "filters": {
        "objectives": ["energy", "training-cost", "operational-efficiency"],
        "architecture": ["centralized-ml", "multicloud"],
        "deployment": ["on-prem", "private-cloud", "public-cloud"],
        "buyers": ["sustainability", "cto", "infra-leader", "cfo"],
        "problems": ["energy-footprint", "training-spend", "storage-growth"],
    },
    "roi_scenario": "infrastructure",

    "challenge": [
        "AI is now a visible part of enterprise energy demand. Training and retraining models, and "
        "storing and moving the data behind them, consume electricity in company data centers and in "
        "the cloud regions that serve them. Sustainability teams are asked to report this footprint and "
        "to show credible reduction plans.",
        "The usual levers sit outside the AI workload: cleaner power contracts, more efficient "
        "facilities and newer hardware. These matter, but they do not change how much computation "
        "each model requires. Inside the workload, the main driver is the amount of data processed "
        "per training run, multiplied by the number of runs.",
        "Organizations need a lever they can apply workload by workload, and evidence strong enough "
        "to survive scrutiny from auditors and stakeholders.",
    ],

    "approaches": [
        {"name": "Renewable power procurement and certificates",
         "limit": "Addresses the carbon intensity of electricity, not the amount of computation; the "
                  "workload consumes the same energy."},
        {"name": "Hardware and facility efficiency upgrades",
         "limit": "Effective but capital-intensive and slow, and gains can be absorbed by growing "
                  "data volumes and more frequent retraining."},
        {"name": "Smaller or simpler models",
         "limit": "Reduces compute but can sacrifice capability; it is a model-design decision, not "
                  "always available for an existing production model."},
        {"name": "Carbon-aware scheduling",
         "limit": "Shifts when and where workloads run, which lowers emissions intensity, but does not "
                  "reduce the energy the workload needs."},
    ],

    "solution": {
        "intro": "GroundTruth AI reduces the amount of data an eligible training workload processes. "
                 "Models are trained on a task-specific distilled dataset validated against the full "
                 "data, so each training run does less computation. Because distillation consumes "
                 "energy too, every assessment measures **net** energy: workload energy saved minus the "
                 "energy of distillation and regeneration.",
        "steps": [
            ("Select eligible workloads", "Identify training workloads where energy scales with data "
             "volume and where accuracy tolerances allow a distilled training set."),
            ("Measure the baseline", "Meter energy per training run on the actual hardware or obtain "
             "provider-reported figures, together with run counts per year."),
            ("Distill and validate", "Generate a distilled dataset and confirm model quality against "
             "the full-data baseline."),
            ("Measure net energy", "Meter distillation and distilled-data training runs; report net "
             "savings per run and per year, distillation included."),
            ("Prepare for reporting", "Hand the measurement method and data to the sustainability team "
             "for verification before any figure is used in external reporting."),
        ],
        "not": [
            "It does not make environmental claims on its own; figures require customer-side lifecycle measurement and verification.",
            "It does not reduce embodied emissions of hardware or facility overheads directly.",
            "Dataset reduction does not translate one-for-one into data center energy reduction.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Group reporting AI energy use",
        "context": "A multinational group reports the energy footprint of its digital operations, including AI workloads.",
        "current": "AI training energy is estimated from installed capacity rather than measured per workload.",
        "problem": "Sustainability teams need levers that reduce AI energy without stopping AI initiatives, and evidence that holds up to scrutiny.",
        "proposed": "Selected training workloads are measured with full and distilled data, including the energy of distillation. Verified results feed internal reporting.",
        "assumptions": [],
        "constraints": [
            "Operational energy only; not a lifecycle assessment",
            "Grid factors and measurement method agreed with the sustainability team",
        ],
        "economic": [
            "Lower training energy cost for eligible workloads",
        ],
        "strategic": [
            "Credible, measured workload-level reductions",
        ],
        "validation": [
            "Metered energy per training run on both paths",
            "Distillation energy included",
            "Methodology reviewed by the sustainability team",
        ],
        "stakeholder": "Chief Sustainability Officer, with the CIO",
    },

    "architecture": {
        "current": {
            "title": "Conventional: every training run processes the full dataset",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["lake", "Full training datasets", "store"]]},
                {"id": "dc", "label": "Data center / cloud region", "kind": "central",
                 "nodes": [["train", "Training workloads", "system"], ["model", "Trained models", "model"]]},
                {"id": "fac", "label": "Facility", "kind": "external",
                 "nodes": [["pwr", "Power and cooling", "system"], ["rep", "Energy reporting", "user"]]},
            ],
            "flows": [
                ["lake", "train", "raw", "full volume, every run"],
                ["train", "model", "raw", ""],
                ["pwr", "train", "control", "energy per run"],
                ["pwr", "rep", "control", "facility-level only"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distilled training, net energy measured per workload",
            "zones": [
                {"id": "data", "label": "Data platform", "kind": "source",
                 "nodes": [["lake", "Full training datasets", "store"], ["gt", "GroundTruth distillation runtime", "gt"]]},
                {"id": "dc", "label": "Data center / cloud region", "kind": "central",
                 "nodes": [["train", "Training workloads", "system"], ["model", "Trained models", "model"]]},
                {"id": "fac", "label": "Measurement", "kind": "external",
                 "nodes": [["meter", "Workload energy metering", "system"], ["rep", "Sustainability reporting", "user"]]},
            ],
            "flows": [
                ["lake", "gt", "raw", "on regeneration only"],
                ["gt", "train", "distilled", "validated distilled set"],
                ["train", "model", "distilled", ""],
                ["gt", "meter", "control", "distillation energy"],
                ["train", "meter", "control", "training energy"],
                ["meter", "rep", "control", "net figure, verified"],
            ],
        },
        "notes": [
            "Distillation energy is metered and subtracted from training energy savings; only the net "
            "figure is reported.",
            "Workload metering can use hardware power telemetry or provider-reported data; the method "
            "is agreed with the sustainability team before the pilot.",
        ],
    },

    "outcomes": {
        "direct": [
            "Potentially lower energy per training run for eligible workloads, net of distillation.",
            "Lower compute spend for the same workloads.",
            "Less storage for training datasets and snapshots where distilled sets replace copies.",
        ],
        "operational": [
            "Workload-level energy baselines that most AI teams do not have today.",
            "Less unnecessary data processing across recurring training runs.",
            "A repeatable measurement method that can extend to other workloads.",
        ],
        "strategic": [
            "A measurable, workload-level lever for sustainable AI initiatives.",
            "Evidence the sustainability team can verify before using it in reporting.",
            "AI growth less tightly coupled to energy growth.",
        ],
    },

    "metrics": [
        ["Energy per training run", "kWh per run, full vs. distilled data, metered on the same hardware", "direct"],
        ["Distillation energy", "kWh per distillation and regeneration run", "direct"],
        ["Net annual workload energy", "(Saved kWh per run × runs per year) − distillation kWh", "direct"],
        ["Compute cost per run", "GPU/CPU hours and cost per run", "direct"],
        ["Model predictive performance", "Task metric vs. full-data baseline on the same test set", "quality"],
        ["Emissions estimate", "Net kWh × location- or market-based emission factor chosen by the customer", "strategic"],
        ["Workloads measured", "Number of AI workloads with a metered energy baseline", "operational"],
        ["Storage for training data", "TB of training datasets and snapshots", "direct"],
    ],

    "stakeholders": {
        "sponsor": ["Chief Sustainability Officer", "Needs credible, verifiable reductions tied to the AI estate."],
        "economic": ["CFO or CTO", "Owns compute and energy budgets; expects savings to be net and auditable."],
        "technical": ["Infrastructure & data center leader", "Provides metering, hardware access and the measurement method."],
        "operational": [
            ["Head of ML / MLOps", "Model quality and pipeline impact of distilled training data."],
            ["Sustainability reporting team", "Method, boundaries and emission factors used in any figure."],
            ["Internal audit or assurance", "Traceability from measurement to reported number."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to compare full-data and distilled-data training."],
            ["CNN training on image data", "verified", "Exercised on the MNIST benchmark."],
            ["Hardware power telemetry (e.g. GPU/CPU power counters, PDU metering)", "proposed", "Measurement method to be agreed per site; no packaged integration exists."],
            ["Cloud provider energy or carbon reports", "customer", "Customer-owned data; granularity varies by provider."],
            ["Sustainability reporting tools", "customer", "Receive verified figures from the customer's own team."],
        ],
        "infrastructure": [
            "Access to the hardware or cloud environment where the selected workload trains.",
            "A metering method that can isolate energy per training and distillation run.",
            "Compute for distillation runs (CPU-first; sizing set in the pilot).",
        ],
        "deployment": "For a pilot, distillation runs as a batch job alongside the selected workload, and "
                      "energy is metered for baseline training, distillation and distilled training on the "
                      "same hardware. Cloud workloads may rely on provider-reported energy, which can limit "
                      "precision; that limitation is documented in the results.",
        "constraints": [
            "Workload-level energy metering is not available in every environment.",
            "Facility overheads (cooling, power conversion) are allocated, not measured per workload.",
            "Lifecycle and embodied emissions are outside the measurement scope unless the customer adds them.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "Internal measurements indicate lower training energy per run after data reduction on a "
                   "workstation and on IoT/edge devices. The methodology is not yet published, the "
                   "figures do not separately report distillation energy, and no data-center or lifecycle "
                   "measurement exists. No environmental claim should be made until a pilot measures net "
                   "energy end to end.",
        "supports": [
            "86% less energy per training run on a workstation after data reduction (internal measurement; distillation energy not separately reported).",
            "39% less energy on IoT/edge devices at the point of capture (internal measurement).",
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp.",
        ],
        "gaps": [
            "No published measurement methodology for the energy figures.",
            "Distillation energy has not been reported separately.",
            "No data-center-scale or cloud-workload measurement.",
            "No lifecycle assessment or third-party verification.",
        ],
        "risks": [
            "Net savings can be small if distillation must be re-run frequently.",
            "Rebound effect: cheaper training can lead to more training runs, offsetting savings.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One recurring training workload whose energy the customer wants to reduce and measure.",
        "inputs": [
            "The workload's training data, pipeline and evaluation metric",
            "Run frequency over the past year",
            "Access to power telemetry or provider-reported energy for the workload",
            "Compute for distillation runs",
        ],
        "baseline": "Metered energy and cost of the current training run on the full dataset.",
        "method": [
            "Meter energy for full-data training, distillation and distilled-data training on the same hardware.",
            "Evaluate model quality for both on the same held-out test set.",
            "Compute net annual energy and cost using actual run frequency, distillation included.",
            "Document measurement boundaries and uncertainty with the sustainability team.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of baseline.",
            "Energy measurements reproducible within an agreed uncertainty.",
        ],
        "economic_criteria": [
            "Net energy and compute cost per year reduced by a customer-defined target.",
            "Saving remains positive after distillation and regeneration energy.",
        ],
        "deliverables": [
            "Net energy and cost report, distillation included",
            "Documented measurement method and boundaries",
            "Evaluation report (full vs. distilled)",
            "Roll-out plan for further eligible workloads",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Measurement method accepted by the sustainability team",
            "Verification route agreed before any external use of figures",
        ],
    },

    "caveats": [
        "Energy figures shown today are internal measurements. Any environmental claim requires "
        "customer-side lifecycle measurement that includes the energy of distillation itself.",
    ],
    "related": ["BC06", "BC03", "BC09"],
}
