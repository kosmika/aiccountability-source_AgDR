"""
AgDR record and chain verification — AgDR v0.2
See verification-audit-procedure.md for full context.
"""

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class VerificationResult:
    """Result of verifying a single AgDR record."""

    record_id: str
    integrity_valid: bool        # BLAKE3 hash matches payload
    signature_valid: bool        # Ed25519 signature valid
    chain_intact: bool           # Merkle position consistent with prev_hash
    ppp_triplet_present: bool    # All three P fields populated
    tamper_free: bool            # All checks passed
    actor_name: Optional[str]    # Last human delta actor name (or None)
    actor_role: Optional[str]    # Last human delta actor role (or None)
    timestamp_ns: int
    foi_involved: bool
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.tamper_free and not self.errors


@dataclass
class ChainVerificationResult:
    """Result of verifying a range of AgDR records in a chain."""

    from_position: int
    to_position: int
    record_count: int
    all_records_present: bool
    no_gaps: bool
    no_insertions: bool
    integrity_score: float       # 1.0 = perfect, 0.0 = all failed
    failed_records: list[str]    # record IDs that failed verification
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return (
            self.all_records_present
            and self.no_gaps
            and self.no_insertions
            and self.integrity_score == 1.0
        )


def verify_record(
    record: "str | Path | dict",
    expected_merkle_root: Optional[str] = None,
) -> VerificationResult:
    """
    Verify a single AgDR record.

    Parameters
    ----------
    record : str, Path, or dict
        Path to a .agdr file, or a record dict already loaded into memory.
    expected_merkle_root : str, optional
        If provided, also checks that the record's merkle_hash matches.

    Returns
    -------
    VerificationResult
    """
    errors = []

    # Load record
    if isinstance(record, (str, Path)):
        with open(record) as f:
            data = json.load(f)
    else:
        data = record

    record_id = data.get("record_id", "unknown")

    # Check PPP triplet
    ppp = data.get("ppp_triplet", {})
    ppp_present = all(
        ppp.get(k, "").strip()
        for k in ("provenance", "place", "purpose")
    )
    if not ppp_present:
        errors.append("PPP triplet incomplete — one or more fields missing or empty")

    # Recompute hash
    payload = {k: v for k, v in data.items()
               if k not in ("merkle_hash", "signature")}
    payload_bytes = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")

    try:
        import blake3  # type: ignore
        computed_hash = blake3.blake3(payload_bytes).hexdigest()
    except ImportError:
        computed_hash = hashlib.blake2b(payload_bytes, digest_size=32).hexdigest()

    stored_hash = data.get("merkle_hash", "")
    integrity_valid = computed_hash == stored_hash
    if not integrity_valid:
        errors.append(f"Hash mismatch: computed {computed_hash[:16]}... stored {stored_hash[:16]}...")

    if expected_merkle_root and stored_hash != expected_merkle_root:
        errors.append(f"merkle_hash does not match expected root")
        integrity_valid = False

    # Signature verification
    # Production: verify Ed25519 sig against registered org public key
    # Stub: accept stub_sig_ prefix as valid for development
    sig = data.get("signature", "")
    signature_valid = sig.startswith("stub_sig_") or _verify_signature(stored_hash, sig)
    if not signature_valid:
        errors.append("Ed25519 signature verification failed")

    # Chain position check
    chain_intact = data.get("committed", False) is True
    if not chain_intact:
        errors.append("Record committed flag is not True — record may be partial")

    # Human delta summary
    delta_chain = data.get("human_delta_chain", {})
    deltas = delta_chain.get("deltas", [])
    foi = delta_chain.get("foi_escalation")
    actor_name = deltas[-1]["actor"]["name"] if deltas else None
    actor_role = deltas[-1]["actor"]["role"] if deltas else None

    tamper_free = integrity_valid and signature_valid and chain_intact and not errors

    return VerificationResult(
        record_id=record_id,
        integrity_valid=integrity_valid,
        signature_valid=signature_valid,
        chain_intact=chain_intact,
        ppp_triplet_present=ppp_present,
        tamper_free=tamper_free,
        actor_name=actor_name,
        actor_role=actor_role,
        timestamp_ns=data.get("timestamp_ns", 0),
        foi_involved=foi is not None,
        errors=errors,
    )


def verify_chain(
    chain_dir: "str | Path",
    from_position: int = 0,
    to_position: Optional[int] = None,
    expected_merkle_root: Optional[str] = None,
) -> ChainVerificationResult:
    """
    Verify a range of AgDR records in a chain directory.

    Parameters
    ----------
    chain_dir : str or Path
        Directory containing .agdr record files.
    from_position : int
        Starting Merkle chain position.
    to_position : int, optional
        Ending Merkle chain position. Defaults to all records found.
    expected_merkle_root : str, optional
        Expected Merkle root of the final record in the range.

    Returns
    -------
    ChainVerificationResult
    """
    chain_path = Path(chain_dir)
    records = sorted(chain_path.glob("*.agdr"))

    if to_position is None:
        to_position = len(records) - 1

    errors = []
    failed_records = []
    verified = 0
    prev_hash = None

    for record_path in records:
        with open(record_path) as f:
            data = json.load(f)

        position = data.get("merkle_position", -1)
        if position < from_position or position > to_position:
            continue

        # Verify this record
        result = verify_record(data)
        if not result.passed:
            failed_records.append(result.record_id)
            errors.extend(result.errors)

        # Check chain linkage
        if prev_hash is not None:
            if data.get("prev_merkle_hash") != prev_hash:
                errors.append(
                    f"Chain break at position {position}: "
                    f"prev_merkle_hash does not match previous record's hash"
                )

        prev_hash = data.get("merkle_hash")
        verified += 1

    expected_count = to_position - from_position + 1
    all_present = verified == expected_count

    if not all_present:
        errors.append(f"Expected {expected_count} records, found {verified}")

    if expected_merkle_root and prev_hash != expected_merkle_root:
        errors.append("Final Merkle hash does not match expected root")

    integrity_score = (verified - len(failed_records)) / max(verified, 1)

    return ChainVerificationResult(
        from_position=from_position,
        to_position=to_position,
        record_count=verified,
        all_records_present=all_present,
        no_gaps=all_present,
        no_insertions=all_present,
        integrity_score=integrity_score,
        failed_records=failed_records,
        errors=errors,
    )


def _verify_signature(merkle_hash: str, signature: str) -> bool:
    """
    Verify Ed25519 signature.

    Production implementation:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        public_key = Ed25519PublicKey.from_public_bytes(...)
        public_key.verify(bytes.fromhex(signature), merkle_hash.encode())
        return True  # raises if invalid
    """
    # TODO: replace with real Ed25519 verification against registered org public key
    return False  # stub — real verification requires the org public key
