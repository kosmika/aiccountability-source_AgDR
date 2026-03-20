# GitHub Artifacts Index

**Repository:** https://github.com/aiccountability-source/AgDR
**Branch:** main
**Last synced:** March 2026

This folder contains documentation and supporting artifacts from the AgDR GitHub repository.

---

## Core Specification

> **The canonical, buildable AgDR v0.2 spec lives in [`specs/agdr-v0.2.json`](https://github.com/aiccountability-source/AgDR/blob/main/specs/agdr-v0.2.json).**
> > It includes the full JSON Schemas (PPP Triplet, Human Delta Chain, AgDR Record) required to implement the standard.
> >
> > **Quick install:**
> > ```bash
> > curl -O https://raw.githubusercontent.com/aiccountability-source/AgDR/main/specs/agdr-v0.2.json
> > ```
> >
> > ---
> >
> > ## Documentation Pages (Markdown Source)
> >
> > | File | Title | Live URL |
> > |---|---|---|
> > | README.md | AgDR Specification v0.2 | — |
> > | CHANGELOG.md | Changelog | — |
> > | aki-formal-definition.md | AKI Formal Definition | https://accountability.ai/aki-formal-definition.html |
> > | ppp-pillars.md | PPP Pillars | https://accountability.ai/ppp-pillars.html |
> > | ppp-legal-compliance.md | PPP Legal Compliance | https://accountability.ai/ppp-legal-compliance.html |
> > | ppp-export-control.md | PPP Export Control | https://accountability.ai/ppp-export-control.html |
> > | cbca-fiduciary-mapping.md | CBCA Fiduciary Mapping | https://accountability.ai/cbca-fiduciary-mapping.html |
> > | cbsa-mapping.md | CBSA Mapping | https://accountability.ai/cbsa-mapping.html |
> > | comparison-aviation-black-box.md | Aviation Black Box Comparison | https://accountability.ai/comparison-aviation-black-box.html |
> > | comparison-medical-records.md | Medical Records Comparison | https://accountability.ai/comparison-medical-records.html |
> > | agi-court-precedents.md | AGI Court Precedents | https://accountability.ai/agi-court-precedents.html |
> > | future-agi-court.md | Future AGI Court (2076) | https://accountability.ai/future-agi-court.html |
> > | technical-details.md | Technical Details | https://accountability.ai/technical-details.html |
> > | technical-note-coherence.md | Technical Note on Coherence | https://accountability.ai/technical-note-coherence.html |
> > | tsx-stress-test.md | TSX Stress Test | https://accountability.ai/tsx-stress-test.html |
> > | getting-started.md | Getting Started | https://accountability.ai/getting-started.html |
> >
> > ---
> >
> > ## Supporting Files
> >
> > | File | Description |
> > |---|---|
> > | LICENSE | Dual license notice |
> > | LICENSE-CC0 | CC0 1.0 Universal full text |
> > | LICENSE-UPDATE.md | License update notes |
> > | Apache | Apache 2.0 license text |
> > | robots.txt | Search engine directives |
> > | sitemap.xml | Site sitemap |
> > | Llms.txt | LLM instructions |
> > | CANADA | Canada-specific context |
> >
> > ---
> >
> > ## GitHub Actions Workflow
> >
> > | File | Description |
> > |---|---|
> > | `.github/workflows/convert.yml` | Auto-converts MD → HTML and generates sitemap on push to main |
> >
> > **Workflow does:**
> > 1. Converts all `*.md` files → `*.html` via Pandoc
> > 2. 2. Regenerates `sitemap.xml`
> >    3. 3. Commits and pushes back to `main` (tagged `[skip ci]`)
> >      
> >       4. ---
> >      
> >       5. ## Additional Documents (repo root)
> >      
> >       6. | File | Description |
> > |---|---|
> > | `AKI Capture explanation` | Plain-language AKI capture explanation |
> > | `Deep Explanation of the PPP Triplet in AgDR v0.2` | Deep-dive on PPP |
> >
> > ---
> >
> > ## How to Sync This Folder
> >
> > To update this folder with latest GitHub artifacts:
> >
> > ```bash
> > # Clone or pull the repo
> > git clone https://github.com/aiccountability-source/AgDR.git
> > # or
> > git pull origin main
> >
> > # Copy key files to Drive
> > cp AgDR/specs/agdr-v0.2.json ./agdr-v0.2.json
> > cp AgDR/*.md ./
> > ```
> >
> > Or use GitHub's "Download ZIP" from:
> > https://github.com/aiccountability-source/AgDR/archive/refs/heads/main.zip
