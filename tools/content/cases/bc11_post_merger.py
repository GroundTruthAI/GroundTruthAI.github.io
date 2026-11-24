"""BC11 — Post-merger analytical integration. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC11",
    "slug": "post-merger-analytical-integration",
    "rank": 10,
    "tier": "explorer",
    "title": "Post-merger analytical integration",
    "eyebrow": "M&A and integration",
    "headline": "Run selected joint analytics after a merger, before the data platforms are integrated.",
    "summary": (
        "Generate approved, task-specific distilled datasets inside each company's existing data "
        "domain and combine them for selected cross-company analytical workloads."
    ),
    "problem_short": "Merged organizations want joint analytics early, but platform integration and data migration take years.",
    "solution_short": "Each legacy domain produces approved distilled datasets for a defined task; selected workloads train on the combination.",
    "outcome_short": "Earlier joint analytical capabilities with less dependency on complete data migration.",
    "cta": "Assess your post-merger analytics roadmap",
    "industries": ["multinational-groups", "financial-services", "healthcare"],
    "filters": {
        "objectives": ["segregated-analytics", "replication", "data-movement"],
        "architecture": ["multi-domain", "multi-jurisdiction"],
        "deployment": ["private-cloud", "hybrid", "on-prem"],
        "buyers": ["corp-dev", "cio", "cdo", "enterprise-architect"],
        "problems": ["integration-backlog", "consolidation-blocked", "raw-replication"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Merger business cases often depend on combined analytics: cross-selling to a joint customer "
        "base, consolidated risk views, shared demand forecasting, pooled operational benchmarks. "
        "These analytics usually wait for the data platforms to be integrated.",
        "Platform integration is a multi-year program. Systems, schemas, identifiers and data "
        "definitions differ; migration is sequenced by operational priority; legal entities, "
        "contracts and consent terms may restrict data sharing until reorganizations are complete. "
        "Meanwhile, the analytical value the deal assumed is deferred.",
        "Integration teams need a way to start selected joint analytical workloads early, without "
        "pre-empting the integration roadmap or the governance decisions that come with it.",
    ],

    "approaches": [
        {"name": "Wait for full platform integration",
         "limit": "Lowest technical risk, but defers analytical synergies by the length of the "
                  "integration program."},
        {"name": "Ad hoc raw data extracts into a shared sandbox",
         "limit": "Fast to start, but creates unmanaged raw copies, duplicates sensitive data and is "
                  "difficult to govern or retire."},
        {"name": "Early migration of selected datasets",
         "limit": "Moves whole datasets ahead of schedule, which disrupts the integration sequence and "
                  "still requires schema harmonization first."},
        {"name": "Federated queries or data virtualization",
         "limit": "Useful for reporting across systems, but heavy model training over live federated "
                  "queries is often slow and costly, and still depends on mapped schemas."},
    ],

    "solution": {
        "intro": "GroundTruth AI produces task-specific distilled datasets inside each company's existing "
                 "data domain, under that domain's controls. For a selected analytical workload with an "
                 "agreed common feature definition, the approved distilled datasets are combined in a "
                 "governed joint environment for model training. Combining distilled sets from separate "
                 "domains is an **architectural hypothesis** that a pilot is designed to test.",
        "steps": [
            ("Select a joint workload", "Integration and business leaders choose one cross-company "
             "analytical use case and confirm the legal basis for the data use."),
            ("Agree the common definition", "Data teams map the features and labels the workload needs "
             "to a shared definition. This semantic work is still required."),
            ("Distill in each domain", "The runtime runs separately in each company's environment and "
             "produces a distilled dataset and fidelity report for the task."),
            ("Approve and combine", "Data owners on each side approve their dataset; approved sets are "
             "combined in a governed joint environment."),
            ("Train and evaluate", "The joint model is trained on the combined distilled data and "
             "evaluated against each company's own data."),
        ],
        "not": [
            "It does not replace semantic interoperability, master-data harmonization or the data integration program.",
            "It does not provide legal authorization to share data before or after closing; competition-law, clean-team, contractual and consent constraints still apply.",
            "Distilled datasets are derived from source data and are not anonymized by default.",
        ],
    },

    "architecture": {
        "current": {
            "title": "Conventional: joint analytics wait for migration, or rely on raw extracts",
            "zones": [
                {"id": "a", "label": "Company A data domain", "kind": "source",
                 "nodes": [["wa", "Company A warehouse", "store"]]},
                {"id": "b", "label": "Company B data domain", "kind": "source",
                 "nodes": [["wb", "Company B warehouse", "store"]]},
                {"id": "mig", "label": "Integration program", "kind": "boundary",
                 "nodes": [["etl", "Migration / raw extracts", "system"]]},
                {"id": "joint", "label": "Joint analytics", "kind": "central",
                 "nodes": [["lake", "Consolidated raw copy", "store"], ["ml", "Joint models", "model"]]},
            ],
            "flows": [
                ["wa", "etl", "raw", "full datasets"],
                ["wb", "etl", "raw", "full datasets"],
                ["etl", "lake", "raw", "after harmonization"],
                ["lake", "ml", "raw", ""],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill per company, combine approved sets",
            "zones": [
                {"id": "a", "label": "Company A data domain", "kind": "source",
                 "nodes": [["wa", "Company A warehouse", "store"], ["ga", "GroundTruth runtime (A)", "gt"]]},
                {"id": "b", "label": "Company B data domain", "kind": "source",
                 "nodes": [["wb", "Company B warehouse", "store"], ["gb", "GroundTruth runtime (B)", "gt"]]},
                {"id": "gov", "label": "Governance", "kind": "boundary",
                 "nodes": [["appr", "Owner approval + legal basis", "system"]]},
                {"id": "joint", "label": "Joint analytics environment", "kind": "central",
                 "nodes": [["ds", "Combined distilled datasets", "store"], ["ml", "Joint models", "model"]]},
            ],
            "flows": [
                ["wa", "ga", "raw", "stays in domain"],
                ["wb", "gb", "raw", "stays in domain"],
                ["ga", "appr", "distilled", "distilled set + report"],
                ["gb", "appr", "distilled", "distilled set + report"],
                ["appr", "ds", "distilled", "approved only"],
                ["ds", "ml", "distilled", ""],
            ],
        },
        "notes": [
            "Each runtime operates inside its company's environment and security perimeter; raw data is "
            "not exchanged between the companies.",
            "A shared feature definition for the selected workload is a prerequisite, agreed by both "
            "data teams before distillation.",
        ],
    },

    "outcomes": {
        "direct": [
            "Less raw data copied into interim joint sandboxes.",
            "Lower storage and processing for selected joint training workloads.",
        ],
        "operational": [
            "Fewer unmanaged raw extracts to secure, track and retire during integration.",
            "Joint analytics that do not disrupt the migration sequence.",
            "A governed, repeatable pattern for each additional joint use case.",
        ],
        "strategic": [
            "Earlier analytical collaboration between the merged companies.",
            "Reduced dependency on complete data migration for selected workloads.",
            "Support for phased technology integration.",
            "Selected shared predictive capabilities available before platform consolidation.",
        ],
    },

    "metrics": [
        ["Time to first joint model", "Weeks from approval to a validated joint model, vs. integration roadmap date", "strategic"],
        ["Raw data copied for joint analytics", "TB of raw extracts held outside the source domains", "direct"],
        ["Joint training data volume", "TB used for the joint workload, full vs. distilled", "direct"],
        ["Model predictive performance", "Task metric of the joint model on each company's held-out data", "quality"],
        ["Segment coverage per company", "Representation of each company's key segments in the combined set", "quality"],
        ["Distillation overhead per domain", "Compute and time to produce each company's distilled set", "direct"],
        ["Joint use cases enabled", "Number of cross-company workloads running before full integration", "strategic"],
        ["Governance effort", "Approvals, reviews and person-days per joint dataset", "operational"],
    ],

    "stakeholders": {
        "sponsor": ["M&A integration lead", "Needs early evidence of deal synergies without derailing the integration plan."],
        "economic": ["CIO of the combined organization", "Owns integration budget and the interim data architecture."],
        "technical": ["Enterprise architect and data platform leads of both companies", "Must agree feature definitions, placement and the joint environment."],
        "operational": [
            ["CDO / data owners on each side", "Approval of each distilled dataset and its permitted use."],
            ["Legal, privacy and competition counsel", "Legal basis for data use, especially before closing."],
            ["Business unit analytics leads", "Value and validity of the joint model for their market."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to evaluate fidelity against a full-data baseline."],
            ["Warehouse exports (Parquet / CSV) in each domain", "proposed", "File-based hand-off for the pilot."],
            ["Combining distilled sets from separate domains", "proposed", "Core hypothesis of this case; not yet benchmarked."],
            ["Data catalogs and access-approval workflows", "customer", "Customer-owned governance tools record approvals."],
            ["Joint analytics environment (e.g. a governed cloud workspace)", "customer", "Consumes approved distilled datasets."],
        ],
        "infrastructure": [
            "Compute inside each company's environment for its distillation runtime.",
            "A governed joint environment for combined distilled datasets and model training.",
            "Agreed feature mapping for the selected workload.",
        ],
        "deployment": "For a pilot, a runtime is deployed separately in each company's environment and "
                      "operates on exports of the agreed features. Approved distilled datasets move to a "
                      "joint workspace under the access rules set by the integration governance board.",
        "constraints": [
            "Before closing, competition law may prohibit sharing competitively sensitive information; a clean-team arrangement and counsel's approval are needed.",
            "Schema and identifier differences must be resolved for the selected features before distillation.",
            "Consent and contractual terms in each legacy company may limit permitted use.",
        ],
    },

    "evidence": {
        "status": "Proposed enterprise application — not yet validated in production",
        "summary": "Internal experiments support large data reductions within a single dataset. Combining "
                   "distilled datasets produced independently in different organizations, with different "
                   "data distributions, has not been tested; a pilot is the first measurement.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "Distillation runs as a software step on a standard Python runtime that can be deployed separately in each environment.",
        ],
        "gaps": [
            "No experiment on combining distilled sets from heterogeneous, independently governed sources.",
            "No measurement of how well a joint model generalizes to each company's population.",
            "No production deployment in an M&A context.",
        ],
        "risks": [
            "Differences in data definitions can make combined datasets misleading if mapping is incomplete.",
            "Legal or competition-law review may restrict or delay the selected workload.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative), after legal basis is confirmed",
        "problem": "One cross-company analytical workload the deal case depends on, e.g. joint churn, demand or risk modeling.",
        "inputs": [
            "Agreed feature and label definitions for the workload",
            "Exports of those features in each company's environment",
            "Compute in each environment and a governed joint workspace",
            "Written confirmation of the legal basis from counsel",
        ],
        "baseline": "A joint model trained on a harmonized full-data extract, or each company's separate model where a joint extract is not permitted.",
        "method": [
            "Distill separately in each domain; combine the approved distilled sets.",
            "Train the joint model and evaluate it on each company's held-out data.",
            "Compare against the baseline on performance, data copied and time to model.",
            "Record approvals and governance effort per dataset.",
        ],
        "technical_criteria": [
            "Joint model performance within the customer-defined tolerance of the baseline on each company's data.",
            "Key segments of both companies represented in the combined set.",
            "No raw data exchanged between the companies.",
        ],
        "economic_criteria": [
            "Joint model available earlier than the integration roadmap would allow.",
            "Raw data copied for the workload reduced by a customer-defined target.",
        ],
        "deliverables": [
            "Per-domain fidelity reports and a joint model evaluation",
            "Reference architecture for interim joint analytics",
            "Governance and approval playbook for further workloads",
            "Assessment of fit with the integration roadmap",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Legal, privacy and competition review completed",
            "Data owners on both sides sign off the approval workflow",
            "Integration program confirms the interim pattern and its retirement path",
        ],
    },

    "caveats": [
        "Dataset distillation is not a substitute for semantic interoperability, data integration or legal "
        "authorization. Before closing, competition-law constraints on exchanging information apply in full.",
    ],
    "related": ["BC02", "BC07", "BC08"],
}
