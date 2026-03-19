# Fiduciary Office Intervener (FOI) — Formal Definition

**AgDR v0.2 — Terminal Accountability Role**
Published March 2026

---

## What Is the FOI?

The **Fiduciary Office Intervener (FOI)** is the designated human being who holds terminal accountability in the AgDR human delta chain. Every autonomous agent decision that escalates beyond its authorized boundary must ultimately arrive at an FOI. The FOI cannot be another agent, a committee without a named chair, or an organizational abstraction. It is a specific, named, accountable human being.

The FOI does not need to review every decision. The FOI must be reachable — and when reached, their decision is final, recorded atomically, and carries their legal identity.

This is not a new concept. It is the application of existing fiduciary law — specifically CBCA s.122 — to the reality of autonomous agents.

---

## Formal Definition

```
FOI := {
  actor:        <legal name of the designated individual>,
  title:        <organizational role conferring fiduciary authority>,
  jurisdiction: <applicable legal jurisdiction>,
  scope:        <class of agent decisions this FOI is responsible for>,
  appointed_by: <board resolution / governance instrument reference>,
  appointed_at: <timestamp of designation>,
  record_ref:   <AgDR Merkle root of the appointment record>
}
```

An FOI escalation record in the human delta chain:

```json
{
  "type": "foi_escalation",
  "actor": "C. Wong",
  "title": "Chief Compliance Officer",
  "jurisdiction": "Ontario, Canada",
  "decision": "HALT — escalated to board review",
  "decision_code": 0,
  "rationale": "Decision exceeds authorized risk threshold under mandate 2026-Q1",
  "timestamp_ns": 1742000000000000100,
  "signature": "<Ed25519 signature over this record>"
}
```

**`decision_code`:**
- `1` — Approved (FOI endorses the agent's decision)
- `0` — Halted / modified (FOI overrides or escalates further)

---

## Why the FOI Exists

Autonomous agents can make millions of decisions per second. The binary human delta chain captures every human touch point. But a chain with no terminal node is legally meaningless — it is diffused accountability, which courts and regulators have consistently held to be no accountability at all.

The FOI solves this. It is the node at which accountability becomes singular, named, and enforceable under existing law.

Under CBCA s.122, a director or officer must act honestly, in good faith, and in the best interests of the corporation. The FOI role is the mechanism by which this duty extends to decisions made by agents acting on behalf of that corporation.

**If an agent acts and no human can be named as the terminal accountable party, there is no accountability. The FOI closes that gap.**

---

## Designation Requirements

### Who Can Be an FOI

An FOI must be:

1. **A natural person** — not a committee, not an AI, not a legal entity
2. **Legally authorized** — holding a role that carries fiduciary duty under applicable law (director, officer, or equivalent)
3. **Named explicitly** — full legal name on record
4. **Reachable** — with a defined escalation path and response SLA
5. **Informed** — must have actual knowledge of the scope of agent decisions they are accountable for

### How to Designate an FOI

1. Pass a **board resolution** naming the FOI and defining their scope
2. Record the resolution as an AgDR record (eat your own cooking — the appointment itself is atomic and tamper-evident)
3. Register the FOI's public key in the organization's AgDR keyring
4. Define the **escalation trigger conditions** — what causes a decision to reach the FOI
5. Define the **response SLA** — how quickly the FOI must act once escalated
6. Review and re-affirm annually or upon role change

### Escalation Trigger Conditions (examples)

Organizations define their own triggers. Common examples:

| Domain | Trigger |
|---|---|
| Trading | Order exceeds authorized risk limit |
| Healthcare | Diagnosis confidence below threshold or high-severity recommendation |
| Government | Decision affects a protected class or exceeds delegated authority |
| Legal | Agent-generated document has binding legal effect |
| Any | Human delta chain reaches N layers without resolution |

---

## FOI in the AgDR Record

The FOI is the only node in the human delta chain that carries a **fiduciary signature** — a cryptographic signature using a key that is formally registered to a named individual with a designated fiduciary role.

This signature is what elevates an AgDR record from a technical log to a **legally actionable evidentiary document**.

```
Chain:  Agent Decision
           ↓
        Human Delta (Reviewer — action = 1, approved with modification)
           ↓
        Human Delta (Senior Reviewer — action = 0, escalated)
           ↓
        FOI Terminal Node (C. Wong, CCO — decision = HALT)
              └── Ed25519 signature with registered fiduciary key
```

---

## Multiple FOIs

Large organizations with multiple agent workstreams may designate multiple FOIs, each with a defined scope:

```json
{
  "foi_registry": [
    {
      "actor": "C. Wong",
      "title": "Chief Compliance Officer",
      "scope": "trading_desk, risk_management"
    },
    {
      "actor": "A. Patel",
      "title": "Chief Medical Officer",
      "scope": "clinical_decision_support"
    },
    {
      "actor": "S. Tremblay",
      "title": "General Counsel",
      "scope": "legal_document_generation, regulatory_filings"
    }
  ]
}
```

Scopes must be non-overlapping for any given class of decision.

---

## What Happens When the FOI Is Unreachable

An unreachable FOI is a governance failure, not a technical one. Organizations must:

1. Define a **backup FOI** for each scope
2. Define **automatic halt conditions** — decisions requiring FOI review are suspended, not bypassed, if the FOI is unreachable within the SLA
3. Log the unreachability as an AgDR event — this itself becomes an auditable record

**There is no exception path that bypasses the FOI.** An agent that continues acting after an FOI-required escalation without FOI response is operating outside its authorized boundary, and the organization bears full fiduciary liability for that.

---

## Liability

The designation of an FOI does not create new liability — it makes existing liability legible. Under CBCA s.122 and common law duty of care, the fiduciary was always accountable. AgDR simply makes that accountability provable, contemporaneous, and court-ready.

An FOI who acts within their designated scope and in good faith — and whose AgDR record proves it — has the strongest possible legal defence. The record is their shield, not just their obligation.

---

## The FOI and the Standard of Care

The Fiduciary Office Intervener is the human expression of the standard of care that AgDR exists to enforce. Every AgDR record points, ultimately, to a human being who was accountable. The FOI is that human being.

This is the architecture of accountability: not rules without humans, not humans without records — but both, locked together, at the exact instant of decision.

*Part of the AgDR v0.2 foundational standard*
Canonical source: https://github.com/aiccountability-source/AgDR
