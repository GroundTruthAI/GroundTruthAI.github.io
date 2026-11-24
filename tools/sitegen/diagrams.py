"""Architecture diagram renderer (content DSL → inline SVG) and homepage visuals.

All colors come from CSS classes so diagrams follow the light/dark theme and print styles.
"""
import textwrap

from .core import esc

CW = 196        # column (zone) width
GX = 112        # gap between columns (room for flow labels)
PAD = 14        # outer padding
ZH = 34         # zone header height
NW = CW - 28    # node width
ROWGAP = 40     # vertical gap between nodes (room for vertical flow labels)
LH = 15         # node text line height
BACK_LANE = 34  # spacing of return-flow lanes under the zones

FLOW_LABEL = {"raw": "Raw data", "distilled": "Distilled dataset", "model": "Model / results", "control": "Control / approvals"}
NODE_KIND = {"system": "System", "store": "Data store", "gt": "GroundTruth AI component", "model": "Model training / analytics", "user": "People"}


def _wrap(text, width):
    return textwrap.wrap(text, width=width, break_long_words=True) or [""]


def _node_h(label):
    return max(46, len(_wrap(label, 21)) * LH + 22)


def _marker_defs(uid):
    out = []
    for k in FLOW_LABEL:
        out.append(f'<marker id="{uid}-a-{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" '
                   f'orient="auto-start-reverse"><path class="mk mk-{k}" d="M0 0 10 5 0 10z"/></marker>')
    return "<defs>" + "".join(out) + "</defs>"


def arch_svg(diagram, uid):
    zones = diagram["zones"]
    flows = diagram["flows"]
    # --- layout nodes
    pos = {}   # id -> (x, y, w, h, col)
    col_h = []
    for ci, z in enumerate(zones):
        x0 = PAD + ci * (CW + GX)
        y = PAD + ZH + 14
        for nid, label, kind in z["nodes"]:
            h = _node_h(label)
            pos[nid] = (x0 + (CW - NW) / 2, y, NW, h, ci)
            y += h + ROWGAP
        col_h.append(y - ROWGAP + 16)
    zone_bottom = max(col_h) if col_h else 200
    back = [f for f in flows if pos[f[0]][4] > pos[f[1]][4]]
    total_h = zone_bottom + PAD + (len(back) * BACK_LANE + 10 if back else 0)
    total_w = PAD * 2 + len(zones) * CW + (len(zones) - 1) * GX

    parts = [_marker_defs(uid)]
    # --- zones
    for ci, z in enumerate(zones):
        x0 = PAD + ci * (CW + GX)
        parts.append(f'<g class="zone zone-{esc(z["kind"])}"><rect x="{x0}" y="{PAD}" width="{CW}" height="{zone_bottom - PAD}" rx="12"/>')
        for li, line in enumerate(_wrap(z["label"].upper(), 28)[:2]):
            parts.append(f'<text class="zone-t" x="{x0 + CW / 2}" y="{PAD + 20 + li * 12}" text-anchor="middle">{esc(line)}</text>')
        parts.append("</g>")

    # --- anchor distribution so several flows on one edge do not overlap
    edge_slots = {}
    def slot(nid, side, key):
        edge_slots.setdefault((nid, side), []).append(key)

    for i, (a, b, kind, label) in enumerate(flows):
        ca, cb = pos[a][4], pos[b][4]
        if ca < cb:
            slot(a, "r", i); slot(b, "l", i)
        elif ca > cb:
            slot(a, "b", i); slot(b, "b", i)
        else:
            if pos[b][1] > pos[a][1]:
                slot(a, "b", i); slot(b, "t", i)
            else:
                slot(a, "t", i); slot(b, "b", i)

    def anchor(nid, side, key):
        x, y, w, h, _ = pos[nid]
        keys = edge_slots[(nid, side)]
        n, k = len(keys), keys.index(key)
        frac = (k + 1) / (n + 1)
        if side == "r":
            return x + w, y + h * frac
        if side == "l":
            return x, y + h * frac
        if side == "b":
            return x + w * frac, y + h
        return x + w * frac, y

    flow_svg, label_svg = [], []
    back_i = 0
    for i, (a, b, kind, label) in enumerate(flows):
        ca, cb = pos[a][4], pos[b][4]
        mk = f'marker-end="url(#{uid}-a-{kind})"'
        if ca < cb:
            x1, y1 = anchor(a, "r", i)
            x2, y2 = anchor(b, "l", i)
            dx = (x2 - x1) / 2
            d = f"M{x1:.1f} {y1:.1f} C{x1 + dx:.1f} {y1:.1f} {x2 - dx:.1f} {y2:.1f} {x2 - 2:.1f} {y2:.1f}"
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
            if cb - ca > 1:  # skipping a column: label near the source gap
                lx = x1 + GX / 2
                ly = y1 + (y2 - y1) * 0.1
        elif ca > cb:
            x1, y1 = anchor(a, "b", i)
            x2, y2 = anchor(b, "b", i)
            lane = zone_bottom + 18 + back_i * BACK_LANE
            back_i += 1
            d = f"M{x1:.1f} {y1:.1f} L{x1:.1f} {lane:.1f} L{x2:.1f} {lane:.1f} L{x2:.1f} {y2 + 2:.1f}"
            lx, ly = (x1 + x2) / 2, lane
        else:
            if pos[b][1] > pos[a][1]:
                x1, y1 = anchor(a, "b", i)
                x2, y2 = anchor(b, "t", i)
                d = f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2 - 2:.1f}"
            else:
                x1, y1 = anchor(a, "t", i)
                x2, y2 = anchor(b, "b", i)
                d = f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2 + 2:.1f}"
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
        flow_svg.append(f'<path class="flow f-{kind}" d="{d}" {mk}/>')
        if label:
            lines = _wrap(label, 17)[:2]
            wpx = max(len(l) for l in lines) * 5.9 + 10
            hpx = len(lines) * 12 + 6
            label_svg.append(
                f'<g class="fl fl-{kind}"><rect x="{lx - wpx / 2:.1f}" y="{ly - hpx / 2:.1f}" width="{wpx:.1f}" height="{hpx}" rx="4"/>'
                + "".join(f'<text x="{lx:.1f}" y="{ly - hpx / 2 + 13 + j * 12:.1f}" text-anchor="middle">{esc(t)}</text>'
                          for j, t in enumerate(lines)) + "</g>")

    node_svg = []
    for z in zones:
        for nid, label, kind in z["nodes"]:
            x, y, w, h, _ = pos[nid]
            lines = _wrap(label, 21)
            ty = y + h / 2 - (len(lines) - 1) * LH / 2 + 4.5
            glyph = ""
            if kind == "store":
                glyph = f'<path class="glyph" d="M{x + 10} {y + 9} h10 M{x + 10} {y + 13} h10 M{x + 10} {y + 17} h10"/>'
            elif kind == "gt":
                glyph = (f'<circle class="glyph-gt" cx="{x + 14}" cy="{y + 13}" r="5"/>'
                         f'<circle class="glyph-gt2" cx="{x + 14}" cy="{y + 13}" r="1.8"/>')
            node_svg.append(
                f'<g class="node node-{kind}"><rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="9"/>{glyph}'
                + "".join(f'<text x="{x + w / 2:.1f}" y="{ty + j * LH:.1f}" text-anchor="middle">{esc(t)}</text>'
                          for j, t in enumerate(lines)) + "</g>")

    names = {nid: label for z in zones for nid, label, _ in z["nodes"]}
    desc = "; ".join(f"{names[a]} to {names[b]}: {FLOW_LABEL[k].lower()}" + (f" ({l})" if l else "")
                     for a, b, k, l in flows)
    svg = (f'<svg class="arch" viewBox="0 0 {total_w:.0f} {total_h:.0f}" width="{total_w:.0f}" height="{total_h:.0f}" '
           f'role="img" aria-labelledby="{uid}-t {uid}-d"><title id="{uid}-t">{esc(diagram["title"])}</title>'
           f'<desc id="{uid}-d">{esc(desc)}</desc>'
           + "".join(parts) + "".join(flow_svg) + "".join(node_svg) + "".join(label_svg) + "</svg>")
    return svg


def arch_text(diagram):
    """Text alternative listing zones, components and flows."""
    names = {nid: (label, z["label"]) for z in diagram["zones"] for nid, label, _ in z["nodes"]}
    zones = "".join(f'<li><strong>{esc(z["label"])}:</strong> ' + ", ".join(esc(n[1]) for n in z["nodes"]) + "</li>"
                    for z in diagram["zones"])
    flows = "".join(f'<li>{esc(names[a][0])} → {esc(names[b][0])} · <span class="lg lg-{k}">{FLOW_LABEL[k]}</span>'
                    + (f" · {esc(l)}" if l else "") + "</li>" for a, b, k, l in diagram["flows"])
    return f'<div class="arch-text"><p class="mini-h">Zones and components</p><ul>{zones}</ul><p class="mini-h">Data flows</p><ul>{flows}</ul></div>'


def legend():
    items = "".join(f'<li><span class="lg-line lg-{k}" aria-hidden="true"></span>{v}</li>' for k, v in FLOW_LABEL.items())
    return f'<ul class="arch-legend" aria-label="Diagram legend">{items}<li><span class="lg-node" aria-hidden="true"></span>GroundTruth AI component</li></ul>'


def arch_figure(diagram, uid, label):
    return (f'<figure class="arch-fig"><figcaption><span class="arch-k">{esc(label)}</span> {esc(diagram["title"])}</figcaption>'
            f'<div class="arch-scroll" tabindex="0" role="group" aria-label="{esc(diagram["title"])} (scrollable diagram)">{arch_svg(diagram, uid)}</div>'
            f'<details class="arch-alt"><summary>Text description of this diagram</summary>{arch_text(diagram)}</details></figure>')


# ---------------------------------------------------------------------------
# Homepage visuals (hand-drawn, decorative-but-meaningful; each has a text title)
# ---------------------------------------------------------------------------

def _svg(viewbox, title, inner, cls="viz"):
    import hashlib
    uid = "v" + hashlib.md5(title.encode()).hexdigest()[:6]
    return (f'<svg class="{cls}" viewBox="{viewbox}" role="img" aria-labelledby="{uid}"><title id="{uid}">{esc(title)}</title>'
            f'{_marker_defs(uid)}{inner.replace("UID", uid)}</svg>')


def hero_visual():
    domains = [("Plant OT zone", 40), ("Subsidiary", 128), ("EU region", 216), ("Edge fleet", 304)]
    g = []
    for i, (name, y) in enumerate(domains):
        g.append(f'<g class="hv-dom"><rect x="10" y="{y}" width="190" height="64" rx="12"/>'
                 f'<text class="hv-t" x="24" y="{y + 26}">{name}</text>'
                 f'<text class="hv-s" x="24" y="{y + 46}">raw data stays here</text>'
                 f'<g class="hv-bars">' + "".join(
                     f'<rect x="{138 + k * 7}" y="{y + 18 + (k % 3) * 4}" width="4" height="{28 - (k % 3) * 4}" rx="1"/>' for k in range(7)) + "</g></g>")
        g.append(f'<g class="node node-gt"><rect x="236" y="{y + 14}" width="46" height="36" rx="9"/>'
                 f'<circle class="glyph-gt" cx="259" cy="{y + 32}" r="7"/><circle class="glyph-gt2" cx="259" cy="{y + 32}" r="2.4"/></g>')
        g.append(f'<path class="flow f-raw" d="M200 {y + 32} H232" marker-end="url(#UID-a-raw)"/>')
        g.append(f'<path class="flow f-distilled hv-anim" d="M282 {y + 32} C350 {y + 32} 360 200 424 200" marker-end="url(#UID-a-distilled)"/>')
    g.append('<g class="hv-core"><circle cx="486" cy="200" r="62"/><circle class="hv-core2" cx="486" cy="200" r="40"/>'
             '<text class="hv-t" x="486" y="196" text-anchor="middle">Central</text>'
             '<text class="hv-t" x="486" y="214" text-anchor="middle">intelligence</text></g>')
    g.append('<text class="hv-cap" x="259" y="392" text-anchor="middle">distill at source</text>'
             '<text class="hv-cap" x="486" y="300" text-anchor="middle">train &amp; analyze</text>'
             '<text class="hv-cap" x="486" y="316" text-anchor="middle">on approved datasets</text>')
    return _svg("0 0 560 400", "Raw data stays in four separate domains; each distills locally and only approved distilled datasets flow to central intelligence.",
                "".join(g), "viz hero-viz")


def viz_bc01():
    inner = (
        '<g class="zone zone-source"><rect x="8" y="10" width="150" height="180" rx="12"/><text class="zone-t" x="83" y="32" text-anchor="middle">OT ZONE</text></g>'
        '<g class="zone zone-boundary"><rect x="186" y="10" width="88" height="180" rx="12"/><text class="zone-t" x="230" y="32" text-anchor="middle">DMZ</text></g>'
        '<g class="zone zone-central"><rect x="302" y="10" width="150" height="180" rx="12"/><text class="zone-t" x="377" y="32" text-anchor="middle">IT / CLOUD</text></g>'
        '<g class="node node-store"><rect x="24" y="52" width="118" height="38" rx="8"/><text x="83" y="76" text-anchor="middle">Historian</text></g>'
        '<g class="node node-gt"><rect x="24" y="122" width="118" height="44" rx="8"/><text x="83" y="148" text-anchor="middle">Distill in OT</text></g>'
        '<g class="node node-model"><rect x="318" y="122" width="118" height="44" rx="8"/><text x="377" y="148" text-anchor="middle">Central training</text></g>'
        '<path class="flow f-raw" d="M83 90 V118" marker-end="url(#UID-a-raw)"/>'
        '<path class="flow f-raw f-blocked" d="M142 71 H300"/>'
        '<g class="x-mark"><path d="M222 63 l16 16 M238 63 l-16 16"/></g>'
        '<path class="flow f-distilled" d="M142 144 H314" marker-end="url(#UID-a-distilled)"/>'
        '<text class="hv-cap" x="230" y="104" text-anchor="middle">no raw copy</text>'
        '<text class="hv-cap" x="230" y="182" text-anchor="middle">approved set</text>')
    return _svg("0 0 460 200", "Raw historian data no longer crosses the DMZ; a distilled dataset produced inside the OT zone is transferred for central training.", inner)


def viz_bc02():
    doms = [("Subsidiary A", 14), ("Subsidiary B", 62), ("Insurance unit", 110), ("LATAM region", 158)]
    g = []
    for name, y in doms:
        g.append(f'<g class="node node-system"><rect x="8" y="{y}" width="132" height="36" rx="8"/><text x="74" y="{y + 23}" text-anchor="middle">{name}</text></g>'
                 f'<g class="node node-gt"><rect x="160" y="{y + 6}" width="24" height="24" rx="6"/></g>'
                 f'<path class="flow f-distilled" d="M184 {y + 18} C250 {y + 18} 250 106 300 106" marker-end="url(#UID-a-distilled)"/>')
    g.append('<g class="node node-model"><rect x="304" y="74" width="148" height="64" rx="10"/>'
             '<text x="378" y="102" text-anchor="middle">Enterprise-wide</text><text x="378" y="120" text-anchor="middle">model</text></g>')
    return _svg("0 0 460 200", "Four business domains each distill locally; approved datasets combine into one enterprise-wide model while ownership stays distributed.", "".join(g))


def viz_bc03(benchmarks):
    rows = []
    y = 18
    for name, _t, red, base, dist, delta in benchmarks:
        w_full = 300
        w_dist = round(w_full * (100 - red) / 100)
        rows.append(f'<text class="bv-n" x="8" y="{y + 12}">{esc(name)}</text>'
                    f'<rect class="bv-full" x="104" y="{y}" width="{w_full}" height="8" rx="3"/>'
                    f'<rect class="bv-dist" x="104" y="{y + 11}" width="{max(w_dist, 3)}" height="8" rx="3"/>'
                    f'<text class="bv-v" x="{104 + w_dist + 8}" y="{y + 19}">{100 - red}% of data · {delta:+.1f} pp</text>')
        y += 40
    rows.append(f'<text class="hv-cap" x="104" y="{y + 6}">full set vs. distilled set · internal experiments</text>')
    return _svg(f"0 0 460 {y + 14}", "Benchmark training-set size after distillation: 5 to 14 percent of the original data, with accuracy changes between minus 1.4 and minus 2.8 points.",
                "".join(rows))


def viz_bc04():
    sites = [("Site A", 20, "M20 0 C30 -10 40 8 50 -4 S70 6 80 -2"), ("Site B", 92, "M20 0 C30 6 40 -8 50 2 S70 -10 80 0"),
             ("Site C", 164, "M20 0 L30 0 L34 -12 L38 8 L42 0 L80 0")]
    g = []
    for name, y, path in sites:
        g.append(f'<g class="node node-system"><rect x="8" y="{y - 6}" width="150" height="50" rx="8"/>'
                 f'<text x="20" y="{y + 12}">{name}</text>'
                 f'<path class="spark" transform="translate(50 {y + 28})" d="{path}"/></g>'
                 f'<g class="node node-gt"><rect x="176" y="{y + 7}" width="24" height="24" rx="6"/></g>'
                 f'<path class="flow f-distilled" d="M200 {y + 19} C260 {y + 19} 260 102 312 102" marker-end="url(#UID-a-distilled)"/>')
    g.append('<g class="node node-model"><rect x="316" y="66" width="136" height="72" rx="10"/>'
             '<text x="384" y="94" text-anchor="middle">Shared equipment</text><text x="384" y="112" text-anchor="middle">health model</text></g>'
             '<text class="hv-cap" x="384" y="160" text-anchor="middle">rare failures pooled</text>'
             '<text class="hv-cap" x="384" y="174" text-anchor="middle">across regimes</text>')
    return _svg("0 0 460 216", "Three facilities with different operating regimes distill locally; distilled datasets train a shared equipment health model.", "".join(g))
