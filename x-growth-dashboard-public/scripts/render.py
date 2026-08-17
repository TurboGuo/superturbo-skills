#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render metrics + per post analysis + suggestions into the single file dashboard.

Usage:
  python3 render.py --metrics metrics.json --analysis analysis.json \
                    --suggestions suggestions.json --meta meta.json \
                    --out dashboard.html

Output is one self contained HTML file. No network, no external assets.
Every input is validated before rendering, because a board with an empty cell
or a placeholder in it is worse than no board.
"""
import argparse, json, os, sys

CELLS = ['fanAlgo', 'fanBlog', 'fanFix', 'covAlgo', 'covBlog', 'covFix',
         'erAlgo', 'erBlog', 'erFix']
MAX_BULLETS = 2          # hard cap, see references/writing-guide.md


def die(msg):
    sys.exit('render.py: ' + msg)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--metrics', default='metrics.json')
    ap.add_argument('--analysis', default='analysis.json')
    ap.add_argument('--suggestions', default='suggestions.json')
    ap.add_argument('--meta', default='meta.json')
    ap.add_argument('--template')
    ap.add_argument('--out', default='dashboard.html')
    a = ap.parse_args()

    M = json.load(open(a.metrics))
    AN = json.load(open(a.analysis))
    SUG = json.load(open(a.suggestions))
    META = json.load(open(a.meta))

    tpl_path = a.template or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          '..', 'assets', 'template.html')
    if not os.path.exists(tpl_path):
        die('template not found at ' + tpl_path)

    # ------------------------------------------------------------ validation
    ids = [p['id'] for p in M['posts']]
    missing = [i for i in ids if i not in AN]
    if missing:
        die('analysis.json is missing %d posts: %s' % (len(missing), missing[:3]))
    for i in ids:
        for c in CELLS:
            v = AN[i].get(c)
            if not v:
                die('empty cell %s on post %s. Every cell needs at least one bullet.' % (c, i))
            if len(v) > MAX_BULLETS:
                die('cell %s on post %s has %d bullets, the cap is %d.' % (c, i, len(v), MAX_BULLETS))
            for b in v:
                if not any(ch.isdigit() for ch in b) and not b.lstrip().lower().startswith(
                        ('keep', 'change', 'sample too small')):
                    die('bullet in %s on post %s carries no number and no action:\n  %s'
                        % (c, i, b))
    if not (3 <= len(SUG) <= 5):
        die('suggestions.json has %d entries, the range is 3 to 5.' % len(SUG))
    for s in SUG:
        for k in ('h', 't', 'p', 's'):
            if not s.get(k):
                die('a suggestion is missing field "%s".' % k)
        if not (2 <= len(s['p']) <= 4):
            die('suggestion "%s" has %d actions, the range is 2 to 4.' % (s['h'][:40], len(s['p'])))
    for k in ('title', 'subtitle', 'intro', 'folRaw', 'footnotes'):
        if k not in META:
            die('meta.json is missing "%s".' % k)
    if len(META['footnotes']) < 5:
        die('meta.json needs at least 5 footnotes. See references/writing-guide.md.')

    DATA = dict(acc=M['acc'], posts=M['posts'], series=M['series'],
                analysis=AN, sug=SUG,
                meta=dict(title=META['title'], subtitle=META['subtitle'],
                          intro=META['intro'], folRaw=META['folRaw'],
                          folBase=META.get('folBase', '')),
                foot=META['footnotes'])

    html = open(tpl_path, encoding='utf-8').read()
    html = html.replace('__TITLE__', META['title'])
    html = html.replace('__DATA__', json.dumps(DATA, ensure_ascii=False))
    open(a.out, 'w', encoding='utf-8').write(html)
    print('wrote %s  %.1f KB  (%d posts, %d suggestions, %d footnotes)'
          % (a.out, len(html.encode()) / 1024, len(ids), len(SUG), len(META['footnotes'])))


if __name__ == '__main__':
    main()
