# Methodology

## Atomic Kernel Inference (AKI) — AgDR v0.2 Methodology

**Document Status:** Published Open Canadian Standard  
**Effective Date:** March 2026  
**Version:** 0.2  
**Spec Identifier:** AgDR_Atomic_Kernel_AKI_v0.2

---

## 1. Purpose

This document describes the methodology underlying the Atomic Kernel Inference (AKI) enforcement layer of the Agent Decision Record (AgDR) v0.2 standard. It accompanies the machine-readable specification (`spec/v0.2/agdr-v0.2.json`) and provides the rationale, design principles, and formal guarantees that make the standard mathematically and legally above reproach.

This methodology document is a key artifact for ISBN registration and archival deposit with Library and Archives Canada.

---

## 2. Design Principles

### 2.1 Atomicity at the Inference Instant

Every agent decision is captured at the exact moment of inference — the "i" point. The AKI kernel guarantees that the full decision record (context, reasoning trace, PPP triplet, human delta chain, output) is assembled, hashed, signed, and persisted as a single indivisible operation. No partial records ever exist.

### 2.2 Policy = PPP (Provenance, Place, Purpose)

The policy framework is reduced to three mandatory fields — the PPP triplet:

- **Provenance:** Where we are today. Who is acting, on whose behalf, from what verified state.
- - **Place:** Where we are going. The intended destination, target state, and regulatory boundary.
  - - **Purpose:** Why we are going. The explicit intent, desired behaviour, and ethical anchor. Closed by Beauty, Truth & Wisdom.
   
    - The precise meaning of each P is "of the beholder" — the standard captures the structural requirement while semantic interpretation belongs to the implementing organization.
   
    - ### 2.3 Binary Human Delta Policy
   
    - Human intervention follows a binary decision model. Each delta represents a single human decision: halt (-1), escalate (0), approve as-is (1), or approve with modification (2). The chain supports unlimited escalation layers, terminating at either a human delta node or the Fiduciary Office Intervener (FOI).
   
    - ### 2.4 Tamper-Evidence Through Cryptographic Chaining
   
    - Every record is hashed using BLAKE3, signed with Ed25519, and appended to a forward-secret Merkle chain. This guarantees no post-facto editing, immediate tamper detection, and mathematical verifiability.
   
    - ---

    ## 3. Formal Guarantee

    The core guarantee is expressed formally as:

    ```
    AtomicInferenceCapture(...) := {
      sign(BLAKE3(ctx || reasoning_trace || ppp_triplet || human_delta_chain)),
      persist(Merkle-append),
      return committed
    }
    ```

    ### Invariants

    1. Policy = PPP is captured atomically at every inference instant.
    2. 2. The evidentiary standard remains mathematically indivisible and legally above reproach.
       3. 3. The full record is directly enforceable under existing fiduciary and corporate governance rules.
         
          4. ---
         
          5. ## 4. Architecture
         
          6. AKI follows a single-path, kernel-only architecture. The universal inference wrapper:
         
          7. ```
             agdr_capture(ctx, prompt, model_id, reasoning_trace, output, ppp_triplet, human_delta_chain)
             ```

             This wrapper is compatible with any current or future inference model.

             ---

             ## 5. Schema Specifications

             Three JSON Schemas (draft 2020-12):

             1. **PPP Triplet Schema** — Three mandatory string fields, extensible via `additionalProperties: true`.
             2. 2. **Human Delta Chain Schema** — Ordered interventions, FOI escalation, chain resolution.
                3. 3. **AgDR Record Schema** — Top-level evidentiary unit. `committed` is always `true`.
                  
                   4. ---
                  
                   5. ## 6. Cryptographic Choices
                  
                   6. - **Hashing:** BLAKE3 — speed, security, streaming
                      - - **Signing:** Ed25519 — small signatures, fast verification
                        - - **Chaining:** Merkle append-only — forward secrecy, tamper-evident
                          - - **Timestamps:** Nanosecond precision
                           
                            - ---

                            ## 7. Legal and Regulatory Alignment

                            The standard aligns with Canadian fiduciary and corporate governance frameworks, including CBCA fiduciary duty, EU AI Act documentation requirements, and provincial securities regulations.

                            ---

                            ## 8. Publication and Archival

                            Published as an open Canadian standard under dual license (CC0-1.0 / Apache-2.0). Intended for ISBN registration, Library and Archives Canada deposit, DOI assignment via Zenodo, and open-source ecosystem development.

                            ---

                            *Published by Accountability.ai — Toronto, Canada — March 2026*
