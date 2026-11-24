"""BC05 — Edge-to-cloud data optimization. Schema: see bc01_ot_it.py."""

CASE = {
    "id": "BC05",
    "slug": "edge-to-cloud-data-optimization",
    "rank": 6,
    "tier": "explorer",
    "title": "Edge-to-cloud data optimization",
    "eyebrow": "Distributed data flows",
    "headline": "Send the data your models need, not everything your devices produce.",
    "summary": (
        "Optimize task-relevant datasets close to where sensors, cameras and edge systems generate "
        "them, and transfer only approved, distilled datasets to central infrastructure."
    ),
    "problem_short": "Sensors, cameras and edge systems generate more data than networks, cloud ingestion and central storage can economically absorb.",
    "solution_short": "Task-aware distillation on an edge gateway or site server reduces training data before it is transmitted.",
    "outcome_short": "Less network traffic and cloud ingestion for AI training, with a scalable distributed architecture.",
    "cta": "Evaluate your edge-to-cloud data flows",
    "industries": ["telecommunications", "manufacturing", "energy-utilities", "transportation-logistics", "oil-gas-mining"],
    "filters": {
        "objectives": ["data-movement", "distributed-infra", "energy", "operational-efficiency"],
        "architecture": ["edge", "multi-site", "centralized-ml"],
        "deployment": ["edge-gateway", "on-prem", "hybrid"],
        "buyers": ["cto", "ot-leader", "infra-leader", "enterprise-architect"],
        "problems": ["bandwidth", "storage-growth", "raw-replication"],
    },
    "roi_scenario": "transfer",

    "challenge": [
        "Distributed sensors, industrial devices, network equipment, vehicles and cameras produce "
        "continuous data streams. In many estates the volume generated at the edge already exceeds "
        "what can be transmitted, ingested, stored or processed centrally at an acceptable cost, "
        "particularly where connectivity is cellular, satellite or shared with operational traffic.",
        "Central AI teams still need representative training data from these fleets. The usual "
        "answer is to ship as much as the link allows and sort it out in the cloud, which turns "
        "bandwidth, ingestion fees and central storage into a cost that grows with every new device.",
        "The decision of what to keep is therefore made by link capacity and fixed retention rules, "
        "not by what a given model actually needs to learn.",
    ],

    "approaches": [
        {"name": "Transmit everything and filter centrally",
         "limit": "Simple to operate, but bandwidth, ingestion and central storage scale with raw volume, "
                  "and constrained links force data to be dropped or delayed without regard to its value."},
        {"name": "Fixed sampling, compression or aggregation at the edge",
         "limit": "Predictable and lightweight, but task-agnostic: generic compression keeps redundancy and "
                  "fixed sampling or averaging can discard the rare events a model must learn from."},
        {"name": "Event-triggered capture rules",
         "limit": "Useful for known conditions, but rules must be maintained by hand for every device type "
                  "and miss patterns nobody anticipated."},
        {"name": "Run full model training at the edge",
         "limit": "Avoids transfer but requires training-capable hardware and ML operations at every site, "
                  "and fragments model development across the fleet."},
    ],

    "solution": {
        "intro": "GroundTruth AI places the data-reduction step near the point of generation. A distillation "
                 "runtime on an edge gateway or site server builds a compact, task-specific training dataset "
                 "from locally buffered data, validates it, and forwards only the approved distilled dataset "
                 "through the existing uplink. Raw data stays at the edge under local retention rules.",
        "steps": [
            ("Define the task", "Central teams specify the model, the variables and the acceptance thresholds "
             "for accuracy and event coverage."),
            ("Buffer locally", "Edge data is collected in a local buffer on the gateway or site server, as many "
             "estates already do for store-and-forward."),
            ("Distill near the source", "The runtime generates a distilled dataset for the task from each batch "
             "of buffered data, on a schedule set by the customer."),
            ("Validate and forward", "A fidelity summary accompanies each dataset; approved datasets are sent "
             "through the existing uplink and ingestion pipeline."),
            ("Train centrally", "Central teams train on aggregated distilled datasets and adjust the task "
             "definition when requirements change."),
        ],
        "not": [
            "It does not claim real-time or streaming execution; distillation runs on batches at a cadence set by the customer.",
            "It does not imply compatibility with any specific edge device; target hardware must be qualified during the pilot.",
            "It does not replace edge security, device management or network design.",
        ],
    },

    # 3b. Illustrative enterprise scenario — never a customer story; numbers are planning assumptions
    "scenario": {
        "name": "Telecommunications operator",
        "context": "A telecommunications operator runs thousands of network sites that generate telemetry, performance counters, alarms and operational events.",
        "current": "Telemetry is aggregated regionally and shipped to central platforms. Much of it is stored only to feed periodic model training.",
        "problem": "The operator wants centralized anomaly-detection and network-performance models. Moving raw telemetry from every region consumes transport capacity, ingestion pipelines and central storage, and most of the volume is routine.",
        "proposed": "Distillation runs in regional data centers or aggregation points. It produces task-specific training datasets that keep unusual network events and the temporal context around them. Only those datasets travel to the central platform for training.",
        "assumptions": [
            "12 regions × 50 TB of eligible telemetry per training cycle = 600 TB",
            "Assumed dataset reduction: 85%, an illustrative planning value",
            "Optimized data transferred: 90 TB",
            "Potential avoided transfer: 510 TB per training cycle",
        ],
        "constraints": [
            "Unusual network events are rare and must survive distillation",
            "Temporal dependencies (alarm sequences, load patterns) matter to the models",
            "No interference with network operations systems",
        ],
        "economic": [
            "Less transport capacity, central ingestion and storage used for training data",
            "Smaller central processing and training runs, net of regional distillation compute",
        ],
        "strategic": [
            "Network-wide anomaly models trained on data from every region",
            "A pattern that scales as telemetry volumes grow",
        ],
        "validation": [
            "Recall on rare anomalies and incident precursors",
            "Preservation of the temporal patterns the task depends on",
            "Compute footprint at the regional sites",
            "Net reduction after distillation overhead",
        ],
        "stakeholder": "CTO or head of network operations, with the head of data platforms",
    },

    "architecture": {
        "current": {
            "title": "Conventional: raw edge data shipped to the cloud",
            "zones": [
                {"id": "edge", "label": "Edge · devices and sites", "kind": "source",
                 "nodes": [["dev", "Sensors, cameras, devices", "system"], ["gw", "Edge gateway (store-and-forward)", "system"]]},
                {"id": "net", "label": "Uplink network", "kind": "boundary",
                 "nodes": [["link", "Cellular / WAN / satellite link", "system"]]},
                {"id": "cloud", "label": "Cloud / central platform", "kind": "central",
                 "nodes": [["ing", "Ingestion and raw storage", "store"], ["ml", "Central ML training", "model"]]},
            ],
            "flows": [
                ["dev", "gw", "raw", "continuous streams"],
                ["gw", "link", "raw", "as much as link allows"],
                ["link", "ing", "raw", "raw volume"],
                ["ing", "ml", "raw", "filtered centrally"],
            ],
        },
        "proposed": {
            "title": "With GroundTruth AI: distill near the source, send what the task needs",
            "zones": [
                {"id": "edge", "label": "Edge · devices and sites", "kind": "source",
                 "nodes": [["dev", "Sensors, cameras, devices", "system"], ["gt", "GroundTruth runtime on gateway", "gt"]]},
                {"id": "net", "label": "Uplink network", "kind": "boundary",
                 "nodes": [["link", "Existing uplink", "system"]]},
                {"id": "cloud", "label": "Cloud / central platform", "kind": "central",
                 "nodes": [["ds", "Distilled dataset store", "store"], ["ml", "Central ML training", "model"]]},
            ],
            "flows": [
                ["dev", "gt", "raw", "buffered locally"],
                ["gt", "link", "distilled", "distilled batches"],
                ["link", "ds", "distilled", "approved only"],
                ["ds", "ml", "distilled", ""],
                ["ml", "gt", "control", "task spec updates"],
            ],
        },
        "notes": [
            "The runtime is placed on a gateway or site server with enough local compute and storage to "
            "buffer and process batches; constrained end devices are not targeted.",
            "Raw data remains at the edge under the customer's existing local retention policy.",
        ],
    },

    "outcomes": {
        "direct": [
            "Less uplink traffic attributable to AI training data.",
            "Lower cloud ingestion and central storage for training datasets.",
            "Lower central processing to filter raw data before training, net of edge-side distillation cost.",
        ],
        "operational": [
            "Less dependence on high-bandwidth connectivity at remote sites.",
            "Training data selection driven by the model task rather than by link capacity.",
            "A consistent data-preparation pattern across heterogeneous device fleets.",
        ],
        "strategic": [
            "A scalable architecture for distributed AI that does not grow central costs linearly with device count.",
            "Sites with limited connectivity become viable contributors to central models.",
            "Potential reduction in energy spent transmitting data, subject to measurement in the customer environment.",
        ],
    },

    "metrics": [
        ["Uplink volume for training data", "GB per site per month sent for AI training, before vs. after", "direct"],
        ["Cloud ingestion and storage", "Ingested GB and stored TB for the use case", "direct"],
        ["Central preprocessing compute", "Compute hours spent filtering raw edge data", "direct"],
        ["Edge-side overhead", "CPU time, memory and energy of distillation on the gateway", "direct"],
        ["Model predictive performance", "Task metric on a held-out full-data test set", "quality"],
        ["Rare-event coverage", "Share of labeled events represented in distilled batches", "quality"],
        ["Batch latency", "Time from data capture to distilled dataset availability centrally", "operational"],
        ["Participating sites or devices", "Number of edge locations contributing distilled data", "strategic"],
    ],

    "stakeholders": {
        "sponsor": ["CTO or head of connected operations", "Wants fleet-wide AI without connectivity and cloud costs scaling with every device."],
        "economic": ["Infrastructure or network leader", "Owns connectivity, ingestion and cloud storage budgets."],
        "technical": ["Enterprise or edge architect", "Must confirm gateway capacity, placement and data paths."],
        "operational": [
            ["Field or site operations", "Gateway availability and no interference with operational traffic."],
            ["Security team", "Hardening and update process for software on edge gateways."],
            ["Central data science team", "Model quality and event coverage on distilled data."],
        ],
    },

    "implementation": {
        "integration_points": [
            ["Tabular data via pandas / NumPy", "verified", "Prototype input format used in internal experiments."],
            ["scikit-learn-compatible model adapter", "verified", "Used to compare models trained on full and distilled data."],
            ["Image data with CNN models", "verified", "Exercised on the MNIST benchmark; not on camera fleets."],
            ["MQTT / OPC UA / edge message buses", "proposed", "Candidate ingestion connectors; not built or tested."],
            ["Container packaging for edge gateways", "proposed", "Roadmap item; target hardware to be qualified with the customer."],
            ["Cloud ingestion and object storage", "customer", "Receives distilled datasets as ordinary files."],
        ],
        "infrastructure": [
            "A gateway or site server with a Python runtime and local buffer storage (sizing set during the pilot).",
            "Access to locally buffered data for the pilot variables.",
            "The existing uplink and central ingestion pipeline.",
        ],
        "deployment": "For a pilot, the runtime is installed on one or a few customer-provided gateways or site "
                      "servers and processes buffered batches on a fixed schedule. Packaging for fleet-wide "
                      "rollout and remote updates is a proposed roadmap item.",
        "constraints": [
            "Real-time or streaming distillation has not been validated; batch cadence is a design parameter.",
            "Gateway compute, memory and power budgets limit dataset size per batch and must be measured.",
            "Heterogeneous device types may require separate task definitions.",
        ],
    },

    "evidence": {
        "status": "Enterprise application for pilot evaluation — not yet validated in production",
        "summary": "Internal experiments show large data reductions with limited accuracy change on public "
                   "benchmarks, and an internal measurement indicates lower energy use on IoT / edge devices "
                   "at the point of capture. Edge-fleet data, batch cadence and gateway overhead have not yet "
                   "been measured on customer infrastructure.",
        "supports": [
            "86–95% data reduction on four public benchmarks with a maximum accuracy change of −2.8 pp (experimentally supported technical outcome).",
            "39% less energy on IoT / edge devices at the point of capture (internal measurement; methodology not yet published; distillation's own energy not separately reported).",
        ],
        "gaps": [
            "No benchmark yet on sensor time series, telemetry, logs or video from real device fleets.",
            "No qualification of specific gateway or device hardware.",
            "No measurement of end-to-end uplink and ingestion savings on customer infrastructure.",
            "No production deployment.",
        ],
        "risks": [
            "Gateway resources may be insufficient for the required batch size or cadence.",
            "Rare events may be under-represented unless coverage constraints are enforced.",
        ],
    },

    "pilot": {
        "duration": "8–12 weeks (indicative)",
        "problem": "One fleet-level model whose training data is currently uplinked in raw form from a set of sites or gateways.",
        "inputs": [
            "Buffered raw data from a representative subset of sites or gateways",
            "Event or failure labels where available",
            "The current central training pipeline and evaluation metric",
            "One or more gateways or site servers available for installation",
        ],
        "baseline": "The existing model trained centrally on the raw uplinked data.",
        "method": [
            "Train the same model on raw and distilled data; evaluate both on the same held-out full-data test set.",
            "Measure uplink volume, ingestion and central storage for both paths.",
            "Measure gateway CPU, memory, energy and batch processing time.",
        ],
        "technical_criteria": [
            "Model performance within the customer-defined tolerance of baseline.",
            "Labeled events in the test window represented in distilled batches.",
            "Distillation completes within the agreed batch window on target hardware.",
        ],
        "economic_criteria": [
            "Uplink and ingestion volume for training data reduced by a customer-defined target.",
            "Net saving remains positive after edge-side overhead.",
        ],
        "deliverables": [
            "Fidelity report (raw vs. distilled), including event coverage",
            "Measured uplink, ingestion, storage, compute and energy comparison",
            "Gateway sizing and placement recommendation",
            "Fleet rollout plan and risk register",
        ],
        "adoption": [
            "Technical and economic criteria met",
            "Target gateway hardware qualified",
            "Security approval of packaging and update process",
            "Named owner for task definitions and regeneration",
        ],
    },

    "caveats": [
        "No real-time execution or compatibility with specific edge devices is claimed; both must be validated "
        "on the customer's hardware during a pilot.",
    ],
    "related": ["BC04", "BC01", "BC06"],
}
