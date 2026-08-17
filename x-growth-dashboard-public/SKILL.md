---
name: x-growth-dashboard-public
description: Turn any X (Twitter) account's analytics data into a single file HTML diagnostic dashboard that scores the account on three benchmarked metrics and explains every post from two angles, the published ranking algorithm and professional influencer practice. Accepts data three ways, uploaded CSV exports, a local folder to scan, or a connected X API tool. Use when someone asks why their X account is not growing, wants a post by post review, an X analytics report, an X growth audit or an account dashboard. Also use proactively when someone provides account_analytics_content or account_overview_analytics CSVs from analytics.x.com, even if they did not say the word dashboard.
---

# X growth dashboard

Turns X analytics data into an HTML board the account owner can open and act on.
The point is not the charts. The point is **locating why an account is not growing
to a specific stage, and saying what to do about it.**

This skill is self contained. It needs Python 3 and nothing else. Every optional
capability below degrades gracefully: with no connected tools and no folder access,
two CSV files and a follower count are enough to build the whole board.

## What comes out

```
Title, two basis bullets, window subtitle
┌──────────────────────┬──────────────────────┐
│ Net followers gained │ Follow rate     /100 │
├──────────────────────┼──────────────────────┤
│ Profile visit rate   │ Engagement rate /100 │
└──────────────────────┴──────────────────────┘
Follower curve + follows per post + three scores, one date axis
Overall suggestions, 3 to 5, above the post table on purpose
Post by post: sortable overview + three dimension tabs
Footer
```

Light and dark, hover tooltips, sortable tables, one self contained file, no
network calls. It opens from `file://` on any machine.

## The one thing to understand before starting

**On X, views and impressions are the same number.** The Impressions column in the
export equals the public view count on the post.

So the funnel other platforms have, exposure to view to follow, **does not exist
here**. `follows / impressions` and `follows / views` are one metric, and
`views / impressions` is always 100%.

Do not build a multiplicative identity. The three scores are three different
actions over the same denominator. Full reasoning in `references/benchmarks.md`.

## Process

### 1. Get the data

There are three ways in. Work down the list and stop at the first one that
produces both required tables. Say out loud which mode you used, because it
changes what the footer has to disclose.

#### Mode A, files the user provides (always works, no setup)

Ask for two exports from `analytics.x.com`, signed in as the account owner:

| File | Where | Shape |
|---|---|---|
| `account_analytics_content_*.csv` | Content tab, Export | One row per post |
| `account_overview_analytics*.csv` | Account overview tab, Export | One row per day, and the **only** place unfollows appear |

#### Mode B, a folder to scan

If the user says the files are already saved somewhere, or points at a folder,
scan it rather than making them re-export:

```bash
python3 scripts/discover.py <folder> [more folders...]
```

It walks the folder, identifies each CSV by its header row rather than its
filename, prints the date range and row count of every candidate it finds, and
prints the exact `prepare.py` command to run next. Renamed files are fine.
Duplicates and older exports are fine, it reports all of them and picks the
widest. It reads nothing outside the folders it is given.

#### Mode C, a connected X API tool

If the session has any tool that can call the X API, use it, but understand what
it can and cannot replace:

- The API **can** give post text, public metrics, post type and article content.
- The API **cannot** give profile visits, new follows per post, or unfollows.
  Those are owner only analytics fields that exist solely in the CSV exports.

So Mode C is an **enrichment layer, not a substitute**. Where it genuinely
matters is step 2. If the only data available is the API, say plainly that the
follow rate and profile visit tiles cannot be computed, and offer the reduced
board: engagement rate plus the format split, with the other two tiles marked
unavailable rather than shown as zero.

#### Always required regardless of mode

- **Today's real follower count.** No export or API call carries a follower time
  series, so this is the anchor the curve is walked back from. Read it off the
  profile. Do not guess it.
- **The window.** Default 14 days. Under 10 posts, widen to 30 and say why.

Ask for everything missing in one go, not one question at a time.

### 2. Re read the posts through the X API if one is available

The CSV alone is not enough and the analysis is visibly worse without this. If
any X API tool is available, fetch every post id in the window with fields
`created_at,text,public_metrics,referenced_tweets,note_tweet,conversation_id,entities,article`.

It gives five things the export does not have:

| Field | Why it matters |
|---|---|
| `note_tweet.text` | The **untruncated body**. The export stops at 280 characters, so without this you are diagnosing a stub |
| `public_metrics.bookmark_count`, `quote_count` | The export has no column for either, and they are often the finding |
| `article.title`, `article.plain_text` | What is actually behind an Article link |
| `referenced_tweets` | Reliable original / quote / reply typing |
| `edit_history_post_ids` | More than one id means the post was edited after publishing |

Write the types to `types.json` as `{post_id: "original"|"quote"|"reply"|"article"}`
and short human labels to `titles.json` as `{post_id: "..."}`.

**If no API tool is connected, this step is skipped and the build still works.**
`prepare.py` infers types from the text and reports how many were inferred. Put
that count in the footer. Do not stall waiting for a tool the user does not have,
and do not tell them to install one mid build.

### 3. Compute

```bash
python3 scripts/prepare.py --content content.csv --overview overview.csv \
  --followers <count> --start YYYY-MM-DD --end YYYY-MM-DD \
  [--types types.json] [--titles titles.json] --out metrics.json
```

It prints every calculation, the score derivations, the format split and warnings.
**Read that output before writing a word.** It flags the two situations that change
what the whole board says: a zero follow window, and zero reposts plus zero
bookmarks.

Then read `references/algorithm.md` before writing any Algo analysis cell.

### 4. Search for current material, required

`references/algorithm.md` and `references/benchmarks.md` were verified against
primary sources on the date stamped at the top of each file. Both the platform and
the published benchmarks move. **Run a real search every time.** Cover at least:

1. `xai-org/x-algorithm` current state, and read `home-mixer/params/param.rs`
   directly, since the live weight values are in that file
2. `X algorithm <current year> changes`
3. `X analytics benchmarks engagement rate profile visits by follower count`
4. `X growth <current year> what actually works`

Add one search for the account's niche if it has a clear one. Search on X itself
as well as the open web, since the best material about X often stays on X.

Where a new source conflicts with the reference files, the new one wins and you
note it in the footer. **Only cite numbers you actually read this round.**

### 5. Write the per post analysis

Nine cells per post, following `references/writing-guide.md`. Output `analysis.json`:

```json
{
  "1234567890": {
    "fanAlgo": ["follow rate, algo view, 1 to 2 bullets"],
    "fanBlog": ["follow rate, influencer view"],
    "fanFix":  ["Keep: ... or Change: ..."],
    "covAlgo": [], "covBlog": [], "covFix": [],
    "erAlgo":  [], "erBlog":  [], "erFix":  []
  }
}
```

Keys are post ids. **Two bullets per cell maximum**, and every bullet carries a
real number or a concrete action. `render.py` refuses to build otherwise.

### 6. Write the suggestions and the metadata

`suggestions.json`, 3 to 5 entries, ordered by leverage:

```json
[{
  "h": "A heading that is an action, not an observation",
  "t": "The number from this board that triggered it, key value in <b>",
  "p": ["2 to 4 concrete steps"],
  "s": "Algo basis: ... <a href=\"...\">source</a>. Influencer basis: ... <a href=\"...\">source</a>."
}]
```

`meta.json`:

```json
{
  "title": "X Algo and Professional Influencer Analysis",
  "subtitle": "Mar 2 to Mar 15 · 16 posts · 1,933 views · 14 profile visits · 2 follows",
  "intro": [
    {"k": "Algo analysis:", "v": "what the ranking model does, in one paragraph"},
    {"k": "Professional influencer analysis:", "v": "where the outside numbers came from"}
  ],
  "folRaw": "823 to 820 over 14 days",
  "folBase": "Optional second line under the follower tile",
  "footnotes": [{"k": "Definitions. ", "v": "..."}]
}
```

At least five footnotes. The required list is in `references/writing-guide.md`.

### 7. Render

```bash
python3 scripts/render.py --metrics metrics.json --analysis analysis.json \
  --suggestions suggestions.json --meta meta.json --out dashboard.html
```

Validation runs first and fails loudly on a missing post, an empty cell, a third
bullet, a bullet with no number and no action, or too few footnotes.

### 8. Check before delivering

- [ ] Every score derivation in the `prepare.py` output reproduces by hand
- [ ] Engagement is scored on the **strict** rate, not X's Engagements column
- [ ] Every cell has content, no placeholders, two bullets maximum
- [ ] Suggestions sit above the post table
- [ ] Footer covers definitions, the scale, the follower anchor, sample size, the
      two numerators, which input mode was used, and sources
- [ ] Opened in a browser, all four tabs clicked, a column sorted, dark mode tried
- [ ] Checked at a narrow width, the date column does not wrap
- [ ] Every external number traces to something read this round
- [ ] The delivered file contains the account owner's data only, and no path,
      handle or tool name from the machine that built it

## Traps that have cost real time

**The column order trap.** The content export runs Impressions, Likes, Engagements,
Bookmarks, **Shares**, New follows, Replies, Reposts, Profile visits, Detail
Expands, URL Clicks. The value in the fifth position is Shares, not New follows.
Read by header name, never by index. Misreading it wastes an entire build.

**The engagement definition trap.** X counts profile clicks, link clicks and detail
expands inside Engagements. Published ladders use likes plus replies plus reposts
plus bookmarks only. Scoring the wrong one can inflate a tile from 40 to 85 on the
same data.

**Post level and account level never reconcile**, and should not. The posts in the
window carry fewer views than the account did over the same days, because older
posts keep earning. State both numbers and explain the gap.

**Follows are often unattributed.** Every post can show zero new follows while the
account gained some. Those arrived through the profile, search or a reply thread.
Never present the per post zero as proof the content failed.

**Zero reposts and zero bookmarks is the loudest signal on the board.** If a whole
window has both at zero, lead with it. Nothing was worth saving or passing on, and
that explains flat reach better than any ratio.

**Editing does not re enter distribution.** If `edit_history_post_ids` shows edits,
mention it, but do not suggest editing as a fix.

**Do not score a profile click as a ranking signal.** It reads as one and it is not.
`ProfileClickWeight` is **0.0** in the published weight table. Profile visit rate
is on this board because it is the funnel step before a follow, not because the
ranker rewards it. See `references/algorithm.md`.

## Privacy

This skill is designed to be shared and run by anyone on their own account.

- Everything runs locally. No script in this folder makes a network call, and the
  rendered HTML has no external asset, no font fetch and no telemetry.
- The example data in `assets/example/` is entirely synthetic. It is not a real
  account and the post ids are not real ids.
- The finished `dashboard.html` **does** contain the account's post text, metrics
  and follower count. Treat it as the owner's private data. Do not publish an
  example built from someone's real account without asking them.
- Never bake an account handle, a file path or a session specific tool name into
  any of these files. They belong in the conversation, not in the skill.

## Files

| File | Read it when |
|---|---|
| `references/benchmarks.md` | Before computing. The three metrics, every line, the scale, sample size rules |
| `references/algorithm.md` | Before writing any Algo analysis cell |
| `references/writing-guide.md` | Before writing any text at all |
| `references/design.md` | Only when changing the visual output |
| `assets/template.html` | The board itself. `__DATA__` and `__TITLE__` are the only placeholders |
| `assets/example/` | Synthetic inputs. Smoke test the scripts against these first |
| `scripts/discover.py` | Mode B, when the CSVs are somewhere on disk |
| `scripts/prepare.py` | Step 3 |
| `scripts/render.py` | Step 7 |
