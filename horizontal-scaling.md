# Horizontal Scaling

**AgDR v0.2 — Scaling Beyond the Single-Process Ceiling**
Published March 2026

---

## The Single-Process Ceiling

The TSX stress test proved AgDR at 100 million decisions, reaching a ceiling of approximately **2.85 billion decisions** in a single process (memory-bound). At 253,807 decisions per second, that ceiling is reached in roughly 3.1 hours of sustained operation.

For high-velocity environments — trading desks, clinical systems, government adjudication at scale, autonomous vehicle fleets — the answer is horizontal scaling: multiple AgDR processes, each maintaining its own atomic kernel chain, coordinated through a **Root Merkle Tree** that provides a single, unified, court-provable record of the entire distributed operation.

---

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │        Root Merkle Coordinator       │
                    │   (aggregates shard roots hourly)    │
                    │   Produces: Global Merkle Root        │
                    └──────┬──────────┬──────────┬─────────┘
                           │          │          │
              ┌────────────┘  ┌───────┘  ┌───────┘
              ▼               ▼           ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Shard 0 │   │  Shard 1 │   │  Shard N │
        │  AKI     │   │  AKI     │   │  AKI     │
        │  Process │   │  Process │   │  Process │
        └──────────┘   └──────────┘   └──────────┘
        0–2.85B        0–2.85B        0–2.85B
        decisions      decisions      decisions
```

Each shard is an independent AgDR process with its own:
- Kernel atomic section
- Merkle chain (forward-secret)
- Ed25519 signing key

The Root Merkle Coordinator aggregates shard roots on a defined interval and produces a **Global Merkle Root** — the single hash that commits to every decision across all shards.

---

## Shard Assignment

Decisions are assigned to shards by a deterministic routing function. The routing function must be:

1. **Deterministic** — the same decision always routes to the same shard
2. **Auditable** — the routing decision is itself logged
3. **Collision-free for related decisions** — decisions that must appear in the same evidentiary chain (e.g., all decisions for a single trade) must route to the same shard

**Routing strategies:**

| Strategy | Use Case | How |
|---|---|---|
| Hash-by-entity | All decisions for entity X on same shard | `shard = hash(entity_id) % num_shards` |
| Hash-by-session | All decisions in a session on same shard | `shard = hash(session_id) % num_shards` |
| Time-partitioned | Different shards own different time windows | `shard = floor(timestamp_ns / window_ns) % num_shards` |
| Domain-partitioned | Different shard per business domain | Static mapping: trading → shard 0, risk → shard 1, etc. |

---

## Root Merkle Coordinator

The coordinator runs on a configurable interval (default: every 60 seconds) and:

1. Requests the current Merkle root from each live shard
2. Assembles the shard roots into a Root Merkle Tree
3. Signs the Global Merkle Root with the coordinator's Ed25519 key
4. Appends the Global Root to the permanent audit log
5. Publishes the Global Root (optionally: to a public transparency log)

```python
from agdr_aki.coordinator import RootMerkleCoordinator

coordinator = RootMerkleCoordinator(
    shards=["shard-0:50051", "shard-1:50052", "shard-2:50053"],
    aggregation_interval_s=60,
    signing_key_path="coordinator_key.pem",
    output_log="global_merkle_roots.log",
)
coordinator.start()
```

**Global Root record structure:**

```json
{
  "global_root_id": "gr_20260315_094200",
  "timestamp_ns": 1742000000000000000,
  "interval_start_ns": 1741999940000000000,
  "interval_end_ns": 1742000000000000000,
  "shard_roots": [
    { "shard_id": "shard-0", "root": "a8f3c1...", "record_count": 15228441 },
    { "shard_id": "shard-1", "root": "b2e9d4...", "record_count": 15191033 },
    { "shard_id": "shard-2", "root": "c7f1a8...", "record_count": 15384526 }
  ],
  "global_merkle_root": "9e2b7f...",
  "total_records_in_interval": 45803000,
  "signature": "<Ed25519 signature of global_merkle_root>"
}
```

---

## Throughput at Scale

Each shard runs at the single-process rate. With N shards:

| Shards | Throughput | Daily capacity |
|---|---|---|
| 1 | 253,807 decisions/sec | ~21.9 billion |
| 4 | ~1,000,000 decisions/sec | ~86.4 billion |
| 10 | ~2,500,000 decisions/sec | ~216 billion |
| 100 | ~25,000,000 decisions/sec | ~2.16 trillion |

Horizontal scaling is bounded only by network and storage — not by the AKI algorithm itself.

---

## Evidentiary Properties at Scale

The horizontal architecture preserves all evidentiary guarantees of the single-process model:

| Property | Single-process | Horizontal |
|---|---|---|
| Per-record integrity | BLAKE3 hash + Ed25519 | Same — per shard |
| Chain completeness | Merkle chain per process | Merkle chain per shard |
| Global integrity | Single root | Global Merkle Root across all shards |
| Court production | Single chain | Shard + global root + routing log |
| Tamper evidence | Breaking any hash breaks chain | Breaking any shard hash breaks that shard's chain AND the global root |

**For court production in a horizontal deployment**, produce:
1. The specific record(s) from the relevant shard
2. The shard's Merkle chain proof
3. The Global Merkle Root log entry covering the record's time interval
4. The routing log proving this entity/session was assigned to this shard

---

## Deployment Considerations

### Shard key management
Each shard has its own Ed25519 signing key. The coordinator has its own key. All keys must be:
- Generated securely at deployment
- Backed up in a key management system (e.g., HashiCorp Vault, AWS KMS)
- Rotated on a defined schedule
- Never shared between shards

### FOI assignment in horizontal deployments
FOI designation is per decision class, not per shard. A single FOI may cover decisions across all shards in their designated scope. The routing function ensures escalated decisions from any shard reach the correct FOI through the same escalation path.

### Network failure handling
If a shard is unreachable during root aggregation:
- The coordinator logs the missing shard
- The global root is computed from available shards
- The missing interval is flagged for reconstruction when the shard comes back online
- **No decisions are dropped** — the shard's local chain remains intact

### Storage
At 253,807 decisions/second per shard, with a typical record size of ~2KB:
- Single shard: ~500 MB/sec — plan for ~43 TB/day
- Use tiered storage: hot (NVMe) for recent records, cold (object storage) for archive
- The Merkle chain structure allows cold records to be verified without loading into memory

---

*Part of the AgDR v0.2 foundational standard*
Canonical source: https://github.com/aiccountability-source/AgDR
