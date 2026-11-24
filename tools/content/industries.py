"""Industries. Many-to-many with business cases: each "cases" list is the inverse of the
BC -> industry mapping in tools/CONTENT_BRIEF.md. Industry pages explain sector-specific
constraints and point to business cases; they do not repeat business-case content.
Plain strings only; inline **bold** / *italic* allowed.
"""

INDUSTRIES = [
    {
        "slug": "manufacturing",
        "name": "Manufacturing & industrial AI",
        "short": "Plants generate high-frequency process and equipment data behind OT boundaries, while AI teams work centrally.",
        "context": [
            "Manufacturers run AI for predictive maintenance, quality inspection, process optimization "
            "and energy management. The data that matters most (sensor histories, machine states, "
            "quality measurements) lives in plant historians and control systems, segmented from "
            "enterprise IT and often different at every site.",
            "The constraint is rarely a shortage of data. It is the cost and policy friction of moving "
            "plant data to where models are trained, the heterogeneity between lines and sites, and the "
            "scarcity of labeled failures that predictive models depend on.",
        ],
        "data_estate": [
            "Process historians and time-series databases",
            "SCADA, PLC and DCS signals",
            "MES and quality management records",
            "Maintenance work orders (CMMS / EAM)",
            "Machine vision and inspection images",
        ],
        "constraints": {
            "technical": [
                "High-frequency, multivariate time series with site-specific tag naming.",
                "Rare, sparsely labeled failure events.",
                "Different equipment generations and configurations across lines and plants.",
            ],
            "operational": [
                "No added load or risk on control systems; availability comes first.",
                "Change windows in OT environments are limited and planned well in advance.",
                "Plant engineering time for labeling and validation is scarce.",
            ],
            "governance": [
                "OT security architectures based on zones and conduits, often aligned with IEC 62443.",
                "Process data may be trade secret or export-controlled.",
                "Equipment vendor contracts can restrict data use or remote access.",
            ],
        },
        "cases": [
            ["BC01", "Central AI programs need plant data without opening new raw data paths from OT into IT."],
            ["BC04", "Multi-plant producers want shared equipment-health and anomaly models without consolidating every historian."],
            ["BC03", "Vision and process models retrained on large image and sensor archives carry significant compute cost."],
            ["BC05", "Line-side sensors and cameras produce more data than site uplinks and central platforms can usefully absorb."],
            ["BC09", "Quality and maintenance models need regular retraining as products, materials and equipment change."],
        ],
        "buyers": ["COO", "Industrial digitalization leader", "OT architect", "CIO", "Head of manufacturing analytics"],
        "pilot_hint": "Start with one predictive-maintenance model for a well-instrumented asset class at a single plant that already exports historian data to IT.",
    },
    {
        "slug": "energy-utilities",
        "name": "Energy, utilities & critical infrastructure",
        "short": "Grid, generation and network operators combine strict OT security with geographically dispersed assets.",
        "context": [
            "Utilities and critical infrastructure operators use analytics for asset health, outage "
            "prediction, load forecasting and network optimization. Their data comes from substations, "
            "generation plants, pipelines and field devices spread over large territories, and much of it "
            "sits inside control environments subject to dedicated security regulation.",
            "Moving raw operational data to central platforms is constrained by regulation, by limited "
            "telemetry bandwidth at remote assets, and by the operator's obligation to keep control "
            "systems isolated and available.",
        ],
        "data_estate": [
            "SCADA and energy management system telemetry",
            "Substation and protection relay records",
            "Smart meter and AMI data",
            "Asset registers and maintenance histories",
            "Weather and environmental data feeds",
        ],
        "constraints": {
            "technical": [
                "Remote assets with limited or intermittent connectivity.",
                "Mixed legacy and modern protocols across decades-old installations.",
                "Strong seasonality and regime changes in load and generation data.",
            ],
            "operational": [
                "Continuity of supply takes precedence over analytics workloads.",
                "Field changes require formal outage and change planning.",
                "Small central data teams serving large asset bases.",
            ],
            "governance": [
                "Sector cybersecurity obligations such as NERC CIP in North America or NIS2 in the EU.",
                "Customer metering data is personal data in many jurisdictions.",
                "Regulators may scrutinize technology spend and its benefit to customers.",
            ],
        },
        "cases": [
            ["BC01", "Control-environment data is needed for central asset-health models, but operators must keep OT isolated."],
            ["BC04", "Fleets of substations, plants or wind farms differ in equipment and conditions, yet share failure modes worth learning jointly."],
            ["BC05", "Remote assets generate telemetry faster than constrained links can carry it to central systems."],
            ["BC10", "Energy companies face scrutiny of their own digital footprint and need measurable reductions."],
        ],
        "buyers": ["COO / Head of network operations", "OT security lead", "CIO", "Head of asset management analytics"],
        "pilot_hint": "Start with an asset-health model for one equipment class (for example transformers) using historical data already exported from the control environment.",
    },
    {
        "slug": "oil-gas-mining",
        "name": "Oil, gas & mining",
        "short": "Remote, harsh-environment operations with costly connectivity and strict separation of control systems.",
        "context": [
            "Upstream, midstream and mining operators apply AI to equipment reliability, process "
            "optimization, safety monitoring and production forecasting. Assets such as offshore "
            "platforms, pipelines and remote mine sites generate large volumes of sensor data far from "
            "central data centers.",
            "Connectivity from these sites is often satellite or microwave, expensive and limited, and "
            "operational networks are tightly segregated for safety reasons. Moving full raw histories "
            "to a central platform is slow, costly and frequently against policy.",
        ],
        "data_estate": [
            "Process historians on platforms, plants and mine sites",
            "Rotating-equipment vibration and condition data",
            "Drilling, production and haulage telemetry",
            "Maintenance and inspection records",
            "Geospatial and survey data",
        ],
        "constraints": {
            "technical": [
                "Low-bandwidth, high-cost links from remote sites.",
                "Harsh-environment hardware with limited compute at site.",
                "Heterogeneous equipment across assets acquired over decades.",
            ],
            "operational": [
                "Safety-critical operations with strict permit-to-work and change control.",
                "Limited on-site IT staff; remote support is the norm.",
                "Production continuity drives every intervention window.",
            ],
            "governance": [
                "Segregated control networks under corporate and sector security standards.",
                "Joint-venture and partner agreements that govern data ownership and sharing.",
                "Host-country rules on data and operational information in some jurisdictions.",
            ],
        },
        "cases": [
            ["BC01", "Process data from segregated control networks is needed for central reliability models."],
            ["BC04", "Operators run similar equipment across many remote sites and want to learn from rare failures across the fleet."],
            ["BC05", "Satellite and microwave links make every transferred gigabyte from site expensive."],
        ],
        "buyers": ["COO / VP operations", "Head of reliability engineering", "OT architect", "CIO"],
        "pilot_hint": "Start with rotating-equipment condition data from one asset with an existing historian export and a known history of failures.",
    },
    {
        "slug": "transportation-logistics",
        "name": "Transportation & logistics",
        "short": "Distributed fleets, terminals and networks produce telemetry that is costly to centralize in full.",
        "context": [
            "Rail operators, airlines, ports, fleet operators and logistics networks use AI for "
            "predictive maintenance, network planning, energy efficiency and safety. Data is produced by "
            "vehicles, signaling systems, terminal equipment and depots spread across regions or "
            "countries.",
            "Much operational data sits in safety-relevant or segregated systems, and connectivity from "
            "moving assets is intermittent. Central teams therefore receive partial, delayed or "
            "aggregated data, which limits fleet-wide models.",
        ],
        "data_estate": [
            "Onboard vehicle and rolling-stock telemetry",
            "Signaling, traffic management and terminal control data",
            "Maintenance and depot records",
            "Telematics and GPS traces",
            "Operational schedules and event logs",
        ],
        "constraints": {
            "technical": [
                "Intermittent connectivity from moving assets.",
                "Mixed fleets with different sensor sets and data formats.",
                "Event-heavy data where rare incidents carry the most value.",
            ],
            "operational": [
                "Safety-relevant systems with certification and change constraints.",
                "Maintenance windows tied to timetables and asset availability.",
                "Data often owned by different operators, lessors or manufacturers.",
            ],
            "governance": [
                "Transport safety regulation and operator security requirements.",
                "Critical-infrastructure cybersecurity obligations in many jurisdictions.",
                "Location data from vehicles can be personal data when linked to drivers or crew.",
            ],
        },
        "cases": [
            ["BC04", "Fleet-wide maintenance models need data from many depots, vehicles and regions with different operating conditions."],
            ["BC01", "Signaling and terminal control data sits in segregated environments that central analytics cannot freely access."],
            ["BC05", "Vehicles and terminal equipment generate telemetry beyond what intermittent links can upload."],
        ],
        "buyers": ["COO / Head of operations", "Head of fleet engineering", "CIO", "Enterprise architect"],
        "pilot_hint": "Start with a component-failure model for one vehicle or equipment class where depot data is already collected centrally in part.",
    },
    {
        "slug": "financial-services",
        "name": "Banking, insurance & financial services",
        "short": "Large, regulated data estates split across entities, countries and platforms, with heavy model portfolios.",
        "context": [
            "Banks and insurers run large model portfolios for credit, fraud, pricing, claims, marketing "
            "and risk. Their data is spread across legal entities, countries, legacy core systems and "
            "cloud platforms, and every model is subject to validation and governance requirements.",
            "Consolidating data across entities is slowed by regulation, legacy architecture and "
            "ownership boundaries, while the cost of training, retraining and storing data for hundreds "
            "of models keeps growing.",
        ],
        "data_estate": [
            "Core banking and policy administration systems",
            "Transaction and payment records",
            "Claims, underwriting and credit files",
            "Customer interaction and digital channel data",
            "Market and reference data",
        ],
        "constraints": {
            "technical": [
                "Highly imbalanced targets (fraud, default, large claims) where rare cases matter most.",
                "Legacy core systems with complex extracts and inconsistent identifiers.",
                "Large model portfolios on mixed on-premises and cloud platforms.",
            ],
            "operational": [
                "Model changes go through validation and approval cycles.",
                "Retraining calendars tied to risk, regulatory and business reporting cycles.",
                "Strong separation between business lines and legal entities.",
            ],
            "governance": [
                "Model risk management expectations (for example SR 11-7 in the US) and validation evidence.",
                "Data protection and banking secrecy rules, plus cross-border transfer restrictions.",
                "Operational resilience and ICT third-party rules such as DORA in the EU.",
            ],
        },
        "cases": [
            ["BC02", "Group-wide risk and customer models need data held by separate entities and business lines."],
            ["BC09", "Large model portfolios are retrained regularly, and each retrain reprocesses growing histories."],
            ["BC03", "Training spend for fraud, credit and pricing models grows with transaction volumes."],
            ["BC07", "Customer data often must remain in its country of origin while group analytics are centralized."],
            ["BC08", "Workloads split between on-premises cores and several clouds duplicate large datasets."],
            ["BC11", "Bank and insurer mergers promise joint analytics long before core systems are integrated."],
            ["BC06", "Data and compute footprints grow with regulatory retention and analytics demand."],
        ],
        "buyers": ["CDO", "CIO", "Head of model risk / validation", "Head of ML platform", "CFO"],
        "pilot_hint": "Start with one well-understood, regularly retrained model (for example a fraud or propensity model) where validation teams can compare outcomes directly.",
    },
    {
        "slug": "healthcare",
        "name": "Healthcare & life sciences",
        "short": "Sensitive data distributed across hospitals, labs and research partners, under strict protection rules.",
        "context": [
            "Hospital groups, payers, research networks and life-sciences companies want analytics across "
            "institutions: outcome prediction, operational planning, real-world evidence and research "
            "cohorts. The data is held by separate institutions with their own systems, consent regimes "
            "and ethics approvals.",
            "Pooling raw patient data is slow and often not permitted. Even where it is, the governance "
            "effort per dataset is high, so analytics programs move at the pace of data-sharing agreements.",
        ],
        "data_estate": [
            "Electronic health records",
            "Laboratory and imaging systems",
            "Claims and administrative data",
            "Clinical trial and registry data",
            "Device and remote-monitoring data",
        ],
        "constraints": {
            "technical": [
                "Heterogeneous coding systems and data models across institutions.",
                "Small, sensitive subpopulations where under-representation creates bias.",
                "Mixed structured, imaging and free-text data.",
            ],
            "operational": [
                "Clinical systems are prioritized over analytics workloads.",
                "Ethics, consent and data-access committees review each new use.",
                "Limited data engineering capacity in individual institutions.",
            ],
            "governance": [
                "Health data is special-category personal data under GDPR and protected health information under HIPAA.",
                "Distilled datasets derived from patient records are not anonymized by default.",
                "Data-sharing agreements and ethics approvals define permitted use per project.",
            ],
        },
        "cases": [
            ["BC02", "Multi-hospital groups and research networks want shared models without pooling all patient-level data."],
            ["BC07", "Patient data frequently must stay within a country or institution, while analytics span several."],
            ["BC11", "Hospital and life-sciences mergers need joint analytics before clinical systems are integrated."],
        ],
        "buyers": ["CDO / Chief Medical Information Officer", "CIO", "Head of research data", "Data protection officer"],
        "pilot_hint": "Start with an operational (non-clinical-decision) model, such as capacity or length-of-stay forecasting, across two sites with existing data-sharing approval.",
    },
    {
        "slug": "telecommunications",
        "name": "Telecommunications",
        "short": "Network and device data at massive scale, produced at the edge and processed centrally.",
        "context": [
            "Operators use AI for network planning, fault prediction, energy optimization, churn and "
            "customer experience. Network elements, devices and customer interactions generate data "
            "volumes that dominate storage and transport budgets.",
            "Much of that data is collected, transported and stored in full before anyone decides what "
            "is useful. Training and retraining models on it is expensive, and transporting it from the "
            "network edge consumes capacity the operator would rather sell.",
        ],
        "data_estate": [
            "Network element performance counters and alarms",
            "Device and CPE logs",
            "Call detail and usage records",
            "Customer care and digital channel interactions",
            "Network inventory and topology data",
        ],
        "constraints": {
            "technical": [
                "Very high data rates from distributed network elements.",
                "Multi-vendor equipment with different counters and log formats.",
                "Rapid change in traffic patterns and network configuration.",
            ],
            "operational": [
                "Network stability and capacity take priority over analytics traffic.",
                "Distributed operations across regions and subsidiaries.",
                "Large model estates spanning network and commercial teams.",
            ],
            "governance": [
                "Communications data confidentiality and data protection obligations.",
                "Data localization requirements in some markets.",
                "Critical-infrastructure security obligations for network operators.",
            ],
        },
        "cases": [
            ["BC05", "Device logs and network telemetry can be reduced near the source before consuming transport capacity."],
            ["BC03", "Network and customer models are trained on very large historical datasets."],
            ["BC09", "Traffic and behavior shift quickly, forcing frequent retraining of production models."],
            ["BC06", "Operators run their own data centers and want better utilization of storage and compute."],
            ["BC07", "Multinational operators must keep subscriber data in-country while sharing analytical capabilities."],
        ],
        "buyers": ["CTO", "Head of network analytics", "CIO", "Head of ML platform", "Infrastructure leader"],
        "pilot_hint": "Start with one device-log or network-fault prediction model where the transported data volume and its cost are already known.",
    },
    {
        "slug": "retail-consumer",
        "name": "Retail & consumer",
        "short": "High-volume transactional and behavioral data feeding many frequently retrained models.",
        "context": [
            "Retailers and consumer brands run forecasting, pricing, personalization, assortment and "
            "supply-chain models. These depend on transaction, clickstream and inventory data whose "
            "volume grows with every channel and season.",
            "Data is typically spread across e-commerce platforms, store systems and several cloud "
            "services, and models are retrained often to keep up with demand shifts and promotions.",
        ],
        "data_estate": [
            "Point-of-sale and e-commerce transactions",
            "Clickstream and app behavior data",
            "Inventory, supply-chain and logistics data",
            "Loyalty and CRM records",
            "Product catalog and pricing data",
        ],
        "constraints": {
            "technical": [
                "Strong seasonality, promotions and long-tail products.",
                "Data split across commerce platforms, store systems and clouds.",
                "Many models per category, region or channel.",
            ],
            "operational": [
                "Retraining peaks before seasonal events, competing for compute.",
                "Fast-moving merchandising decisions depend on model freshness.",
                "Lean central data teams relative to the model estate.",
            ],
            "governance": [
                "Consumer data protection and consent requirements for personalization.",
                "Contractual limits on data held by marketplace and platform partners.",
                "Cost accountability for cloud spend across business units.",
            ],
        },
        "cases": [
            ["BC09", "Demand and personalization models are retrained frequently on growing histories."],
            ["BC03", "Training spend scales with transaction and clickstream volumes."],
            ["BC08", "Data duplicated between commerce platforms and analytics clouds adds transfer and storage cost."],
        ],
        "buyers": ["CDO / Head of analytics", "CTO", "Head of ML platform", "CFO"],
        "pilot_hint": "Start with one demand-forecasting or propensity model with a weekly or monthly retraining cadence and known compute cost.",
    },
    {
        "slug": "multinational-groups",
        "name": "Industrial groups & multinationals",
        "short": "Decentralized subsidiaries, regions and acquisitions, each with its own data platform and rules.",
        "context": [
            "Diversified industrial groups and multinational corporations operate through subsidiaries, "
            "divisions and regional entities that often run separate data platforms. Group functions "
            "want enterprise-wide analytics; local entities own their data and answer to local rules.",
            "Full consolidation into one platform is expensive, politically sensitive and, in some "
            "jurisdictions, restricted. Acquisitions add new estates faster than integration programs "
            "can absorb them.",
        ],
        "data_estate": [
            "Subsidiary ERP and operational systems",
            "Regional data warehouses and lakes",
            "Group finance and procurement data",
            "Divisional operational and customer data",
            "Data estates inherited through acquisitions",
        ],
        "constraints": {
            "technical": [
                "Different platforms, schemas and identifiers per entity.",
                "Uneven data maturity between divisions and regions.",
                "Varying cloud providers and hosting models across the group.",
            ],
            "operational": [
                "Local data ownership and decision rights.",
                "Group programs depend on local engineering capacity.",
                "Integration of acquisitions competes with business-as-usual change.",
            ],
            "governance": [
                "Multiple jurisdictions with their own data protection and transfer rules.",
                "Intra-group data transfer agreements required for personal data.",
                "Competition-law limits on information exchange before acquisitions close.",
            ],
        },
        "cases": [
            ["BC02", "Group analytics need subsidiary data without forcing complete consolidation."],
            ["BC07", "Entities in different jurisdictions must keep original data in place."],
            ["BC11", "Acquisitions promise joint analytics before platforms are integrated."],
            ["BC08", "Subsidiaries on different clouds duplicate data to share it."],
            ["BC10", "Group sustainability commitments increasingly extend to digital and AI workloads."],
        ],
        "buyers": ["Group CIO", "Group CDO", "Enterprise architect", "M&A integration lead", "Chief Sustainability Officer"],
        "pilot_hint": "Start with one group-level model (for example demand, procurement or risk) using data from two subsidiaries that already agree on the feature definitions.",
    },
    {
        "slug": "ai-infrastructure",
        "name": "AI infrastructure, cloud & data center providers",
        "short": "Providers and platform teams whose margins depend on storage, compute and energy efficiency.",
        "context": [
            "Cloud providers, data center operators, AI platform vendors and hardware OEMs sell capacity "
            "and efficiency. Their customers' training workloads consume storage, compute and energy that "
            "the provider must supply, cool and price competitively.",
            "For these organizations, dataset optimization is both an internal efficiency lever and a "
            "potential value-added capability to embed in their own offerings, which is why OEM and "
            "co-sell models are relevant here.",
        ],
        "data_estate": [
            "Customer training datasets hosted on the platform",
            "Platform telemetry and utilization data",
            "Storage, backup and replication tiers",
            "Power, cooling and facility monitoring data",
        ],
        "constraints": {
            "technical": [
                "Multi-tenant environments where customer data cannot be inspected without permission.",
                "Very large, diverse workloads with different accuracy requirements.",
                "Energy and utilization must be measured precisely to be marketable.",
            ],
            "operational": [
                "Any embedded capability must operate at platform scale and with clear SLAs.",
                "Customer opt-in and control over dataset changes.",
                "Integration into existing platform services and billing.",
            ],
            "governance": [
                "Providers act as processors for customer data and cannot change its use unilaterally.",
                "Energy and sustainability claims to customers must be substantiated.",
                "Contractual commitments on data location and handling.",
            ],
        },
        "cases": [
            ["BC06", "Storage, compute and energy per workload drive provider costs and pricing."],
            ["BC03", "Offering lower-cost training to customers can differentiate an AI platform."],
            ["BC10", "Customers expect measurable sustainability data for their AI workloads."],
            ["BC08", "Data moving between clouds and on-premises environments generates transfer and ingestion cost."],
        ],
        "buyers": ["CTO / Head of product", "Infrastructure & data center leader", "Head of partnerships / OEM", "Chief Sustainability Officer"],
        "pilot_hint": "Start with one internal or design-partner training workload where energy and utilization can be metered on dedicated hardware.",
    },
]
