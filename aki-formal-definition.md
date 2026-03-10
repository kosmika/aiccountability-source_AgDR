# AKI Formal Definition

**Atomic Kernel Inference (AKI)** — AgDR v0.2 Enforcement Layer

### Formal Mathematical Definition

AKI is defined as a single indivisible kernel transaction:

\[
\text{AtomicInferenceCapture}(ctx, \ reasoning\_trace, \ output, \ ppp\_triplet, \ human\_delta\_chain) \equiv
\begin{cases}
\text{sign}(\text{BLAKE3}(ctx \Vert reasoning\_trace \Vert ppp\_triplet \Vert human\_delta\_chain)) \\
\text{persist}(\text{Merkle-append to forward-secret chain}) \\
\text{return committed}
\end{cases}
\]

### Execution Invariants (Enforced by CPU)
- Interrupts disabled: `local_irq_save(flags)`
- Preemption disabled: `preempt_disable()`
- No clocks or timers used (clock-independent)
- Zero-copy signing path
- Full rollback on failure — record never becomes visible

### Integration with PPP Triplet
The PPP triplet (Provenance · Place · Purpose) is captured verbatim inside the same atomic block. This guarantees that the meaning of each P is frozen at the exact inference instant and cannot be altered later.

### How to Import and Use AKI

**Python Wrapper Example** (import this):
```python
from agdr_aki import aki_capture

record = aki_capture(
    ctx=system_context,
    reasoning_trace=full_trace,
    output=decision_output,
    ppp_triplet=ppp_dict,
    human_delta_chain=delta_chain
)
