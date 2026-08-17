# 可复制的 HTML 片段

放进 `suggestions.json` 的 `demo` 字段。**直接复制，不要重新发明**，模板里的 CSS 只认这些类名。

## 封面反面示例

经验是反面示例比正面示例有用。好封面的吸引力画不出来，直接在 bullet 里点名用户自己点击率最高的那几篇，让他翻原图。

用几个就留几个 `<div class="dm">…</div>`，其余删掉。每个 `.dm` 必须是 `dmslot > dmbox` 加一个 `dmcap`，结构不能改。

### A. 大字压在密集小字上（糊）

```html
<div class="dm"><div class="dmslot"><div class="dmbox"><div class="dense"></div>
<div class="bigred blurred">这里放<br>用户的真实标题</div></div></div>
<div class="dmcap"><span class="no">✗</span> 红字压在密集小字上，缩略图下糊掉。点击率 X.X%</div></div>
```

### B. 超宽横图（两头被裁）

```html
<div class="dm"><div class="dmslot"><div class="dmbox wide"><div class="shot"></div>
<div class="crop l"></div><div class="crop r"></div>
<div class="bigred" style="font-size:10px">真实标题</div></div></div>
<div class="dmcap"><span class="no">✗</span> X.XX:1 超宽横图，双列流里两头被裁。点击率 X.X%</div></div>
```

### C. 深色底上的低对比大字

```html
<div class="dm"><div class="dmslot"><div class="dmbox" style="background:#2b3a34">
<div class="bigred" style="color:#c0392b">真实标题</div></div></div>
<div class="dmcap"><span class="no">✗</span> 红字压在深色图上，对比度不足。点击率 X.X%</div></div>
```

### 正面示例（一般不用，确有需要时才加）

```html
<div class="dm"><div class="dmslot"><div class="dmbox"><div class="shot"></div>
<div class="bigred">真实截图<br>加三行<br>红色大字</div></div></div>
<div class="dmcap"><span class="yes">✓</span> 真实截图 + 大字落在留白处。点击率 X.X%</div></div>
```

```html
<div class="dm"><div class="dmslot"><div class="dmbox"><div class="plainbg"></div>
<div class="bigink">纯色底<br>三行黑字<br>3:4 竖版</div></div></div>
<div class="dmcap"><span class="yes">✓</span> 纯色底 + 三行黑字。点击率 X.X%</div></div>
```

## 组装

外层固定这样写，标题行必须有：

```html
<div class="demolbl">以下两种一律不要做</div>
<div class="demo">
  …若干个 .dm…
</div>
```

## 可用类名清单

| 类 | 作用 |
|---|---|
| `.demolbl` | 示意图上方的一行小标题 |
| `.demo` | 横向排列容器 |
| `.dm` | 单张示意（宽 118px） |
| `.dmslot` | 固定 157px 高，保证所有 caption 对齐，**不能省** |
| `.dmbox` | 3:4 画框 |
| `.dmbox.wide` | 47px 高的横图画框 |
| `.shot` | 截图纹理背景 |
| `.dense` | 密集小字纹理背景 |
| `.plainbg` | 米色纯底 |
| `.bigred` | 红色大字 |
| `.bigink` | 深色大字 |
| `.blurred` | 加在 `.bigred` 上表示看不清 |
| `.crop.l` / `.crop.r` | 左右裁切斜纹 |
| `.dmcap` | 图下说明 |
| `.dmcap .yes` / `.no` | 绿勾 / 红叉 |
