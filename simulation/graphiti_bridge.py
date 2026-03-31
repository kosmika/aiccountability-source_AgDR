"""
simulation/graphiti_bridge.py
AgDR Neural Spine — Graphiti Temporal Knowledge Graph Bridge

For each AgDR record, constructs a Graphiti episode with:
  - episode_body  = record payload
  - reference_time = record timestamp
  - metadata       = { signature, merkle_root, decision_id }

Supports bi-temporal validity windows as described in AgDR v0.2 spec.

Install Graphiti:
    pip install graphiti-core

Usage:
    from simulation.graphiti_bridge import GraphitiBridge
    bridge = GraphitiBridge(neo4j_uri="bolt://localhost:7687",
                            neo4j_user="neo4j", neo4j_password="password")
    await bridge.ingest_jsonl("simulation/data/agdr_oasis_seed_events.jsonl")
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class AgDREpisode:
    name: str
    episode_body: str
    reference_time: datetime
    source_description: str
    metadata: dict
    valid_from: datetime = None
    valid_to: Optional[datetime] = None

    def to_graphiti_kwargs(self) -> dict:
        return {
            "name": self.name,
            "episode_body": self.episode_body,
            "reference_time": self.reference_time,
            "source_description": self.source_description,
            "metadata": self.metadata,
        }


class GraphitiBridge:
    """AgDR-to-Graphiti temporal KG bridge (AgDR v0.2)."""

    def __init__(
        self,
        neo4j_uri: str = "bolt://localhost:7687",
        neo4j_user: str = "neo4j",
        neo4j_password: str = "password",
        openai_api_key: Optional[str] = None,
        dry_run: bool = False,
    ):
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.openai_api_key = openai_api_key
        self.dry_run = dry_run
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            from graphiti_core import Graphiti
            import os
            if self.openai_api_key:
                os.environ.setdefault("OPENAI_API_KEY", self.openai_api_key)
            self._client = Graphiti(self.neo4j_uri, self.neo4j_user, self.neo4j_password)
            return self._client
        except ImportError:
            raise ImportError("pip install graphiti-core")

    def record_to_episode(self, record: dict) -> AgDREpisode:
        payload = record.get("payload", {})
        ts_str = record.get("timestamp", datetime.now(timezone.utc).isoformat())
        try:
            ref_time = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            ref_time = datetime.now(timezone.utc)
        episode_body = json.dumps(payload, sort_keys=True)
        source_desc = f"{record.get('provenance', 'unknown')} | {record.get('purpose', 'unknown')}"
        metadata = {
            "decision_id": record.get("decision_id", ""),
            "signature": record.get("signature", ""),
            "merkle_root": record.get("merkle_root", ""),
            "place": record.get("place", ""),
            "purpose": record.get("purpose", ""),
            "agdr_version": "v0.2",
        }
        return AgDREpisode(
            name=record.get("decision_id", f"episode_{id(record)}"),
            episode_body=episode_body,
            reference_time=ref_time,
            source_description=source_desc,
            metadata=metadata,
            valid_from=ref_time,
            valid_to=None,
        )

    async def add_episode(self, episode: AgDREpisode) -> None:
        if self.dry_run:
            print(f"[GraphitiBridge DRY-RUN] Would add: {episode.name}")
            return
        client = self._get_client()
        await client.add_episode(**episode.to_graphiti_kwargs())
        print(f"[GraphitiBridge] Added episode: {episode.name}")

    async def ingest_records(self, records: list) -> list:
        episodes = [self.record_to_episode(r) for r in records]
        for ep in episodes:
            await self.add_episode(ep)
        print(f"[GraphitiBridge] Ingested {len(episodes)} episodes.")
        return episodes

    async def ingest_jsonl(self, path="simulation/data/agdr_oasis_seed_events.jsonl") -> list:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Seed file not found: {path}")
        records = []
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        print(f"[GraphitiBridge] Loaded {len(records)} records from {path}")
        return await self.ingest_records(records)

    def ingest_jsonl_sync(self, path="simulation/data/agdr_oasis_seed_events.jsonl") -> list:
        return asyncio.run(self.ingest_jsonl(path))


if __name__ == "__main__":
    import sys
    seed = sys.argv[1] if len(sys.argv) > 1 else "simulation/data/agdr_oasis_seed_events.jsonl"
    bridge = GraphitiBridge(dry_run=True)
    episodes = bridge.ingest_jsonl_sync(seed)
    print("\n--- AgDREpisodes ---")
    for ep in episodes:
        print(f"  {ep.name}  ref_time={ep.reference_time.isoformat()}")
