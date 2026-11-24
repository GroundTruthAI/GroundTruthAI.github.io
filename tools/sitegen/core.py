"""Layout, escaping and small HTML helpers shared by every page."""
import html
import os
import re

from content import site as S

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; "
       "img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'self'; "
       "form-action 'none'; upgrade-insecure-requests")

ASSET_VERSION = "20261124"

PAGES = []  # (path, priority) for sitemap


def esc(s):
    return html.escape(str(s), quote=True)


def md(s):
    """Escape, then apply the tiny inline markup allowed in content: **bold**, *italic*."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def paras(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return "".join(f"<p{c}>{md(p)}</p>" for p in items)


def ul(items, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(f"<li>{md(i)}</li>" for i in items) + "</ul>"


def icon(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="/assets/img/icons.svg#{name}"></use></svg>'


def button(label, href, kind="primary", extra=""):
    return f'<a class="btn btn-{kind}" href="{esc(href)}"{extra}>{esc(label)}</a>'


def badge(text, kind="neutral"):
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


LOGO = ('<svg class="logo" viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<circle cx="16" cy="16" r="14" fill="none" class="logo-o" stroke-width="2" stroke-dasharray="2 3.2"/>'
        '<circle cx="16" cy="16" r="8.5" fill="none" class="logo-m" stroke-width="2"/>'
        '<circle cx="16" cy="16" r="3.6" class="logo-c"/></svg>')

BRAND = f'{LOGO}<span class="brand-t">Ground<b>Truth</b> AI</span>'


def _flagship_menu(cases):
    flag = [c for c in cases if c["tier"] == "flagship"]
    items = "".join(
        f'<li><a href="/business-cases/{c["slug"]}/"><span class="mm-code">{c["id"]}</span>'
        f'<span class="mm-t">{esc(c["title"])}</span><span class="mm-d">{esc(c["outcome_short"])}</span></a></li>'
        for c in flag)
    return (
        '<div class="megamenu" id="mm-cases" hidden>'
        '<div class="mm-col"><p class="mm-h">Flagship business cases</p>'
        f'<ul class="mm-list">{items}</ul></div>'
        '<div class="mm-col mm-side"><p class="mm-h">Find your case</p><ul class="mm-links">'
        '<li><a href="/business-cases/">All 11 business cases · explorer</a></li>'
        '<li><a href="/roi/">ROI calculator</a></li>'
        '<li><a href="/industries/">Business cases by industry</a></li>'
        '<li><a href="/pilot/">Pilot program</a></li>'
        '</ul></div></div>')


def header(active, cases):
    links = []
    for label, href, key in S.NAV:
        cur = ' aria-current="page"' if key == active else ""
        if key == "business-cases":
            links.append(
                f'<li class="has-mm"><a class="nav-l nav-primary" href="{href}"{cur}>{label}</a>'
                '<button class="mm-toggle" type="button" aria-expanded="false" aria-controls="mm-cases">'
                '<span class="sr-only">Show business cases menu</span>'
                '<svg viewBox="0 0 12 12" aria-hidden="true" focusable="false"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
                f'</button>{_flagship_menu(cases)}</li>')
        else:
            links.append(f'<li><a class="nav-l" href="{href}"{cur}>{label}</a></li>')
    return (
        '<a class="skip" href="#main">Skip to content</a>'
        '<header class="site-header"><div class="wrap hdr">'
        f'<a class="brand" href="/" aria-label="GroundTruth AI home">{BRAND}</a>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">'
        '<span class="nav-toggle-bars" aria-hidden="true"></span><span class="sr-only">Menu</span></button>'
        '<nav id="site-nav" class="site-nav" aria-label="Primary">'
        f'<ul class="nav-list">{"".join(links)}</ul>'
        '<a class="btn btn-primary btn-sm nav-cta" href="/pilot/">Request a Pilot</a>'
        '</nav></div></header>')


def footer(cases):
    flag = [c for c in cases if c["tier"] == "flagship"]
    more = [c for c in cases if c["tier"] != "flagship"]
    fl = "".join(f'<li><a href="/business-cases/{c["slug"]}/">{esc(c["title"])}</a></li>' for c in flag)
    mo = "".join(f'<li><a href="/business-cases/{c["slug"]}/">{esc(c["title"])}</a></li>' for c in more)
    return (
        '<footer class="site-footer"><div class="wrap">'
        '<div class="ft-top">'
        f'<div class="ft-brand"><a class="brand" href="/">{BRAND}</a>'
        '<p>Keep data distributed. Centralize intelligence.</p>'
        '<a class="btn btn-primary btn-sm" href="/pilot/">Request a Pilot</a></div>'
        '<nav class="ft-nav" aria-label="Footer">'
        f'<div><p class="ft-h">Flagship cases</p><ul>{fl}</ul></div>'
        f'<div><p class="ft-h">More business cases</p><ul>{mo}</ul></div>'
        '<div><p class="ft-h">Explore</p><ul>'
        '<li><a href="/business-cases/">Business case explorer</a></li>'
        '<li><a href="/roi/">ROI calculator</a></li>'
        '<li><a href="/industries/">Industries</a></li>'
        '<li><a href="/platform/">Platform</a></li>'
        '<li><a href="/technology/">Technology</a></li>'
        '<li><a href="/evidence/">Evidence</a></li>'
        '<li><a href="/partners/">Partners</a></li>'
        '<li><a href="/company/">Company</a></li>'
        '</ul></div></nav></div>'
        '<div class="ft-legal"><p>All business cases are <strong>proposed enterprise applications</strong> that have not yet been validated in production. '
        'Technical results come from internal experiments on public benchmark datasets. '
        'Financial figures are illustrative scenarios based on stated assumptions. '
        '<a href="/evidence/">How we classify evidence</a>.</p>'
        '<p>Distilled datasets remain subject to applicable data protection, residency, transfer and security requirements.</p>'
        '<p>© 2026 GroundTruth AI</p></div>'
        '</div></footer>')


def page(path, title, description, body, active="", cases=(), priority="0.6", extra_js=(), body_class=""):
    """Render and write a full page. `path` is the URL path, e.g. '/business-cases/'."""
    canonical = S.BASE_URL + path
    full_title = title if title.startswith(S.SITE_NAME) else f"{title} · {S.SITE_NAME}"
    js = "".join(f'<script src="{j}?v={ASSET_VERSION}" defer></script>' for j in ("/assets/js/site.js",) + tuple(extra_js))
    bc = f' class="{body_class}"' if body_class else ""
    doc = (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<meta http-equiv="Content-Security-Policy" content="{CSP}">\n'
        '<meta name="referrer" content="strict-origin-when-cross-origin">\n'
        f'<title>{esc(full_title)}</title>\n'
        f'<meta name="description" content="{esc(description)}">\n'
        f'<link rel="canonical" href="{esc(canonical)}">\n'
        f'<meta property="og:title" content="{esc(full_title)}">\n'
        f'<meta property="og:description" content="{esc(description)}">\n'
        f'<meta property="og:url" content="{esc(canonical)}">\n'
        '<meta property="og:type" content="website">\n'
        '<meta name="color-scheme" content="dark light">\n'
        '<meta name="theme-color" content="#05080F" media="(prefers-color-scheme: dark)">\n'
        '<meta name="theme-color" content="#F6F8FB" media="(prefers-color-scheme: light)">\n'
        '<link rel="icon" href="/assets/img/favicon.png">\n'
        '<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">\n'
        '<link rel="preload" href="/assets/fonts/Inter-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
        f'<link rel="stylesheet" href="/assets/css/site.css?v={ASSET_VERSION}">\n'
        f'{js}\n'
        f'</head>\n<body{bc}>\n'
        f'{header(active, cases)}\n'
        f'<main id="main" tabindex="-1">\n{body}\n</main>\n'
        f'{footer(cases)}\n'
        '</body>\n</html>\n')
    write(path, doc)
    PAGES.append((path, priority))


def write(path, content):
    rel = path.lstrip("/")
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    out = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)


def breadcrumb(items):
    """items: list of (label, href or None)."""
    lis = []
    for i, (label, href) in enumerate(items):
        if href and i < len(items) - 1:
            lis.append(f'<li><a href="{href}">{esc(label)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def section(id_, title, inner, eyebrow="", cls="", lead=""):
    eb = f'<p class="eyebrow">{esc(eyebrow)}</p>' if eyebrow else ""
    ld = f'<p class="lead">{md(lead)}</p>' if lead else ""
    return (f'<section class="sec {cls}" id="{id_}" aria-labelledby="{id_}-h"><div class="wrap">'
            f'{eb}<h2 id="{id_}-h">{md(title)}</h2>{ld}{inner}</div></section>')
