# GroundTruth AI website

Static, business-case-led website served by GitHub Pages from `main` (repository root).
Pages are **generated** from structured content by a stdlib-only Python build. Do not edit the generated HTML by hand.

## Build and verify

```bash
python3 tools/build.py     # writes index.html, business-cases/, industries/, … into the repo root
python3 tools/verify.py    # must print OK before any push
python3 -m http.server 8765  # preview at http://127.0.0.1:8765
```

`verify.py` checks internal links and anchors, a single `h1` and heading order, ARIA references, form labels,
CSP compliance (no inline styles or scripts), colour-token contrast (WCAG AA) in light and dark themes, content schema and
filter vocabularies, the business-case ↔ industry mapping, the acceptance criteria (navigation, homepage order,
per-case sections, pilot and ROI links), and claim hygiene (banned superlatives, unqualified "real-time" or anonymization statements).

## Where content lives

| What | File |
|---|---|
| Editorial rules, verified facts, evidence vocabulary, fixed priorities | `tools/CONTENT_BRIEF.md` |
| One file per business case (schema documented in BC01) | `tools/content/cases/bc*.py` |
| Industries and their case relevance | `tools/content/industries.py` |
| Navigation, filter vocabularies, benchmarks, contact address | `tools/content/site.py` |
| Home, Platform, Technology, Evidence, ROI, Partners, Company, Pilot pages | `tools/sitegen/pages_main.py` |
| Architecture diagram renderer (DSL → SVG) and homepage visuals | `tools/sitegen/diagrams.py` |
| Styles / scripts | `assets/css/site.css`, `assets/js/*.js` |

To add a business case, copy `bc01_ot_it.py`, keep every key, use only vocabulary keys from `site.py`, add the case to the
relevant industries in `industries.py`, then build and verify.

## Security

Every page sets a strict Content-Security-Policy (`default-src 'self'`, no inline code, no third-party requests; fonts are self-hosted).
Forms send nothing to any server: the pilot form opens a pre-filled email or prepares a copyable request; the ROI calculator runs in the browser.

## Release blockers

- `CONTACT_EMAIL` in `tools/content/site.py` is empty until an official company mailbox is approved. `verify.py` warns about it.

## Internal documents

`internal/` holds `BUSINESS_CASES.md`, `BUSINESS_CASE_PRIORITIZATION.md`, `SALES_PLAYBOOK.md` and `BUSINESS_CASE_EVIDENCE_MATRIX.md`.
It is **git-ignored on purpose**: this repository is public and published by GitHub Pages. Keep those files in a private location.

## Legacy URLs

Old template pages (`distillation.html`, `data-drift.html`, …) are now redirects. The previous homepage deck lives at
`/resources/smart-data-savings/`.
