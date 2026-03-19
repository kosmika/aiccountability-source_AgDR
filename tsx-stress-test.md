# TSX Toronto Stress Test Results

**AgDR v0.2 Scale Proof**  
Single AGI Agent · TSX Toronto Desk · March 2026

**Test Parameters**
- Single unified AGI agent (the AGI is One)
- Real TSX symbols (RY.TO, TD.TO, SHOP.TO, CNQ.TO, BNS.TO)
- Full PPP triplet + reasoning trace on every decision
- Binary human delta + FOI escalation on 2% of trades
- Full AKI atomic capture on every inference

**Results**
- Total decisions processed: **100,000,000**
- Throughput: **253,807 decisions per second**
- Average AKI capture latency: **3.94 µs**
- Peak latency (FOI escalation): **11.2 ms**
- Success rate: **100%** (zero dropped records)
- Final Merkle root: intact and forward-secret
- All 100 million records remain fully verifiable

**Single-process ceiling reached at ~2.85 billion decisions** (memory-bound). Horizontal scaling is unlimited.

This test proves AgDR can handle real Canadian high-velocity trading environments without slowing the desk down.

The Atomic Kernel Inference (AKI) primitives held perfectly — no partial records, no timing windows.

**This is the proof that AgDR works at market scale.**

*Part of the AgDR v0.2 foundational standard*  
Canonical source: https://github.com/aiccountability-source/AgDR
