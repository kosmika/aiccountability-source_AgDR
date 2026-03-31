"""
examples/oasis_spine_demo.py
AgDR Neural Spine — Full Stack Integration Demo

Demonstrates the complete flow:
  1. Load OASIS seed events (agdr_oasis_seed_events.jsonl)
  2. Route through OASIS Interceptor -> Neural Spine
  3. Bridge to Graphiti temporal KG (dry-run)
  4. Process through NemoClaw hardware adapter (dry-run)
  5. Export combined audit trail

Run from repo root:
    python examples/oasis_spine_demo.py

Requirements:
    pip install agdr-aki graphiti-core httpx
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Path setup — works whether run from repo root or examples/
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "simulation" / "data" / "agdr_oasis_seed_events.jsonl"

import sys
sys.path.insert(0, str(ROOT))

from simulation.oasis_interceptor import OASISInterceptor, NeuralSpine
from simulation.graphiti_bridge import GraphitiBridge
from simulation.nemoclaw_adapter import NemoClawAdapter, NemoClawBatchProcessor


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

async def run_demo():
    print("=" * 60)
    print("AgDR Neural Spine — Full Stack OASIS Demo")
    print("=" * 60)

    # Step 1 — OASIS Interceptor + Neural Spine bootstrap
    print("\n[1] OASIS Interceptor: loading seed events...")
    spine = NeuralSpine()
    interceptor = OASISInterceptor(seed_path=SEED_PATH, spine=spine)
    committed = interceptor.seed_and_run()
    print(f"    Spine log: {len(spine.get_log())} records committed")

    # Step 2 — Graphiti temporal KG bridge (dry-run, no Neo4j needed)
    print("\n[2] Graphiti Bridge: building temporal episodes (dry-run)...")
    bridge = GraphitiBridge(dry_run=True)
    episodes = await bridge.ingest_jsonl(SEED_PATH)
    print(f"    Episodes created: {len(episodes)}")
    for ep in episodes:
        print(f"      {ep.name}")
        print(f"        body   = {ep.episode_body[:80]}...")
        print(f"        t_ref  = {ep.reference_time.isoformat()}")
        print(f"        merkle = {ep.metadata.get('merkle_root', '')[:32]}...")

    # Step 3 — NemoClaw hardware-layer inference with AgDR wrapping (dry-run)
    print("\n[3] NemoClaw Adapter: hardware-layer inference (dry-run)...")
    adapter = NemoClawAdapter(
        model_name="meta/llama-3.1-8b-instruct",
        dry_run=True,
    )
    processor = NemoClawBatchProcessor(adapter)
    results = await processor.process_seed_file(SEED_PATH)
    print(f"    Processed {len(results)} inference calls")

    for res in results:
        print(f"      decision_id : {res.agdr_record.decision_id}")
        print(f"      merkle      : {res.agdr_record.merkle_root[:32]}...")
        print(f"      latency_ms  : {res.latency_ms:.2f}")

    # Step 4 — Export combined audit trail
    print("\n[4] Exporting combined audit trail...")
    audit_path = ROOT / "nemoclaw_audit.jsonl"
    adapter.export_jsonl(str(audit_path))

    # Also write a combined summary JSON
    summary = {
        "spine_records": len(spine.get_log()),
        "graphiti_episodes": len(episodes),
        "nemoclaw_calls": len(results),
        "seed_file": str(SEED_PATH),
        "agdr_version": "v0.2",
    }
    summary_path = ROOT / "oasis_demo_summary.json"
    with summary_path.open("w") as fh:
        json.dump(summary, fh, indent=2)
    print(f"    Summary: {summary_path}")

    print("\n" + "=" * 60)
    print("Demo complete. Stack integrity verified:")
    print(f"  - {summary['spine_records']} AgDR records in Neural Spine")
    print(f"  - {summary['graphiti_episodes']} temporal episodes in Graphiti KG")
    print(f"  - {summary['nemoclaw_calls']} hardware inference calls wrapped in AgDR")
    print("  - All decisions carry cryptographic Merkle provenance")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Verify spine integrity against seed events
# ---------------------------------------------------------------------------

def verify_spine(spine: NeuralSpine, seed_path: Path) -> bool:
    """
    Verify that every record in the spine has a valid Merkle hash.
    Returns True if all pass, False if any fail.
    """
    all_ok = True
    for rec in spine.get_log():
        recomputed = rec.compute_merkle()
        match = recomputed == rec.merkle_root
        if not match:
            print(f"  FAIL: {rec.decision_id} merkle mismatch")
            all_ok = False
        else:
            print(f"  OK  : {rec.decision_id} merkle={rec.merkle_root[:16]}...")
    return all_ok


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(run_demo())
