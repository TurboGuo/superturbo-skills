# data.json reference

Read `example-data.json` alongside this. The example is a complete, validated
payload and is usually faster to copy than to build from this table.

Every string is rendered as prose, so **no hyphen character in any of them**.
URLs in `sources` are the only exception. `build.py` hard fails on a violation.

Any string field marked **md** supports `**like this**`, which renders the
wrapped text as an emphasised number.

## Top level

| Key | Type | Notes |
|---|---|---|
| `language` | string | `zh` for a fully Chinese dashboard or `en` for English. The template defaults to `en` only for backward compatibility |
| `title` | string | Page and browser tab title |
| `stamp` | string | Datestamp line. Include the time and the day's driver, e.g. "As of Wednesday, August 19, 2026, 2:25pm ET, hours after Treasury doubled its long end buybacks." |
| `regime` | string | Two or three words, e.g. "late cycle repression" |
| `banner` | string **md** | One short paragraph on the single thing that set today's tone |
| `assets` | array | One per asset class, in Turbo's order: US Stocks, US Cash, Gold, Crypto |
| `matrix` | array | Factor grid rows |
| `tiles` | array | Master signal stat tiles |
| `calcs` | array | Worked calculation steps |
| `barChart` | object or omitted | Diverging bar chart |
| `lineChart` | object or omitted | Line chart with a reference line |
| `sources` | array | `[name, url]` pairs |

## assets[]

| Key | Type | Notes |
|---|---|---|
| `emoji` | string | 📊 stocks, 💵 cash, 🥇 gold, ₿ crypto |
| `name` | string | Display name |
| `verdict` | string | Machine value `BULLISH` or `BEARISH`. Keep it in English even for Chinese output because the template localizes it |
| `dir` | string | `bull` or `bear`, must agree with `verdict` |
| `cap` | string | Machine value `capped`, `bottoming`, or `""` for none. Keep it in English even for Chinese output because the template localizes it |
| `one` | string **md** | One line summary for the scoreboard block |
| `qual` | string | Longer qualifier line on the detail card, e.g. "capped, valuation leaves no room for an earnings miss" |
| `factors` | array of 3 | See below |

`factors[]`: `{ "s": "up" or "down", "h": "Factor headline", "b": "one sentence **md**" }`

Two `up` and one `down` is the usual shape. Mark the odd one out `(offset)` in
its headline. Each `b` is exactly one sentence and must contain a live number.

## matrix[]

`{ "f": "Factor name", "r": "current reading", "c": ["p", "z", "z", "n"] }`

`c` has one cell per asset, in the same order as `assets`. `p` bullish, `n`
bearish, `z` not a driver of that asset. Blanks are deliberate, only score a
factor where the framework says it drives that asset.

Net scores are computed from this array at render time and are never typed
anywhere. `build.py` fails if a net score contradicts its asset's verdict, which
is the main thing keeping the top of the page honest against the bottom.

## tiles[]

| Key | Type | Notes |
|---|---|---|
| `lab` | string | Signal name |
| `val` | string | Formatted headline value, e.g. `"2.44%"`, `"275 bp"`, `"$68,000"` |
| `src` | string | Source and observation date. FRED runs a day or two behind, so state the observation date, not today's |
| `lo` / `hi` | number | The band the meter spans. Pick a plausible trading range, not the all time range |
| `v` | number | The raw value, used to fill the meter |
| `mark` | number | Where the tick goes: the level that flips the signal |
| `markLab` | string | Short label under the tick, e.g. `"2.00"`, `"50"`, `"200d"`, `"target"` |
| `spark` | array of numbers | 3 to 5 recent observations, oldest first. `[]` to omit |
| `read` | string | One sentence on what the level means |

## calcs[]

`{ "lab": "...", "left": "4.72", "op": "minus", "right": "2.30", "res": "2.42 percent", "note": "..." }`

Renders as `4.72 minus 2.30 = 2.42 percent`. `op` is prose ("minus", "divided
by"), never a symbol. Always include the 10 year real yield and the real yield on
cash. Add any other derived figure quoted elsewhere on the page.

## barChart

Diverging bars around a zero baseline. Good for flows, weekly changes, or
surprise versus consensus.

| Key | Notes |
|---|---|
| `title`, `sub` | Card heading and subheading |
| `unit` | Prefix in the tooltip, e.g. `"$"` |
| `min`, `max` | Y domain. Leave only a little empty space on the unused side |
| `ticks` | Array of tick values, must include 0 |
| `note` | Optional footnote under the plot |
| `itemHeader`, `valueHeader` | Table view column headings |
| `extraRows` | Optional `[label, value]` string pairs appended to the table view |
| `data` | `[{ "label": "Mon Aug 10", "value": -114.1 }]` |

## lineChart

Single series against a reference line. Good for PMI against 50, CPI against
target, a yield against a threshold.

| Key | Notes |
|---|---|
| `title`, `sub` | Card heading and subheading |
| `seriesName` | Used in the tooltip |
| `min`, `max`, `ticks` | Y domain and ticks |
| `refLine` | Value that gets the emphasised rule, e.g. `50` |
| `refLabel` | Label beside it, e.g. `"50, expansion above"` |
| `itemHeader`, `valueHeader` | Table view column headings |
| `data` | `[{ "label": "Jul", "value": 55.6 }]`, oldest first. The last point is auto labelled |

Omit either chart, or leave its `data` empty, and the card is dropped.
