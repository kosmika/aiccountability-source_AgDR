# Human Delta Chain — Formal Specification

**AgDR v0.2 — Human Accountability Layer**
Published March 2026

---

## What Is the Human Delta Chain?

The **Human Delta Chain** is the ordered, append-only sequence of human interventions recorded atomically alongside every AgDR decision. It is the formal proof that the right humans were involved, at the right points, with the right authority — and that their involvement (or deliberate non-involvement) is on permanent, tamper-evident record.

"Delta" means the difference a human made. A delta of zero is itself meaningful: it means a human reviewed and chose not to change the decision. That choice is as accountable as any modification.

---

## Data Structure

### Single Delta Record

```json
{
  "delta_id": "d_20260315_001_0",
  "sequence": 0,
  "actor": {
    "name": "J. Smith",
    "role": "Senior Trader",
    "employee_id": "EMP-04421",
    "jurisdiction": "Ontario, Canada"
  },
  "action": 1,
  "action_label": "approved_with_modification",
  "modification": {
    "field": "output.order_size",
    "original": 10000,
    "revised": 8000,
    "unit": "shares",
    "rationale": "Reduced to stay within intraday risk limit per mandate 2026-Q1"
  },
  "timestamp_ns": 1742000000000000000,
  "latency_ns": 142000000,
  "escalated": false,
  "signature": "<Ed25519 signature over this delta record>"
}
```

### Action Codes

| Code | Label | Meaning |
|---|---|---|
| `1` | `approved_as_is` | Human reviewed, accepted the agent's decision without change |
| `2` | `approved_with_modification` | Human reviewed, accepted with documented change |
| `0` | `escalated` | Human reviewed, escalated to next layer — decision not yet final |
| `-1` | `halted` | Human reviewed, halted the decision — agent must not proceed |

### Full Chain Structure

```json
{
  "chain_id": "chain_20260315_001",
  "agent_decision_ref": "agdr_20260315_001",
  "initiated_at_ns": 1742000000000000000,
  "resolved": true,
  "resolution": "approved_with_modification",
  "terminal_node": "human_delta",
  "deltas": [
    {
      "delta_id": "d_20260315_001_0",
      "sequence": 0,
      "actor": { "name": "J. Smith", "role": "Senior Trader" },
      "action": 2,
      "action_label": "approved_with_modification",
      "modification": { ... },
      "escalated": false,
      "timestamp_ns": 1742000000000000000
    }
  ],
  "foi_escalation": null,
  "merkle_root": "<root hash of this chain>",
  "chain_signature": "<Ed25519 signature over the complete chain>"
}
```

---

## Fully Autonomous Decision (Empty Chain)

When an agent acts fully within its authorized boundary with no human review, the chain is empty — and that emptiness is itself recorded and signed:

```json
{
  "chain_id": "chain_20260315_002",
  "agent_decision_ref": "agdr_20260315_002",
  "deltas": [],
  "foi_escalation": null,
  "autonomous": true,
  "autonomous_authority_ref": "mandate_2026-Q1_section_3.2",
  "merkle_root": "<root hash>",
  "chain_signature": "<signature>"
}
```

The `autonomous_authority_ref` is critical: it points to the governance document that authorized the agent to act without human review for this class of decision. **Autonomous action without an authority reference is a compliance gap.**

---

## Multi-Layer Escalation

When a decision escalates through multiple human reviewers:

```json
{
  "deltas": [
    {
      "sequence": 0,
      "actor": { "name": "J. Smith", "role": "Junior Analyst" },
      "action": 0,
      "action_label": "escalated",
      "escalation_reason": "Decision magnitude exceeds my delegated authority",
      "timestamp_ns": 1742000000000000000
    },
    {
      "sequence": 1,
      "actor": { "name": "M. Chen", "role": "Head of Desk" },
      "action": 0,
      "action_label": "escalated",
      "escalation_reason": "Requires compliance sign-off",
      "timestamp_ns": 1742000000000000100
    }
  ],
  "foi_escalation": {
    "actor": { "name": "C. Wong", "title": "Chief Compliance Officer" },
    "decision": "HALT — requires board resolution",
    "decision_code": 0,
    "timestamp_ns": 1742000000000000200,
    "signature": "<FOI Ed25519 signature>"
  },
  "terminal_node": "foi"
}
```

The chain grows by append only. No delta can be removed or modified after it is written. Each delta is signed by the actor at the time of their review. Any modification to a past delta breaks every subsequent signature.

---

## Invariants

These are enforced by the AKI kernel layer and must be validated by any AgDR-compliant verifier:

1. **Sequence is monotonically increasing** — no gaps, no reordering
2. **Each delta is signed by the actor** — no unsigned deltas
3. **Escalated deltas must be followed by the next delta or FOI escalation** — an escalated decision cannot be the last record in a resolved chain
4. **Halted decisions have no subsequent deltas** — once halted, the chain is terminal
5. **Autonomous chains must carry an authority reference** — no empty chain without `autonomous_authority_ref`
6. **The FOI node, if present, is always last** — FOI is terminal by definition
7. **The chain's Merkle root commits to all deltas and the FOI node** — verified by the top-level AgDR record

---

## Timing Requirements

| Requirement | Value |
|---|---|
| Maximum latency per delta | Organization-defined (e.g., 30s for trading, 24h for clinical) |
| Timestamp precision | Nanosecond (`timestamp_ns`) |
| Clock source | System monotonic clock at capture instant |
| Latency recorded | `latency_ns` — time from agent decision to human action |

Latency is evidence of genuine review. A delta timestamped 1 millisecond after the agent decision is not credible review — it is a rubber stamp. Organizations should define minimum credible review times per decision class and flag anomalies.

---

## Schema Reference

Full JSON Schema for the human delta chain is included in `specs/agdr-v0.2.json` under `human_delta_chain_schema`.

```bash
# Validate a chain against the schema
agdr validate-chain --chain chain_20260315_001.json
```

---

## Legal Significance

The human delta chain is the instrument that answers the question every court and regulator will ask:

**"Was there meaningful human oversight?"**

Not just "was a human in the loop" — but:
- Which human?
- What was their authority?
- What did they actually do?
- How long did they take?
- Did they escalate when they should have?
- Who ultimately bore fiduciary responsibility?

The chain answers all of these, atomically, at the time of the decision. Not reconstructed. Not explained after the fact. Present and signed at the inference instant.

This is the architecture that makes AgDR more than logging. It is the proof of governance.

*Part of the AgDR v0.2 foundational standard*
Canonical source: https://github.com/aiccountability-source/AgDR
