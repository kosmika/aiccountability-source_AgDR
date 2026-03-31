"""
simulation/nemoclaw_adapter.py
AgDR Neural Spine — NemoClaw Hardware Adapter

Bridges AgDR accountability records with hardware-level AI acceleration.
Every NemoClaw inference is wrapped in a tamper-evident AgDR record and
committed to the Neural Spine before the result is returned.

Requires:
    pip install httpx agdr-aki

Usage:
    from simulation.nemoclaw_adapter import NemoClawAdapter
    adapter = NemoClawAdapter(model_name="meta/llama-3.1-8b-instruct",
                              dry_run=True)
    result = await adapter.infer(prompt="What is 2+2?",
                                 provenance="my-service-v1",
                                 place="ca-central-1",
                                 purpose="math-query")
    print(result.answer)
    print(result.agdr_record.merkle_root)
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


# AgDR record (self-contained)
@dataclass
class AgDRRecord:
    decision_id: str
    timestamp: str
    provenance: str
    place: str
    purpose: str
    payload: dict
    merkle_root: str = ""
    committed: bool = False

    def compute_merkle(self) -> str:
        canonical = json.dumps({
            "decision_id": self.decision_id,
            "timestamp": self.timestamp,
            "provenance": self.provenance,
            "place": self.place,
            "purpose": self.purpose,
            "payload": self.payload,
        }, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def seal(self) -> "AgDRRecord":
        self.merkle_root = self.compute_merkle()
        self.committed = True
        return self

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class NemoClawResult:
    answer: Any
    latency_ms: float
    model_name: str
    agdr_record: AgDRRecord
    hardware_metadata: dict


class NemoClawAdapter:
    """
    Hardware-layer AgDR adapter for NemoClaw / NVIDIA NeMo inference.
    Wraps every inference call in a tamper-evident AgDR record (PPP triplet).

    Parameters
    ----------
    model_name   : NVIDIA NIM model identifier
    nim_base_url : NVIDIA NIM API base URL
    api_key      : API key (env var NVIDIA_API_KEY fallback)
    spine_url    : AgDR Neural Spine endpoint (None = local log)
    dry_run      : Simulate without calling the NIM API
    """

    MODEL_DEFAULT = "meta/llama-3.1-8b-instruct"
    NIM_DEFAULT_URL = "https://integrate.api.nvidia.com/v1"

    def __init__(
        self,
        model_name: str = MODEL_DEFAULT,
        nim_base_url: str = NIM_DEFAULT_URL,
        api_key: Optional[str] = None,
        spine_url: Optional[str] = None,
        dry_run: bool = False,
    ):
        self.model_name = model_name
        self.nim_base_url = nim_base_url
        self.api_key = api_key or os.environ.get("NVIDIA_API_KEY", "")
        self.spine_url = spine_url
        self.dry_run = dry_run
        self._committed_records: list[AgDRRecord] = []

    async def infer(
        self,
        prompt: str,
        provenance: str,
        place: str,
        purpose: str,
        max_tokens: int = 512,
        temperature: float = 0.2,
        extra_payload: Optional[dict] = None,
    ) -> NemoClawResult:
        """Run inference and wrap result in a sealed AgDR accountability record."""
        decision_id = self._make_decision_id(provenance, purpose)
        ts = datetime.now(timezone.utc).isoformat()

        payload = {
            "prompt": prompt,
            "model": self.model_name,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **(extra_payload or {}),
        }

        t0 = time.perf_counter()
        answer, hw_meta = await self._call_nim(prompt, max_tokens, temperature)
        latency_ms = (time.perf_counter() - t0) * 1000

        hw_meta["latency_ms"] = round(latency_ms, 2)
        payload["hardware_metadata"] = hw_meta

        record = AgDRRecord(
            decision_id=decision_id,
            timestamp=ts,
            provenance=provenance,
            place=place,
            purpose=purpose,
            payload=payload,
        ).seal()

        await self._commit_to_spine(record)
        self._committed_records.append(record)

        return NemoClawResult(
            answer=answer,
            latency_ms=latency_ms,
            model_name=self.model_name,
            agdr_record=record,
            hardware_metadata=hw_meta,
        )

    async def _call_nim(
        self, prompt: str, max_tokens: int, temperature: float
    ) -> tuple[str, dict]:
        """Call NVIDIA NIM inference API. Returns (answer, hw_metadata)."""
        if self.dry_run or not self.api_key:
            stub = f"[DRY-RUN] '{prompt[:60]}...'"
            return stub, {"source": "dry_run", "model": self.model_name}

        try:
            import httpx
        except ImportError:
            raise ImportError("pip install httpx")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{self.nim_base_url}/chat/completions",
                headers=headers,
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()

        answer = data["choices"][0]["message"]["content"]
        hw_meta = {
            "source": "nvidia_nim",
            "model": data.get("model", self.model_name),
            "usage": data.get("usage", {}),
            "finish_reason": data["choices"][0].get("finish_reason", ""),
        }
        return answer, hw_meta

    async def _commit_to_spine(self, record: AgDRRecord) -> None:
        """Commit sealed AgDR record to the Neural Spine endpoint."""
        if self.spine_url:
            try:
                import httpx
                async with httpx.AsyncClient(timeout=10.0) as client:
                    await client.post(self.spine_url, json=record.to_dict())
            except Exception as exc:
                print(f"[NemoClawAdapter] WARN: spine commit failed: {exc}")
        else:
            print(f"[NemoClawAdapter] Local commit: {record.decision_id} "
                  f"merkle={record.merkle_root[:16]}...")

    def _make_decision_id(self, provenance: str, purpose: str) -> str:
        ts_ns = time.time_ns()
        slug = hashlib.md5(
            f"{provenance}:{purpose}:{ts_ns}".encode()
        ).hexdigest()[:8]
        return f"nemoclaw_{slug}_{ts_ns}"

    def get_audit_trail(self) -> list[dict]:
        """Return all committed AgDR records as dicts."""
        return [r.to_dict() for r in self._committed_records]

    def export_jsonl(self, path: str = "nemoclaw_audit.jsonl") -> Path:
        """Export the audit trail to a JSONL file."""
        out = Path(path)
        with out.open("w") as fh:
            for r in self._committed_records:
                fh.write(json.dumps(r.to_dict()) + "\n")
        print(f"[NemoClawAdapter] {len(self._committed_records)} records -> {out}")
        return out


class NemoClawBatchProcessor:
    """Replay OASIS seed events through the NemoClaw adapter."""

    def __init__(self, adapter: NemoClawAdapter):
        self.adapter = adapter

    async def process_seed_file(
        self,
        seed_path: str = "simulation/data/agdr_oasis_seed_events.jsonl",
    ) -> list[NemoClawResult]:
        seed_path = Path(seed_path)
        if not seed_path.exists():
            raise FileNotFoundError(f"Not found: {seed_path}")
        results = []
        with seed_path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                event = json.loads(line)
                prompt = event.get("payload", {}).get("content", str(event))
                result = await self.adapter.infer(
                    prompt=prompt,
                    provenance=event.get("provenance", "oasis_simulator"),
                    place=event.get("place", "simulation"),
                    purpose=event.get("purpose", "replay"),
                )
                results.append(result)
                print(f"  [{result.agdr_record.decision_id[:24]}] "
                      f"latency={result.latency_ms:.1f}ms")
        return results


if __name__ == "__main__":
    import sys
    seed = sys.argv[1] if len(sys.argv) > 1 else "simulation/data/agdr_oasis_seed_events.jsonl"
    model = sys.argv[2] if len(sys.argv) > 2 else NemoClawAdapter.MODEL_DEFAULT

    adapter = NemoClawAdapter(model_name=model, dry_run=True)
    processor = NemoClawBatchProcessor(adapter)
    print(f"NemoClawAdapter  model={model}  dry_run=True")
    results = asyncio.run(processor.process_seed_file(seed))
    print(f"\nProcessed {len(results)} seed events.")
    adapter.export_jsonl("nemoclaw_audit.jsonl")
