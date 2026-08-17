#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把小红书「笔记列表明细表」导出算成看板需要的指标。

用法:
  python3 prepare.py 笔记列表明细表.xlsx --followers 1240 --start 2026-08-02 --end 2026-08-15 --out metrics.json

输出 metrics.json，字段说明见 references/scoring.md。
本脚本只做确定性计算，不产生任何文字结论。
"""
import argparse, csv, datetime, json, os, re, sys

# 三档基准线，依据见 references/algorithm.md
TH = {
    "fan":     (0.05, 0.30, 0.90),   # 涨粉/曝光 %
    "cover":   (10.0, 20.0, 30.0),   # 观看/曝光 %
    "content": (0.5,  1.5,  3.0),    # 涨粉/观看 %
}

# CES 权重，见 references/algorithm.md。转发和评论同权重，都是 4。
CES_W = dict(like=1, save=1, cmt=4, shr=4, fol=8)

# 按表头名取列，不按位置。小红书改过导出表的列顺序，也会随账号类型给不同列，
# 写死下标迟早读错列，而读错列的结果看起来完全正常，最难发现。
# 每个字段给若干别名，命中任意一个即可；找不到的字段按 0 处理并在启动时报告。
ALIASES = {
    'title':  ['笔记标题', '标题', '笔记名称'],
    'dt':     ['首次发布时间', '发布时间', '首次发布'],
    'fmt':    ['体裁', '笔记类型', '类型'],
    'imp':    ['曝光', '曝光量', '曝光次数'],
    'views':  ['观看量', '阅读量', '观看数', '阅读数'],
    'ctr':    ['封面点击率', '点击率'],
    'like':   ['点赞', '点赞数', '赞'],
    'cmt':    ['评论', '评论数'],
    'save':   ['收藏', '收藏数'],
    'fol':    ['涨粉', '涨粉数', '新增关注', '关注数'],
    'shr':    ['分享', '分享数', '转发', '转发数'],
    'dwell':  ['人均观看时长', '平均观看时长', '观看时长'],
}
NUMERIC = ['imp', 'views', 'like', 'cmt', 'save', 'fol', 'shr', 'dwell', 'ctr']


def score(v, mid, good, exc):
    """分段线性映射到 0-100：0→中等线 = 0-40 分，中等→良好 = 40-70，良好→优秀 = 70-100。"""
    if v < mid:
        return max(0.0, v / mid * 40)
    if v < good:
        return 40 + (v - mid) / (good - mid) * 30
    return min(100.0, 70 + (v - good) / (exc - good) * 30)


def band(s):
    return ("良好", "good") if s >= 70 else (("中等", "mid") if s >= 40 else ("较弱", "weak"))


def load_rows(path):
    """读成一个二维列表。支持 .xlsx 和 .csv，导出后另存为 csv 的也能用。"""
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.csv', '.txt'):
        for enc in ('utf-8-sig', 'gbk', 'utf-16'):
            try:
                with open(path, newline='', encoding=enc) as f:
                    return [r for r in csv.reader(f)]
            except (UnicodeDecodeError, UnicodeError):
                continue
        sys.exit('读不出这个 csv 的编码，另存为 UTF-8 再试。')
    try:
        import openpyxl
    except ImportError:
        sys.exit('读 .xlsx 需要 openpyxl：pip install openpyxl --break-system-packages\n'
                 '（或者把导出表另存为 .csv，本脚本也能直接读）')
    ws = openpyxl.load_workbook(path, data_only=True).worksheets[0]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def find_header(rows):
    """定位表头行并返回 {字段: 列下标}。

    导出表首行通常是一句说明文字，表头在第二行，但这一点小红书改过，
    所以逐行找哪一行最像表头，而不是假设它在第几行。
    """
    best, best_idx, best_hit = None, -1, 0
    for i, r in enumerate(rows[:10]):
        cells = [str(c).strip() if c is not None else '' for c in r]
        idx, hit = {}, 0
        for field, names in ALIASES.items():
            for j, c in enumerate(cells):
                if c in names:
                    idx[field] = j
                    hit += 1
                    break
        if hit > best_hit:
            best, best_idx, best_hit = idx, i, hit
    if not best or 'title' not in best or 'imp' not in best:
        sys.exit('找不到表头行。需要至少有「笔记标题」和「曝光」两列。\n'
                 '如果小红书又改了表头名，把新名字加进 prepare.py 的 ALIASES 里。')
    missing = [f for f in ALIASES if f not in best]
    if missing:
        print('提示：导出表里没有这些列，按 0 处理：' + '、'.join(missing))
    return best, best_idx


def read_notes(path):
    rows = load_rows(path)
    idx, head = find_header(rows)

    def cell(r, field):
        j = idx.get(field)
        return r[j] if j is not None and j < len(r) else None

    out = []
    for r in rows[head + 1:]:
        if not r or all(x is None or str(x).strip() == '' for x in r):
            continue
        d = {f: cell(r, f) for f in ALIASES}
        m = re.match(r'(\d+)\D+(\d+)\D+(\d+)\D+(\d+)', str(d['dt'] or ''))
        if not m:
            continue
        d['date'] = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        d['hour'] = int(m.group(4))
        d['title'] = (str(d['title']).strip() if d['title'] is not None else '')
        for k in NUMERIC:
            v = str(d[k]).strip().rstrip('%') if d[k] is not None else ''
            try:
                d[k] = float(v) if v else 0.0
            except ValueError:
                d[k] = 0.0
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('export', help='笔记列表明细表，.xlsx 或 .csv')
    ap.add_argument('--followers', type=int, required=True, help='今天的真实粉丝总数，必须问用户')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--out', default='metrics.json')
    ap.add_argument('--keep-untitled', action='store_true', help='保留导出表里标题为空的笔记')
    a = ap.parse_args()

    start = datetime.date.fromisoformat(a.start)
    end = datetime.date.fromisoformat(a.end)
    allnotes = read_notes(a.export)
    win = [n for n in allnotes if start <= n['date'] <= end]
    dropped = [n for n in win if not n['title']]
    if not a.keep_untitled:
        win = [n for n in win if n['title']]
    if not win:
        sys.exit('时间窗口内没有笔记，检查 --start / --end')

    notes = []
    for i, d in enumerate(sorted(win, key=lambda x: (x['date'], x['hour']))):
        imp, views, fol = d['imp'], d['views'], d['fol']
        fanR = fol / imp * 100 if imp else 0.0
        covR = views / imp * 100 if imp else 0.0
        conR = fol / views * 100 if views else 0.0
        e = dict(
            key=str(i), title=d['title'] or '（导出无标题）', date=d['date'].isoformat(),
            hour=d['hour'], fmt=d['fmt'],
            imp=int(imp), views=int(views), fol=int(fol), like=int(d['like']),
            cmt=int(d['cmt']), save=int(d['save']), shr=int(d['shr']), dwell=int(d['dwell']),
            fanR=round(fanR, 3), covR=round(covR, 1), conR=round(conR, 3),
            fanS=round(score(fanR, *TH['fan'])),
            covS=round(score(covR, *TH['cover'])),
            conS=round(score(conR, *TH['content'])),
            coverKey=None, ratio=None, coverDesc='',
        )
        # CES 与千曝光效率。让小而精的笔记和大而空的爆款可比。
        e['ces'] = round(sum(CES_W[k] * e[k] for k in CES_W))
        e['cesK'] = round(e['ces'] / imp * 1000, 1) if imp else 0.0
        for sk, bk in [('fanS','fanB'), ('covS','covB'), ('conS','conB')]:
            e[bk], e[bk + 'c'] = band(e[sk])
        notes.append(e)

    I = sum(n['imp'] for n in notes)
    V = sum(n['views'] for n in notes)
    F = sum(n['fol'] for n in notes)
    acc = dict(imp=I, views=V, fol=F,
               fanR=round(F / I * 100, 3) if I else 0,
               covR=round(V / I * 100, 1) if I else 0,
               conR=round(F / V * 100, 3) if V else 0)
    acc['fanS'] = round(score(acc['fanR'], *TH['fan']))
    acc['covS'] = round(score(acc['covR'], *TH['cover']))
    acc['conS'] = round(score(acc['conR'], *TH['content']))
    for sk, bk in [('fanS','fanB'), ('covS','covB'), ('conS','conB')]:
        acc[bk], acc[bk + 'c'] = band(acc[sk])

    # 粉丝曲线：以今天的真实粉丝数为锚点往回推
    byd = {}
    for n in notes:
        byd.setdefault(n['date'], []).append(n)
    run = a.followers - F
    series = []
    for i in range((end - start).days + 1):
        d = (start + datetime.timedelta(i)).isoformat()
        lst = byd.get(d, [])
        run += sum(x['fol'] for x in lst)
        series.append(dict(d=d, f=run, n=len(lst),
                           list=[dict(t=x['title'], f=x['fol']) for x in lst]))
    if series[-1]['f'] != a.followers:
        sys.exit('锚点校验失败：曲线终点 %s 不等于传入的粉丝数 %s。'
                 % (series[-1]['f'], a.followers))

    zero = sum(1 for n in notes if n['fol'] == 0)
    # 页脚由脚本生成，保证每次结构一致。Claude 只能追加「数据缺口」一条，不要改写前五条。
    prod = round(acc['covR'] * acc['conR'] / 100, 3)
    foot = [
        {"k": "口径。", "v": f"粉丝转化率 = 涨粉 ÷ 曝光，标题封面吸引力 = 观看 ÷ 曝光，内容吸引力 = 涨粉 ÷ 观看。"
                          f"三者是恒等关系：粉丝转化率 = 标题封面吸引力 × 内容吸引力，"
                          f"{acc['covR']}% × {acc['conR']}% = {prod}%，可验算。"},
        {"k": "百分制怎么来的。", "v": "三档基准全部锚定外部数据，不用账号内排名。分段线性映射：0 到中等线映射到 0 至 40 分，"
                                "中等线到良好线映射到 40 至 70 分，良好线到优秀线映射到 70 至 100 分。"
                                "标题封面的中等/良好/优秀线是 10% / 20% / 30%，来自平台点击率均值 11% 与优秀线 25%；"
                                "内容吸引力是 0.5% / 1.5% / 3.0%，来自转粉率低于 0.5% 判定为关注引导缺失、"
                                "知识类初期 1.5% 算不错、健康值 3%；粉丝转化率的 0.05% / 0.30% / 0.90% 由前两者相乘推导。"},
        {"k": "粉丝曲线的做法。", "v": f"导出表没有粉丝时间序列，曲线以今天真实的 {a.followers:,} 为锚点倒推，"
                               f"每篇的累计涨粉记在首发日。总量准确，单日时点是近似。"},
        {"k": "日期。", "v": "用导出表的首次发布时间，是北京时间，所以部分笔记可能比你记忆中的发布日晚一天。"},
    ]
    if dropped and not a.keep_untitled:
        di = sum(int(n['imp']) for n in dropped); df = sum(int(n['fol']) for n in dropped)
        foot.append({"k": "剔除项。", "v": f"导出表里有 {len(dropped)} 篇标题为空，无法定位到具体笔记，"
                                       f"已从全部统计与排名中剔除（合计曝光 {di:,}、涨粉 {df}）。"
                                       f"建议去后台把真实标题补回。"})
    # 只写文件名，不写路径。写全路径会把用户的用户名和目录结构带进交付出去的 HTML。
    foot.append({"k": "数据来源。", "v": f"{os.path.basename(a.export)}，"
                                     f"处理于 {datetime.date.today().isoformat()}。"})
    meta = dict(
        title='小红书算法专家 + 专业博主诊断',
        subtitle=f"统计口径：{start.year} 年 {start.month} 月 {start.day} 日至 {end.month} 月 {end.day} 日 · "
                 f"{len(notes)} 篇笔记 · 曝光 {I:,} · 观看 {V:,}",
        folRaw=f"该时段新增关注，共 {len(notes)} 篇笔记",
        folBase=f"其中 {len(notes)-zero} 篇有涨粉，{zero} 篇为 0",
        footnotes=foot,
        dropped=[dict(dt=n['dt'].isoformat() if hasattr(n['dt'],'isoformat') else str(n['dt']),
                      imp=int(n['imp']), fol=int(n['fol'])) for n in dropped],
    )
    json.dump(dict(meta=meta, acc=acc, notes=notes, series=series),
              open(a.out, 'w'), ensure_ascii=False, indent=1)

    print(f"笔记 {len(notes)} 篇" + (f"（剔除无标题 {len(dropped)} 篇）" if dropped and not a.keep_untitled else ""))
    print(f"粉丝转化率 {acc['fanR']}% → {acc['fanS']} 分 {acc['fanB']}")
    print(f"标题封面吸引力 {acc['covR']}% → {acc['covS']} 分 {acc['covB']}")
    print(f"内容吸引力 {acc['conR']}% → {acc['conS']} 分 {acc['conB']}")
    print(f"恒等式校验：{acc['covR']}% × {acc['conR']}% = {acc['covR']*acc['conR']/100:.3f}%（应等于 {acc['fanR']}%）")
    print(f"→ {a.out}")


if __name__ == '__main__':
    main()
