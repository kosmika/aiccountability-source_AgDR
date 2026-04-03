---
title: "Getting Started with AgDR v0.2"
description: "Step-by-step guide to implementing AgDR — install the SDK, capture your first atomic decision record, and verify the chain in minutes."
slug: "docs/getting-started"
---

# Getting Started with AgDR v0.2

**Welcome to the Atomic Kernel Inference Standard**

AgDR gives every autonomous agent decision a tamper-evident, cryptographically signed record that is admissible in court today — and in 2076. This guide takes you from zero to a running AgDR capture in minutes.

---

## 1. Download the Spec

```bash
curl -O https://raw.githubusercontent.com/aiccountability-source/AgDR/main/specs/agdr-v0.2.json
```

Read it. Understand the core guarantee before writing any code:

```json
"core_guarantee": {
  "formal_definition": "AtomicInferenceCapture(...) ≡ { sign(BLAKE3(...)), persist(Merkle-append), return committed }"
}
```

---

## 2. Install the Python SDK

```bash
pip install agdr-aki
```

Or from source:

```bash
git clone https://github.com/aiccountability-source/AgDR.git
cd AgDR/sdk/python
pip install -e .
```

---

## 3. Wrap Your First Inference

Add one call around your existing model invocation. That is the entire integration surface.

```python
from agdr_aki import aki_capture

# Your existing inference call
output = my_model.infer(prompt)

# Wrap it — this is all AgDR requires
record = aki_capture(
    ctx={
        "system": "trading-desk-v3",
        "session_id": "sess_20260315_001",
        "operator": "acme-corp"
    },
    reasoning_trace=output.reasoning_trace,   # full chain-of-thought
    output=output.decision,
    ppp_triplet={
        "provenance": "TSX equity desk — RY.TO buy order — authorized trader J.Smith",
        "place":      "Fill at market open, within 0.5% slippage, regulatory boundary: IIROC",
        "purpose":    "Rebalance portfolio to target allocation as per mandate 2026-Q1"
    },
    human_delta_chain=[]                       # empty = fully autonomous, no human override
)

print(record.merkle_hash)    # cryptographic proof
print(record.timestamp_ns)   # nanosecond-precision inference instant
print(record.committed)      # True = fully captured, False never happens (rollback)
```

---

## 4. Define Your PPP Triplet

PPP is **meaning of the beholder**. You define what each P means for your context.
The standard only requires that your definition is captured verbatim and atomically.

**The three questions to answer before you write a single line:**

| P | Question to answer |
|---|---|
| **Provenance** | Who is acting, on whose behalf, starting from what verified state? |
| **Place** | Where is this decision supposed to take the system — and what are the boundaries? |
| **Purpose** | Why is this decision being made — what duty, mandate, or ethical commitment does it fulfil? |

**Do not over-engineer this.** One sentence per P is sufficient. The atomic capture is what matters — not the length of the prose.

See [PPP Industry Templates](ppp-industry-templates.md) for ready-made definitions by sector.

---

## 5. Handle Human Overrides

When a human reviews and modifies an agent decision, record it in the delta chain:

```python
from agdr_aki import aki_capture, HumanDelta

delta = HumanDelta(
    actor="J.Smith",
    role="Senior Trader",
    action=1,           # 1 = approved with modification, 0 = approved as-is
    modification="Reduced order size from 10,000 to 8,000 shares — risk limit",
    timestamp_ns=1742000000000000000
)

record = aki_capture(
    ctx=ctx,
    reasoning_trace=output.reasoning_trace,
    output=output.decision,
    ppp_triplet=ppp,
    human_delta_chain=[delta]
)
```

If escalation reaches the **Fiduciary Office Intervener (FOI)**, mark it explicitly:

```python
from agdr_aki import FOIEscalation

foi = FOIEscalation(
    actor="C.Wong",
    title="Chief Compliance Officer",
    decision="HALT — escalated to board review",
    timestamp_ns=1742000000000000100
)

record = aki_capture(..., foi_escalation=foi)
```

See [FOI Formal Definition](foi-formal-definition.md) for full duties and designation process.

---

## 6. Verify a Record

Any party — including a court or regulator — can verify a record with no access to your system:

```bash
agdr verify --record record_20260315_001.agdr --merkle-root <root_hash>
```

Or in Python:

```python
from agdr_aki import verify_record

result = verify_record("record_20260315_001.agdr", expected_merkle_root=root_hash)
assert result.valid
assert result.tamper_free
assert result.chain_intact
```

See [Verification & Audit Procedure](verification-audit-procedure.md) for court-ready evidence packaging.

---

## 7. Understand What You Have Built

Every captured record provides:

| Property | Guarantee |
|---|---|
| **Tamper-evident** | Any modification breaks the BLAKE3 hash and Merkle chain |
| **Non-repudiable** | Ed25519 signed at the exact inference instant |
| **Contemporaneous** | Captured at the "i" point — not reconstructed after the fact |
| **Legally admissible** | Meets Canada Evidence Act business records reliability test |
| **FOI-terminal** | Human accountability chain always ends at a designated fiduciary |
| **Court-ready today** | No new legislation required — maps to existing CBCA s.122, common law duty of care |

---

## 8. Next Steps

| Topic | Document |
|---|---|
| PPP by industry (banking, healthcare, government) | [ppp-industry-templates.md](ppp-industry-templates.md) |
| FOI — what it is, how to designate one | [foi-formal-definition.md](foi-formal-definition.md) |
| Human delta chain data structure | [human-delta-chain-spec.md](human-delta-chain-spec.md) |
| Legal compliance mapping (Canada) | [ppp-legal-compliance.md](ppp-legal-compliance.md) |
| EU AI Act mapping | [eu-ai-act-mapping.md](eu-ai-act-mapping.md) |
| Verification and court evidence packaging | [verification-audit-procedure.md](verification-audit-procedure.md) |
| Horizontal scaling beyond 2.85B decisions | [horizontal-scaling.md](horizontal-scaling.md) |
| AKI formal mathematical definition | [aki-formal-definition.md](aki-formal-definition.md) |
| TSX 100M stress test results | [tsx-stress-test.md](tsx-stress-test.md) |

---

## 9. Licence

AgDR is open, royalty-free, and dual-licensed:
**CC0 1.0 Universal** OR **Apache License 2.0** — your choice.

Use it. Build on it. The ecosystem is the point.

---

*"Don't believe a word I say. Check the AgDR."*
— @aiccountability, Founder
