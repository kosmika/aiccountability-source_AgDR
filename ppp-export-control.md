# PPP Export Control Mapping

**How AgDR v0.2 Supports CBSA Export Control & Sanctions Screening**

AgDR v0.2 provides atomic, tamper-evident records that directly satisfy Canada Border Services Agency (CBSA) requirements for export compliance, sanctions screening, and controlled goods.

| CBSA Requirement                     | How AgDR Satisfies It                                                                 | AgDR Component Used |
|--------------------------------------|---------------------------------------------------------------------------------------|---------------------|
| Export Control Decision Traceability | Full reasoning trace captured at inference instant                                    | Reasoning Trace     |
| Sanctions & Jurisdiction Screening   | Provenance records exact stakeholder context and jurisdiction at decision time        | Provenance pillar   |
| Intended Outcome Verification        | Place defines the intended destination and regulatory boundary                        | Place pillar        |
| Intent & Human Oversight             | Purpose captures explicit compliance intent + binary human delta chain                | Purpose + Human Delta |
| Audit-Ready Reporting                | Cryptographic signature + Merkle chain provides permanent, verifiable evidence        | Atomic Kernel + Merkle |

**Key Benefit**  
When CBSA requests documentation for an export licence or sanctions screening decision, companies can instantly provide a mathematically irrefutable AgDR record instead of reconstructed logs. This reduces audit time from weeks to minutes and strengthens compliance defence.

**Practical Use Case**  
In an export control screening scenario, the AgDR record captures:
- Provenance: Who the stakeholders were and the exact context
- Place: The intended destination and CBSA regulatory boundary
- Purpose: The explicit compliance intent behind the decision

Any later CBSA inquiry can be answered with one verifiable file: “Check the AgDR.”

*Part of the AgDR v0.2 foundational standard*  
Canonical source: https://github.com/aiccountability-source/AgDR
