---
name: macro-dashboard
description: Build Turbo's visual Macro Impact Dashboard as a self contained HTML page and publish it as an artifact. Pulls live macro data, scores each asset class against a fixed factor framework, and renders a localized two tab dashboard. Use for explicit dashboard requests in English or Chinese and for any Chinese request asking for current macro analysis or its impact on assets, including 给我宏观分析, 宏观怎么看, 宏观对资产有什么影响, 宏观环境, 宏观仪表盘, and 宏观影响看板. Chinese macro requests default to a fully Chinese dashboard even when the word dashboard is absent. Use the separate macro-impact skill only when the user explicitly requests a plain text or text only response.
---

# Macro Impact Dashboard

Produce a dashboard answering one question: is the CURRENT macro environment
bullish or bearish for each asset class Turbo holds. Output is an HTML file plus
a published artifact, never a text only reply.

This skill is **self contained**. It is usually the first thing invoked in a fresh
session, so it gathers its own data. Do not assume any earlier macro read exists.

## Routing and default format

Treat the language of the user's deliverable request as a format preference.

- If the request is in Chinese and asks for a current macro analysis, macro view,
  macro environment, or macro impact on any covered asset, invoke this skill and
  return a fully Chinese dashboard by default. The user does not need to say
  `dashboard`, `仪表盘`, or `看板`.
- Examples that must route here include `给我宏观分析`, `宏观怎么看`,
  `分析一下当前宏观`, `宏观对美国资产的影响`, and `现在宏观利多什么`.
- Route a Chinese request to the text only `macro-impact` skill only when the user
  explicitly says `文字版`, `纯文本`, `只要文字`, `简短文字`, `不要 dashboard`,
  `不要 HTML`, or otherwise clearly rejects a dashboard.
- For English requests, preserve the existing distinction: generic macro reads are
  text, while explicit dashboard or visual requests use this skill.

## Step 0, decide whether to re fetch

If a `macro-impact` text read was already produced **earlier in this same
conversation**, reuse those numbers and skip to step 2. Otherwise run step 1.
Never answer from memory or from a cached verdict.

## Step 1, gather the data

Use **Exa** for every web search (`mcp__exa__web_search_exa`,
`mcp__exa__web_fetch_exa`). Prefer OFFICIAL primary sources: the Federal Reserve
(H.15, FOMC), FRED, the US Treasury, BLS (CPI), BEA (PCE), ISM (PMI), Cboe (VIX),
the World Gold Council, and issuer or on chain data for flows. Fall back to a
third party only when the official source is unavailable, lagged, or does not
carry the figure, and only to an established outlet (Bloomberg, Reuters, CNBC,
FT, WSJ, ICE, S&P, Morningstar, Trading Economics, FXStreet, Kitco).
Never cite a random blog, forum, or unvetted aggregator as the source of a number.

Batch these fetches in as few calls as possible. `web_fetch_exa` takes several
URLs at once, so pull the FRED series in one call.

**Master signals** (fetch every run):

| Signal | Source |
|---|---|
| 10 year real yield | `https://fred.stlouisfed.org/series/DFII10` |
| 10 year nominal yield | `https://fred.stlouisfed.org/series/DGS10` |
| 10 year breakeven | `https://fred.stlouisfed.org/series/T10YIE` |
| High yield OAS | `https://fred.stlouisfed.org/series/BAMLH0A0HYM2` |
| 3 month T bill | `https://fred.stlouisfed.org/series/DGS3MO` |
| Fed funds effective | `https://fred.stlouisfed.org/series/DFF` |
| VIX | `https://fred.stlouisfed.org/series/VIXCLS` |
| S&P 500 | `https://fred.stlouisfed.org/series/SP500` |

Each FRED page prints the latest observation plus the previous four, which is
exactly the five point sparkline the tiles want. Record the observation date, not
today's date, because FRED runs a day or two behind.

Then search for the rest:

- Core CPI and headline CPI year over year, latest BLS release
- ISM Manufacturing PMI, latest month, plus the trailing 12 months for the line chart
- Fed funds target range and the next meeting's hike or cut odds
- DXY level and today's change
- Per asset: BTC price versus its 50, 100, and 200 day averages, spot BTC ETF
  flows, on chain or whale positioning; S&P 500 level, distance from its record,
  trailing and forward P/E; spot gold versus its 200 day, plus the live safe
  haven or geopolitical driver
- Anything that moved markets **today**, since a single policy or geopolitical
  event often reprices every asset at once and belongs in the banner line

**Cross check X for crypto and for any product or flow sentiment.** Use
`mcp__remote-devices__opentwitter__search_twitter_advanced` with
`exclude_retweets: true` and a `min_likes` floor around 30 so only posts with
traction come back. Glassnode, on chain desks, and macro accounts reacting to
the day's driver are the useful signal.

If a data point cannot be fetched, say so in that factor rather than guessing,
and still give the verdict from the factors you do have.

## Step 2, score each asset

Default coverage is four assets in this fixed order. **This order is Turbo's and
overrides any other ordering.**

1. US Stocks
2. US Cash
3. Gold
4. Crypto

If Turbo names a subset, cover only those, keeping the relative order.

Score each factor `+1` when it is bullish for that asset right now and `-1` when
bearish, based on its current direction and level. A factor only scores where it
actually drives that asset. Leave the rest blank, do not force a cell.

**US Stocks** (a claim on earnings, sensitive to the discount rate)

| Factor | Bullish when | Bearish when |
|---|---|---|
| Growth, ISM PMI | above 50 and firm | below 50 |
| Credit spreads | tight | widening |
| Rates, 10 year | stable or falling | rising fast |
| VIX | low or normal | rising or elevated |
| Valuation, P/E and resistance | cheap | stretched or stalled |

**US Cash** (T bills, money market)

| Factor | Bullish when | Bearish when |
|---|---|---|
| Fed funds level and bias | high, held, hawkish | cutting fast |
| Real yield on cash | positive | negative |
| Risk backdrop | risk off, other assets below trend | strong risk on |

**Gold** (a non yielding monetary asset)

| Factor | Bullish when | Bearish when |
|---|---|---|
| Real yields | falling or low | rising or high |
| Dollar, DXY | weak | strong |
| Inflation expectations, breakevens | rising | falling |
| Safe haven and geopolitics | elevated risk | calm |

**Crypto** (the highest beta liquidity asset)

| Factor | Bullish when | Bearish when |
|---|---|---|
| Real yields | falling or low | rising or high |
| Dollar, DXY | weak or falling | strong or rising |
| Fed and liquidity | easing, cutting | hawkish, hiking, tight |
| Credit spreads | tight or tightening | widening |
| ETF flows, whales, on chain | inflows, accumulation | outflows |
| Trend | above key EMAs | below key EMAs |

Net the dominant factors to one word: net positive is `BULLISH`, net negative is
`BEARISH`. Add ONE qualifier only when it is true:

- `capped` when bullish but valuation, resistance, or policy limits the upside
- `bottoming` when bearish but flows or on chain show the downside being absorbed

**A factor that moves several assets at once gets one row, not four.** A policy
event, a dollar move, or a liquidity shift belongs in a single row with cells in
each column it touches. Do not split it, and do not stack four separate risk
rows against cash when the framework calls that one "risk backdrop", or the
score will drift away from the framework.

Show the arithmetic for anything derived. At minimum:

- 10 year real yield = nominal minus breakeven, cross checked against DFII10
- Real yield on cash = 3 month T bill minus core CPI, and again versus headline CPI

## Step 3, write the data file

Write a `data.json`. The full field reference is in
`reference/data-schema.md` and a filled in example is
`reference/example-data.json` — read the example first, it is faster than the
schema for getting the shape right.

Set the top level `language` field before writing any visible copy:

- Use `"zh"` when the user's request is in Chinese or explicitly asks for Chinese.
- Use `"en"` for English requests unless the user explicitly chooses Chinese.
- If a request mixes languages, follow the language of the actual deliverable request.

Rules that matter while writing it:

- **No hyphen character anywhere in visible text.** Write "10 year", "T bill",
  "risk on", "late cycle", "year over year". The build script hard fails on a
  hyphen, so this is enforced, not advisory. URLs are exempt.
- Wrap every live number in `**` so it renders emphasised: `at **2.44%** the`.
- One factor per bullet, one sentence each, and the sentence must carry a
  concrete number. Never chain two data points into one sentence.
- Pick the three most decisive factors per asset: usually two that confirm the
  verdict plus one offset, and mark the offset `(offset)` in its headline.
- Sources go in the `sources` array only. Never inline a citation in prose.
- The `banner` is one short paragraph on the single thing that set today's tone.
- Do not type net scores anywhere. They are computed from the matrix at render
  time so the top of the page can never disagree with the bottom.

The two charts are optional and generic. Use them for whatever the day's data
supports: `barChart` is a diverging bar chart around a zero baseline (ETF flows,
weekly changes, surprise versus consensus), `lineChart` is a single series with a
reference line (PMI against 50, CPI against target, a yield against a threshold).
Omit either by leaving its `data` empty and the card is dropped.

## Step 4, build and verify

```bash
python3 scripts/build.py data.json macro-dashboard-YYYY-MM-DD.html
```

The script validates before writing and refuses to write on an error. It checks
required fields, matrix width against the asset count, cell values, meter bands,
source pairs, that every verdict agrees with its own net score, and the no hyphen
rule. Fix the data file and rerun until it prints `OK`.

Then **render it and look at it** before shipping. Do not skip this, the
validator checks data, not layout:

```bash
python3 scripts/verify.py macro-dashboard-YYYY-MM-DD.html
```

That screenshots both tabs in both themes to `verify-*.png`, reports any console
error, and re greps the rendered text for hyphens. Read the screenshots.

## Step 5, publish

Deliver the file, then publish a **new** artifact each run so Turbo keeps a dated
history:

1. `SendUserFile` with the HTML path, which returns a `file_uuid`
2. `mcp__remote-devices__create_artifact` with
   `id: "macro-dashboard-YYYY-MM-DD"` and that `file_uuid`

Do not call `update_artifact` and do not reuse a previous day's id.

Close with two or three sentences on what changed and which verdict is closest to
flipping. Do not restate the dashboard, Turbo can read it.

## Language

Language applies to the complete rendered page, not just the analysis paragraphs.

For a Chinese request, set `language` to `"zh"` and write every authored display
field in Chinese: `title`, `stamp`, `regime`, `banner`, asset names, summaries,
qualifiers, factor headlines and reasoning, matrix factor names and readings,
signal labels and interpretations, calculation labels and notes, chart titles,
subtitles, series names, reference labels, table headings, dates, and chart item
labels. Keep numbers, standard market tickers, and source links unchanged. Source
names may retain their official English names.

Keep the machine fields in English exactly as the schema requires:
`verdict` remains `BULLISH` or `BEARISH`, `dir` remains `bull` or `bear`, and
`cap` remains `capped`, `bottoming`, or empty. The template localizes them to
`看多 BULLISH`, `看跌 BEARISH`, `受限 capped`, and `筑底 bottoming`. It also
localizes all fixed interface copy, including tabs, section headings, factor grid
labels, tooltips, theme controls, table view labels, and the full disclaimer.

For an English request, set `language` to `"en"` and write authored display
fields in English. Do not produce a bilingual page unless Turbo explicitly asks
for one. The no hyphen rule applies in both languages.

## Design notes

The template already encodes the visual system, so do not restyle it. If a chart
form ever needs to change, read the `dataviz` skill first and run its palette
validator rather than picking colors by eye. The palette in the template is
already validated in both light and dark mode.

The disclaimer block is baked into the template and renders on both tabs. Leave
it in. If the dashboard is ever going anywhere public, tell Turbo the wording is
unreviewed boilerplate and worth a lawyer's eye.
