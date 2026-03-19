# PPP Industry Templates

**AgDR v0.2 — Sector-Specific PPP Triplet Definitions**
Published March 2026

---

## How to Use These Templates

PPP is **meaning of the beholder**. These templates are starting points — not requirements. Copy the template for your sector, fill in your organization's specific context, and capture it verbatim in every AgDR record.

The standard only requires that your definition is:
1. Written down before the agent acts
2. Captured atomically at every inference instant
3. Honest — it reflects what you actually believe

---

## Template 1 — Capital Markets & Trading

**Sector:** Investment dealers, asset managers, trading desks, algorithmic trading systems
**Relevant law:** IIROC Rules, CBCA s.122, OSC regulations, Securities Act (Ontario)

```json
{
  "ppp_triplet": {
    "provenance": "TSX equity desk — {symbol} {order_type} order — authorized trader {name}, employee {id} — acting under client mandate {mandate_ref} — verified account standing as of {timestamp}",
    "place": "Execute within {slippage_bps}bps of VWAP, comply with IIROC best-execution obligation, remain within intraday risk limit {risk_limit}, settlement T+2, jurisdictional boundary: Canada",
    "purpose": "Rebalance portfolio to target allocation per mandate {mandate_ref} — acting honestly and in good faith in the best interests of the client under CBCA s.122 and common law fiduciary duty"
  }
}
```

**FOI designation for this sector:** Chief Compliance Officer or Head of Risk
**Escalation triggers:** Order exceeds authorized size, risk limit breach, unusual market conditions, client dispute flag

---

## Template 2 — Healthcare & Clinical Decision Support

**Sector:** Hospitals, clinical AI systems, diagnostic tools, treatment recommendation engines
**Relevant law:** PHIPA (Ontario), PIPEDA, College of Physicians standards, duty of care

```json
{
  "ppp_triplet": {
    "provenance": "Clinical decision support — patient {anonymized_id} — attending physician {name}, license {license_no} — AI system {model_id} v{version} — patient consent on file — operating under {institution} clinical AI policy v{policy_ver}",
    "place": "Recommendation only — final clinical judgment reserved for licensed practitioner — no autonomous action on patient — comply with PHIPA data residency: Ontario — outcome target: {clinical_objective}",
    "purpose": "Support evidence-based clinical decision-making in the best interests of the patient — acting with the care, diligence, and skill expected of a competent practitioner — recommendation to be reviewed and confirmed by attending physician before any action"
  }
}
```

**FOI designation for this sector:** Chief Medical Officer or Medical Director
**Escalation triggers:** High-severity diagnosis, recommendation conflicts with attending judgment, patient safety flag, consent ambiguity

---

## Template 3 — Government & Public Administration

**Sector:** Federal/provincial agencies, automated benefit adjudication, regulatory enforcement
**Relevant law:** Treasury Board Directive on Automated Decision-Making, Canadian Human Rights Act, Privacy Act, ATIA

```json
{
  "ppp_triplet": {
    "provenance": "Automated decision system — {agency} — application {ref_no} — applicant identity verified via {auth_method} — authorized decision-maker {name}, position {title} — system operating under Treasury Board AIA Level {level} authorization",
    "place": "Adjudicate within {program_name} eligibility criteria — comply with Canadian Human Rights Act (no discrimination on prohibited grounds) — preserve right of human review under Directive s.6.3 — jurisdictional boundary: Canada",
    "purpose": "Deliver timely, consistent, and fair public administration in the public interest — acting transparently, accountably, and in accordance with the rule of law — applicant retains right to reconsideration by a human decision-maker"
  }
}
```

**FOI designation for this sector:** Deputy Minister delegate or Director General
**Escalation triggers:** Protected ground flag (race, gender, disability, etc.), novel legal question, public interest concern, media risk flag, threshold confidence below {value}

---

## Template 4 — Legal & Document Generation

**Sector:** Legal tech, AI-drafted contracts, regulatory filings, court documents
**Relevant law:** Law Society rules, solicitor-client privilege, Rules of Professional Conduct, court rules

```json
{
  "ppp_triplet": {
    "provenance": "Legal document generation — matter {matter_id} — instructing lawyer {name}, LSO #{license_no} — client {client_id} — AI system {model_id} — instructions provided {timestamp} — acting under retainer {retainer_ref}",
    "place": "Draft only — no filing, execution, or delivery without lawyer review and sign-off — comply with applicable court rules and Rules of Professional Conduct — jurisdictional boundary: {jurisdiction}",
    "purpose": "Advance the client's lawful legal interests as instructed — subject to overriding duty to the court and the rule of law — lawyer retains full professional responsibility for any document bearing their name or filed in their capacity"
  }
}
```

**FOI designation for this sector:** Managing Partner or General Counsel
**Escalation triggers:** Novel legal argument, conflict of interest flag, privilege concern, cross-border jurisdiction, court deadline risk

---

## Template 5 — Financial Services & Credit

**Sector:** Banks, credit unions, insurance underwriters, mortgage originators
**Relevant law:** OSFI guidelines, Bank Act, FCAC regulations, anti-discrimination law

```json
{
  "ppp_triplet": {
    "provenance": "Credit adjudication system — application {app_id} — applicant {anonymized_id} — product {product_name} — institution {institution_name} — adjudicator {name}, role {title} — operating under credit policy version {policy_ver} — OSFI guidelines compliant",
    "place": "Adjudicate within approved credit policy — comply with FCAC consumer protection obligations — no discrimination on prohibited grounds under Canadian Human Rights Act — outcome: approve / decline / refer — applicant retains right to human review",
    "purpose": "Extend credit responsibly in accordance with sound lending principles and regulatory obligations — acting in the long-term interests of both the institution and the customer — decision is explainable and the applicant may request reasons"
  }
}
```

**FOI designation for this sector:** Chief Risk Officer
**Escalation triggers:** Protected ground proximity, appeal flag, novel product, systemic bias alert, regulatory threshold

---

## Template 6 — Critical Infrastructure & Operations

**Sector:** Energy grids, water systems, transportation, industrial control systems
**Relevant law:** Critical Infrastructure Protection, provincial safety acts, CSA standards

```json
{
  "ppp_triplet": {
    "provenance": "Operational control system — facility {facility_id} — control action {action_type} — authorized operator {name}, certification {cert_id} — system {system_id} v{version} — baseline state verified at {timestamp} — operating under {safety_standard}",
    "place": "Execute within {operational_boundary} — maintain safety margins per {safety_standard} section {section} — no action that creates irreversible system state without human confirmation — jurisdictional authority: {regulator}",
    "purpose": "Maintain safe, reliable, and continuous operation of critical infrastructure in the public interest — human safety is the overriding priority — any action affecting public safety requires human confirmation before execution"
  }
}
```

**FOI designation for this sector:** Chief Operating Officer or licensed Control Room Supervisor
**Escalation triggers:** Safety margin breach, irreversible action, public impact threshold, novel failure mode, regulatory notification required

---

## How to Extend These Templates

These templates are starting points. Every organization should:

1. **Customize** — replace `{placeholders}` with your specific values
2. **Version** — maintain a version history of your PPP definitions as policy changes
3. **Register** — store the authoritative PPP definition document as an AgDR record itself
4. **Train** — ensure every person in the human delta chain understands what PPP means for your organization
5. **Audit** — periodically review whether captured PPP values match the definitions

The "meaning of the beholder" principle does not mean PPP is vague. It means PPP is *yours to define precisely* — and then to be held to.

---

*Part of the AgDR v0.2 foundational standard*
Canonical source: https://github.com/aiccountability-source/AgDR
