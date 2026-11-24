#!/usr/bin/env python3
"""Build the GroundTruth AI website from tools/content into the repository root.

Usage:  python3 tools/build.py        (stdlib only; no dependencies)
Then:   python3 tools/verify.py       (links, accessibility, integrity and claim checks)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from content import site as S                      # noqa: E402
from content.industries import INDUSTRIES          # noqa: E402
from sitegen import core                           # noqa: E402
from sitegen.pages_cases import load_cases, render_case, render_explorer   # noqa: E402
from sitegen.pages_industries import render_industry, render_industries_index  # noqa: E402
from sitegen import pages_main as M                # noqa: E402


def main():
    cases = load_cases()
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids)) == 11, f"expected 11 unique business cases, got {ids}"

    M.render_home(cases, INDUSTRIES)
    render_explorer(cases, INDUSTRIES)
    for c in cases:
        render_case(c, cases, INDUSTRIES)
    render_industries_index(cases, INDUSTRIES)
    for i in INDUSTRIES:
        render_industry(i, cases, INDUSTRIES)
    M.render_platform(cases)
    M.render_technology(cases)
    M.render_evidence(cases)
    M.render_roi(cases)
    M.render_partners(cases)
    M.render_company(cases)
    M.render_pilot(cases, INDUSTRIES)
    M.render_404(cases)
    M.render_legacy()

    urls = [(p, pr) for p, pr in core.PAGES if pr]
    urls.append(("/resources/smart-data-savings/", "0.3"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{S.BASE_URL}{p}</loc><priority>{pr}</priority></url>" for p, pr in urls]
    sm.append("</urlset>")
    core.write("/sitemap.xml", "\n".join(sm) + "\n")
    core.write("/robots.txt", f"User-agent: *\nDisallow: /tools/\nSitemap: {S.BASE_URL}/sitemap.xml\n")
    core.write("/.nojekyll", "")
    print(f"Built {len(core.PAGES)} pages, {len(M.LEGACY)} legacy redirects, sitemap with {len(urls)} URLs.")


if __name__ == "__main__":
    main()
