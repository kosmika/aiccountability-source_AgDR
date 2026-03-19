# Public Resources — Accountability.ai / AgDR

This document catalogs publicly available resources related to accountability.ai, AgDR, and the broader
AI accountability and governance landscape that contextualizes this work.

---

## Primary Sources (accountability.ai / @aiccountability)

### Official Website
- **https://accountability.ai** — The AgDR standard homepage
  - Hero: "We make autonomous intelligence accountable — forever."
  - Live sandbox: https://accountability.ai/sandbox.html

### GitHub Repositories
- **https://github.com/aiccountability-source/AgDR** — Canonical AgDR specification repository
  - `specs/agdr-v0.2.json` — Machine-readable spec (CC0 / Apache 2.0)
  - All documentation pages (MD + HTML)

### Published Standard Pages
All pages below are publicly accessible at https://accountability.ai/

| Topic | URL |
|---|---|
| AKI Formal Definition | https://accountability.ai/aki-formal-definition.html |
| PPP Pillars | https://accountability.ai/ppp-pillars.html |
| Legal Compliance (Canada Evidence Act, CBCA s.122) | https://accountability.ai/ppp-legal-compliance.html |
| Export Control Analysis | https://accountability.ai/ppp-export-control.html |
| CBCA Fiduciary Mapping | https://accountability.ai/cbca-fiduciary-mapping.html |
| CBSA Regulatory Mapping | https://accountability.ai/cbsa-mapping.html |
| Aviation Black Box Comparison | https://accountability.ai/comparison-aviation-black-box.html |
| Medical Records Comparison | https://accountability.ai/comparison-medical-records.html |
| AGI Court Precedents | https://accountability.ai/agi-court-precedents.html |
| Future AGI Court Vision (2076) | https://accountability.ai/future-agi-court.html |
| Technical Details | https://accountability.ai/technical-details.html |
| Technical Note on Coherence | https://accountability.ai/technical-note-coherence.html |
| TSX 100M Stress Test | https://accountability.ai/tsx-stress-test.html |
| Getting Started | https://accountability.ai/getting-started.html |

### Contact
- **Email:** admin@accountability.ai
- **Founding inquiries:** founding@accountability.ai

---

## Related Regulatory & Legal Frameworks Referenced by AgDR

### Canada
| Framework | Description | Relevance |
|---|---|---|
| **Canada Evidence Act** | Federal rules of evidence | AgDR records designed to meet evidentiary standards |
| **CBCA s.122** | Canada Business Corporations Act — director fiduciary duty | AgDR maps the "Fiduciary Office Intervener (FOI)" concept here |
| **CBSA** | Canada Border Services Agency | AgDR regulatory mapping for border/import context |
| **Canadian Human Rights Stewardship** | Foundational value of AgDR | Mentioned in README as guiding principle |

### Industry Analogues Referenced
| Standard | Description | AgDR Parallel |
|---|---|---|
| **Aviation Black Box (CVR/FDR)** | Mandatory tamper-evident flight data recorder | AgDR is the "AI flight recorder" — same tamper-evidence principle |
| **Electronic Medical Records (EMR)** | Immutable patient record standards | AgDR applies same immutability + chain of custody to AI decisions |

---

## Broader AI Accountability & Governance Context

### International AI Governance Frameworks
| Framework | Jurisdiction | URL |
|---|---|---|
| EU AI Act | European Union | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689 |
| NIST AI Risk Management Framework (AI RMF) | United States | https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf |
| OECD AI Principles | International | https://oecd.ai/en/ai-principles |
| UNESCO Recommendation on the Ethics of AI | International | https://unesdoc.unesco.org/ark:/48223/pf0000381137 |
| Canada's Directive on Automated Decision-Making | Canada | https://www.tbs-sct.canada.ca/pol/doc-eng.aspx?id=32592 |
| Canada's AIDA (Artificial Intelligence and Data Act) | Canada | https://ised-isde.canada.ca/site/innovation-better-canada/en/artificial-intelligence-and-data-act |

### Cryptographic Standards Used by AgDR
| Standard | Use in AgDR | Reference |
|---|---|---|
| **BLAKE3** | Hashing for tamper-evident records | https://github.com/BLAKE3-team/BLAKE3 |
| **Merkle Trees** | Append-only chain proof | https://en.wikipedia.org/wiki/Merkle_tree |

### AI Auditability & Explainability Research
| Resource | Description | URL |
|---|---|---|
| "Accountability of AI Under the Law" — Doshi-Velez et al. | Foundational academic paper on AI accountability | https://arxiv.org/abs/1711.01134 |
| "The Right to Explanation" — Goodman & Flaxman | GDPR explainability right paper | https://arxiv.org/abs/1606.08813 |
| Partnership on AI — Tenets | Industry coalition principles | https://partnershiponai.org/about/ |
| AI Now Institute | Research on AI accountability | https://ainowinstitute.org/ |
| Algorithmic Justice League | Accountability advocacy | https://www.ajl.org/ |

---

## Key Concepts for Reference

### AgDR Terminology Quick Reference
| Term | Definition |
|---|---|
| **AgDR** | Agent Decision Record — tamper-evident flight recorder for autonomous agents |
| **AKI** | Atomic Kernel Inference — capture at the exact "i" inference point |
| **PPP** | Provenance · Place · Purpose — the policy triplet (meaning of the beholder) |
| **FOI** | Fiduciary Office Intervener — terminal escalation role in human delta chain |
| **Human Delta Policy** | Binary policy: human approved/overrode at each decision layer |
| **Merkle-append** | Cryptographic append-only chain — no record can be altered post-capture |

### Why This Matters
The AgDR standard addresses a gap: when an AI agent makes a consequential decision, there is currently no universal, tamper-evident, legally admissible record of:
- What exactly was decided (the output)
- Why it was decided (the reasoning trace)
- Who was accountable (the PPP triplet + human delta chain)
- Whether it was tampered with after the fact (BLAKE3 + Merkle proof)

AgDR provides this — compatible with any current or future inference model.

---

*This document is maintained as part of the AAI project hub.*
*Primary source: https://github.com/aiccountability-source/AgDR*
