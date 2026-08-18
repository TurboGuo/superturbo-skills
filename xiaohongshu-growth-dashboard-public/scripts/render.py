#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把指标 + 逐篇诊断 + 总建议渲染成单文件 HTML 看板。

用法:
  python3 render.py --metrics metrics.json --analysis analysis.json \
                    --suggestions suggestions.json --covers covers/ --out dashboard.html

covers/ 可选，里面放封面图，文件名用 metrics.json 里的 coverKey，例如 covers/note-3.jpg。
脚本会自动缩成缩略图并内联成 data URL，保证输出是单文件。
"""
import argparse, base64, io, json, os, sys


def thumbs(folder, notes):
    if not folder or not os.path.isdir(folder):
        return {}
    try:
        from PIL import Image
    except ImportError:
        print('提示：未安装 Pillow，跳过封面缩略图。pip install pillow --break-system-packages')
        return {}
    out = {}
    for n in notes:
        k = n.get('coverKey')
        if not k:
            continue
        for ext in ('.jpg', '.jpeg', '.png', '.webp'):
            p = os.path.join(folder, k + ext)
            if os.path.exists(p):
                im = Image.open(p).convert('RGB')
                n['ratio'] = round(im.size[0] / im.size[1], 2)
                im.thumbnail((240, 320))
                buf = io.BytesIO()
                im.save(buf, 'JPEG', quality=72)
                out[k] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
                break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--metrics', required=True)
    ap.add_argument('--analysis', required=True)
    ap.add_argument('--suggestions', required=True)
    ap.add_argument('--covers', default=None)
    ap.add_argument('--template', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'template.html'))
    ap.add_argument('--out', default='dashboard.html')
    a = ap.parse_args()

    M = json.load(open(a.metrics))
    AN = json.load(open(a.analysis))
    SUG = json.load(open(a.suggestions))

    if not (3 <= len(SUG) <= 5):
        sys.exit(f'总建议必须是 3 到 5 条，当前 {len(SUG)} 条')

    missing = [n['title'] for n in M['notes'] if n['title'] not in AN]
    if missing:
        sys.exit('以下笔记缺少诊断，请补齐 analysis.json：\n  ' + '\n  '.join(missing))

    need = ['fanAlgo','fanBlog','fanFix','covAlgo','covBlog','covFix','conAlgo','conBlog','conFix']
    for t, v in AN.items():
        for k in need:
            if k not in v or not isinstance(v[k], list) or not v[k]:
                sys.exit(f'「{t}」的 {k} 缺失或不是非空数组')

    TH = thumbs(a.covers, M['notes'])
    data = dict(meta=M['meta'], acc=M['acc'], notes=M['notes'],
                series=M['series'], analysis=AN, thumbs=TH, sug=SUG)
    html = open(a.template).read().replace('__DATA__', json.dumps(data, ensure_ascii=False))
    open(a.out, 'w').write(html)
    print(f'{len(M["notes"])} 篇笔记 · {len(SUG)} 条建议 · {len(TH)} 张封面 → {a.out}（{len(html)//1024} KB）')


if __name__ == '__main__':
    main()
