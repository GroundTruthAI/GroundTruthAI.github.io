# Content brief — GroundTruth AI business-case website

This file is the single source of truth for everyone writing site content or internal
commercial documents. Read it fully before writing.

## 1. Commercial principle

Lead with the business problem, not the algorithm. Every page follows this order:
business problem → opportunity → proposed solution → business outcomes → supporting
technology → evidence → integration/deployment → commercial engagement.

Audience: CIOs, CTOs, CDOs, COOs, industrial technology executives, OT architects,
enterprise architects, heads of ML platforms. Write like a senior enterprise architect
briefing an executive: concrete, specific, calm. No hype words ("revolutionary",
"game-changing", "radical", "unparalleled", "magic"). No exclamation marks. US English.

Brand name in prose: **GroundTruth AI**.

## 2. Facts we may state (and only these)

Company stage: proof-of-concept-ready technology seeking structured enterprise pilots.
There are **no production deployments, no customers, no testimonials, no certifications,
no partner integrations and no published case studies**. Never imply otherwise.
Do not name team members. Do not publish pricing or license prices.

Experimental evidence (internal experiments, public benchmark datasets, classification
tasks, not independently replicated):

| Dataset | Type / model | Data reduction | Baseline acc. | Distilled acc. | Change |
|---|---|---|---|---|---|
| Iris | Tabular · deep learning (MLP) | 95% | 97.4% | 94.7% | −2.7 pp |
| Wine | Tabular · deep learning (MLP) | 86% | 97.8% | 95.6% | −2.2 pp |
| Breast Cancer | Tabular · deep learning (MLP) | 95% | 96.5% | 95.1% | −1.4 pp |
| MNIST | Image · CNN | 93% | 96.5% | 93.7% | −2.8 pp |

Internal energy measurements (methodology not yet published; energy estimated with
Schneider Electric reference data; the published figures do not separately report the
energy consumed by the distillation step itself):
- 86% less energy per model training run on a workstation after data reduction.
- 39% less energy on IoT / edge devices at the point of capture.

Limits of the evidence that must be acknowledged where relevant:
- Small, clean, i.i.d. public benchmarks; classification only.
- No industrial time-series, OT historian, log or event-stream benchmarks yet.
- No experiment yet on distilling **separately in several domains and combining the
  distilled sets** (non-IID / heterogeneous sources). This is the core hypothesis behind
  BC01, BC02, BC04, BC07, BC08, BC11 and must be called an architectural hypothesis.
- No rare-event / minority-class coverage study yet.
- No end-to-end cost measurement on enterprise infrastructure.
- No real-time or specific edge-device execution has been validated: never claim real-time
  execution or device compatibility.

Verified technical surface (from the prototype code): Python runtime; scikit-learn-compatible
model adapter; tabular numeric data via pandas / NumPy; classification tasks; CNN training on
image data (MNIST). **Everything else is "proposed"**: OT historians (e.g. AVEVA PI), OPC UA,
MQTT, Kafka, cloud object stores, Spark/Databricks, MLflow, Kubeflow, data catalogs,
container/Kubernetes packaging, drift-triggered regeneration, etc. Name such tools only as
"proposed integration" or "typical customer system".

Adjacent capabilities from the same engine (maturity: prototype; not validated on customer
data): data drift detection, anomaly detection.

## 3. Evidence vocabulary (use exactly)

- **Demonstrated business outcome** — measured in a customer production environment. *None exist today.*
- **Experimentally supported technical outcome** — measured in internal experiments (the table above).
- **Proposed enterprise application** — architecture and value hypothesis; not yet validated in production.
- **Illustrative financial scenario** — arithmetic on stated assumptions, not a forecast.

Every business case is currently a *Proposed enterprise application — not yet validated in production*.

## 4. Mandatory qualifications

- Distilled datasets are derived from source data. They can still contain personal, confidential,
  export-controlled or regulated information and remain subject to the same data protection,
  residency, transfer, contractual and security controls. Distillation is **not**
  anonymization and does **not** grant legal authorization for any transfer.
- Distillation does not replace network segmentation, OT security controls, semantic
  interoperability, master-data harmonization or data integration programs.
- Dataset reduction ≠ equivalent reduction of total infrastructure or data-center spend.
  Only the data-proportional share of a cost line is affected, net of the cost of
  distillation itself (compute, energy, operations, governance).
- Energy and sustainability statements must include the distillation step's own energy and
  must say lifecycle measurement is required before any environmental claim.
- Accuracy can drop (benchmarks: up to −2.8 pp). Acceptance thresholds are set per task by the customer.

## 5. Fixed decisions

Commercial priority ranking (do not change):
1 BC01 OT/IT data segregation (flagship) · 2 BC02 Cross-enterprise analytics (flagship) ·
3 BC03 AI training cost optimization (flagship) · 4 BC04 Distributed industrial intelligence (flagship) ·
5 BC09 Continuous model retraining · 6 BC05 Edge-to-cloud data optimization ·
7 BC07 Data residency and sovereignty · 8 BC08 Multicloud data optimization ·
9 BC06 AI infrastructure and data center efficiency · 10 BC11 Post-merger analytical integration ·
11 BC10 Sustainable AI infrastructure.

Slugs: BC01 `ot-it-data-segregation` · BC02 `cross-enterprise-analytics` · BC03 `ai-training-cost-optimization` ·
BC04 `distributed-industrial-intelligence` · BC05 `edge-to-cloud-data-optimization` · BC06 `ai-infrastructure-efficiency` ·
BC07 `data-residency-and-sovereignty` · BC08 `multicloud-data-optimization` · BC09 `continuous-model-retraining` ·
BC10 `sustainable-ai-infrastructure` · BC11 `post-merger-analytical-integration`.

Industries (slug — name):
`manufacturing` Manufacturing & industrial AI · `energy-utilities` Energy, utilities & critical infrastructure ·
`oil-gas-mining` Oil, gas & mining · `transportation-logistics` Transportation & logistics ·
`financial-services` Banking, insurance & financial services · `healthcare` Healthcare & life sciences ·
`telecommunications` Telecommunications · `retail-consumer` Retail & consumer ·
`multinational-groups` Industrial groups & multinationals · `ai-infrastructure` AI infrastructure, cloud & data center providers.

Business case → industries:
BC01 manufacturing, energy-utilities, oil-gas-mining, transportation-logistics ·
BC02 financial-services, healthcare, multinational-groups ·
BC03 financial-services, telecommunications, retail-consumer, manufacturing, ai-infrastructure ·
BC04 manufacturing, energy-utilities, oil-gas-mining, transportation-logistics ·
BC05 telecommunications, manufacturing, energy-utilities, transportation-logistics, oil-gas-mining ·
BC06 ai-infrastructure, telecommunications, financial-services ·
BC07 financial-services, healthcare, multinational-groups, telecommunications ·
BC08 financial-services, retail-consumer, ai-infrastructure, multinational-groups ·
BC09 financial-services, retail-consumer, telecommunications, manufacturing ·
BC10 ai-infrastructure, multinational-groups, energy-utilities ·
BC11 multinational-groups, financial-services, healthcare.

Filter vocabularies (use these keys only):
- objectives: `segregated-analytics` Enable analytics across segregated data · `training-cost` Reduce AI training costs ·
  `data-movement` Reduce data movement · `distributed-infra` Optimize distributed infrastructure ·
  `replication` Reduce data replication · `operational-efficiency` Improve operational efficiency ·
  `residency` Support data residency objectives · `energy` Reduce energy consumption
- architecture: `ot-it` Segregated OT/IT networks · `multi-domain` Multiple data domains or subsidiaries ·
  `multi-site` Multi-site or multi-facility · `edge` Edge and device fleets · `multicloud` Hybrid and multicloud ·
  `centralized-ml` Centralized ML platform · `multi-jurisdiction` Multi-jurisdiction data estate
- deployment: `on-prem` On-premises or plant · `private-cloud` Private cloud or VPC · `public-cloud` Public cloud ·
  `edge-gateway` Edge gateway · `hybrid` Hybrid
- buyers: `cio` CIO · `cto` CTO · `cdo` CDO / Chief Data Officer · `coo` COO · `ot-leader` Industrial / OT technology leader ·
  `enterprise-architect` Enterprise architect · `ml-platform` Head of ML / MLOps platform · `infra-leader` Infrastructure & data center leader ·
  `sustainability` Chief Sustainability Officer · `corp-dev` M&A integration lead · `cfo` CFO
- problems: `raw-replication` Raw data replicated only to train models · `training-spend` Rising training and retraining spend ·
  `bandwidth` Constrained bandwidth or transfer cost · `consolidation-blocked` Data consolidation blocked or too slow ·
  `rare-events` Rare failures scattered across sites · `storage-growth` Growing storage footprint ·
  `cross-border` Cross-border transfer restrictions · `model-staleness` Models going stale between retrains ·
  `energy-footprint` AI energy footprint · `integration-backlog` Post-merger integration backlog

ROI scenario keys: `transfer` (data movement & replication), `training` (training & retraining spend),
`infrastructure` (storage, compute & energy of eligible workloads).

Pilot convention: indicative duration 8–12 weeks, one bounded workload, customer-defined acceptance
thresholds, side-by-side comparison against a baseline trained on the full data, all measurements
include distillation overhead, customer keeps the results. Pilot pricing is not published.
