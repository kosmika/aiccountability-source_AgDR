# Google Drive Setup Guide — AAI Project Manager Central

This guide explains how to organize the Google Drive **AAI** folder as a project manager hub
for Accountability.ai / AgDR.

---

## Recommended Drive Folder Structure

```
📁 AAI/  ← Top-level shared drive folder
│
├── 📄 HUB.md (or HUB.gdoc)             ← START HERE — master navigation hub
├── 📄 DRIVE-SETUP.md                   ← This file
│
├── 📁 01 - Spec & Artifacts/
│   ├── 📄 agdr-v0.2.json               ← Canonical spec (machine-readable)
│   ├── 📄 INDEX.md                     ← Index of all GitHub artifacts
│   ├── 📁 Markdown Source/             ← .md source for all spec pages
│   └── 📁 HTML Pages/                  ← Rendered HTML versions
│
├── 📁 02 - Public Resources/
│   ├── 📄 accountability-ai-resources.md  ← This repo: public resources doc
│   ├── 📁 Regulatory Frameworks/
│   └── 📁 Research & References/
│
├── 📁 03 - Project Docs/
│   ├── 📄 ROADMAP.md                   ← Product/spec roadmap
│   ├── 📄 NOTES.md                     ← Working notes
│   ├── 📁 Founding/                    ← Founding partner materials
│   └── 📁 Legal/                       ← License files, legal docs
│
├── 📁 04 - Outreach & Communications/
│   ├── 📁 Email Templates/
│   └── 📁 Press & Media/
│
└── 📁 99 - Archive/
    └── [older versions, deprecated docs]
```

---

## Step-by-Step Drive Setup

### Step 1: Create the AAI folder
1. Go to Google Drive
2. Create a new folder named **AAI**
3. (Optional) Right-click → Add to Starred for quick access

### Step 2: Upload GitHub artifacts
**Option A — Manual upload:**
1. Go to https://github.com/aiccountability-source/AgDR
2. Click **Code → Download ZIP**
3. Extract the ZIP
4. Upload all files to `AAI/01 - Spec & Artifacts/`

**Option B — Direct file links (right-click → Save As):**
```
https://raw.githubusercontent.com/aiccountability-source/AgDR/main/specs/agdr-v0.2.json
https://raw.githubusercontent.com/aiccountability-source/AgDR/main/README.md
https://raw.githubusercontent.com/aiccountability-source/AgDR/main/CHANGELOG.md
```

**Option C — Rclone sync (automated):**
```bash
# Install rclone and configure Google Drive remote named "gdrive"
# Then sync the repo to Drive:
git clone https://github.com/aiccountability-source/AgDR.git /tmp/AgDR
rclone copy /tmp/AgDR "gdrive:AAI/01 - Spec & Artifacts" \
  --include "*.md" \
  --include "*.html" \
  --include "*.json" \
  --progress
```

### Step 3: Upload the AAI hub files (from this repo)
Upload the entire `AAI/` folder from this repository to Google Drive `AAI/`.

### Step 4: Convert HUB.md to a Google Doc (recommended)
1. Upload `HUB.md` to Drive
2. Right-click → **Open with Google Docs**
3. File → **Save as Google Docs**
4. This makes it fully editable and linkable within Drive

### Step 5: Set sharing & access
For team access:
1. Right-click `AAI/` → **Share**
2. Add team members with appropriate access levels:
   - **Editor** — core team
   - **Commenter** — reviewers
   - **Viewer** — stakeholders / read-only
3. For public reference pages, use **Anyone with the link → Viewer**

### Step 6: Pin the hub
1. Right-click `HUB.md` (or `HUB.gdoc`) → **Add shortcut to Drive**
2. Place shortcut in **My Drive** root for instant access
3. Or add to a shared **Workspace** in Google Drive

---

## Keeping Artifacts in Sync

### Manual sync cadence (recommended: weekly or on spec updates)
1. Check https://github.com/aiccountability-source/AgDR/commits/main for new commits
2. Download updated files
3. Replace in `AAI/01 - Spec & Artifacts/`

### Automated sync via GitHub Actions (advanced)
The existing `.github/workflows/convert.yml` auto-publishes HTML to GitHub.
To also sync to Drive, add a step using the `google-github-actions/upload-cloud-storage` action
or `rclone` with a service account credential.

---

## Quick Access Links (bookmark these)

| Resource | URL |
|---|---|
| accountability.ai | https://accountability.ai |
| Live Sandbox | https://accountability.ai/sandbox.html |
| GitHub Repo | https://github.com/aiccountability-source/AgDR |
| Canonical Spec JSON | https://raw.githubusercontent.com/aiccountability-source/agdr-spec/main/specs/agdr-v0.2.json |
| Download ZIP | https://github.com/aiccountability-source/AgDR/archive/refs/heads/main.zip |
| Contact | admin@accountability.ai |
| Founding | founding@accountability.ai |

---

## Drive Naming Conventions

| Prefix | Meaning |
|---|---|
| `01 -` `02 -` ... | Ordered top-level folders |
| `[DRAFT]` | Work in progress, not finalized |
| `[ARCHIVED]` | Superseded, kept for reference |
| `v0.2_` prefix | Version-tagged copies of spec files |

---

*This guide is part of the AAI project hub.*
*Source: https://github.com/aiccountability-source/AgDR/tree/main/AAI*
