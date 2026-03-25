from agdr_aki import aki_capture
import json

# Load the official spec (already in the repo)
with open("specs/agdr-v0.2.json") as f:
      spec = json.load(f)

print("🔥 AgDR Virtual Engine ready!")
print("Core guarantee:", spec["core_guarantee"]["formal_definition"])

# Example capture (replace with your real inference)
record = aki_capture(
      ctx={
                "provenance": "your-app-v1",
                "place": "canada",
                "purpose": "regulatory-compliance"
      },
      reasoning_trace="User asked X → Model output Y",
      output={"answer": "42"},
      ppp_triplet={
                "provenance": "your-app-v1",
                "place": "canada",
                "purpose": "regulatory-compliance"
      },
      human_delta_chain=[]
)

print("✅ Tamper-evident record created:", record["record_id"])
print("Run `agdr verify --record ...` to verify it")
