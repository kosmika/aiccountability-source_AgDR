"""
agdr_aki — AgDR v0.2 Python SDK
Atomic Kernel Inference (AKI) reference implementation

License: CC0 1.0 Universal OR Apache License 2.0 — your choice
Canonical source: https://github.com/aiccountability-source/AgDR
"""

from .capture import aki_capture, AgDRRecord
from .delta import HumanDelta, FOIEscalation
from .verify import verify_record, verify_chain, VerificationResult, ChainVerificationResult
from .evidence import package_evidence

__version__ = "0.2.0"
__all__ = [
    "aki_capture",
    "AgDRRecord",
    "HumanDelta",
    "FOIEscalation",
    "verify_record",
    "verify_chain",
    "VerificationResult",
    "ChainVerificationResult",
    "package_evidence",
]
