# CBSA Compliance Mapping

**How AgDR v0.2 Supports Canada Border Services Agency (CBSA) Requirements**

AgDR v0.2 provides tamper-evident, atomic records that directly address CBSA’s core needs in export controls, sanctions screening, and border security.

| CBSA Requirement                     | How AgDR Satisfies It                                                                 | AgDR Component Used |
|--------------------------------------|---------------------------------------------------------------------------------------|---------------------|
| Export Control & Sanctions Screening | Every decision is recorded with full reasoning trace and PPP triplet at inference instant | Provenance + Purpose |
| "Know Your Client" & Due Diligence   | Binary human delta chain + FOI escalation proves meaningful human oversight           | Human Delta + FOI   |
| Audit & Reporting Obligations        | Cryptographic signature + forward-secret Merkle chain creates permanent, verifiable audit trail | Atomic Kernel + Merkle |
| Real-Time Decision Accountability    | Record is created in the same atomic transaction as the decision (no post-hoc logs)   | AKI Capture         |

**Key Benefit for CBSA-Regulated Entities**  
When CBSA requests documentation for an export or sanctions screening decision, companies can instantly provide a mathematically irrefutable AgDR record instead of reconstructed logs or manual reports. This reduces audit time from weeks to minutes and strengthens compliance defence.

**Practical Use Case**  
In an export control screening scenario, the AgDR record captures:
- Provenance: Who the stakeholders were and the exact context at decision time
- Place: The intended destination and regulatory boundary
- Purpose: The explicit compliance intent behind the decision

Any later CBSA inquiry can be answered with one verifiable file: “Check the AgDR.”

*Part of the AgDR v0.2 foundational standard*  
Canonical source: https://github.com/aiccountability-source/agdr-spec
