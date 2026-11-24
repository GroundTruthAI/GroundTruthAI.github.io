#!/usr/bin/env python3
"""Verify the built site: links, accessibility basics, CSP compliance, content integrity,
claim hygiene and the business-case acceptance criteria. Exit code 1 on any error.

Usage: python3 tools/build.py && python3 tools/verify.py
"""
import glob
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from content import site as S                  # noqa: E402
from content.industries import INDUSTRIES      # noqa: E402
from sitegen.pages_cases import load_cases     # noqa: E402
from sitegen.pages_main import LEGACY as LEGACY_MAP  # noqa: E402

errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)

SKIP_DIRS = ("tools", "internal", "resources", ".git", "_dbg")
LEGACY = set(LEGACY_MAP)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.headings, self.refs = [], [], [], []
        self.labels_for, self.controls, self.imgs = set(), [], []
        self.inline_style = self.inline_script = self.style_tag = False
        self.title = self.desc = self.lang = None
        self.in_title = False
        self.label_depth = 0
        self.text = []
        self._skip = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if "id" in a: self.ids.append(a["id"])
        if "style" in a: self.inline_style = True
        if tag == "style": self.style_tag = True
        if tag == "script":
            if not a.get("src"): self.inline_script = True
            self._skip += 1
        if tag == "html": self.lang = a.get("lang")
        if tag == "title": self.in_title = True
        if tag == "meta" and a.get("name") == "description": self.desc = a.get("content")
        for k in ("href", "src"):
            if k in a and tag != "link" or (tag == "link" and k == "href" and a.get("rel") in ("stylesheet", "icon", "preload")):
                if k in a: self.links.append(a[k])
        if re.fullmatch(r"h[1-6]", tag): self.headings.append(int(tag[1]))
        for k in ("aria-labelledby", "aria-describedby", "aria-controls"):
            if k in a: self.refs.extend((k, x) for x in a[k].split())
        if tag == "label":
            self.label_depth += 1
            if "for" in a: self.labels_for.add(a["for"])
        if tag in ("input", "select", "textarea") and a.get("type") != "hidden":
            self.controls.append((a.get("id"), self.label_depth > 0, a.get("aria-label")))
        if tag == "img": self.imgs.append(a.get("alt"))

    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "label": self.label_depth -= 1
        if tag == "script": self._skip -= 1

    def handle_data(self, d):
        if self.in_title: self.title = (self.title or "") + d
        if not self._skip: self.text.append(d)


def built_pages():
    out = []
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in SKIP_DIRS or rel in LEGACY: continue
        out.append(rel)
    return sorted(out)


def url_for(rel):
    return "/" + (rel[:-10] if rel.endswith("index.html") else rel)


def resolve(href):
    p = urlparse(href).path
    f = os.path.join(ROOT, p.lstrip("/"))
    if p.endswith("/"): f = os.path.join(f, "index.html")
    return f


# ----------------------------------------------------------------------------- parse
pages = {}
for rel in built_pages():
    p = Page()
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        p.feed(fh.read())
    pages[rel] = p
by_url = {url_for(r): p for r, p in pages.items()}

# ----------------------------------------------------------------------------- per-page checks
for rel, p in pages.items():
    where = url_for(rel)
    if p.lang not in ("en", "es"): err(f"{where}: missing lang")
    if not p.title: err(f"{where}: missing <title>")
    if not p.desc and rel != "404.html": err(f"{where}: missing meta description")
    if p.inline_style or p.style_tag: err(f"{where}: inline style violates CSP")
    if p.inline_script: err(f"{where}: inline script violates CSP")
    if p.headings.count(1) != 1: err(f"{where}: expected exactly one h1, found {p.headings.count(1)}")
    for a, b in zip(p.headings, p.headings[1:]):
        if b > a + 1: err(f"{where}: heading level skips h{a} → h{b}"); break
    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup: err(f"{where}: duplicate ids {sorted(dup)[:5]}")
    for k, ref in p.refs:
        if ref not in p.ids: err(f"{where}: {k} → missing id '{ref}'")
    for cid, wrapped, al in p.controls:
        if not (wrapped or al or (cid and cid in p.labels_for)): err(f"{where}: form control '{cid}' has no label")
    if any(a is None for a in p.imgs): err(f"{where}: <img> without alt")
    for href in p.links:
        if href.startswith(("http://", "https://", "mailto:", "data:")):
            if href.startswith("http://"): warn(f"{where}: insecure link {href}")
            continue
        if href.startswith("#"):
            if href[1:] and href[1:] not in p.ids: err(f"{where}: broken anchor {href}")
            continue
        if not href.startswith("/"):
            err(f"{where}: relative link {href} (use root-absolute paths)"); continue
        f = resolve(href)
        if not os.path.exists(f): err(f"{where}: broken link {href}"); continue
        frag = urlparse(href).fragment
        tgt = by_url.get(urlparse(href).path)
        if frag and tgt and frag not in tgt.ids: err(f"{where}: broken anchor {href}")

# ----------------------------------------------------------------------------- content integrity
cases = load_cases()
ref_keys = list(cases[0].keys())
vocab = {d: {k for k, _ in v[1]} for d, v in S.FILTERS.items()}
ind_slugs = [i["slug"] for i in INDUSTRIES]
case_ids = {c["id"] for c in cases}
if [c["rank"] for c in cases] != list(range(1, 12)): err("ranks are not 1..11")
flag = [c["id"] for c in cases if c["tier"] == "flagship"]
if flag != ["BC01", "BC02", "BC03", "BC04"]: err(f"flagship set/order wrong: {flag}")
for c in cases:
    cid = c["id"]
    if list(c.keys()) != ref_keys: err(f"{cid}: keys differ from schema")
    for d, vals in c["filters"].items():
        bad = set(vals) - vocab[d]
        if bad: err(f"{cid}: unknown {d} {bad}")
    for s in c["industries"]:
        if s not in ind_slugs: err(f"{cid}: unknown industry {s}")
    if c["roi_scenario"] not in S.ROI_SCENARIOS: err(f"{cid}: unknown roi scenario")
    for r in c["related"]:
        if r not in case_ids: err(f"{cid}: unknown related {r}")
    for k in ("current", "proposed"):
        dg = c["architecture"][k]
        ids = {n[0] for z in dg["zones"] for n in z["nodes"]}
        for f in dg["flows"]:
            if f[0] not in ids or f[1] not in ids: err(f"{cid}/{k}: flow endpoint missing {f[:2]}")
            if f[2] not in ("raw", "distilled", "model", "control"): err(f"{cid}/{k}: bad flow kind {f[2]}")
    for n, st, _ in c["implementation"]["integration_points"]:
        if st not in ("verified", "proposed", "customer"): err(f"{cid}: bad integration status {st}")
    if "not yet validated in production" not in c["evidence"]["status"]: err(f"{cid}: evidence status must say not yet validated")
    for k in ("problem", "inputs", "baseline", "method", "technical_criteria", "economic_criteria", "deliverables", "adoption"):
        if not c["pilot"].get(k): err(f"{cid}: pilot missing {k}")
for i in INDUSTRIES:
    expect = sorted(c["id"] for c in cases if i["slug"] in c["industries"])
    got = sorted(x[0] for x in i["cases"])
    if expect != got: err(f"industry {i['slug']}: cases {got} != mapping {expect}")

# ----------------------------------------------------------------------------- acceptance criteria
home = by_url.get("/")
if S.NAV[0][2] != "business-cases": err("Business Cases is not the first primary navigation item")
if home:
    t = " ".join(home.text)
    if "Keep data distributed." not in t: err("home: hero headline missing")
    if "Solve your most critical data challenges" not in t: err("home: flagship section missing")
    for c in cases[:4]:
        if f"/business-cases/{c['slug']}/" not in home.links: err(f"home: flagship {c['id']} not linked")
    hero_pos = t.find("Solve your most critical data challenges")
    tech_pos = t.find("How dataset distillation works")
    if tech_pos != -1 and tech_pos < hero_pos: err("home: technology introduced before business cases")
for c in cases:
    u = f"/business-cases/{c['slug']}/"
    p = by_url.get(u)
    if not p: err(f"missing page {u}"); continue
    order = ("challenge", "opportunity", "solution", "scenario", "architecture", "outcomes", "metrics", "considerations", "evidence", "engage")
    for sid in order + ("pilot",):
        if sid not in p.ids: err(f"{u}: missing section #{sid}")
    pos = [p.ids.index(x) for x in order if x in p.ids]
    if pos != sorted(pos): err(f"{u}: sections out of the required order")
    if f"/pilot/?case={c['id']}" not in p.links: err(f"{u}: no case-specific pilot CTA")
    if f"/roi/?case={c['id']}" not in p.links: err(f"{u}: no ROI scenario link")
    if not any(l.startswith("/industries/") and l != "/industries/" for l in p.links): err(f"{u}: no industry links")
    pt = " ".join(p.text)
    if "Illustrative enterprise scenario" not in pt: err(f"{u}: scenario not labelled as illustrative")
    if "not yet validated in production" not in pt: err(f"{u}: validation status missing")
    pil = S.PILLAR_OF.get(c["id"])
    if not pil: err(f"{c['id']}: not in a solution family")
    elif f"/solutions/{pil['slug']}/" not in p.links: err(f"{u}: no link to its solution family")
for i in INDUSTRIES:
    p = by_url.get(f"/industries/{i['slug']}/")
    if not p: err(f"missing industry page {i['slug']}"); continue
    for cid, _ in i["cases"]:
        c = next(x for x in cases if x["id"] == cid)
        if f"/business-cases/{c['slug']}/" not in p.links: err(f"industry {i['slug']}: no link to {cid}")
# solution families (commercial pillars)
seen = [cid for pl in S.PILLARS for cid in pl["cases"]]
if sorted(seen) != sorted(case_ids) or len(seen) != len(set(seen)): err("every business case must be in exactly one solution family")
if not S.PILLARS[0]["flagship"] or "BC01" not in S.PILLARS[0]["cases"]: err("distributed enterprise intelligence must be the flagship family incl. OT/IT")
for pl in S.PILLARS:
    p = by_url.get(f"/solutions/{pl['slug']}/")
    if not p: err(f"missing solution page {pl['slug']}"); continue
    for cid in pl["cases"]:
        c = next(x for x in cases if x["id"] == cid)
        if f"/business-cases/{c['slug']}/" not in p.links: err(f"solution {pl['slug']}: no link to {cid}")
    if "Illustrative enterprise scenario" not in " ".join(p.text): err(f"solution {pl['slug']}: scenario label missing")
if home:
    t = " ".join(home.text)
    for k in ("Discuss your use case", "Explore business cases", "Illustrative enterprise scenario"):
        if k not in t: err(f"home: '{k}' missing")
    for pl in S.PILLARS:
        if pl["name"] not in t: err(f"home: pillar {pl['name']} missing")
    if re.search(r"production deployments|what we have not|validation backlog", t, re.I): err("home: defensive wording on the homepage")
    order = ["solutions", "scenario", "challenges", "how", "evidence", "engage"]
    pos = [home.ids.index(x) if x in home.ids else -1 for x in order]
    if -1 in pos or pos != sorted(pos): err(f"home: section hierarchy wrong {list(zip(order, pos))}")
for rel, p in pages.items():
    if rel != "404.html" and "have no contractual value" not in " ".join(p.text):
        err(f"{url_for(rel)}: legal disclaimer missing from footer")
LEGAL_URLS = ("/aviso-legal/", "/privacidad/", "/cookies/", "/legal-notice/", "/privacy/", "/cookie-policy/")
for u in LEGAL_URLS:
    if u not in by_url: err(f"missing legal page {u}")
for rel, p in pages.items():
    for u in LEGAL_URLS:
        if u not in p.links: err(f"{url_for(rel)}: footer link to {u} missing"); break
missing = [k for k in ("owner", "nif", "address", "email") if not S.LEGAL.get(k)]
if missing:
    err(f"RELEASE BLOCKER: legal owner data missing in content/site.py LEGAL: {missing} (required by LSSI-CE art. 10 and RGPD art. 13)")
pending = [k for k in ("nif", "address", "registry") if "pendiente" in S.LEGAL.get(k, "").lower()]
if pending:
    warn(f"Legal data still pending ({', '.join(pending)}): replace in content/site.py LEGAL as soon as the company has them")
for u in ("/simulator/", "/roi/"):
    if u in by_url and "Not contractual." not in " ".join(by_url[u].text): err(f"{u}: non-contractual note missing next to results")
sim = by_url.get("/simulator/")
if not sim: err("missing page /simulator/")
else:
    if "Illustrative architecture simulator" not in " ".join(sim.text): err("simulator: label missing")
    if "/pilot/?type=assessment" not in sim.links: err("simulator: conversion CTA missing")
for u in ("/roi/", "/business-cases/", "/pilot/", "/simulator/", "/evidence/", "/platform/", "/technology/", "/partners/", "/company/", "/industries/"):
    if u not in by_url: err(f"missing page {u}")
    elif u != "/" and "/pilot/" not in by_url[u].links: err(f"{u}: Request a Pilot CTA missing")

# ----------------------------------------------------------------------------- claim hygiene
BANNED = [r"revolutionar", r"game[- ]chang", r"unparalleled", r"trusted by", r"testimonial", r"award[- ]winning",
          r"guarantee", r"100% accura", r"happy clients", r"lorem", r"example\.com", r"sarah johnson", r"555",
          r"industry[- ]leading", r"world[- ]class", r"\bproven\b", r"certified", r"same intelligence",
          r"accuracy intact", r"radical", r"customer success", r"case study"]
ALLOW_CTX = {r"certified": r"no(t| security)? ?certif|holds no security certifications",
             r"guarantee": r"(\bno|\bnot) guarantee|not provide the privacy guarantees|not claim equivalent privacy guarantees|guarantee privacy or anonymization\? no|no warranty or guarantee",
             r"\bproven\b": r"not yet been proven|designed to be proven|to be proven"}
for rel, p in pages.items():
    t = " ".join(p.text).lower()
    for b in BANNED:
        for m in re.finditer(b, t):
            ctx = t[max(0, m.start() - 60): m.end() + 60]
            if b in ALLOW_CTX and re.search(ALLOW_CTX[b], ctx): continue
            err(f"{url_for(rel)}: banned claim '{b}' … {ctx.strip()} …")
    for m in re.finditer(r"\bbc\d{2}\b", t):
        err(f"{url_for(rel)}: internal case ID visible to customers … {t[max(0, m.start() - 40): m.end() + 40].strip()} …")
    for m in re.finditer(r"real[- ]time", t):
        ctx = t[max(0, m.start() - 80): m.end() + 40]
        if not re.search(r"\bno\b|\bnot\b|never|without", ctx):
            err(f"{url_for(rel)}: unqualified 'real-time' claim … {ctx.strip()} …")
    for m in re.finditer(r"anonymi[sz]", t):
        ctx = t[max(0, m.start() - 60): m.end() + 20]
        if not re.search(r"\bnot\b|\bno\b|does not|isn't|never", ctx):
            err(f"{url_for(rel)}: unqualified anonymization statement … {ctx.strip()} …")

# ----------------------------------------------------------------------------- color contrast of tokens
def lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
css = open(os.path.join(ROOT, "assets/css/site.css"), encoding="utf-8").read()
blocks = {"dark": css.split("*,*::before")[0]}
for theme, blk in blocks.items():
    tok = dict(re.findall(r"--([a-z0-9-]+):(#[0-9A-Fa-f]{6})", blk))
    for fg in ("text", "muted", "dim", "save", "cyan", "violet", "raw", "amber", "danger"):
        for bg in ("bg", "bg-2"):
            if fg in tok and bg in tok:
                r = ratio(tok[fg], tok[bg])
                if r < 4.5: err(f"contrast {theme}: --{fg} on --{bg} = {r:.2f} < 4.5")
    if "save" in tok and "save-ink" in tok and ratio(tok["save"], tok["save-ink"]) < 4.5:
        err(f"contrast {theme}: primary button text {ratio(tok['save'], tok['save-ink']):.2f}")

# ----------------------------------------------------------------------------- release blockers
if not S.CONTACT_EMAIL:
    warn("RELEASE BLOCKER: content/site.py CONTACT_EMAIL is empty — the pilot form prepares a copyable request only.")
for f in LEGACY:
    if not os.path.exists(os.path.join(ROOT, f)): err(f"legacy redirect missing: {f}")
import subprocess
try:
    tracked = subprocess.run(["git", "ls-files", "internal"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if tracked: err(f"internal documents are tracked by git: {tracked.splitlines()[:3]}")
except OSError:
    warn("git not available: could not confirm internal/ is untracked")
if not os.path.exists(os.path.join(ROOT, "internal")) or ".gitignore" not in os.listdir(ROOT) or \
        "internal/" not in open(os.path.join(ROOT, ".gitignore")).read():
    err("internal/ must exist and be git-ignored")

print(f"Checked {len(pages)} pages, {len(cases)} business cases, {len(INDUSTRIES)} industries.")
for w in warnings: print("WARN ", w)
for e in errors: print("ERROR", e)
print("OK" if not errors else f"{len(errors)} error(s)")
sys.exit(1 if errors else 0)
