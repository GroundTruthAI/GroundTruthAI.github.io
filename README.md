# GroundTruth AI website

Static, business-case-led website served by GitHub Pages from `main` (repository root).
Pages are **generated** from structured content by a stdlib-only Python build. Do not edit the generated HTML by hand.

## Build and verify

```bash
python3 tools/build.py     # writes index.html, business-cases/, industries/, … into the repo root
python3 tools/verify.py    # must print OK before any push
node tools/test_math.js    # simulator and ROI formula tests
python3 tools/build_pdf.py  # regenerate the executive-brief PDFs (needs Chrome) after changing the presentation
python3 -m http.server 8765  # preview at http://127.0.0.1:8765
```

`verify.py` checks internal links and anchors, a single `h1` and heading order, ARIA references, form labels,
CSP compliance (no inline styles or scripts), colour-token contrast (WCAG AA), content schema and
filter vocabularies, the business-case ↔ industry mapping, the acceptance criteria (navigation, homepage order,
per-case sections in the required order, labelled illustrative scenarios, solution-family coverage, simulator), claim hygiene
(banned superlatives, retired legacy claims, unqualified "real-time" or anonymization statements) and that no internal
case ID (`BC01`…) is visible to visitors. IDs stay in URLs and content files only.

## Where content lives

| What | File |
|---|---|
| Editorial rules, verified facts, evidence vocabulary, fixed priorities | `tools/CONTENT_BRIEF.md` |
| One file per business case (schema documented in BC01) | `tools/content/cases/bc*.py` |
| Industries and their case relevance | `tools/content/industries.py` |
| Navigation, solution families (`PILLARS`), engagement stages, ROI presets, filter vocabularies, benchmarks, contact | `tools/content/site.py` |
| Home, Platform, Technology, Evidence (+ validation roadmap), ROI, Simulator, Partners, Company, engagement form | `tools/sitegen/pages_main.py` |
| Solution-family pages (`/solutions/…`) | `tools/sitegen/pages_pillars.py` |
| Architecture diagram renderer (DSL → SVG) and homepage visuals | `tools/sitegen/diagrams.py` |
| Styles / scripts | `assets/css/site.css`, `assets/js/*.js` |

To add a business case, copy `bc01_ot_it.py`, keep every key, use only vocabulary keys from `site.py`, add the case to the
relevant industries in `industries.py` and to exactly one solution family in `site.py` → `PILLARS`, then build and verify.
Every case carries an illustrative `scenario`; it must never describe a real customer.

## Security

Every page sets a strict Content-Security-Policy (`default-src 'self'`, no inline code; fonts are self-hosted).
The only third-party request is the engagement form on `/pilot/`, which posts to FormSubmit (`connect-src` is opened for
that origin on that page only); it falls back to a pre-filled email if delivery is not confirmed. The ROI calculator and
the simulator run entirely in the browser.

## Executive brief

`/resources/executive-brief/` (English) and `es.html` (Spanish) are seven-slide presentations generated from
`tools/sitegen/pages_brief.py` with `assets/css/brief.css` and `assets/js/brief.js`. The downloadable PDFs in the same
folder are printed from those same pages by `tools/build_pdf.py` (headless Chrome, one 13.333 × 7.5 in page per slide,
vector text and links, metadata added). `build.py` never deletes them; `verify.py` checks the slide count, matching PDF page count and 16:9 size,
and warns when a PDF is older than the presentation source.

## Release notes

- The form delivers to `CONTACT_EMAIL` in `tools/content/site.py`. Replace it with a corporate address (or FormSubmit's
  random alias) when one is approved; FormSubmit requires a one-time activation from that mailbox.
- `BASE_URL` drives canonical URLs, Open Graph, the sitemap and robots; change it for a custom domain.

## Internal documents

`internal/` holds the commercial and QA documents (business cases, prioritization, sales playbook, evidence matrix,
commercial refinement, scenarios, claims registry, validation roadmap, company information requirements, deployment
review, website QA) and retired legacy material.
It is **git-ignored on purpose**: this repository is public and published by GitHub Pages. Keep those files in a private location.

## Legacy URLs

Old template pages and earlier benchmark pages (`iris.html`, `mnist.html`, …) are `noindex` redirects defined in
`LEGACY` in `tools/sitegen/pages_main.py`. The retired Smart Data Savings deck URL `/resources/smart-data-savings/`
redirects to `/evidence/`; its claims are superseded.
