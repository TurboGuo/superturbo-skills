---
name: fomc-short-analysis-plain-bot
description: Produce Turbo's ultra short FOMC analysis in plain text only, no markdown file, no visualization, no rendered widgets or artifacts, sized for a bot message on general gateways like Telegram and Slack that only display plain text and emoji. This is the trimmed "bot" variant of fomc-short-analysis-plain, inline chat answer only, no artifact of record. Verdict first as POTENTIAL HIKE or POTENTIAL CUT, exactly one one sentence reason with an official Fed source, and one or two institutions (two only if they disagree, otherwise one). No split line. Use when Turbo says "fomc bot", "fomc plain bot", "fomc short bot", "quick fomc", "fomc for the bot", "fomc for telegram", "fomc for slack", or asks for the shortest possible FOMC read on a past decision, a minutes release, or an upcoming meeting preview.
---

# FOMC short analysis (plain, bot)

**Plain text only. Inline chat answer only.** This variant produces nothing but a short plain text and emoji message. No markdown file, no charts, no visualizations, no rendered widgets, no HTML artifacts, no `present_files`. The single deliverable is one bot sized chat message that renders correctly inside Claude and on Telegram, Slack, and any surface that shows only plain text and emoji.

This is the trimmed sibling of `fomc-short-analysis-plain`. Same research rigor, far less output.

## Standing preferences, apply throughout

- Use Exa for all web search (`web_search_exa`, `web_fetch_exa`). Cross check X for institutional reaction where useful.
- **Never use the "-" hyphen character in narrative prose.** Use spaces, "and", "to", commas or parentheses. Hyphens inside URLs and inside directly quoted official text are fine.
- Cite the source for every data point.
- Do the arithmetic internally to reach the verdict, but **never print calculation steps.** State only the result.
- Primary Fed documents outrank secondary coverage.
- Dates in narrative use spaces: 2026 07 29.
- No filler, no throat clearing, no "here is what you asked for". Keep every sentence short and concise.

## Step 1. Work out which meeting

Check today's date against the official calendar at https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm. Never trust a hardcoded schedule.

- If Turbo names a meeting, use it.
- If Turbo says "last meeting" or "previous meeting", use the most recent completed decision date.
- If Turbo says "preview" or "next meeting", use the next decision date.

If no FOMC event exists for the date implied, say so plainly and stop. Do not manufacture analysis.

## Step 2. Read the primary documents first

Fetch in this order, before touching any commentary:

1. Statement: `https://www.federalreserve.gov/newsevents/pressreleases/monetaryYYYYMMDDa.htm`
2. **Prior meeting's statement**, same URL pattern, for the wording diff. Not optional. The diff is usually where the signal is.
3. Implementation note: same pattern with `a1.htm`
4. Press conference transcript: `https://www.federalreserve.gov/mediacenter/files/FOMCpresconfYYYYMMDD.pdf`
5. If an SEP meeting: `https://www.federalreserve.gov/monetarypolicy/files/fomcprojtablYYYYMMDD.pdf`
6. If minutes are out: `https://www.federalreserve.gov/monetarypolicy/fomcminutesYYYYMMDD.htm`

**SEP PDF warning.** The projections table frequently extracts with the character order reversed, so a median reads as "8.3" instead of "3.8". Reverse the token order and reverse each token, then cross check every median against at least two secondary sources before using it. The accessible HTML version at `fomcprojtabl20YYMMDD.htm` usually extracts cleanly and is the fastest cross check. Trust the PDF or accessible HTML over secondary sources, which routinely confuse core PCE with headline PCE.

**Dot plot arithmetic.** SEP dots round to the nearest 1/8. A published median that is not on the 1/8 grid is the average of the two middle dots. Do this math internally; do not print it.

## Step 3. Form the verdict

The verdict is always one of two words: **POTENTIAL HIKE** or **POTENTIAL CUT**. Never "unchanged direction", never "on hold", never "no change". A hold at the meeting is not the verdict; the verdict is where the next move points.

Hedge the confidence, not the direction. "Potential hike, not a potential cut" is right. "Direction is unchanged" is wrong.

Anchor the verdict on the real policy rate versus the Committee's own neutral estimate. Compute this internally:

    Policy midpoint  = (lower bound + upper bound) / 2
    Real policy rate = policy midpoint − latest core PCE
    Real neutral r*  = SEP longer run fed funds median − SEP longer run PCE median
    Gap              = real policy rate − real neutral

Below neutral with inflation above target points to a potential hike. Above neutral with inflation falling points to a potential cut. **Do not print the arithmetic.** State only the rounded result inside the reason, for example "roughly 88 bp below neutral".

Then pick the single strongest supporting reason. One, not two.

## Step 4. Pick one or two institutions

Prefer large and named houses: Goldman Sachs, Morgan Stanley, JPMorgan, Deutsche Bank, BofA, Citi, Barclays, Nomura, UBS, PIMCO, BlackRock, Apollo, Pantheon Macroeconomics, Scotiabank, RBC, Western Asset, TrendMacro. Avoid consultancies and retail brokers unless nothing better exists. Name the individual economist or strategist where you have them.

**How many to include:**

- **If the houses disagree, include exactly two**, one on each side of the split, to show the disagreement.
- **If the houses agree, include exactly one.** Do not pad to two when there is no difference of opinion.

**Two hard rules on institution sourcing. Both must hold for every house you cite.**

1. **Official source only.** The link must be the institution's own official site (for example morganstanley.com, goldmansachs.com, citigroup.com, jpmorgan.com). Never cite a third party aggregator (TradingKey, HTX, TipRanks, Yahoo, Bloomberg, Reuters, CNBC, biggo, stockwirex, and the like) as the institution's view, even if the aggregator quotes the bank accurately. If the only source for a house is an aggregator, drop it and pick a house that has published on its own site.
2. **Direct reaction to this specific meeting, published after the decision.** The piece must be that institution reacting to the meeting you are analyzing, dated on or after the decision date. A pre meeting preview or a stale quarterly outlook does not qualify.

Each institution gets a tendency tag in parentheses, one to three words, using the same vocabulary as the verdict: (potential hike), (potential cut), (potential hike, low conviction), (potential cut, 2027), (potential hike, deferred).

## Step 5. Write the bot message

This is the only output. Reproduce this exact shape. Do not add sections. Do not write any file. Do not call present_files.

```
🏛️ FOMC analysis, [Month DD YYYY]

[⬆️ or ⬇️] POTENTIAL HIKE
[One short sentence: the verdict, the size if it happens, the earliest realistic window.]

🔥 [One short sentence reason. State the result, no arithmetic.]
Source: [Short title](url)

🏦 Key analysis from institutions
[🐂/🕊️/⚖️] [House] ([tendency tag]). [One short sentence.] [Official post meeting source](url)
```

Shape rules:

- **The title carries the FOMC date**, formatted `🏛️ FOMC analysis, [Month DD YYYY]`. For a two day meeting use the decision day. Example: `🏛️ FOMC analysis, June 17 2026`.
- **No Meeting / Decision date / Reviewed line.** Removed on purpose.
- **Conclusion line** carries ⬆️ for a hike lean or ⬇️ for a cut lean, then the two word verdict, then one short sentence under it.
- **Exactly one reason**, prefixed 🔥, one short sentence, no calculation steps. Its Source line sits directly underneath.
- **Institutions:** one line each. Two lines only if the houses disagree, otherwise one line. Tendency emoji at the front: 🐂 hike lean, 🕊️ cut lean, ⚖️ balanced or low conviction. Same tendency tag and official post meeting link as the research.
- **No closing split line.** Removed on purpose.
- One emoji per header or line. Do not scatter emoji inside sentences.
- Do not narrate the shortening. Do not explain the emoji. Do not add a "full analysis is in the md" marker; there is no md.

## Common failure modes

- Writing "the Fed held rates" as the conclusion. That is the decision, not the verdict.
- Skipping the prior statement, so the wording diff is missed.
- Printing calculation steps. This variant never shows arithmetic.
- Writing an md file or calling present_files. This variant is inline only.
- Keeping the Meeting / Decision date / Reviewed line. It is removed.
- Keeping the closing split line. It is removed.
- Padding to two institutions when they agree. One house when they agree, two only when they differ.
- Citing an aggregator as an institution's view. Only the bank's own site counts.
- Citing a pre meeting preview or a stale outlook as the read on this meeting.
- Long sentences. Keep every line short.
