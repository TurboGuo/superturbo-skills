#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在一个或多个文件夹里找出小红书的「笔记列表明细表」导出。

用法:
  python3 discover.py <文件夹> [更多文件夹...] [--days 14]

按**表头内容**认文件，不按文件名，所以改过名、下载了好几份、混在一堆
别的表格里，都还能找出来。同时会顺带把封面图目录报出来。

只读。不改任何文件，不联网。
"""
import argparse, csv, datetime, os, re, sys

NEED = ['笔记标题', '曝光']
NICE = ['观看量', '涨粉', '首次发布时间', '点赞', '收藏', '评论', '分享']
IMG_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.heic'}
MAX_BYTES = 64 * 1024 * 1024


def header_cells(path):
    """返回前 10 行里的所有单元格文本，读不出来就返回 None。"""
    ext = os.path.splitext(path)[1].lower()
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return None
        if ext in ('.csv', '.txt'):
            for enc in ('utf-8-sig', 'gbk', 'utf-16'):
                try:
                    with open(path, newline='', encoding=enc) as f:
                        r = csv.reader(f)
                        return [[str(c).strip() for c in row] for _, row in zip(range(10), r)]
                except (UnicodeDecodeError, UnicodeError):
                    continue
            return None
        if ext == '.xlsx':
            import openpyxl
            ws = openpyxl.load_workbook(path, data_only=True, read_only=True).worksheets[0]
            out = []
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                if i >= 10:
                    break
                out.append([str(c).strip() if c is not None else '' for c in row])
            return out
    except Exception:
        return None
    return None


def sniff(path):
    rows = header_cells(path)
    if not rows:
        return None
    flat = [c for row in rows for c in row]
    if not all(any(n == c for c in flat) for n in NEED):
        return None
    extras = sum(1 for n in NICE if any(n == c for c in flat))
    dates = []
    for row in rows:
        for c in row:
            m = re.match(r'(\d{4})\D+(\d{1,2})\D+(\d{1,2})', c or '')
            if m:
                try:
                    dates.append(datetime.date(*map(int, m.groups())))
                except ValueError:
                    pass
    return dict(path=path, extras=extras, sample_dates=dates)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('folders', nargs='+')
    ap.add_argument('--days', type=int, default=14)
    a = ap.parse_args()

    hits, covers, scanned = [], {}, 0
    for folder in a.folders:
        if not os.path.isdir(folder):
            print('  跳过，不是目录：%s' % folder)
            continue
        for root, dirs, files in os.walk(folder):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            nimg = 0
            for name in files:
                if name.startswith('.'):
                    continue
                p = os.path.join(root, name)
                ext = os.path.splitext(name)[1].lower()
                if ext in IMG_EXT:
                    nimg += 1
                    continue
                if ext not in ('.xlsx', '.csv', '.txt'):
                    continue
                scanned += 1
                hit = sniff(p)
                if hit:
                    hits.append(hit)
            if nimg >= 3:
                covers[root] = nimg

    print('扫了 %d 个表格文件\n' % scanned)

    print('笔记列表明细表  --  找到 %d 份' % len(hits))
    if not hits:
        print('  一份都没有。到创作者中心 → 数据中心 → 笔记数据 → 导出，'
              '拿到「笔记列表明细表」再来。\n')
        sys.exit('没有可用的导出文件。')
    hits.sort(key=lambda h: -h['extras'])
    for i, h in enumerate(hits):
        mark = '->' if i == 0 else '  '
        span = ''
        if h['sample_dates']:
            span = '  样本日期 %s 起' % min(h['sample_dates'])
        print('  %s %-56s 认出 %d 个可选列%s' % (mark, h['path'], h['extras'], span))
    print('')

    if covers:
        print('可能是封面图的目录：')
        for d, n in sorted(covers.items(), key=lambda x: -x[1])[:5]:
            print('     %-56s %d 张图' % (d, n))
        print('  封面文件名要和 metrics.json 里的 coverKey 对上，渲染时用 --covers 指过去。\n')
    else:
        print('没找到封面图目录。没有封面也能出看板，但封面分析只能用点击率反推，'
              '要在页脚注明。\n')

    end = datetime.date.today()
    start = end - datetime.timedelta(days=a.days - 1)
    print('接下来，把 <粉丝总数> 换成主页上的真实粉丝数：\n')
    print('python3 scripts/prepare.py "%s" \\\n  --followers <粉丝总数> '
          '--start %s --end %s \\\n  --out metrics.json' % (hits[0]['path'], start, end))
    print('\n窗口内不足 8 篇笔记就把 --days 放宽到 30，并在页脚说明原因。')


if __name__ == '__main__':
    main()
