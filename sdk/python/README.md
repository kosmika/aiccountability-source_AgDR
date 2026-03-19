# agdr-aki — AgDR v0.2 Python SDK

**Atomic Kernel Inference (AKI) reference implementation**

The Python SDK for the AgDR v0.2 standard. One call wraps your inference and produces a tamper-evident, court-ready record.

## Install

```bash
pip install agdr-aki
# With full cryptographic support:
pip install agdr-aki[crypto]
```

## Quickstart

```python
from agdr_aki import aki_capture

record = aki_capture(
    ctx={"system": "my-agent", "operator": "acme-corp"},
    reasoning_trace=output.reasoning_trace,
    output=output.decision,
    ppp_triplet={
        "provenance": "Who is acting, from what state",
        "place":      "Where this decision is headed",
        "purpose":    "Why this decision is being made"
    },
    human_delta_chain=[]
)

print(record.merkle_hash)   # cryptographic proof
print(record.committed)     # always True
```

## License

CC0 1.0 Universal OR Apache License 2.0 — your choice.

## Canonical source

https://github.com/aiccountability-source/AgDR
