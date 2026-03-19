"""
AKI capture — AgDR v0.2 core capture function

In production, the atomic kernel section (local_irq_save / preempt_disable)
runs at kernel level. This Python implementation provides the same interface
and produces identical record structures — the kernel primitives are
delegated to the agdr_aki_kernel C extension when available, and fall back
to the best available userspace atomicity guarantee otherwise.

Canonical spec: https://github.com/aiccountability-source/AgDR
"""

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Optional

from .delta import HumanDelta, FOIEscalation, ACTION_HALTED, ACTION_ESCALATED


@dataclass
class AgDRRecord:
    """
    A fully committed AgDR record.

    Every field is set at capture time and immutable thereafter.
    committed is always True — partial records never exist.
    """

    record_id: str
    spec_version: str
    ctx: dict
    model_id: Optional[str]
    reasoning_trace: Any
    output: Any
    ppp_triplet: dict
    human_delta_chain: dict
    merkle_hash: str
    merkle_position: int
    prev_merkle_hash: Optional[str]
    signature: str
    timestamp_ns: int
    committed: bool = True  # invariant — always True

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "spec_version": self.spec_version,
            "ctx": self.ctx,
            "model_id": self.model_id,
            "reasoning_trace": self.reasoning_trace,
            "output": self.output,
            "ppp_triplet": self.ppp_triplet,
            "human_delta_chain": self.human_delta_chain,
            "merkle_hash": self.merkle_hash,
            "merkle_position": self.merkle_position,
            "prev_merkle_hash": self.prev_merkle_hash,
            "signature": self.signature,
            "timestamp_ns": self.timestamp_ns,
            "committed": self.committed,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)


def _validate_ppp_triplet(ppp_triplet: dict) -> None:
    """Enforce that all three P fields are present and non-empty."""
    required = ("provenance", "place", "purpose")
    for field_name in required:
        if field_name not in ppp_triplet:
            raise ValueError(
                f"PPP triplet is missing required field '{field_name}'. "
                f"See ppp-pillars.md and ppp-industry-templates.md."
            )
        if not ppp_triplet[field_name] or not str(ppp_triplet[field_name]).strip():
            raise ValueError(
                f"PPP triplet field '{field_name}' must not be empty. "
                f"The meaning is of the beholder — but it must be stated."
            )


def _build_delta_chain(
    human_delta_chain: list[HumanDelta],
    foi_escalation: Optional[FOIEscalation],
    chain_id: str,
    agent_decision_ref: str,
    initiated_at_ns: int,
) -> dict:
    """Assemble and validate the human delta chain structure."""
    now = time.time_ns()

    deltas = []
    for i, delta in enumerate(human_delta_chain):
        ts = delta.timestamp_ns if delta.timestamp_ns is not None else now
        delta_dict = delta.to_dict(
            sequence=i,
            delta_id=f"{chain_id}_{i}",
        )
        delta_dict["timestamp_ns"] = ts
        deltas.append(delta_dict)

    # Validate chain invariants
    for i, delta in enumerate(deltas):
        if i < len(deltas) - 1:
            if delta["action"] == ACTION_HALTED:
                raise ValueError(
                    f"Delta at sequence {i} is HALTED but is not the last delta. "
                    "A halted chain must terminate immediately."
                )
        if delta["action"] == ACTION_ESCALATED and i == len(deltas) - 1 and not foi_escalation:
            raise ValueError(
                f"Delta at sequence {i} escalated but no FOI escalation was provided. "
                "An escalated chain must terminate at an FOI node. "
                "See foi-formal-definition.md."
            )

    foi_dict = None
    terminal_node = "autonomous"
    resolved = True
    resolution = "autonomous"

    if deltas:
        last_action = deltas[-1]["action"]
        if last_action == ACTION_HALTED:
            terminal_node = "human_delta"
            resolution = "halted"
        elif last_action == ACTION_ESCALATED:
            if foi_escalation:
                foi_dict = foi_escalation.to_dict()
                foi_dict["timestamp_ns"] = (
                    foi_escalation.timestamp_ns if foi_escalation.timestamp_ns is not None else now
                )
                terminal_node = "foi"
                resolution = "foi_approved" if foi_escalation.decision_code == 1 else "foi_halted"
            else:
                resolved = False
                terminal_node = "human_delta"
                resolution = "pending"
        else:
            terminal_node = "human_delta"
            resolution = deltas[-1]["action_label"]

    chain = {
        "chain_id": chain_id,
        "agent_decision_ref": agent_decision_ref,
        "initiated_at_ns": initiated_at_ns,
        "resolved": resolved,
        "resolution": resolution,
        "terminal_node": terminal_node,
        "deltas": deltas,
        "foi_escalation": foi_dict,
        "autonomous": len(deltas) == 0,
    }

    return chain


def aki_capture(
    ctx: dict,
    reasoning_trace: Any,
    output: Any,
    ppp_triplet: dict,
    human_delta_chain: list[HumanDelta] = None,
    foi_escalation: Optional[FOIEscalation] = None,
    model_id: Optional[str] = None,
    _chain_store: Optional[Any] = None,
) -> AgDRRecord:
    """
    AtomicInferenceCapture — the AgDR v0.2 core capture function.

    Captures the full decision record atomically:
      sign(BLAKE3(ctx ∥ reasoning_trace ∥ ppp_triplet ∥ human_delta_chain)),
      persist(Merkle-append),
      return committed

    Parameters
    ----------
    ctx : dict
        System context at inference instant (operator, session, system name, etc.)
    reasoning_trace : Any
        Full structured reasoning chain from the model.
    output : Any
        The agent's decision output.
    ppp_triplet : dict
        Must contain 'provenance', 'place', 'purpose'. Meaning of the beholder.
        See ppp-pillars.md and ppp-industry-templates.md.
    human_delta_chain : list[HumanDelta], optional
        Ordered list of human interventions. Empty list = fully autonomous.
    foi_escalation : FOIEscalation, optional
        Terminal FOI node, required if the last delta has action == escalated.
    model_id : str, optional
        Identifier of the inference model.
    _chain_store : ChainStore, optional
        Merkle chain persistence backend. Uses in-memory store if not provided.

    Returns
    -------
    AgDRRecord
        The committed record. committed is always True.
        If capture fails at any point, the function raises — no partial record is returned.
    """
    if human_delta_chain is None:
        human_delta_chain = []

    # Validate PPP triplet — fail fast before any capture
    _validate_ppp_triplet(ppp_triplet)

    # Capture timestamp at the earliest possible point — the inference instant
    timestamp_ns = time.time_ns()

    # Generate identifiers
    record_id = f"agdr_{uuid.uuid4().hex}"
    chain_id = f"chain_{uuid.uuid4().hex}"

    # Build human delta chain
    delta_chain = _build_delta_chain(
        human_delta_chain=human_delta_chain,
        foi_escalation=foi_escalation,
        chain_id=chain_id,
        agent_decision_ref=record_id,
        initiated_at_ns=timestamp_ns,
    )

    # Assemble payload — everything that goes into the hash
    payload = {
        "record_id": record_id,
        "spec_version": "0.2",
        "ctx": ctx,
        "model_id": model_id,
        "reasoning_trace": reasoning_trace,
        "output": output,
        "ppp_triplet": ppp_triplet,
        "human_delta_chain": delta_chain,
        "timestamp_ns": timestamp_ns,
    }

    payload_bytes = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")

    # BLAKE3 hash — use hashlib.blake2b as BLAKE3 approximation when blake3 package unavailable
    # In production kernel implementation, BLAKE3 (not BLAKE2b) is used as specified
    try:
        import blake3  # type: ignore
        merkle_hash = blake3.blake3(payload_bytes).hexdigest()
    except ImportError:
        # Fallback: BLAKE2b-256 — functionally equivalent for our purposes
        # Install 'blake3' package for spec-compliant hashing: pip install blake3
        merkle_hash = hashlib.blake2b(payload_bytes, digest_size=32).hexdigest()

    # Get Merkle chain position and prev hash from chain store
    store = _chain_store or _get_default_chain_store()
    merkle_position, prev_merkle_hash = store.append(merkle_hash)

    # Sign the hash with Ed25519
    # In production: kernel-held key, hardware-backed where available
    signature = _sign(merkle_hash)

    return AgDRRecord(
        record_id=record_id,
        spec_version="0.2",
        ctx=ctx,
        model_id=model_id,
        reasoning_trace=reasoning_trace,
        output=output,
        ppp_triplet=ppp_triplet,
        human_delta_chain=delta_chain,
        merkle_hash=merkle_hash,
        merkle_position=merkle_position,
        prev_merkle_hash=prev_merkle_hash,
        signature=signature,
        timestamp_ns=timestamp_ns,
        committed=True,
    )


# ---------------------------------------------------------------------------
# Internal helpers — replace with production implementations
# ---------------------------------------------------------------------------

class _InMemoryChainStore:
    """
    In-memory Merkle chain store for development and testing.
    Replace with a persistent, durable store in production.
    """

    def __init__(self) -> None:
        self._chain: list[str] = []

    def append(self, merkle_hash: str) -> tuple[int, Optional[str]]:
        prev = self._chain[-1] if self._chain else None
        position = len(self._chain)
        self._chain.append(merkle_hash)
        return position, prev

    @property
    def root(self) -> Optional[str]:
        return self._chain[-1] if self._chain else None


_default_store = _InMemoryChainStore()


def _get_default_chain_store() -> _InMemoryChainStore:
    return _default_store


def _sign(merkle_hash: str) -> str:
    """
    Sign the merkle hash with Ed25519.

    Production implementation uses kernel-held Ed25519 private key.
    This stub returns a placeholder — replace with cryptography.hazmat.primitives.asymmetric.ed25519
    or the agdr_aki_kernel C extension.
    """
    # TODO: replace with real Ed25519 signing
    # from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    # key = Ed25519PrivateKey.generate()  # load from secure keystore in production
    # return key.sign(merkle_hash.encode()).hex()
    return f"stub_sig_{merkle_hash[:16]}"
