"""BC07 — Data residency and sovereignty. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC07",
    "slug": "data-residency-and-sovereignty",
    "rank": 7,
    "tier": "explorer",
    "title": "Data residency and sovereignty",
    "eyebrow": "Distributed data governance",
    "headline": "Keep original data where it must live, and still collaborate on analytics.",
    "summary": (
        "Generate approved, task-specific datasets inside authorized source environments, potentially "
        "reducing the need to transfer complete original datasets across jurisdictions or organizations."
    ),
    "problem_short": "Multinational and regulated organizations must keep original data in specific jurisdictions or domains, which limits shared analytics.",
    "solution_short": "Distillation runs inside each authorized environment; only approved task-specific datasets are considered for permitted transfer.",
    "outcome_short": "Less cross-border replication of complete datasets, with source data ownership preserved.",
    "cta": "Discuss your data residency architecture",
    "industries": ["financial-services", "healthcare", "multinational-groups", "telecommunications"],
    "filters": {
        "objectives": ["residency", "segregated-analytics", "replication", "data-movement"],
        "architecture": ["multi-jurisdiction", "multi-domain", "centralized-ml"],
        "deployment": ["on-prem", "private-cloud", "hybrid"],
        "buyers": ["cdo", "cio", "enterprise-architect"],
        "problems": ["cross-border", "consolidation-blocked", "raw-replication"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Multinational and regulated organizations often need to retain original data within specific "
        "countries, regions or legal entities. Data protection law, sector regulation, contractual "
        "commitments and customer expectations all shape where data may be stored and processed.",
        "Group-level analytics and AI still need data from every region. The conventional route is to "
        "copy complete datasets to a central platform, which may require legal assessments, transfer "
        "mechanisms and additional safeguards for each flow, and in some cases is not permitted at all.",
        "Many organizations therefore run fragmented regional models or postpone group-wide initiatives "
        "while the data question is resolved.",
    ],

    "approaches": [
        {"name": "Centralize complete datasets under transfer mechanisms",
         "limit": "Enables group analytics where permitted, but every complete copy expands the scope of "
                  "transfer assessments, safeguards and ongoing compliance obligations."},
        {"name": "Regional platforms with separate models",
         "limit": "Respects residency but duplicates infrastructure and skills, and limits learning across regions."},
        {"name": "Aggregated statistics only",
         "limit": "Lower sensitivity, but aggregates often lack the granularity needed to train predictive models."},
        {"name": "Federated learning or privacy-enhancing technologies",
         "limit": "Can keep data local, but require training infrastructure in every jurisdiction, specialized "
                  "orchestration and their own legal assessment; maturity and cost vary widely by use case."},
    ],

    "solution": {
        "intro": "GroundTruth AI runs distillation inside each authorized source environment. For a defined "
                 "analytical task, it produces a compact training dataset, which is then evaluated. The data "
                 "owner and the customer's legal and privacy functions then decide whether, and under which "
                 "safeguards, that dataset may be shared. Where transfer is permitted, the volume moved is "
                 "smaller and task-specific; original datasets stay where they are.",
        "steps": [
            ("Define the task and legal basis", "The central team, data owners and legal/privacy functions agree the "
             "analytical task and the conditions under which derived datasets may be shared."),
            ("Distill in each jurisdiction", "The runtime operates inside each authorized regional environment; original "
             "data does not leave it."),
            ("Validate and review", "Each distilled dataset is accompanied by its evaluation results and reviewed by the data "
             "owner and privacy function before any transfer."),
            ("Transfer only where permitted", "Approved datasets move through existing, authorized transfer mechanisms."),
            ("Analyze centrally", "Group teams train and evaluate models on the combined approved datasets."),
        ],
        "not": [
            "Distillation is not anonymization: distilled datasets may still contain or reveal personal or confidential information.",
            "Distilled datasets remain subject to applicable data protection, residency, transfer and contractual restrictions.",
            "Distillation does not provide legal authorization for any cross-border transfer; that decision remains with the customer's legal and privacy functions.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Multinational insurer with in-country data",
        "context": "An insurer operates in eight countries. Customer data must remain in-country under local law and group policy.",
        "current": "Group analytics use aggregated reports; complete datasets are not replicated across borders.",
        "problem": "The group wants shared actuarial or claims models, but complete cross-border replication is restricted or slow to authorize.",
        "proposed": "Each country distills a task-specific dataset in-country. Legal and data protection teams decide, dataset by dataset, whether a transfer is permitted. Where it is, the group trains centrally; where it is not, the dataset stays in-country.",
        "assumptions": [],
        "constraints": [
            "Distillation is not anonymization and creates no legal basis for transfer",
            "Transfer decisions remain with legal and data protection functions",
        ],
        "economic": [
            "Less cross-border replication of complete datasets",
        ],
        "strategic": [
            "Shared models where transfers are authorized, with original data kept in-country",
        ],
        "validation": [
            "Legal review of each dataset before transfer",
            "Model performance per country",
            "Re-identification risk assessment",
        ],
        "stakeholder": "Chief Data Officer, with the data protection officer and legal",
    },

    "architecture": {
        "current": {
            "title": "Conventional: complete datasets copied to a central platform",
            "zones": [
                {"id": "ra", "label": "Jurisdiction A", "kind": "source",
                 "nodes": [["da", "Regional data platform A", "store"]]},
                {"id": "rb", "label": "Jurisdiction B", "kind": "source",
                 "nodes": [["db", "Regional data platform B", "store"]]},
                {"id": "xfer", "label": "Transfer controls", "kind": "boundary",
                 "nodes": [["tm", "Transfer mechanism per flow", "system"]]},
                {"id": "hq", "label": "Group analytics platform", "kind": "central",
                 "nodes": [["copy", "Complete dataset copies", "store"], ["ml", "Group ML training", "model"]]},
            ],
            "flows": [
                ["da", "tm", "raw", "complete dataset"],
                ["db", "tm", "raw", "complete dataset"],
                ["tm", "copy", "raw", "full copies"],
                ["copy", "ml", "raw", ""],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill locally, share approved datasets where permitted",
            "zones": [
                {"id": "ra", "label": "Jurisdiction A", "kind": "source",
                 "nodes": [["da", "Regional data platform A", "store"], ["ga", "GroundTruth runtime A", "gt"]]},
                {"id": "rb", "label": "Jurisdiction B", "kind": "source",
                 "nodes": [["db", "Regional data platform B", "store"], ["gb", "GroundTruth runtime B", "gt"]]},
                {"id": "xfer", "label": "Transfer controls", "kind": "boundary",
                 "nodes": [["rev", "Owner + privacy review", "system"]]},
                {"id": "hq", "label": "Group analytics platform", "kind": "central",
                 "nodes": [["ds", "Approved distilled datasets", "store"], ["ml", "Group ML training", "model"]]},
            ],
            "flows": [
                ["da", "ga", "raw", "stays in jurisdiction"],
                ["db", "gb", "raw", "stays in jurisdiction"],
                ["ga", "rev", "distilled", "distilled + report"],
                ["gb", "rev", "distilled", "distilled + report"],
                ["rev", "ds", "distilled", "only where permitted"],
                ["ds", "ml", "distilled", ""],
            ],
        },
        "notes": [
            "Each runtime operates inside the authorized environment of its jurisdiction or legal entity.",
            "The review step is a customer governance control; GroundTruth AI supplies the evaluation results, "
            "not the legal assessment.",
        ],
    },

    "outcomes": {
        "direct": [
            "Smaller volumes moved through cross-border transfer mechanisms, where transfer is permitted.",
            "Less central storage of complete regional dataset copies.",
            "Lower central processing for group training data, net of regional distillation cost.",
        ],
        "operational": [
            "Fewer complete copies of regional data to secure, catalog and retire.",
            "Task-specific datasets that are easier to describe in transfer and privacy assessments.",
            "A repeatable pattern for onboarding additional regions.",
        ],
        "strategic": [
            "Group-level analytics without complete centralization of original data.",
            "Source data ownership preserved with regional entities.",
            "Support for distributed data architectures aligned with residency objectives.",
        ],
    },

    "metrics": [
        ["Cross-border transfer volume", "GB/TB transferred per use case, before vs. after", "direct"],
        ["Complete dataset copies outside origin", "Number of full regional copies held centrally", "operational"],
        ["Central storage for training data", "TB held centrally for the use case", "direct"],
        ["Regional distillation overhead", "Compute hours and cost per region per cycle", "direct"],
        ["Model predictive performance", "Task metric on held-out data in each region", "quality"],
        ["Regional representativeness", "Model performance per region vs. regional baselines", "quality"],
        ["Assessment effort", "Time to complete transfer and privacy reviews per use case", "operational"],
        ["Participating jurisdictions", "Number of regions contributing approved datasets", "strategic"],
    ],

    "stakeholders": {
        "sponsor": ["Chief Data Officer", "Needs group analytics while respecting regional data commitments."],
        "economic": ["CIO", "Owns central platform and cross-region infrastructure costs."],
        "technical": ["Enterprise architect", "Must design runtime placement in each regional environment."],
        "operational": [
            ["Data protection officer and legal", "Decide whether and how derived datasets may be transferred."],
            ["Regional data owners", "Approve each distilled dataset before release."],
            ["Information security", "Controls on runtimes and transfer paths."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used for fidelity evaluation against full-data baselines."],
            ["Regional data platforms (warehouse / lake exports)", "proposed", "File-based extracts; no direct connectors built yet."],
            ["Data catalog and lineage tools", "proposed", "Candidate integration to record derivation of distilled datasets; not built."],
            ["Approved transfer mechanisms", "customer", "Customer-owned legal and technical transfer controls."],
            ["Group analytics platform", "customer", "Consumes approved datasets as ordinary training data."],
        ],
        "infrastructure": [
            "A compute environment inside each participating jurisdiction or legal entity.",
            "Read access to regional data for the pilot variables.",
            "A documented review and approval workflow owned by the customer.",
        ],
        "deployment": "For a pilot, runtimes are installed in two regional environments and operate on exports. "
                      "Combination and evaluation happen centrally only if the customer's legal and privacy "
                      "functions approve the transfer of the distilled datasets; otherwise evaluation stays local.",
        "constraints": [
            "Combining distilled datasets from heterogeneous regions is an architectural hypothesis not yet benchmarked.",
            "Legal review timelines are customer-controlled and may dominate pilot duration.",
            "Some data categories may not be transferable in any form; those remain out of scope.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "Internal experiments show large data reductions with limited accuracy change on single "
                   "public benchmarks. Distilling separately in several jurisdictions and combining the results "
                   "is an architectural hypothesis that has not yet been tested, and no privacy or re-identification "
                   "assessment of distilled datasets has been performed.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "Distillation runs on a standard Python runtime that can be deployed inside separate regional environments.",
        ],
        "gaps": [
            "No experiment yet on combining distilled datasets from heterogeneous (non-IID) sources.",
            "No privacy, disclosure-risk or re-identification assessment of distilled datasets.",
            "No legal analysis of distilled datasets under any specific regulation.",
            "No production deployment.",
        ],
        "risks": [
            "Legal and privacy functions may conclude that distilled datasets require the same treatment as originals.",
            "Regions with different data distributions may be unevenly represented in combined models.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative), excluding customer legal review time",
        "problem": "One group-level model that currently requires, or is blocked by, transfer of complete regional datasets.",
        "inputs": [
            "Data from two regional environments for the selected task",
            "A compute environment in each region",
            "Legal and privacy guidance on whether derived datasets may be transferred",
            "The target evaluation metric and regional baselines",
        ],
        "baseline": "Regional models trained locally on full data, or a central model on complete copies where one already exists.",
        "method": [
            "Distill in each region and evaluate locally against regional baselines.",
            "Where transfer is approved, train a combined model on distilled datasets and compare with the baseline.",
            "Measure transfer volume, storage and regional distillation overhead.",
        ],
        "technical_criteria": [
            "Model performance within customer-defined tolerance of baseline in each region.",
            "No region materially under-represented in the combined model.",
        ],
        "economic_criteria": [
            "Transfer volume and central copies reduced by a customer-defined target.",
            "Net saving or avoided cost positive after regional overhead.",
        ],
        "deliverables": [
            "Evaluation report per region and for the combined model",
            "Transfer, storage and overhead comparison",
            "Documentation of the derivation process to support the customer's own legal assessment",
            "Production adoption plan",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Customer legal and privacy approval of the operating model",
            "Named data owners for each region",
        ],
    },

    "caveats": [
        "Distilled datasets remain subject to applicable data protection, residency, transfer and contractual "
        "restrictions. Dataset distillation is not anonymization and does not provide legal authorization for "
        "cross-border data transfers.",
    ],
    "related": ["BC02", "BC11", "BC08"],
}
