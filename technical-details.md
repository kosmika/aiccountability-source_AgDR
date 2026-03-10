# AgDR v0.2 Technical Details

**Current State – March 2026**

The original name **ADR** (Agent Decision Record) v0.1 is now deprecated and obsolete.  
The current standard is **AgDR v0.2** with the enforcement layer called **Atomic Kernel Inference (AKI)**.

### 1. Core Architecture
- Full Name: AgDR v0.2 with Atomic Kernel Inference (AKI)
- Capture Point: Exact inference instant (the “i” point)
- Guarantee: One mathematically indivisible kernel transaction — the entire record is either fully committed or never exists

### 2. Formal Definition of AKI
```math
AtomicInferenceCapture(ctx, reasoning_trace, output, ppp_triplet, human_delta_chain) ≡
{
  sign(BLAKE3(ctx ∥ reasoning_trace ∥ ppp_triplet ∥ human_delta_chain)),
  persist(Merkle-append to forward-secret chain),
  return committed
}
