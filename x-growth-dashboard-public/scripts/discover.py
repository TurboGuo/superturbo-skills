#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find X analytics exports inside one or more folders.

Usage:
  python3 discover.py <folder> [more folders...] [--days 14]

Identifies each CSV by its HEADER ROW, not its filename, so renamed files and
files buried in subfolders are still found. Prints what it found, the date range
and row count of each, and the exact prepare.py command to run next.

Reads nothing outside the folders it is given. Makes no network calls. Writes
nothing to disk.
"""
import argparse, csv, datetime, os, sys

# Column sets that identify each export. Match is by presence, not by order,
# because X has reordered these columns before and will again.
CONTENT_KEYS = {'Post id', 'Impressions', 'Profile visits', 'New follows'}
OVERVIEW_KEYS = {'Impressions', 'Profile visits', 'New follows', 'Unfollows'}

MAX_BYTES = 64 * 1024 * 1024      # skip anything implausibly large for an export
DATE_FORMATS = ('%a, %b %d, %Y', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y')


def parse_date(s):
    s = (s or '').strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def sniff(path):
    """Return (kind, nrows, first_date, last_date) or None if not an export."""
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return None
        with open(path, newline='', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.DictReader(f)
            cols = set(reader.fieldnames or [])
            if not cols:
                return None
            # Content has Post id, overview does not. Check content first.
            if CONTENT_KEYS <= cols:
                kind = 'content'
            elif OVERVIEW_KEYS <= cols and 'Post id' not in cols:
                kind = 'overview'
            else:
                return None
            dates, n = [], 0
            for row in reader:
                n += 1
                d = parse_date(row.get('Date'))
                if d:
                    dates.append(d)
            if not n:
                return None
            return kind, n, (min(dates) if dates else None), (max(dates) if dates else None)
    except (OSError, csv.Error, UnicodeDecodeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('folders', nargs='+')
    ap.add_argument('--days', type=int, default=14,
                    help='window length to suggest, default 14')
    a = ap.parse_args()

    found = {'content': [], 'overview': []}
    scanned = 0
    for folder in a.folders:
        if not os.path.isdir(folder):
            print('  skip, not a directory: %s' % folder)
            continue
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for name in files:
                if not name.lower().endswith('.csv'):
                    continue
                path = os.path.join(root, name)
                scanned += 1
                hit = sniff(path)
                if hit:
                    kind, n, d0, d1 = hit
                    found[kind].append(dict(path=path, n=n, d0=d0, d1=d1))

    print('scanned %d csv files across %d folder(s)\n' % (scanned, len(a.folders)))

    for kind, label in (('content', 'CONTENT export, one row per post'),
                        ('overview', 'OVERVIEW export, one row per day')):
        rows = sorted(found[kind], key=lambda r: (-(r['n']), r['path']))
        print('%s  --  %d found' % (label, len(rows)))
        if not rows:
            print('  none. Export it from analytics.x.com and re run.\n')
            continue
        for i, r in enumerate(rows):
            span = ('%s to %s' % (r['d0'], r['d1'])) if r['d0'] else 'no parsable Date column'
            mark = '->' if i == 0 else '  '
            print('  %s %-58s %5d rows   %s' % (mark, r['path'], r['n'], span))
        print('')

    if not found['content'] or not found['overview']:
        sys.exit('Missing at least one required export. Cannot proceed to prepare.py.')

    c = max(found['content'], key=lambda r: r['n'])
    o = max(found['overview'], key=lambda r: r['n'])

    # Suggest a window that both files actually cover.
    ends = [d for d in (c['d1'], o['d1']) if d]
    starts = [d for d in (c['d0'], o['d0']) if d]
    if ends and starts:
        end = min(ends)
        start = max(max(starts), end - datetime.timedelta(days=a.days - 1))
        print('overlapping coverage: %s to %s' % (max(starts), end))
        print('suggested %d day window: %s to %s\n' % (a.days, start, end))
        win = '--start %s --end %s' % (start, end)
    else:
        print('Could not parse dates. Pass --start and --end yourself.\n')
        win = '--start YYYY-MM-DD --end YYYY-MM-DD'

    print('next, replace <count> with the live follower count from the profile:\n')
    print('python3 scripts/prepare.py \\\n  --content "%s" \\\n  --overview "%s" \\\n'
          '  --followers <count> %s \\\n  --out metrics.json' % (c['path'], o['path'], win))
    print('\nIf fewer than 10 posts land in that window, widen --days and say so in the footer.')


if __name__ == '__main__':
    main()
