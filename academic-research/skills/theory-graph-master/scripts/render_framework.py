#!/usr/bin/env python3
"""
Render a conceptual framework diagram from a JSON spec.

    uv run --with matplotlib render_framework.py spec.json --out fig1
    python3 render_framework.py spec.json --out fig1 --formats svg pdf png

Writes fig1.svg, fig1.pdf and fig1.png (300 dpi). Greyscale safe: every
distinction is carried by shape and line style, never by colour alone.

Spec format (see references/rendering.md for the annotated version):

{
  "title": "Figure 1. Conceptual model",
  "nodes": [
    {"id": "iv",   "label": "Broker\nposition", "col": 0, "row": 1, "kind": "construct"},
    {"id": "med",  "label": "Perceived\ndiscretion", "col": 1, "row": 1, "kind": "construct"},
    {"id": "dv",   "label": "Grant\nsuccess", "col": 2, "row": 1, "kind": "construct"},
    {"id": "mod",  "label": "Formal tie\nassignment", "col": 1, "row": 2, "kind": "moderator"},
    {"id": "ctrl", "label": "Controls:\ntenure, field", "col": 1, "row": 0, "kind": "control"}
  ],
  "edges": [
    {"from": "iv",  "to": "med", "label": "H1 (+)"},
    {"from": "med", "to": "dv",  "label": "H2 (+)"},
    {"from": "iv",  "to": "dv",  "label": "H3 indirect", "style": "dashed", "curve": 0.35},
    {"from": "mod", "onto": ["iv", "med"], "label": "H4 (-)"},
    {"from": "ctrl","to": "dv",  "style": "dotted"}
  ],
  "note": "Solid arrows are hypothesized direct effects. ..."
}

kind: construct | latent | moderator | control | outcome | unobserved
An edge with "onto": [a, b] is a moderator: it terminates on the midpoint of
the a -> b path, which is the correct convention.
"""
import argparse
import json
import sys
import textwrap

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
except ImportError:
    sys.exit("matplotlib is required:  pip install matplotlib   "
             "or  uv run --with matplotlib render_framework.py ...")

COL_W, ROW_H = 3.6, 1.75
BOX_W, BOX_H = 2.5, 1.05

KIND_STYLE = {
    "construct":  dict(fc="white",   ec="#111111", lw=1.6, ls="solid",  shape="box"),
    "outcome":    dict(fc="white",   ec="#111111", lw=2.2, ls="solid",  shape="box"),
    "latent":     dict(fc="white",   ec="#111111", lw=1.6, ls="solid",  shape="ellipse"),
    "moderator":  dict(fc="white",   ec="#111111", lw=1.6, ls="solid",  shape="box"),
    "control":    dict(fc="#f2f2f2", ec="#777777", lw=1.1, ls="dashed", shape="box"),
    "unobserved": dict(fc="white",   ec="#777777", lw=1.4, ls="dashed", shape="ellipse"),
}
EDGE_LS = {"solid": "-", "dashed": (0, (6, 3)), "dotted": (0, (1, 2.5))}


def xy(node):
    return node["col"] * COL_W, node["row"] * ROW_H


def draw_node(ax, node):
    st = KIND_STYLE.get(node.get("kind", "construct"), KIND_STYLE["construct"])
    x, y = xy(node)
    if st["shape"] == "ellipse":
        patch = Ellipse((x, y), BOX_W, BOX_H, facecolor=st["fc"],
                        edgecolor=st["ec"], linewidth=st["lw"], linestyle=st["ls"], zorder=3)
    else:
        patch = FancyBboxPatch((x - BOX_W / 2, y - BOX_H / 2), BOX_W, BOX_H,
                               boxstyle="round,pad=0.02,rounding_size=0.06",
                               facecolor=st["fc"], edgecolor=st["ec"],
                               linewidth=st["lw"], linestyle=st["ls"], zorder=3)
    ax.add_patch(patch)
    label = node["label"].replace("\\n", "\n")
    if "\n" not in label and len(label) > 18:
        label = "\n".join(textwrap.wrap(label, 18))
    ax.text(x, y, label, ha="center", va="center", fontsize=9.5, zorder=4,
            color="#111111", linespacing=1.35)


def edge_endpoints(a, b):
    """Trim the arrow so it stops at the box border rather than the centre."""
    ax_, ay = xy(a)
    bx, by = xy(b)
    dx, dy = bx - ax_, by - ay
    if dx == 0 and dy == 0:
        return (ax_, ay), (bx, by)
    hx, hy = BOX_W / 2 + 0.06, BOX_H / 2 + 0.06
    t = min(hx / abs(dx) if dx else 9e9, hy / abs(dy) if dy else 9e9)
    return (ax_ + dx * t, ay + dy * t), (bx - dx * t, by - dy * t)


def draw_edge(ax, nodes, e):
    ls = EDGE_LS.get(e.get("style", "solid"), "-")
    curve = e.get("curve", 0.0)
    if "onto" in e:                       # moderator -> midpoint of a path
        a, b = nodes[e["onto"][0]], nodes[e["onto"][1]]
        (sx, sy), (ex, ey) = xy(a), xy(b)
        tx, ty = (sx + ex) / 2, (sy + ey) / 2
        src = nodes[e["from"]]
        (p0, p1) = edge_endpoints(src, {"col": tx / COL_W, "row": ty / ROW_H})
        start, end = p0, (tx, ty)
    else:
        start, end = edge_endpoints(nodes[e["from"]], nodes[e["to"]])
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                            linewidth=1.4, linestyle=ls, color="#111111",
                            connectionstyle=f"arc3,rad={curve}", zorder=2,
                            shrinkA=0, shrinkB=(3 if "onto" in e else 0))
    ax.add_patch(arrow)
    if e.get("label"):
        mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        my += 0.20 + abs(curve) * 1.1
        ax.text(mx, my, e["label"], ha="center", va="bottom", fontsize=8.5,
                color="#111111", zorder=5,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))


def render(spec, out, formats, dpi=300):
    nodes = {n["id"]: n for n in spec["nodes"]}
    cols = [n["col"] for n in nodes.values()]
    rows = [n["row"] for n in nodes.values()]
    w = (max(cols) - min(cols)) * COL_W + BOX_W + 1.0
    h = (max(rows) - min(rows)) * ROW_H + BOX_H + 1.3
    fig, ax = plt.subplots(figsize=(w, h))
    for e in spec.get("edges", []):
        draw_edge(ax, nodes, e)
    for n in nodes.values():
        draw_node(ax, n)
    pad_b = BOX_H / 2 + (0.45 if spec.get("note") else 0.18)
    pad_t = BOX_H / 2 + (0.45 if spec.get("title") else 0.18)
    ax.set_ylim(min(rows) * ROW_H - pad_b, max(rows) * ROW_H + pad_t)
    ax.set_xlim(min(cols) * COL_W - BOX_W / 2 - 0.35,
                max(cols) * COL_W + BOX_W / 2 + 0.35)
    ax.set_aspect("equal")
    ax.axis("off")
    if spec.get("title"):
        ax.set_title(spec["title"], fontsize=11, loc="left", pad=12, color="#111111")
    if spec.get("note"):
        note = "\n".join(textwrap.wrap(spec["note"], int(w * 13)))
        fig.text(0.02, 0.015, note, fontsize=8, va="bottom", color="#333333")
    fig.tight_layout()
    written = []
    for fmt in formats:
        path = f"{out}.{fmt}"
        fig.savefig(path, format=fmt, dpi=dpi, bbox_inches="tight",
                    facecolor="white")
        written.append(path)
    plt.close(fig)
    return written


def validate(spec):
    """Structural checks. Warnings, not errors: the researcher decides."""
    ids = {n["id"] for n in spec["nodes"]}
    warn = []
    for e in spec.get("edges", []):
        for ref in [e.get("from"), e.get("to")] + list(e.get("onto", [])):
            if ref and ref not in ids:
                warn.append(f"edge references unknown node '{ref}'")
    incoming = {i: 0 for i in ids}
    outgoing = {i: 0 for i in ids}
    for e in spec.get("edges", []):
        if e.get("from"):
            outgoing[e["from"]] = outgoing.get(e["from"], 0) + 1
        if e.get("to"):
            incoming[e["to"]] = incoming.get(e["to"], 0) + 1
    for n in spec["nodes"]:
        k, i = n.get("kind", "construct"), n["id"]
        if k == "moderator" and not any(e.get("from") == i and "onto" in e
                                        for e in spec.get("edges", [])):
            warn.append(f"'{i}' is a moderator but does not terminate on a path; "
                        f"as drawn it is an independent variable")
        if k == "construct" and incoming.get(i, 0) and outgoing.get(i, 0) == 0 \
                and i != spec["nodes"][-1]["id"]:
            pass
    for n in spec["nodes"]:
        i = n["id"]
        if incoming.get(i, 0) == 1 and outgoing.get(i, 0) == 0 \
                and n.get("kind") == "construct" and n.get("mediator"):
            warn.append(f"'{i}' is flagged as a mediator but has no outgoing path")
    for e in spec.get("edges", []):
        if e.get("style", "solid") == "solid" and not e.get("label") and "onto" not in e:
            if spec["nodes"] and next((n for n in spec["nodes"]
                                       if n["id"] == e.get("to")), {}).get("kind") != "control":
                warn.append(f"path {e.get('from')} -> {e.get('to')} has no hypothesis label")
    return warn


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("spec")
    p.add_argument("--out", default="figure")
    p.add_argument("--formats", nargs="+", default=["svg", "pdf", "png"])
    p.add_argument("--dpi", type=int, default=300)
    p.add_argument("--strict", action="store_true",
                   help="exit non-zero if validation produces warnings")
    a = p.parse_args()
    with open(a.spec, encoding="utf-8") as fh:
        spec = json.load(fh)
    warn = validate(spec)
    for w in warn:
        print(f"WARNING: {w}", file=sys.stderr)
    if warn and a.strict:
        sys.exit(f"{len(warn)} validation warning(s); --strict is set")
    for path in render(spec, a.out, a.formats, a.dpi):
        print(f"wrote {path}")


if __name__ == "__main__":
    try:                                   # tolerate `| head` without a traceback
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    main()
