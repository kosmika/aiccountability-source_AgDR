# AAI — Accountability.ai Project Manager Central

**Last updated:** March 2026
**Canonical GitHub:** https://github.com/aiccountability-source/AgDR
**Live site:** https://accountability.ai
**Founder:** @aiccountability

---

## Quick Navigation

| Section | Description | Link |
|---|---|---|
| AgDR Spec v0.2 | Core standard JSON | [github-artifacts/agdr-v0.2.json](github-artifacts/agdr-v0.2.json) |
| GitHub Artifacts Index | All spec docs & files | [github-artifacts/INDEX.md](github-artifacts/INDEX.md) |
| Public Resources | External coverage & references | [public-resources/accountability-ai-resources.md](public-resources/accountability-ai-resources.md) |
| Drive Setup Guide | How this Drive is organized | [DRIVE-SETUP.md](DRIVE-SETUP.md) |
| Project Docs | Working docs, notes, roadmap | [project-docs/](project-docs/) |

---

## Mission

> **We make autonomous intelligence accountable — forever.**

Accountability.ai publishes **AgDR** (Agent Decision Record) — the open, royalty-free Canadian standard for tamper-evident, cryptographically signed AI decision records.

**Core Concept:**
- **AgDR** — Agent Decision Record: the flight recorder for autonomous agents
- **AKI** — Atomic Kernel Inference: mathematically indivisible capture at the exact inference point
- **Policy = PPP** — Provenance · Place · Purpose (meaning of the beholder)

---

## AgDR v0.2 at a Glance

| Property | Value |
|---|---|
| Version | 0.2 |
| Status | Published — Open Canadian Standard |
| License | CC0 1.0 Universal OR Apache 2.0 (your choice) |
| Effective | March 2026 |
| Capture | Atomic at inference instant — no post-facto editing |
| Chain | BLAKE3 → Merkle-append → signed commit |
| Scale proven | 100,000,000 decisions on TSX Toronto desk |
| Throughput | 253,807 decisions/second, 100% success rate |

**Core Guarantee (formal):**
```
AtomicInferenceCapture(...) ≡ {
  sign(BLAKE3(ctx ‖ reasoning_trace ‖ ppp_triplet ‖ human_delta_chain)),
  persist(Merkle-append),
  return committed
}
```

**Universal Wrapper Signature:**
```
agdr_capture(ctx, prompt, model_id, reasoning_trace, output, ppp_triplet, human_delta_chain)
```

---

## Spec Pages (Published at accountability.ai)

| Page | Description |
|---|---|
| [index.html](https://accountability.ai/) | Home — hero, scale proof, founding |
| [aki-formal-definition](https://accountability.ai/aki-formal-definition.html) | AKI formal mathematical definition |
| [ppp-pillars](https://accountability.ai/ppp-pillars.html) | PPP — Provenance · Place · Purpose |
| [ppp-legal-compliance](https://accountability.ai/ppp-legal-compliance.html) | Legal compliance mapping |
| [ppp-export-control](https://accountability.ai/ppp-export-control.html) | Export control analysis |
| [cbca-fiduciary-mapping](https://accountability.ai/cbca-fiduciary-mapping.html) | CBCA s.122 fiduciary mapping |
| [cbsa-mapping](https://accountability.ai/cbsa-mapping.html) | CBSA regulatory mapping |
| [comparison-aviation-black-box](https://accountability.ai/comparison-aviation-black-box.html) | Aviation black box comparison |
| [comparison-medical-records](https://accountability.ai/comparison-medical-records.html) | Medical records comparison |
| [agi-court-precedents](https://accountability.ai/agi-court-precedents.html) | AGI court precedents |
| [future-agi-court](https://accountability.ai/future-agi-court.html) | Future AGI court (2076 vision) |
| [technical-details](https://accountability.ai/technical-details.html) | Technical implementation details |
| [technical-note-coherence](https://accountability.ai/technical-note-coherence.html) | Technical note on coherence |
| [tsx-stress-test](https://accountability.ai/tsx-stress-test.html) | TSX 100M decision stress test |
| [getting-started](https://accountability.ai/getting-started.html) | Getting started guide |

---

## Key Contacts

| Role | Contact |
|---|---|
| Founder | admin@accountability.ai |
| Founding Technical Co-Founder | founding@accountability.ai (subject: Technical Co-Founder) |
| Regulatory Credibility Anchor | founding@accountability.ai (subject: Regulatory Credibility Anchor) |
| Founding Pilot Partner | founding@accountability.ai (subject: Founding Pilot Partner) |

---

## Drive Folder Structure

```
AAI/  ← You are here
├── HUB.md                          ← This file (project manager central)
├── DRIVE-SETUP.md                  ← Drive organization guide
├── github-artifacts/               ← Copies of all GitHub spec files
│   ├── INDEX.md
│   ├── agdr-v0.2.json
│   ├── specs/
│   └── [all .md and .html pages]
├── public-resources/               ← External references & coverage
│   └── accountability-ai-resources.md
└── project-docs/                   ← Working documents, roadmap, notes
    ├── ROADMAP.md
    └── NOTES.md
```

---

*"Don't believe a word I say. Check the AgDR."*
— @aiccountability, Founder
