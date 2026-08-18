# The three metrics, the scale, and where every line comes from

> **Benchmark lines re verified 2026-08-17** against published analytics guides.
> Two independent 2026 sources put the strict engagement ladder at under 1% below
> average, 1 to 3% average, 3 to 5% good, over 5% excellent, and the profile visit
> tiers at under 2 / 2 to 5 / 5 to 10 / 10 plus visits per 1,000 impressions.
> Published benchmarks move. Re verify before every build and cite what you read.

## 1. Why X has no funnel

On most feed platforms the growth identity is a chain:

```
exposure  ->  view  ->  follow
follow rate = (views / exposure) x (follows / views)
```

**That chain does not exist on X.** In X analytics, the Impressions column *is* the
public view count. The same post reads 246 in the export, 246 in `impression_count`
from the API and 246 under the post on the timeline. So:

- `follows / exposure` and `follows / views` are the same number.
- `views / exposure` would always be 100% and tells you nothing.

Do not try to force a multiplicative identity onto this board. Do not print an
identity check. The three scores are **three different actions measured against
the same denominator**, and that is the honest shape.

## 2. The three scored metrics

| Score | Formula | Question it answers |
|---|---|---|
| Follow rate | new follows / views | Did the post grow the account |
| Profile visit rate | profile visits / views | Did the post make anyone want to know who wrote it |
| Engagement rate | (likes + replies + reposts + bookmarks) / views | Did the post make anyone act |

Profile visit rate sits between the other two for one reason only: on X, a profile
click is the step between seeing a post and following. It is the earliest metric
that moves, so it tells you a post is working before the follows arrive.

**It is not on this board because the ranker rewards it.** `ProfileClickWeight` is
**0.0** in the published weight table, so a profile click contributes nothing to
the ranking score. The action the ranker does pay for is the follow itself,
`FollowAuthorWeight` **4.0**. Older guidance claims a profile click is scored in
its own right and that zero visits "costs twice". That was true of the April 2023
table, where it carried 12.0, and it is not true now. Write the visit tile as a
funnel diagnostic, never as a ranking signal. See `references/algorithm.md`.

## 3. Benchmark lines

**Anchor every line externally. Never score against the account's own percentiles.**
Inside an account where everything underperforms, the worst post still ranks
median, and the board becomes a mirror instead of a measurement.

| Metric | Fair | Good | Excellent | Where the line comes from |
|---|---|---|---|---|
| Profile visit rate | 0.20% | 0.50% | 1.00% | Published tiers of under 2 / 2 to 5 / 5 to 10 / 10 plus profile visits per 1,000 impressions |
| Engagement rate, strict | 1% | 3% | 5% | Published ladder of under 1 below average / 1 to 3 average / 3 to 5 good / over 5 excellent |
| Follow rate | 0.002% | 0.015% | 0.050% | Derived: profile visit line x follower conversion line |

The follow rate derivation, shown so it can be checked:

```
fair       = 0.20% x 1% = 0.002%
good       = 0.50% x 3% = 0.015%
excellent  = 1.00% x 5% = 0.050%
```

The conversion tiers used in that derivation (1% average, 3% solid, 5% excellent
follows per profile visit) come from the same published source as the visit tiers.

**Context figures, not scored, cite them in prose:**

- Platform median strict engagement rate is around **0.70%**. Anything over 1% is
  strong. Note that published platform averages vary wildly depending on whether
  the study uses the strict or the broad definition, so cite the one you read and
  say which definition it used.
- Views per post for a 0 to 1K follower account run roughly **100 to 500**. Use
  this to frame the median, but do not give reach its own tile.
- **1,000 followers and 1,000 views are the two thresholds in the ranking code.**
  `ColdStartFollowerCap` and `ColdStartImpressionThreshold` both default to 1,000.
  An account below both is inside a gate that closes above them, so for a small
  account these are not arbitrary round numbers, they are the published boundary.

Refresh these before each build. Published benchmarks move, and a board scored
against a stale tier is worse than one with no tiers at all.

## 4. The 100 point scale

Piecewise linear, three segments:

| Raw value | Score |
|---|---|
| 0 to fair | 0 to 40 |
| fair to good | 40 to 70 |
| good to excellent | 70 to 100, capped |

Bands: **70 and above Good** (green), **40 to 70 Fair** (amber), **under 40 Weak** (red).

Worked example, a profile visit rate of 0.91%, which sits between good and excellent:

```
70 + (0.91 - 0.50) / (1.00 - 0.50) x 30 = 94.6  ->  95/100, Good
```

## 5. The definition trap that will bite you

X's **Engagements** column counts profile clicks, link clicks and detail expands
alongside likes, replies, reposts and bookmarks. Published engagement ladders use
the strict definition only.

Scoring X's broad column against a strict ladder inflates the tile badly. On one
account the same fortnight read **4.0% broad against 1.0% strict**, which was the
difference between a score of 85 and a score of 40.

**Always compute `strict = likes + replies + reposts + bookmarks` and score that.**
Mention the broad number in prose as the flattering one, never as the score.

## 6. Sample size rules

- Any post under **100 views**: mark it thin and write "Sample too small to assess"
  instead of inventing a cause. `prepare.py` sets the `thin` flag.
- If the whole window has **zero follows**, the follow rate tile reads 0/100 Weak
  on every row. Show it, then say in the footer that this is a sample size result.
  At the 3% conversion benchmark, 20 profile visits predicts 0.6 follows, so zero
  is inside the noise.
- **Zero reposts and zero bookmarks across a whole window is NOT a sample size
  artifact.** A repost is the only free route out of the author's own network and
  a bookmark is the strongest quality signal a reader leaves. If both are zero,
  that is the headline finding and it outranks every rate on the board.
