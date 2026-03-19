# EU AI Act Mapping

**AgDR v0.2 — European Union AI Act Compliance Analysis**
Published March 2026

---

## Overview

The EU AI Act (Regulation 2024/1689, in force August 2024) is the world's first comprehensive legal framework for artificial intelligence. It imposes tiered obligations based on risk level, with the highest requirements for "high-risk" AI systems. AgDR v0.2 addresses the evidentiary and accountability requirements of the EU AI Act directly through its atomic capture architecture.

This document maps AgDR components to EU AI Act obligations. It is not legal advice. Organizations deploying AI systems subject to the Act should obtain qualified EU legal counsel.

---

## Risk Tier Mapping

| EU AI Act Tier | Examples | AgDR Applicability |
|---|---|---|
| **Unacceptable risk** (prohibited) | Social scoring, real-time biometric surveillance | AgDR is an evidentiary standard, not a use-case authorizer — prohibited systems remain prohibited |
| **High risk** (Title III) | Credit scoring, employment, education, critical infrastructure, law enforcement, migration, administration of justice | **Full AgDR compliance directly addresses mandatory obligations** |
| **Limited risk** | Chatbots, emotion recognition (transparency obligation only) | AgDR provides stronger-than-required audit trail |
| **Minimal risk** | Spam filters, AI in video games | AgDR applicable but not required |

---

## High-Risk System Obligations — Article-by-Article Mapping

### Article 9 — Risk Management System

**Requirement:** Providers must establish, implement, document, and maintain a risk management system throughout the lifecycle.

| AgDR Component | How It Satisfies Article 9 |
|---|---|
| AKI atomic capture | Every inference is captured — risk events are never unrecorded |
| PPP triplet — Place | Defines the intended operational boundary at every decision point |
| Human delta chain | Demonstrates ongoing human oversight as part of the risk management process |
| Merkle chain | Provides tamper-evident lifecycle record from deployment through decommission |

**Gap AgDR does not fill:** Prospective risk assessment documentation (Article 9 §2) must be produced separately. AgDR captures what happened; organizations must separately document what risks they assessed before deployment.

---

### Article 10 — Training, Validation and Testing Data

**Requirement:** Data governance and management practices; datasets must be free of errors and biases to the extent possible.

| AgDR Component | How It Contributes |
|---|---|
| Provenance pillar | Captures data provenance at every inference — who supplied the context and under what conditions |
| Reasoning trace | Records what data was actually used at each inference instant |

**Note:** AgDR captures inference-time data provenance. Pre-deployment training data governance is a separate obligation outside AgDR's scope.

---

### Article 11 — Technical Documentation

**Requirement:** Providers must draw up technical documentation before placing a high-risk AI system on the market and keep it up to date.

| AgDR Component | How It Contributes |
|---|---|
| `agdr-v0.2.json` (this spec) | Machine-readable technical specification, dual-licensed CC0/Apache |
| AKI formal definition | Satisfies documentation of capture mechanism |
| PPP triplet schema | Satisfies documentation of data structure and policy triplet |
| Human delta chain spec | Satisfies documentation of human oversight architecture |

AgDR records, taken together, constitute real-time technical documentation of system behaviour — not just design intent.

---

### Article 12 — Record-Keeping

**Requirement:** High-risk AI systems must have the capability to automatically generate logs throughout their operation; logs must enable monitoring for serious incidents and substantial modifications.

| EU AI Act Article 12 Requirement | AgDR Fulfilment |
|---|---|
| Automatic logging | AKI captures every inference — no manual logging, no gaps |
| Log integrity | BLAKE3 + Merkle chain — any tampering is detectable |
| Log durability | Forward-secret Merkle chain is designed to be permanently verifiable |
| Serious incident traceability | Every decision record links to the full reasoning trace and human delta chain |
| Substantial modification detection | Merkle chain continuity — a system modification breaks the expected chain pattern |

**AgDR exceeds Article 12 requirements** by providing cryptographic proof of log integrity, not just log existence.

---

### Article 13 — Transparency and Provision of Information to Deployers

**Requirement:** High-risk AI systems must be transparent and provide deployers with information enabling them to use the system in an informed manner, including instructions for use.

| AgDR Component | How It Satisfies Article 13 |
|---|---|
| PPP triplet — Purpose | Explicit statement of intent captured at every inference |
| Reasoning trace | Full chain-of-thought recorded — system behaviour is never a black box |
| Getting Started guide | Clear implementation documentation |
| Industry templates | Sector-specific guidance for informed deployment |

---

### Article 14 — Human Oversight

**Requirement:** High-risk AI systems must be designed and developed in such a way that they can be effectively overseen by natural persons during the period they are in use.

This is the article where AgDR's contribution is most direct.

| EU AI Act Article 14 Requirement | AgDR Fulfilment |
|---|---|
| Ability to understand capabilities and limitations | PPP triplet + reasoning trace make every decision interpretable |
| Ability to disregard, override, or reverse output | Human delta chain records every override with actor, rationale, and timestamp |
| Ability to intervene through halt or pause | `action: -1` (halted) in delta chain; FOI terminal halt |
| Natural person oversight | FOI formal definition — named human fiduciary is always the terminal node |
| Oversight measures described before deployment | FOI designation process + escalation trigger conditions |

**AgDR directly implements Article 14 human oversight architecture** through the human delta chain and FOI.

---

### Article 16 — Obligations of Providers of High-Risk AI Systems

**Requirement:** Providers must implement quality management systems, register systems in the EU database, affix CE marking, draw up EU declaration of conformity.

AgDR addresses the audit-trail and quality management components. CE marking and EU database registration are separate administrative obligations outside AgDR's scope.

---

### Article 26 — Obligations of Deployers of High-Risk AI Systems

**Requirement:** Deployers must use high-risk AI systems in accordance with instructions, assign human oversight to competent persons, monitor operation, and report serious incidents.

| Article 26 Requirement | AgDR Fulfilment |
|---|---|
| Assign human oversight to competent persons | FOI designation process with named individuals and defined scope |
| Monitor operation for risks | AKI captures every inference — monitoring is the record |
| Report serious incidents | AgDR record provides the evidentiary basis for incident reporting to market surveillance authorities |

---

### Article 72 — Post-Market Monitoring

**Requirement:** Providers must establish and document a post-market monitoring system.

AgDR's Merkle chain constitutes a continuous, tamper-evident post-market monitoring record. Every inference, from first deployment to decommission, is part of the same forward-secret chain. Post-market monitoring is not a separate exercise — it is the natural output of AgDR operation.

---

## GDPR Interaction

The EU AI Act operates alongside GDPR. Where AI systems process personal data, both apply.

| AgDR Component | GDPR Relevance |
|---|---|
| PPP — Place | Captures purpose limitation at inference time (GDPR Article 5(1)(b)) |
| PPP — Provenance | Records data subject context and consent basis |
| Reasoning trace | Supports right of explanation (GDPR Article 22 + Recital 71) |
| Human delta chain | Demonstrates human involvement in significant automated decisions |

**Note:** AgDR records themselves may contain personal data. Organizations must apply appropriate data protection measures to AgDR records under GDPR, including retention periods and access controls. The evidentiary value of AgDR records must be balanced against data minimization principles.

---

## Summary Assessment

| EU AI Act Domain | AgDR Coverage |
|---|---|
| Automatic logging (Article 12) | Full — exceeds requirements |
| Human oversight (Article 14) | Full — direct architectural implementation |
| Transparency (Article 13) | Full — PPP + reasoning trace |
| Risk management (Article 9) | Partial — captures what happened; prospective assessment is separate |
| Technical documentation (Article 11) | Substantial — spec + schemas |
| Post-market monitoring (Article 72) | Full — Merkle chain is continuous monitoring record |
| Data governance (Article 10) | Partial — inference-time provenance; training data is separate |
| CE marking / EU database registration | Outside AgDR scope — administrative obligations |

---

*Part of the AgDR v0.2 foundational standard*
Canonical source: https://github.com/aiccountability-source/AgDR
