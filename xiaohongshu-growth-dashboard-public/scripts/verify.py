#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交付前的结构自检。

用法:
  python3 verify.py dashboard.html

只做机械检查，不判断文字质量。有 FAIL 就不要交付。
"""
import json, re, sys


def main():
    if len(sys.argv) < 2:
        sys.exit('用法: python3 verify.py dashboard.html')
    html = open(sys.argv[1]).read()

    m = re.search(r'const D=(\{.*?\}), ACC=D\.acc', html, re.S)
    if not m:
        sys.exit('FAIL 找不到注入的数据，模板可能被改坏了')
    D = json.loads(m.group(1))
    notes, acc, AN, SUG, META = D['notes'], D['acc'], D['analysis'], D['sug'], D['meta']

    ok, bad = [], []
    def chk(cond, msg):
        (ok if cond else bad).append(msg)

    # 结构
    for cls, name in [('r1','第一行指标'), ('r2','第二行指标'), ('id="main"','合并图'),
                      ('data-k="ovw"','涨粉总览标签'), ('data-k="fan"','粉丝转化率标签'),
                      ('data-k="cov"','标题封面标签'), ('data-k="con"','内容吸引力标签'),
                      ('id="sug"','总建议'), ('id="foot"','页脚'), ('id="bTheme"','明暗切换')]:
        chk(cls in html, f'区块 {name}')
    chk(html.count('.dmslot') >= 1, 'CSS 里有封面示意类')
    chk('__DATA__' not in html, '数据已注入（没有残留占位符）')

    # 恒等式
    prod = round(acc['covR'] * acc['conR'] / 100, 3)
    chk(abs(prod - acc['fanR']) <= 0.01,
        f"恒等式 {acc['covR']}% × {acc['conR']}% = {prod}%，账号级 {acc['fanR']}%")

    # 分档与分数一致
    def band(s): return 'good' if s >= 70 else ('mid' if s >= 40 else 'weak')
    for k in ['fan','cov','con']:
        chk(acc[k+'Bc'] == band(acc[k+'S']), f'账号级 {k} 分档与分数一致')
    chk(all(n[k+'Bc'] == band(n[k+'S']) for n in notes for k in ['fan','cov','con']),
        '每篇的分档与分数一致')

    # 建议
    chk(3 <= len(SUG) <= 5, f'总建议 {len(SUG)} 条（要求 3 到 5）')
    for i, s in enumerate(SUG, 1):
        chk(all(x in s for x in ('h','t','p','s')), f'建议 {i} 字段齐全')
        chk(not s.get('h','').rstrip().endswith(('。','.')), f'建议 {i} 标题不带句号')
        chk(1 <= len(s.get('p', [])) <= 4, f'建议 {i} 做法 1 到 4 条')
        chk('<b>' in s.get('t',''), f'建议 {i} 触发数字有加粗')
        chk('依据' in s.get('s',''), f'建议 {i} 写了依据')
        if s.get('demo'):
            chk(s['demo'].count('dmslot') == s['demo'].count('class="dm"'),
                f'建议 {i} 的封面示意结构完整')

    # 逐篇诊断
    need = ['fanAlgo','fanBlog','fanFix','covAlgo','covBlog','covFix','conAlgo','conBlog','conFix']
    for n in notes:
        t = n['title']
        if t not in AN:
            bad.append(f'「{t[:16]}」缺诊断'); continue
        v = AN[t]
        for k in need:
            arr = v.get(k)
            if not isinstance(arr, list) or not arr:
                bad.append(f'「{t[:16]}」的 {k} 为空'); continue
            if len(arr) > 3:
                bad.append(f'「{t[:16]}」的 {k} 超过 3 条')
            if k.endswith('Fix'):
                pre = '保持：' if n[k[:3]+'S'] >= 40 else '修改：'
                if not arr[0].startswith(pre):
                    bad.append(f'「{t[:16]}」的 {k} 应以「{pre}」开头（当前分数 {n[k[:3]+"S"]}）')
    chk(all(t in AN for t in [n['title'] for n in notes]), f'{len(notes)} 篇诊断齐全')

    # 页脚
    keys = [f['k'] for f in META.get('footnotes', [])]
    for k in ['口径。','百分制怎么来的。','粉丝曲线的做法。','日期。','数据来源。']:
        chk(k in keys, f'页脚有「{k.rstrip("。")}」')

    for m_ in ok:
        print('  PASS', m_)
    for m_ in bad:
        print('  FAIL', m_)
    print(f'\n{len(ok)} 项通过，{len(bad)} 项失败')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
