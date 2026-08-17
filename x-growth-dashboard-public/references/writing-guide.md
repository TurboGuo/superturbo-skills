# How to write the text

The charts are an index. The text is the product. This is what separates
"someone actually read my account" from "a model filled in a template".

## 1. The per post three cell structure

Each post gets three dimensions, each dimension gets three cells:

```
              Algo analysis    Professional influencer analysis    Overall suggestion
Follow rate        .                        .                              .
Profile visits     .                        .                              .
Engagement         .                        .                              .
```

Nine cells per post. **Maximum 2 bullets per cell.** `render.py` enforces it.

**Algo analysis** names a ranking mechanic and attaches this post's number.
Filters, adjustments, scored actions, the 2023 weight ordering. Nothing else.

> Replies only reach your own followers plus people already in that thread.
> **40 views**, against a 48 average for your 6 replies.

**Professional influencer analysis** names a habit or a benchmark. Format mix,
posting cadence, hook shape, what practitioners report. Never restate the algo cell.

> Your median original is 65 views. The published band for a 0 to 1K account is
> 100 to 500.

**Overall suggestion** starts with `Keep:` or `Change:` and names a concrete action.

> Change: reply under accounts 5 to 50 times your size, in the first hour.

## 2. Hard rules

1. **Every bullet carries a real number from this account or a concrete action.**
   Neither, delete it. `render.py` rejects the build.
2. **Two bullets maximum per cell.** Fewer is fine. Padding is not.
3. **Plain language.** "People clicked your name and left" beats "a discontinuity
   exists at the terminal stage of the conversion funnel".
4. **The two analyses must genuinely differ.** If the algo cell and the influencer
   cell say the same thing in different words, one of them is not written yet.
   They are allowed to disagree, and when they do that is the most valuable thing
   on the board.
5. **Say when the sample is too small.** Under 100 views, write "Sample too small
   to assess" and stop. Do not invent a cause for noise.
6. **Do not fabricate.** Practitioner cases, follower counts and percentages must
   come from a source you actually read this round.
7. **No fractional expected counts in prose.** "You would expect 0.06 follows" is
   technically right and unreadable.
8. **Say "views", not "impressions"**, except where the point is specifically the
   export column versus the public count.

## 3. High scores and low scores read differently

- **High score:** explain what won so it can be repeated. Lead with `Keep:`.
- **Low score:** find the earliest stage that failed and talk about that one only.
  If the post never got reach, its conversion ratios are meaningless.
- **High views, nothing else:** the most important case to write well. Say plainly
  that borrowed reach did not carry the author's name with it.
- **Strong writing, no reach:** name it. An account whose best argument got the
  fewest views has a distribution problem, not a content problem, and it deserves
  to be told so.

## 4. Overall suggestions, 3 to 5

Placed **above** the post table, so the actions land before the evidence.

Each one:

- **Heading is an executable action, not an observation.**
  - No: "Engagement is the current bottleneck"
  - Yes: "End every original with a question and answer each reply inside the hour"
- **Trigger line** quotes the number from this board that caused it, key value bold.
- **2 to 4 concrete steps.**
- **Sources line** with an algo basis and an influencer basis, both linked.

Order by leverage, not by discovery order. Delete anything without an action:
"keep monitoring" is not a suggestion.

## 5. Footer, minimum five paragraphs, and these eight are the checklist

1. **Definitions.** All three formulas, plus the sentence that views and
   impressions are the same number on X so there is no funnel to decompose.
2. **The 100 point scale.** Mapping and the source of every line.
3. **Follower curve.** That neither export has a follower series, the real count
   used as the anchor, and that single day timing is approximate.
4. **Sample size.** Zero follow windows, thin rows, and which scores are safe to
   act on. Be blunt.
5. **Two numerators.** Post level and account level totals do not reconcile and
   are not supposed to. State both and explain the gap.
6. **Ranking weights.** That every weight quoted comes from `param.rs` in the
   open source release, the date that file was last synced, and the repository's
   own caveat that weights multiply predicted probabilities and not raw counts,
   so the ratios are not count equivalences. If you quoted anything from the
   April 2023 table instead, say so and say why.
7. **How the data got here.** Which input mode was used: files the owner
   exported, a folder scan, or an API read, and for API reads, when it was read.
   If post types were inferred from text rather than confirmed, give the count.
8. **Sources.** Export filenames and dates, and a link for every external number.

Write the uncertainty in full. It is better than letting a reader assume every
number on the page is equally solid.
