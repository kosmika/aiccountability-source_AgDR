"""
Evidence packaging for courts and regulators — AgDR v0.2
See verification-audit-procedure.md for full context.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .verify import verify_record


def package_evidence(
    record: "str | Path | dict",
    output_dir: "str | Path",
    include_chain_proof: bool = True,
    include_ppp_summary: bool = True,
    include_delta_summary: bool = True,
    signing_key_path: Optional["str | Path"] = None,
) -> Path:
    """
    Generate a court-ready evidence package for one AgDR record.

    Produces:
        - The original record (copied)
        - A verification report (text)
        - A PPP summary (JSON)
        - A human delta summary (JSON)
        - An independent verification instruction sheet

    Parameters
    ----------
    record : str, Path, or dict
        The AgDR record to package.
    output_dir : str or Path
        Directory to write the evidence package into.
    include_chain_proof : bool
        Whether to include chain integrity proof.
    include_ppp_summary : bool
        Whether to include a human-readable PPP summary.
    include_delta_summary : bool
        Whether to include a human-readable delta chain summary.
    signing_key_path : str or Path, optional
        Path to the organization's signing key for attesting the package.

    Returns
    -------
    Path
        Path to the output directory containing the evidence package.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Load record
    if isinstance(record, (str, Path)):
        with open(record) as f:
            data = json.load(f)
        record_path = Path(record)
        (out / record_path.name).write_text(json.dumps(data, indent=2, default=str))
    else:
        data = record
        (out / f"{data['record_id']}.agdr").write_text(
            json.dumps(data, indent=2, default=str)
        )

    record_id = data.get("record_id", "unknown")
    result = verify_record(data)

    # Verification report
    report_lines = [
        "AGDR VERIFICATION REPORT",
        "=" * 60,
        f"Record ID:        {record_id}",
        f"Generated:        {datetime.now(timezone.utc).isoformat()}",
        f"Spec version:     {data.get('spec_version', 'unknown')}",
        "",
        "INTEGRITY CHECK",
        f"  BLAKE3 hash:    {'PASS' if result.integrity_valid else 'FAIL'}",
        f"  Ed25519 sig:    {'PASS' if result.signature_valid else 'FAIL (stub — provide org public key)'}",
        f"  Chain position: {'PASS' if result.chain_intact else 'FAIL'}",
        f"  PPP triplet:    {'PASS' if result.ppp_triplet_present else 'FAIL — incomplete PPP'}",
        "",
        "CONTENT SUMMARY",
        f"  Inference time: {_fmt_ns(data.get('timestamp_ns', 0))}",
        f"  Model:          {data.get('model_id', 'unspecified')}",
        f"  PPP Provenance: {data.get('ppp_triplet', {}).get('provenance', '')}",
        f"  PPP Place:      {data.get('ppp_triplet', {}).get('place', '')}",
        f"  PPP Purpose:    {data.get('ppp_triplet', {}).get('purpose', '')}",
        "",
    ]

    delta_chain = data.get("human_delta_chain", {})
    deltas = delta_chain.get("deltas", [])
    foi = delta_chain.get("foi_escalation")

    report_lines += [
        "HUMAN OVERSIGHT",
        f"  Delta chain:    {len(deltas)} delta(s) recorded",
    ]
    for d in deltas:
        report_lines.append(
            f"  Delta {d['sequence']}:       "
            f"{d['actor']['name']} ({d['actor']['role']}) — {d['action_label']}"
        )
    if foi:
        report_lines.append(
            f"  FOI:            {foi['actor']['name']} ({foi['actor']['title']}) — {foi['decision']}"
        )
    else:
        report_lines.append("  FOI escalation: None")

    report_lines += [
        "",
        f"VERDICT: {'AUTHENTIC — TAMPER-FREE' if result.passed else 'VERIFICATION ISSUES — SEE ERRORS'}",
    ]
    if result.errors:
        report_lines.append("\nERRORS:")
        for e in result.errors:
            report_lines.append(f"  - {e}")

    (out / "verification_report.txt").write_text("\n".join(report_lines))

    # PPP summary
    if include_ppp_summary:
        ppp_summary = {
            "record_id": record_id,
            "timestamp_ns": data.get("timestamp_ns"),
            "ppp_triplet": data.get("ppp_triplet", {}),
        }
        (out / "ppp_summary.json").write_text(json.dumps(ppp_summary, indent=2, default=str))

    # Delta summary
    if include_delta_summary:
        delta_summary = {
            "record_id": record_id,
            "autonomous": delta_chain.get("autonomous", True),
            "terminal_node": delta_chain.get("terminal_node"),
            "resolution": delta_chain.get("resolution"),
            "deltas": deltas,
            "foi_escalation": foi,
        }
        (out / "delta_summary.json").write_text(
            json.dumps(delta_summary, indent=2, default=str)
        )

    # Independent verification instructions
    instructions = """
INDEPENDENT VERIFICATION INSTRUCTIONS
======================================
Any party with standard cryptographic tooling can verify this record
without access to any proprietary systems.

Step 1 — Recompute the BLAKE3 hash:
  Extract payload (all fields except merkle_hash and signature)
  Run: b3sum <payload_file>
  Compare to merkle_hash in the record — must match exactly.

  Fallback if BLAKE3 unavailable: BLAKE2b-256 (hashlib.blake2b, digest_size=32)

Step 2 — Verify the Ed25519 signature:
  Obtain the organization's AgDR public key (provided separately)
  Run: openssl dgst -verify pubkey.pem -signature <sig_bytes> <payload_file>
  Expected output: Verified OK

Step 3 — Verify chain position:
  Each record contains prev_merkle_hash
  record[n].merkle_hash must equal record[n+1].prev_merkle_hash
  Any break in this chain indicates a gap or insertion.

These three steps provide cryptographic proof of:
  - Record integrity (not modified since capture)
  - Record authenticity (signed at the inference instant)
  - Chain completeness (no records deleted or inserted)

No AgDR tools or software are required to perform these checks.
Standard cryptographic libraries in any jurisdiction are sufficient.

Reference: https://github.com/aiccountability-source/AgDR/blob/main/verification-audit-procedure.md
"""
    (out / "INDEPENDENT_VERIFICATION.txt").write_text(instructions.strip())

    return out


def _fmt_ns(timestamp_ns: int) -> str:
    if not timestamp_ns:
        return "unknown"
    ts = timestamp_ns / 1e9
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
