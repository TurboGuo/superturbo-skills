#!/usr/bin/env python3
"""
Check a causal DAG and render it.

    uv run --with networkx --with matplotlib render_dag.py dag.json --out fig2

Does three things, in this order, because the order matters:
  1. Validates the graph is acyclic.
  2. Finds every backdoor path from exposure to outcome, and computes the
     minimal sufficient adjustment sets over MEASURED variables only.
  3. Renders the DAG, with unmeasured variables dashed.

If no adjustment set exists over measured variables, it says the effect is not
identified. That sentence is the reason to draw a DAG at all.

Spec:
{
  "exposure": "X",
  "outcome": "Y",
  "unmeasured": ["U"],
  "edges": [["U","X"], ["U","Y"], ["X","M"], ["M","Y"], ["Z","X"], ["Z","Y"],
            ["X","C"], ["Y","C"]],
  "positions": {"X": [0,0], "Y": [3,0], "M": [1.5,0], "Z": [1.5,1.2],
                "U": [1.5,-1.4], "C": [1.5,-0.7]},
  "title": "Figure 2. Causal DAG"
}
positions are optional; a layered layout is computed when they are absent.
"""
import argparse
import itertools
import json
import sys

try:
    import networkx as nx
except ImportError:
    sys.exit("networkx is required:  uv run --with networkx --with matplotlib render_dag.py ...")


def backdoor_paths(g, x, y):
    """Every path from x to y whose first edge points INTO x."""
    und = g.to_undirected()
    out = []
    for path in nx.all_simple_paths(und, x, y):
        if len(path) > 1 and g.has_edge(path[1], path[0]):
            out.append(path)
    return out


def blocks_backdoor(g, x, y, z):
    """Backdoor criterion: no member of z is a descendant of x, and z
    d-separates x from y in the graph with x's outgoing edges deleted."""
    desc = nx.descendants(g, x)
    if any(v in desc for v in z):
        return False
    h = g.copy()
    h.remove_edges_from(list(g.out_edges(x)))
    return nx.is_d_separator(h, {x}, {y}, set(z))


def minimal_adjustment_sets(g, x, y, unmeasured, max_size=4):
    candidates = [v for v in g.nodes
                  if v not in (x, y) and v not in unmeasured
                  and v not in nx.descendants(g, x)]
    found = []
    for k in range(0, min(max_size, len(candidates)) + 1):
        for combo in itertools.combinations(candidates, k):
            if any(set(f) <= set(combo) for f in found):
                continue                      # not minimal
            if blocks_backdoor(g, x, y, set(combo)):
                found.append(sorted(combo))
        if found and k >= 1:
            break                              # smallest sets only
    return found


def colliders_on(g, path):
    return [path[i] for i in range(1, len(path) - 1)
            if g.has_edge(path[i - 1], path[i]) and g.has_edge(path[i + 1], path[i])]


def layered_positions(g, x, y):
    try:
        order = list(nx.topological_sort(g))
    except nx.NetworkXUnfeasible:
        order = list(g.nodes)
    depth = {n: 0 for n in order}
    for n in order:
        for p in g.predecessors(n):
            depth[n] = max(depth[n], depth[p] + 1)
    by_layer = {}
    for n, d in depth.items():
        by_layer.setdefault(d, []).append(n)
    pos = {}
    for d, names in sorted(by_layer.items()):
        for i, n in enumerate(sorted(names)):
            pos[n] = [d * 2.2, (i - (len(names) - 1) / 2) * 1.5]
    return pos


def render(spec, g, out, formats, dpi):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch, Ellipse
    except ImportError:
        sys.exit("matplotlib is required to draw the figure. The identification "
                 "report above is complete and needs nothing installed; re-run "
                 "with --no-render to skip drawing, or install matplotlib:\n"
                 "  pip install matplotlib\n"
                 "  uv run --with networkx --with matplotlib render_dag.py ...")

    x, y = spec["exposure"], spec["outcome"]
    unm = set(spec.get("unmeasured", []))
    pos = {k: tuple(v) for k, v in spec.get("positions", {}).items()} or layered_positions(g, x, y)
    for n in g.nodes:
        pos.setdefault(n, (0.0, 0.0))

    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    fig, ax = plt.subplots(figsize=(max(xs) - min(xs) + 3.0,
                                    max(ys) - min(ys) + 2.4))
    rx, ry = 0.52, 0.30
    def trim(p0, p1, pad=0.06):
        """Stop the arrow at the ellipse boundary, in data units, so the head
        is never hidden behind a node."""
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        if dx == 0 and dy == 0:
            return p0, p1
        import math
        denom = math.hypot(dx / (rx + pad), dy / (ry + pad))
        tx, ty = (dx / denom), (dy / denom)
        return (p0[0] + tx, p0[1] + ty), (p1[0] - tx, p1[1] - ty)

    for u, v in g.edges:
        a, b = trim(pos[u], pos[v])
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>",
                                     mutation_scale=14, linewidth=1.4,
                                     linestyle=(0, (5, 3)) if (u in unm or v in unm) else "-",
                                     color="#111111", shrinkA=0, shrinkB=0, zorder=4))
    for n in g.nodes:
        is_focal = n in (x, y)
        ax.add_patch(Ellipse(pos[n], rx * 2, ry * 2, facecolor="white",
                             edgecolor="#111111",
                             linewidth=2.2 if is_focal else 1.4,
                             linestyle=(0, (4, 2.5)) if n in unm else "-", zorder=5))
        ax.text(pos[n][0], pos[n][1], n, ha="center", va="center",
                fontsize=10, fontweight="bold" if is_focal else "normal", zorder=6)
    ax.set_xlim(min(xs) - 1.2, max(xs) + 1.2)
    ax.set_ylim(min(ys) - 1.0, max(ys) + 1.0)
    ax.set_aspect("equal"); ax.axis("off")
    if spec.get("title"):
        ax.set_title(spec["title"], fontsize=11, loc="left", pad=10)
    fig.tight_layout()
    written = []
    for fmt in formats:
        p = f"{out}.{fmt}"
        fig.savefig(p, format=fmt, dpi=dpi, bbox_inches="tight", facecolor="white")
        written.append(p)
    plt.close(fig)
    return written


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--out", default="dag")
    ap.add_argument("--formats", nargs="+", default=["svg", "pdf", "png"])
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--no-render", action="store_true", help="report only")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    g = nx.DiGraph(); g.add_edges_from([tuple(e) for e in spec["edges"]])
    x, y = spec["exposure"], spec["outcome"]
    unm = set(spec.get("unmeasured", []))

    if not nx.is_directed_acyclic_graph(g):
        sys.exit(f"NOT A DAG: cycle found {nx.find_cycle(g)}. A causal diagram "
                 f"with a cycle is a dynamic system, not a DAG.")

    print(f"# Identification report: {x} -> {y}\n")
    bps = backdoor_paths(g, x, y)
    print(f"Backdoor paths found: {len(bps)}")
    for p in bps:
        cols = colliders_on(g, p)
        tag = f"   [collider(s): {', '.join(cols)} — LEAVE UNADJUSTED]" if cols else ""
        unm_on = [n for n in p if n in unm]
        tag += f"   [unmeasured on path: {', '.join(unm_on)}]" if unm_on else ""
        print("  " + " - ".join(p) + tag)

    sets = minimal_adjustment_sets(g, x, y, unm)
    print()
    if not sets:
        print("NOT IDENTIFIED over measured variables.")
        print("No adjustment set closes every backdoor path without conditioning "
              "on a descendant of the exposure.")
        print("The effect cannot be estimated from these data by adjustment. "
              "Go back to method-master for a design that identifies it "
              "(instrument, discontinuity, panel shock, or randomization).")
    else:
        print("Minimal sufficient adjustment set(s):")
        for s in sets:
            print("  { " + ", ".join(s) + " }" if s else "  { } (empty — no adjustment needed)")
        bad = [n for n in g.nodes if n in nx.descendants(g, x) and n != y]
        if bad:
            print(f"\nDo NOT adjust for (descendants of {x}): {', '.join(sorted(bad))}")
            print("Adjusting for a mediator removes part of the effect; adjusting "
                  "for a collider opens a path that was closed.")

    if not a.no_render:
        print()
        for p in render(spec, g, a.out, a.formats, a.dpi):
            print(f"wrote {p}")


if __name__ == "__main__":
    try:                                   # tolerate `| head` without a traceback
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    main()
