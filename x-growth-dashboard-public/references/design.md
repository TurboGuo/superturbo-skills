# Visual spec

The template already implements all of this. Read it when changing something,
or when rebuilding the board somewhere else.

**Note on the two type blocks.** `template.html` declares a base set of sizes and
then a second block near the end that overrides most of them upward. The type
table below matches the **second** block, which is what actually renders. If you
change a size, change it in the override block, not the base one.

## Layout, top to bottom

```
Title
  bullet: Algo analysis:            what the ranking model does
  bullet: Professional influencer:  where the practitioner numbers come from
  subtitle: window, post count, headline totals
  [Dark / Light button, top right]

┌───────────────────────┬───────────────────────┐
│ Net followers gained  │ Follow rate      /100 │   .r1
├───────────────────────┼───────────────────────┤
│ Profile visit rate /100│ Engagement rate /100 │   .r2
└───────────────────────┴───────────────────────┘

Card: Total followers and per post performance
  panel 1  thick follower curve, daily
  panel 2  follows per post
  panel 3  three per post scores, 0/40/70/100 gridlines
  shared date axis, table view in a <details>

Card: Overall suggestions        <- ABOVE the post table, deliberately
Card: Post by post               <- overview table + 3 dimension tabs
Footer
```

Four tiles. Not five, not six. The absolute follower number goes first because it
is the only figure that needs no benchmark to interpret.

## Colour

CSS custom properties on `.viz-root`, light and dark defined together. Dark mode
follows the OS by default and the button overrides with `data-theme`.

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--plane` | `#f9f9f7` | `#0d0d0d` | page background |
| `--surface` | `#fcfcfb` | `#1a1a19` | cards and tiles |
| `--ink1` | `#0b0b0b` | `#ffffff` | primary text |
| `--ink2` | `#52514e` | `#c3c2b7` | body text |
| `--muted` | `#898781` | `#898781` | labels, footnotes |
| `--grid` | `#e1e0d9` | `#2c2c2a` | minor gridlines |
| `--axis` | `#c3c2b7` | `#383835` | axis and threshold lines |
| `--ring` | `rgba(11,11,11,.10)` | `rgba(255,255,255,.10)` | borders |
| `--s1` | `#2a78d6` | `#3987e5` | series 1, follower curve and follow rate |
| `--s2` | `#eb6834` | `#d95926` | series 2, profile visit rate |
| `--s3` | `#1baf7a` | `#199e70` | series 3, engagement rate |
| `--s4` | `#4a3aa7` | `#9085e9` | series 4, follows per post |
| `--good` | `#0ca30c` | same | Good pill and chip |
| `--warn` | `#fab219` | same | Fair pill, ink `#3a2c00` |
| `--bad` | `#d03b3b` | same | Weak pill and chip |

Four categorical series maximum. They are distinguishable in both modes and for
the common colour vision deficiencies. If you change one, re-check all four
against each other and against both backgrounds, not just against white.

Score colour is by **band**, never by rank. A red chip always means under 40.

## Type

System stack: `system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif`.

| Element | Size | Notes |
|---|---|---|
| `h1` | 20px / 650 | |
| `.intro li` | 15.5px / 1.9 | the two basis bullets |
| `.sub` | 13px | window and totals line |
| `.card h2` | 16.5px / 640 | |
| `.card .note` | 13.5px / 1.7 | |
| `.tile .lbl` | 13px, muted | metric name and formula |
| `.score` | 34px / 650 | the number |
| `.of` | 15px, muted | the "/100" |
| `.pill` | 11.5px / 650 | Good, Fair, Weak |
| `.tile .raw` | 14px, tabular | raw counts under the score |
| `.tab` | 14.5px | |
| `.ovw` | 14px, header 12.5px | overview table |
| `.ptit` | 15px / 640 | post title in a card |
| `.psc` | 20px / 650 | per post score |
| `.dbox .k / .v` | 11.5 / 16px | data boxes |
| `.tagline` | 12.5px, muted, tracked | the three cell labels |
| `.blk` | 15.5px / 1.85 | per post bullets, the main reading size |
| `.shead` | 15.5px / 645 | suggestion heading |
| `.trig` | 13.5px / 1.7 | trigger box |
| `.sug ul` | 14.5px / 1.8 | suggestion steps |
| `.src` | 12.5px, muted | sources line |
| `.foot` | 12.5px / 1.85 | footnotes |

`font-variant-numeric: tabular-nums` on every number so columns line up.

**Do not ship at the smaller sizes a generic dashboard template ships with.** The
per post cells are the product and they need to be comfortable to read.

## Tables

Both tables wrap in `<div class="tw">` with `overflow-x:auto`, `min-width:720px`
on `.ovw` and `760px` on `table.tv`, `white-space:nowrap` on every cell, and
`max-width:300px` plus ellipsis on the title cell only.

Without nowrap the date column breaks "Aug 10" across two lines and the whole
table reads as broken. This is the first thing anyone notices.

## Chart

- `viewBox="0 0 1000 436"`, width 100%, margins `l:56 r:132 t:16 b:40`.
- Panel heights 132 / 62 / 126, gap 16 plus 14 for the panel label.
- Follower curve `stroke-width:3.5` with an end dot and an end label. Everything
  else is `1.6` to `1.8` with 3.2 radius dots.
- Score panel draws gridlines at 0, 40, 70, 100 with 40 and 70 in `--axis` and
  labelled Fair and Good inline.
- Posts sharing a date spread sideways across 85% of a day slot.
- End labels de-collide by pushing down 15px, then the whole group shifts up if it
  would cross the axis.
- One opaque tooltip, `position:fixed`, clamped to the viewport. The top two
  panels show the day, the bottom panel shows the nearest post.

## Interaction

- Overview table sorts on any header, ascending and descending.
- Four tabs: overview plus one per dimension. Dimension tabs render all posts
  expanded, sorted by that dimension's score, with a direction toggle.
- Every post card links out to the post on X.
- Dark mode toggle redraws the SVG so stroke colours pick up the new variables.
- No `localStorage`, no network calls, no external fonts or scripts. The file must
  work offline from `file://`.
