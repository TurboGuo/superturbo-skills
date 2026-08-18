# X growth dashboard, public edition

A Claude skill that turns any X (Twitter) account's own analytics into a single
file HTML diagnostic board: three benchmarked scores, a follower curve, and a
post by post explanation of what the ranking algorithm did and what a
professional would change.

It is built for the account owner to run on their own data. Nothing in it is
specific to any account, any machine or any particular tool setup.

## Install

Drop the folder into your skills directory, or hand Claude the `.skill` file and
let it install. Then just ask, in your own words:

> Why is my X account not growing? Here are my analytics exports.

## What you need

**Required, and this is the whole list:**

1. `account_analytics_content_*.csv` from [analytics.x.com](https://analytics.x.com),
   Content tab, Export. One row per post.
2. `account_overview_analytics*.csv` from the Account overview tab. One row per
   day, and the only place unfollows appear.
3. Your current follower count, read off your profile. Neither export contains a
   follower time series, so this anchors the curve.

**Optional, improves the result:**

- A connected X API tool. It fills in the untruncated post body, bookmark and
  quote counts, and reliable post typing. The skill works without it and says so
  in the footer.

You do **not** need an API key, a paid tier, a database, or any particular MCP
server. Python 3 and the two CSVs are enough.

## Three ways to hand over the data

| Mode | When | What happens |
|---|---|---|
| **Attach the files** | Default | You upload the two CSVs and Claude reads them |
| **Point at a folder** | Files already saved somewhere | `scripts/discover.py` walks the folder, identifies exports by their header row rather than filename, and prints the command to run next |
| **Connected X API tool** | You have one | Used to enrich, never as a substitute. Profile visits, new follows per post and unfollows exist **only** in the CSV exports, so the API alone cannot build the full board |

## What it will not do

- It will not fetch anyone else's private analytics. Profile visits and per post
  follows are owner only fields. This is a self audit tool.
- It will not score you against your own averages. Every benchmark line is
  external, because inside an account where everything underperforms the worst
  post still ranks median and the board becomes a mirror instead of a measurement.
- It will not tell you your engagement rate is great by quietly using X's
  flattering `Engagements` column, which folds in profile clicks, link clicks and
  detail expands. It scores likes plus replies plus reposts plus bookmarks only.

## Privacy

Everything runs locally. No script here makes a network call, and the rendered
HTML has no external asset, no font fetch and no telemetry. It opens from
`file://` offline.

The example data in `assets/example/` is entirely synthetic, including the post
ids. The `dashboard.html` you generate **does** contain your post text and
metrics, so treat it as your own private file.

## Accuracy

`references/algorithm.md` and `references/benchmarks.md` carry a verification
date and cite primary sources. The X ranking repository and published benchmarks
both move, so the skill instructs Claude to re verify both on every single build
rather than trusting the cached numbers. Where a fresh source disagrees with the
reference file, the fresh one wins and the board's footer records it.

## Try it without your own data

```bash
cd assets/example
python3 ../../scripts/prepare.py --content content.csv --overview overview.csv \
  --followers 820 --start 2026-03-02 --end 2026-03-15 --out metrics.json
python3 ../../scripts/render.py --metrics metrics.json --analysis analysis.json \
  --suggestions suggestions.json --meta meta.json --out example-dashboard.html
```

Open `example-dashboard.html`. That is the shape of the output.

## Layout

```
SKILL.md                     the process Claude follows
README.md                    this file
references/
  algorithm.md               the published ranking pipeline, filters, weights
  benchmarks.md              the three metrics, the lines, the 100 point scale
  writing-guide.md           how the per post text has to read
  design.md                  the visual spec
scripts/
  discover.py                find the exports in a folder
  prepare.py                 CSVs to metrics.json, prints every calculation
  render.py                  metrics + analysis to one HTML file, validates first
assets/
  template.html              the board, two placeholders
  example/                   synthetic inputs for a smoke test
```
