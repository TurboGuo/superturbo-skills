#!/usr/bin/env python3
"""
Build the macro impact dashboard HTML from a data JSON file.

Usage:
    python3 scripts/build.py data.json macro-dashboard-2026-08-19.html

Validates the payload before writing, and refuses to write on a hard error.
Warnings are printed but do not block.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")

# Keys whose string values are allowed to contain a hyphen because they are
# never rendered as prose (URLs, and the artifact slug).
HYPHEN_OK_KEYS = {"artifactId", "outputFile"}

REQUIRED_TOP = ["title", "stamp", "regime", "banner", "assets", "matrix",
                "tiles", "calcs", "sources"]


def walk_strings(node, path="", key=None):
    """Yield (path, key, string) for every string in the payload."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, f"{path}.{k}", k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_strings(v, f"{path}[{i}]", key)
    elif isinstance(node, str):
        yield path, key, node


def validate(d):
    errors, warnings = [], []

    for k in REQUIRED_TOP:
        if k not in d:
            errors.append(f"missing required key: {k}")
    if errors:
        return errors, warnings

    language = d.get("language", "en")
    if language not in ("en", "zh"):
        errors.append(f"language must be en or zh, got {language!r}")
    if "language" not in d:
        warnings.append("language is missing, so the template will default to en")

    n = len(d["assets"])
    if n == 0:
        errors.append("assets is empty")

    for i, a in enumerate(d["assets"]):
        for k in ("emoji", "name", "verdict", "dir", "one", "qual", "factors"):
            if k not in a:
                errors.append(f"assets[{i}] missing {k}")
        if a.get("dir") not in ("bull", "bear"):
            errors.append(f"assets[{i}].dir must be bull or bear, got {a.get('dir')!r}")
        if a.get("verdict") not in ("BULLISH", "BEARISH"):
            errors.append(f"assets[{i}].verdict must be BULLISH or BEARISH")
        if (a.get("verdict") == "BULLISH") != (a.get("dir") == "bull"):
            errors.append(f"assets[{i}] verdict and dir disagree")
        if a.get("cap") not in (None, "", "capped", "bottoming"):
            errors.append(f"assets[{i}].cap must be empty, capped, or bottoming")
        if len(a.get("factors", [])) != 3:
            warnings.append(f"assets[{i}] has {len(a.get('factors', []))} factors, the format expects 3")
        for j, f in enumerate(a.get("factors", [])):
            if f.get("s") not in ("up", "down"):
                errors.append(f"assets[{i}].factors[{j}].s must be up or down")

    # matrix shape and net scores
    net = [0] * n
    for i, r in enumerate(d["matrix"]):
        c = r.get("c", [])
        if len(c) != n:
            errors.append(f"matrix[{i}] '{r.get('f')}' has {len(c)} cells, expected {n}")
            continue
        for k, cell in enumerate(c):
            if cell not in ("p", "n", "z"):
                errors.append(f"matrix[{i}] cell {k} must be p, n, or z, got {cell!r}")
            elif cell == "p":
                net[k] += 1
            elif cell == "n":
                net[k] -= 1

    # the grid must agree with the verdicts
    for i, a in enumerate(d["assets"]):
        if net[i] > 0 and a.get("dir") != "bull":
            errors.append(f"{a.get('name')} nets {net[i]:+d} on the grid but the verdict is {a.get('verdict')}")
        if net[i] < 0 and a.get("dir") != "bear":
            errors.append(f"{a.get('name')} nets {net[i]:+d} on the grid but the verdict is {a.get('verdict')}")
        if net[i] == 0:
            warnings.append(f"{a.get('name')} nets 0 on the grid, so the verdict is not supported either way")

    for i, t in enumerate(d["tiles"]):
        for k in ("lab", "val", "src", "lo", "hi", "v", "mark", "markLab", "read"):
            if k not in t:
                errors.append(f"tiles[{i}] missing {k}")
        if "lo" in t and "hi" in t and t["lo"] >= t["hi"]:
            errors.append(f"tiles[{i}] lo must be less than hi")
        if all(k in t for k in ("lo", "hi", "v")) and not (t["lo"] <= t["v"] <= t["hi"]):
            warnings.append(f"tiles[{i}] '{t.get('lab')}' value {t['v']} sits outside its band, the meter will clamp")

    for i, c in enumerate(d["calcs"]):
        for k in ("lab", "left", "op", "right", "res", "note"):
            if k not in c:
                errors.append(f"calcs[{i}] missing {k}")

    for i, s in enumerate(d["sources"]):
        if not (isinstance(s, list) and len(s) == 2):
            errors.append(f"sources[{i}] must be a [name, url] pair")

    for name in ("barChart", "lineChart"):
        c = d.get(name)
        if not c:
            continue
        if not c.get("data"):
            warnings.append(f"{name} has no data, the card will be dropped")
            continue
        if "min" not in c or "max" not in c or "ticks" not in c:
            errors.append(f"{name} needs min, max, and ticks")

    # Turbo's standing rule: no hyphen anywhere in visible copy
    for path, key, s in walk_strings(d):
        if key in HYPHEN_OK_KEYS:
            continue
        if s.startswith("http"):
            continue
        if "-" in s:
            errors.append(f"hyphen found at {path}: {s!r}  (write it out, e.g. '10 year' not '10-year')")

    return errors, warnings


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    data_path, out_path = sys.argv[1], sys.argv[2]

    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)

    errors, warnings = validate(d)
    for w in warnings:
        print(f"  WARN  {w}")
    if errors:
        for e in errors:
            print(f"  ERROR {e}")
        print(f"\n{len(errors)} error(s). Nothing written. Fix the data file and rerun.")
        sys.exit(1)

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()

    payload = json.dumps(d, ensure_ascii=False)
    # guard against breaking out of the JSON script block
    payload = payload.replace("</script", "<\\/script")

    html = tpl.replace("__DATA__", payload).replace("__TITLE__", d["title"])
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    n = len(d["assets"])
    net = [0] * n
    for r in d["matrix"]:
        for i, c in enumerate(r["c"]):
            if c == "p":
                net[i] += 1
            elif c == "n":
                net[i] -= 1
    scores = ", ".join(f"{a['name']} {net[i]:+d}" for i, a in enumerate(d["assets"]))
    print(f"  OK    wrote {out_path}")
    print(f"  net   {scores}")


if __name__ == "__main__":
    main()
