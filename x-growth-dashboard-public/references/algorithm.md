# The algo side: what the X ranking pipeline actually does

This is the basis for every "Algo analysis" cell. Read it before writing one.

> **Verified against primary sources on 2026-08-17**, by reading
> `xai-org/x-algorithm` directly: `README.md`, `home-mixer/params/param.rs`
> (header comment `last sync 2026-08-12T04:09:22Z`) and
> `home-mixer/scorers/ranking_scorer.rs`. Re verify before every build. This
> repository moves, and the weights are feature switch defaults that can be
> changed server side without a commit.

## What is public

xAI open sourced the For You pipeline at `github.com/xai-org/x-algorithm`. The
release publishes the architecture, the candidate filters, the scored action list,
the post ranking adjustments **and the weight values themselves**, mirrored from
the production feature switch defaults into `home-mixer/params/param.rs`.

> **This is a change from the earlier situation.** Older write ups, and any
> guidance built before this release, say the weights were withheld and fall back
> on the April 2023 `twitter/the-algorithm-ml` table. That table is obsolete and
> in at least one important place it is now actively misleading. Quote the current
> file, not the 2023 one.

**The repository's own caveat, which you must respect.** Each weight multiplies
the *predicted probability* of an action, or a continuous value such as watch
time. It does **not** multiply raw engagement counts. So you cannot read the
ratios as count equivalences. The README calls out "one report cancels N likes"
by name as an incorrect reading: Report carries a large negative weight because
its baseline probability is more than a thousand times lower than a Like, so
without a large multiplier the prediction could not move the ranking at all.

Write it as "in the published weight table, X carries N" and never as "one X is
worth N likes".

## The shape of the pipeline

1. **Candidate sourcing.** In network from `thunder/`, out of network from
   `phoenix/` retrieval and `simclusters/`.
2. **Filters** remove candidates before ranking. Two matter enormously for small
   accounts, see below.
3. **Phoenix**, a transformer, predicts a probability per scored action per
   candidate. Candidates cannot attend to each other, so a post's score does not
   depend on what else is in the batch.
4. **RankingScorer** takes the weighted sum of those predictions.
5. **Adjustments** apply on top of the score.
6. **VMRanker** reorders the result with a determinantal point process over post
   embeddings, trading a little score for less similarity between neighbours.

## The filters that explain small account behaviour

**`OONRetweetReplyFilter`** removes reposts and replies from accounts the viewer
does not follow. This is the single most useful thing on this page.

> Consequence: a reply's reach is **the parent thread's readership**, not yours.
> Replying under a small thread caps you at that thread's size no matter how good
> the reply is. This is why an account can post 7 thoughtful replies and average
> 34 views on them.

**`NewUserMinEngagementFilter`** removes out of network posts below an engagement
threshold for newer accounts. A post with near zero engagement has nothing to
clear it with, which compounds a slow start.

**`AgeFilter`** removes posts older than 48 hours from the candidate pool. A quote
only rides its parent while the parent is still inside that window.

Also present and worth knowing: `PreviouslyServedPostsFilter` and its bloom filter
backup mean a post is not re served to the same viewer, so a post gets roughly one
chance per person. `InventoryHoldoutFilter` removes a configured percentage of
posts deterministically per post and viewer.

## The adjustments, with published values

| Adjustment | Parameter | Default |
|---|---|---|
| Author diversity decay | `AuthorDiversityDecay` | **0.5** per additional post by the same author in one feed |
| Author diversity floor | `AuthorDiversityFloor` | **0.25**, the decay bottoms out here |
| Out of network discount | `OonWeightFactor` | **0.75** |
| Out of network, topic sourced | `TopicOonWeightFactor` | **0.5** |

> **Author diversity consequence.** The second post by the same author in a given
> feed is multiplied by 0.5, the third by 0.25, and it floors there. Posting eight
> times in one evening makes those posts compete with each other rather than with
> the feed. Recommend at least two hours of spacing.

> **Out of network consequence.** Quoting a huge post does not transfer its
> audience. Your copy still takes the 0.75 factor, and the parent's readers see
> the parent, not you. The discount applies to in network replies and reposts too
> when `EnableOonRescoreForInNetworkRepliesRetweets` is on, which it is by default.

## The cold start gate, the most actionable thing here for a small account

`home-mixer/scorers/author_cold_start.rs`, parameters in `param.rs`:

| Parameter | Default | Meaning |
|---|---|---|
| `ColdStartFollowerCap` | **1000** | Author must have at most this many followers |
| `ColdStartImpressionThreshold` | **1000** | Post must be under this many impressions |
| `ColdStartMaxPostAgeSecs` | **86400** | Post must be under 24 hours old |
| `ColdStartSlotMin` / `ColdStartSlotMax` | **15 / 16** | The slot the post is lifted toward |
| `LowImpressionsMaxPositionRatio` | **0.85** | Only the top 85% of the non zero pool is eligible |
| `EnableViewerColdStart` | **true** | On by default |

Eligibility also requires the candidate to be **an original**, not a reply and not
a repost.

> Consequence, and it is a strong one: this is the one published rule keyed on
> follower count, and it opens for accounts at or below 1,000 followers and closes
> above. It applies to **originals only**. An account under 1K that posts nothing
> but replies never touches the one mechanism in the pipeline built to help it.
> The window is 24 hours and the gate closes once a post passes 1,000 views.

## The published weight table

From `home-mixer/params/param.rs`. Positive actions first, largest to smallest.

| Action | Parameter | Weight |
|---|---|---|
| Share via copy link | `ShareViaCopyLinkWeight` | **20.0** |
| Reply, author is a mutual follow | `BidirectionalFollowReplyWeightBoost` | **+15.0** on top of reply |
| Reply | `ReplyWeight` | **5.0** |
| Share via DM | `ShareViaDmWeight` | **5.0** |
| Quote | `QuoteWeight` | **5.0** |
| Follow author | `FollowAuthorWeight` | **4.0** |
| Share | `ShareWeight` | **2.0** |
| Repost | `RetweetWeight` | **1.0** |
| Favorite (like) | `FavoriteWeight` | **0.5** |
| Click | `ClickWeight` | **0.4** |
| Open link | `OpenLinkWeight` | **0.2** |
| Photo expand / video open / VQV | | **0.05** each |
| Post unexplored | `PostUnexploredWeight` | **0.02**, in network only by default |
| Continuous dwell time | `ContDwellTimeWeight` | **0.004** |
| **Profile click** | `ProfileClickWeight` | **0.0** |
| **Dwell** | `DwellWeight` | **0.0** |

| Negative action | Parameter | Weight |
|---|---|---|
| Report | `ReportWeight` | **-234.0** |
| Mute author | `MuteAuthorWeight` | **-58.8** |
| Not interested | `NotInterestedWeight` | **-43.2** |
| Block author | `BlockAuthorWeight` | **-31.2** |
| Not dwelled | `NotDwelledWeight` | **-0.02** |

Four readings worth putting on a board:

- **Share via copy link is the largest positive weight in the table, 20.0.** Someone
  copying your link and taking it somewhere else is the strongest positive signal
  the ranker has. Nothing in X's own analytics export exposes this action directly,
  which is exactly why a board that only reads likes misses it. The proxies you
  can see are bookmarks and quotes.
- **Profile click is weighted 0.0.** This is the correction that matters most
  against older guidance, which claimed a profile click was scored in its own
  right and that zero visits "cost twice". It does not. Profile visit rate is on
  this board because it is the funnel step before a follow, not because the ranker
  pays for it. Say it that way.
- **Follow author is weighted 4.0, eight times a like.** The action the account
  actually wants is directly and heavily scored. A post that converts is rewarded
  by the ranker with more distribution, which is the compounding loop.
- **A reply between mutual follows is worth 20.0, four times an ordinary reply.**
  Building genuine mutuals is a ranking mechanic, not just a social one. The boost
  applies only when the candidate is an original, not a reply or repost.

## Format specific notes

**X Articles.** The body sits behind a link, so dwell accrues on the Article rather
than on the post carrying it. Note that `DwellWeight` is 0.0 and continuous dwell
time is 0.004, among the smallest weights in the table, so the "Articles earn long
dwell" argument is much weaker than it once looked. What an Article can earn is a
link open at 0.2 and a click at 0.4. Shipping an Article as a bare `t.co` link with
no text gives a scroller one decision, click or scroll, and almost everyone scrolls.

**Quotes.** A quote is weighted 5.0 for the person quoting you, which makes being
quoted valuable. Quoting someone else hands the ranker their post to score and
takes the out of network discount. Reach usually goes up and everything else goes
down.

**Replies.** See `OONRetweetReplyFilter`. Reply under accounts 5 to 50 times your
size, inside the first 30 to 60 minutes, when the first few replies get most of the
visibility. Note the cold start gate does **not** cover replies, so a reply only
ladder forgoes it.

**Secondary reporting, flag it as such if you use it.** Practitioner write ups of
the repository describe an extra spam screen on replies from accounts under 1,000
followers, bucketed `lte_1000` in the content understanding pipeline, and a 1,000
follower viewer threshold on the "people you follow replied to this" badge. These
are second hand readings of files this note did not verify directly. If you cite
them, attribute them to the write up, not to the repository.

## Writing the cell

An Algo analysis bullet names a **mechanic** and attaches **this post's number**.

Good:
> Replies only reach your own followers plus people already in that thread.
> **40 views**, against a 48 average for your 6 replies.

Good:
> Originals are the only format the cold start gate covers, and it closes at
> 1,000 views. This one stopped at **122**, well inside the window it never used.

Bad, no mechanic:
> This post did not perform well.

Bad, no number:
> Replies are limited by the out of network filter.

Bad, obsolete and wrong:
> A profile click is scored in its own right, so zero visits costs you twice.
