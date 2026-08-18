#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn the two X analytics exports into metrics.json for the dashboard.

Usage:
  python3 prepare.py --content account_analytics_content_*.csv \
                     --overview account_overview_analytics*.csv \
                     --followers 1234 --start 2026-08-02 --end 2026-08-15 \
                     [--types types.json] [--titles titles.json] --out metrics.json

--followers  today's real follower count, read from the profile. There is no
             follower time series in either export, so this is the anchor the
             curve is walked back from. Do not guess it.
--types      optional {post_id: "original"|"quote"|"reply"|"article"} map.
             Get it from the X API referenced_tweets field. Without it, types
             are inferred from the text and the inference is reported.
--titles     optional {post_id: "short human title"} map. Without it the first
             60 characters of the post text are used.

The script prints every calculation it makes. Read the output before trusting it.
"""
import argparse, csv, datetime, json, sys

# ---------------------------------------------------------------- benchmarks
# Every line is external. Never score against the account's own percentiles:
# in an account where everything underperforms, the worst post still ranks median.
# See references/benchmarks.md for the sources and the reasoning.
PV = (0.20, 0.50, 1.00)   # profile visits / views, %
FC = (1.0, 3.0, 5.0)      # follows / profile visit, %  (used only to derive FR)
FR = (PV[0] * FC[0] / 100, PV[1] * FC[1] / 100, PV[2] * FC[2] / 100)   # follows / views, %
ER = (1.0, 3.0, 5.0)      # strict engagements / views, %
ER_MEDIAN = 0.70          # platform median, strict definition
REACH_BAND = (100, 500)   # views per post, 0 to 1K follower account, context only

THIN_VIEWS = 100          # below this, every ratio on the row is noise


def score(v, b):
    """Piecewise linear onto 0 to 100. 0->fair maps 0-40, fair->good 40-70,
    good->excellent 70-100, capped at 100."""
    lo, mid, hi = b
    if v <= 0:
        return 0
    if v < lo:
        return round(v / lo * 40)
    if v < mid:
        return round(40 + (v - lo) / (mid - lo) * 30)
    if v < hi:
        return round(70 + (v - mid) / (hi - mid) * 30)
    return 100


def band(s):
    return ('Good', 'good') if s >= 70 else (('Fair', 'mid') if s >= 40 else ('Weak', 'weak'))


def pdate(s):
    return datetime.datetime.strptime(s.strip(), '%a, %b %d, %Y').date()


def med(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def infer_type(text):
    t = text.strip()
    if t.startswith('@'):
        return 'reply'
    if t.startswith('https://t.co/') and len(t.split()) == 1:
        return 'article'
    if len(t) < 60:
        return 'quote'
    return 'original'


TYPE_LABEL = {'original': 'Original', 'quote': 'Quote', 'reply': 'Reply', 'article': 'Article'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--content', required=True)
    ap.add_argument('--overview', required=True)
    ap.add_argument('--followers', type=int, required=True)
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--types')
    ap.add_argument('--titles')
    ap.add_argument('--out', default='metrics.json')
    a = ap.parse_args()

    start = datetime.date.fromisoformat(a.start)
    end = datetime.date.fromisoformat(a.end)
    types = json.load(open(a.types)) if a.types else {}
    titles = json.load(open(a.titles)) if a.titles else {}

    posts, inferred = [], 0
    with open(a.content, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            d = pdate(r['Date'])
            if not (start <= d <= end):
                continue
            pid = r['Post id']
            # COLUMN ORDER TRAP: the export order is Impressions, Likes, Engagements,
            # Bookmarks, Shares, New follows, Replies, Reposts, Profile visits,
            # Detail Expands, URL Clicks. Always read by header name, never by index.
            views = int(r['Impressions'])          # on X, impressions == public views
            pv = int(r['Profile visits'])
            fol = int(r['New follows'])
            eng = int(r['Engagements'])            # inflated: X counts clicks in here
            like, rep = int(r['Likes']), int(r['Replies'])
            rt, bmk = int(r['Reposts']), int(r['Bookmarks'])
            shr, det = int(r['Shares']), int(r['Detail Expands'])
            lnk = int(r['URL Clicks'])
            strict = like + rep + rt + bmk          # the comparable definition
            if pid in types:
                typ = types[pid]
            else:
                typ = infer_type(r['Post text']); inferred += 1
            pvR = pv / views * 100 if views else 0.0
            frR = fol / views * 100 if views else 0.0
            erR = eng / views * 100 if views else 0.0
            srR = strict / views * 100 if views else 0.0
            sFR, sPV, sER = score(frR, FR), score(pvR, PV), score(srR, ER)
            posts.append(dict(
                id=pid, title=titles.get(pid, r['Post text'][:60]), date=d.isoformat(),
                url=r['Post Link'], typ=typ, typL=TYPE_LABEL[typ],
                imp=views, pv=pv, fol=fol, eng=eng, like=like, rep=rep, rt=rt,
                bmk=bmk, shr=shr, det=det, lnk=lnk, strict=strict,
                strictR=round(srR, 2), pvR=round(pvR, 2), frR=round(frR, 4), erR=round(erR, 2),
                frS=sFR, pvS=sPV, erS=sER,
                frB=band(sFR)[0], frBc=band(sFR)[1],
                pvB=band(sPV)[0], pvBc=band(sPV)[1],
                erB=band(sER)[0], erBc=band(sER)[1],
                thin=views < THIN_VIEWS))

    days = []
    with open(a.overview, newline='', encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            d = pdate(r['Date'])
            if not (start <= d <= end):
                continue
            days.append(dict(d=d.isoformat(), imp=int(r['Impressions']),
                             eng=int(r['Engagements']), pv=int(r['Profile visits']),
                             nf=int(r['New follows']), uf=int(r['Unfollows'])))
    days.sort(key=lambda x: x['d'])
    if not days:
        sys.exit('No overview rows inside the window. Check --start and --end.')

    # follower curve: anchor on the real count, walk backwards on daily net
    f = a.followers
    for i in range(len(days) - 1, -1, -1):
        days[i]['f'] = f
        f -= days[i]['nf'] - days[i]['uf']
    start_fol = f

    by_day = {}
    for p in posts:
        by_day.setdefault(p['date'], []).append(p)
    for r in days:
        r['list'] = [dict(t=p['title'], f=p['fol'], i=p['imp'], v=p['pv'])
                     for p in by_day.get(r['d'], [])]

    views = sum(p['imp'] for p in posts)
    pv = sum(p['pv'] for p in posts)
    fol = sum(p['fol'] for p in posts)
    eng = sum(p['eng'] for p in posts)
    strict = sum(p['strict'] for p in posts)
    if not views:
        sys.exit('Zero views in the window. Nothing to score.')
    pvR, frR = pv / views * 100, fol / views * 100
    erR, srR = eng / views * 100, strict / views * 100
    mv = med([p['imp'] for p in posts])
    sFR, sPV, sER = score(frR, FR), score(pvR, PV), score(srR, ER)

    acc = dict(imp=views, pv=pv, fol=fol, eng=eng, strict=strict,
               pvR=round(pvR, 2), frR=round(frR, 4), erR=round(erR, 2), strictR=round(srR, 2),
               medImp=mv, nPosts=len(posts), nThin=sum(1 for p in posts if p['thin']),
               nDays=len(days), startFol=start_fol, nowFol=a.followers,
               netFol=a.followers - start_fol,
               dayImp=sum(r['imp'] for r in days), dayNf=sum(r['nf'] for r in days),
               dayUf=sum(r['uf'] for r in days), dayPv=sum(r['pv'] for r in days),
               frS=sFR, pvS=sPV, erS=sER,
               frB=band(sFR)[0], frBc=band(sFR)[1],
               pvB=band(sPV)[0], pvBc=band(sPV)[1],
               erB=band(sER)[0], erBc=band(sER)[1],
               likes=sum(p['like'] for p in posts), replies=sum(p['rep'] for p in posts),
               reposts=sum(p['rt'] for p in posts), bookmarks=sum(p['bmk'] for p in posts))

    types_agg = {}
    for p in posts:
        t = types_agg.setdefault(p['typ'], dict(n=0, imp=0, pv=0, fol=0, strict=0, imps=[]))
        t['n'] += 1; t['imp'] += p['imp']; t['pv'] += p['pv']
        t['fol'] += p['fol']; t['strict'] += p['strict']; t['imps'].append(p['imp'])
    for k, v in types_agg.items():
        v['label'] = TYPE_LABEL[k]
        v['avg'] = round(v['imp'] / v['n'], 1)
        v['med'] = med(v['imps'])
        v['pvR'] = round(v['pv'] / v['imp'] * 100, 2) if v['imp'] else 0
        v['srR'] = round(v['strict'] / v['imp'] * 100, 2) if v['imp'] else 0

    # ------------------------------------------------------------- printout
    P = print
    P('WINDOW %s to %s   %d posts   %d days' % (start, end, len(posts), len(days)))
    if inferred:
        P('  NOTE: %d of %d post types were inferred from text, not confirmed against the API.'
          % (inferred, len(posts)))
    P('')
    P('views %d   profile visits %d   follows %d' % (views, pv, fol))
    P('likes %d   replies %d   reposts %d   bookmarks %d'
      % (acc['likes'], acc['replies'], acc['reposts'], acc['bookmarks']))
    P('')
    P('follow rate        = %d / %d = %.4f %%   -> %d/100 %s' % (fol, views, frR, sFR, acc['frB']))
    P('profile visit rate = %d / %d = %.4f %%   -> %d/100 %s' % (pv, views, pvR, sPV, acc['pvB']))
    P('engagement, strict = %d / %d = %.4f %%   -> %d/100 %s' % (strict, views, srR, sER, acc['erB']))
    P("engagement, X's own Engagements column = %d / %d = %.3f %%   (inflated by clicks, never scored)"
      % (eng, views, erR))
    P('median views per post = %g   (context band %d to %d for a 0 to 1K account)'
      % (mv, *REACH_BAND))
    P('')
    P('followers %d -> %d   net %+d over %d days' % (start_fol, a.followers,
                                                     a.followers - start_fol, len(days)))
    P('reconciliation: post level views %d vs account level %d, gap %d is traffic on posts '
      'published before %s' % (views, acc['dayImp'], acc['dayImp'] - views, start))
    P('')
    P('BY FORMAT')
    for k, v in sorted(types_agg.items(), key=lambda x: -x[1]['avg']):
        P('  %-9s n=%2d  total %5d  avg %7.1f  median %6g  visit rate %5.2f%%  strict %5.2f%%  follows %d'
          % (v['label'], v['n'], v['imp'], v['avg'], v['med'], v['pvR'], v['srR'], v['fol']))
    P('')
    P('posts under %d views: %d of %d  (every ratio on those rows is noise)'
      % (THIN_VIEWS, acc['nThin'], len(posts)))
    P('posts with zero follows: %d of %d' % (sum(1 for p in posts if p['fol'] == 0), len(posts)))
    if fol == 0:
        P('  !! Zero follows in the whole window. The follow rate tile will read 0/100 Weak on')
        P('     every row. Say plainly in the footer that this is a sample size result, not a')
        P('     verdict. At the 3%% conversion benchmark, %d profile visits predicts %.2f follows.'
          % (pv, pv * 0.03))
    if acc['reposts'] == 0 and acc['bookmarks'] == 0:
        P('  !! Zero reposts AND zero bookmarks across the whole window. This is not a sample')
        P('     size artifact. Lead the analysis with it.')

    json.dump(dict(acc=acc, posts=posts, series=days, types=types_agg,
                   bench=dict(PV=PV, FC=FC, FR=FR, ER=ER, ER_MEDIAN=ER_MEDIAN,
                              REACH=REACH_BAND, THIN=THIN_VIEWS)),
              open(a.out, 'w'), ensure_ascii=False, indent=1)
    P('\nwrote %s' % a.out)


if __name__ == '__main__':
    main()
