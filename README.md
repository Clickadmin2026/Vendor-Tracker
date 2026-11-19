# Vendor & Partner Tracker

Static, filterable vendor/partner portal (no build step). Data lives in `data/vendors.json`.

## Run locally
    python3 -m http.server 8000   # then open http://localhost:8000

## Deploy
Push to `main`; enable **Settings → Pages → Source: GitHub Actions**. The included workflow publishes it.

## Data
- `data/vendors.json` is generated from the original Excel (`scripts/extract_xlsx.py` then `scripts/normalize.py`; adjust the paths at the top).
- Going forward, edit the JSON in PRs (git history = audit trail for Tier / verification changes).
- In-page edits are saved to the viewer's browser only (localStorage). "Copy edits (JSON)" exports them to merge.

## Roadmap
1. Shared editing: Supabase/Firebase or a small API behind the same UI.
2. SSO (Entra/Okta) in front of the page: it contains partner IDs and contacts, keep the repo private.
3. Per-vendor tabs from the xlsx (A10, Check Point, Cisco...) and OEM letter attachments per vendor.
4. Verification expiry alerts (certs, tier renewals).
