---
name: fomc-short-analysis-plain
description: Produce Turbo's short FOMC analysis in plain text only, no visualization, no rendered widgets or artifacts, so the output works inside Claude and on general gateways like Telegram and Slack that only display plain text and emoji. The full analysis lives in a markdown file; the inline chat answer is a shortened, emoji enhanced version pointing to the md. Verdict first as POTENTIAL HIKE or POTENTIAL CUT, two one sentence reasons each with official Fed sources, and exactly three institutions each tagged with their tendency. Institution sources must be the bank's own official research site and a direct reaction to the specific meeting, published after the decision. Use when Turbo says "fomc plain", "fomc analysis", "analyze the last fomc", "fomc short", "what did the fed do", "run fomc on the last meeting", "fomc preview", or names a specific FOMC meeting date. Works for a past decision, a minutes release, or a preview of an upcoming meeting.
---

# FOMC short analysis (plain)

**Plain text only.** This variant produces nothing but plain text and emoji. No charts, no visualizations, no rendered widgets, no HTML artifacts. The output must render correctly inside Claude and on general gateways such as Telegram, Slack, and any chat surface that only shows plain text. The two deliverables are the plain markdown file and the plain inline chat answer, nothing else.

Produce a short, decision first FOMC note. There are two deliverables and they differ on purpose:

1. **The markdown file** holds the FULL analysis. Reasons carry the arithmetic inline, institution takes run two to three sentences, all sources are shown. This is the artifact of record.
2. **The inline chat answer** is a SHORTENED version of the same note. Reasons are one sentence with no calculation steps, institution takes are one to two sentences, emoji are used to enhance readability, and a marker under the answer tells Turbo the full analysis is in the md.

Short means short: the inline answer fits on one screen.

## Standing preferences, apply throughout

- Use Exa for all web search (`web_search_exa`, `web_fetch_exa`). Cross check X for institutional reaction where useful.
- **Never use the "-" hyphen character in narrative prose.** Use spaces, "and", "to", commas or parentheses. Hyphens inside URLs and inside directly quoted official text are fine.
- Cite the source for every data point.
- **In the markdown file, show every calculation step.** Never state a derived number without the arithmetic. In the inline answer, drop the calculation steps and state only the result.
- Primary Fed documents outrank secondary coverage. If a figure only exists via journalists quoting a source, say so.
- Dates in narrative use spaces: 2026 07 29.
- No filler, no throat clearing, no "here is what you asked for".

## Step 1. Work out which meeting

Check today's date against the official calendar at https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm. Never trust a hardcoded schedule.

- If Turbo names a meeting, use it.
- If Turbo says "last meeting" or "previous meeting", use the most recent completed decision date.
- If Turbo says "preview" or "next meeting", use the next decision date.

If no FOMC event exists for the date implied, say so plainly and stop. Do not manufacture analysis.

## Step 2. Read the primary documents first

Fetch in this order, before touching any commentary:

1. Statement: `https://www.federalreserve.gov/newsevents/pressreleases/monetaryYYYYMMDDa.htm`
2. **Prior meeting's statement**, same URL pattern, for the wording diff. This is not optional. The diff is usually where the signal is.
3. Implementation note: same pattern with `a1.htm`
4. Press conference transcript: `https://www.federalreserve.gov/mediacenter/files/FOMCpresconfYYYYMMDD.pdf`
5. If an SEP meeting: `https://www.federalreserve.gov/monetarypolicy/files/fomcprojtablYYYYMMDD.pdf`
6. If minutes are out: `https://www.federalreserve.gov/monetarypolicy/fomcminutesYYYYMMDD.htm`

**SEP PDF warning.** The projections table frequently extracts with the character order reversed, so a median reads as "8.3" instead of "3.8". Reverse the token order and reverse each token, then cross check every median against at least two secondary sources before using it. The accessible HTML version at `fomcprojtabl20YYMMDD.htm` usually extracts cleanly and is the fastest cross check. Secondary sources routinely confuse core PCE with headline PCE, so trust the PDF or accessible HTML over them once you have parsed it.

**Dot plot arithmetic.** SEP dots round to the nearest 1/8. A published median that is not on the 1/8 grid is the average of the two middle dots. Example: a published 3.8 at a 3.50 to 3.75 target means (3.625 + 3.875) / 2 = 3.75, which is exactly half a hike from the 3.625 midpoint. Always state which.

## Step 3. Form the verdict

The verdict is always one of two words: **POTENTIAL HIKE** or **POTENTIAL CUT**. Never "unchanged direction", never "on hold", never "no change". A hold at the meeting is not the verdict; the verdict is where the next move points.

Hedge the confidence, not the direction. "Potential hike, not a potential cut" is right. "Direction is unchanged" is wrong.

Anchor the verdict on the real policy rate versus the Committee's own neutral estimate. Always compute this and show it in full in the md:

    Policy midpoint  = (lower bound + upper bound) / 2
    Real policy rate = policy midpoint − latest core PCE
    Real neutral r*  = SEP longer run fed funds median − SEP longer run PCE median
    Gap              = real policy rate − real neutral

Below neutral with inflation above target points to a potential hike. Above neutral with inflation falling points to a potential cut. State the gap in basis points in the md. In the inline answer, state only the rounded gap ("roughly 88 bp below neutral"), not the arithmetic.

Then pick the two strongest supporting reasons. Two, not three.

## Step 4. Pick exactly three institutions

Three, no more. Prefer large and named houses: Goldman Sachs, Morgan Stanley, JPMorgan, Deutsche Bank, BofA, Citi, Barclays, Nomura, UBS, PIMCO, BlackRock, Apollo, Pantheon Macroeconomics, Scotiabank, RBC, Western Asset, TrendMacro. Avoid consultancies and retail brokers unless nothing better exists. Name the individual economist or strategist where you have them.

**Two hard rules on institution sourcing. Both must hold for every one of the three.**

1. **Official source only.** The link must be the institution's own official site (for example morganstanley.com, goldmansachs.com, citigroup.com, jpmorgan.com). Never cite a third party aggregator (TradingKey, HTX, TipRanks, Yahoo, Bloomberg, Reuters, CNBC, biggo, stockwirex, and the like) as the institution's view, even if that aggregator is quoting the bank accurately. If the only source you can find for a house is an aggregator, drop that house and pick a different one that has published on its own site.
2. **Direct reaction to this specific meeting, published after the decision.** The piece must be that institution reacting to the meeting you are analyzing, dated on or after the decision date. A pre meeting preview, a generic quarterly outlook that predates the meeting, or a note about a different meeting does not qualify. When a house's canonical Fed page predates the meeting, find the post meeting piece (a post decision client note writeup, a post meeting insights article, an asset management strategist's read on the meeting) and cite that instead.

**Aim for disagreement.** At least one of the three should lean the other way if any house does. If all three genuinely agree, that is fine, say so.

Each institution gets a tendency tag in parentheses, one to three words, using the same vocabulary as the verdict: (potential hike), (potential cut), (potential hike, low conviction), (potential cut, 2027), (potential hike, deferred), (potential hike risk, base case hold).

## Step 5. Write the markdown file (the full version)

Exact output shape for the md. Do not add sections.

```markdown
# FOMC analysis

**Meeting: [Month DD to DD YYYY] · Decision date: [YYYY MM DD] · Reviewed: [today]**

## Conclusion: POTENTIAL HIKE

[One or two lines. The verdict, the size if it happens, the earliest realistic window.]

**Reason 1. [One sentence claim.]** [Two or three sentences WITH the arithmetic shown inline.]

Sources: [Short title](url) · [Short title](url)

**Reason 2. [One sentence claim.]** [Two or three sentences.]

Sources: [Short title](url) · [Short title](url)

## Key analysis from institutions

**[House] ([tendency tag]).** [One to three sentences: the house's direct post meeting call, quoted where useful, plus its reasoning.] [Official post meeting source](url)

**[House] ([tendency tag]).** [One to three sentences.] [Official post meeting source](url)

**[House] ([tendency tag]).** [One to three sentences.] [Official post meeting source](url)

[One line on where the split sits.]
```

Rules on the md shape:

- Sources go on their own line **underneath** each reason, never inline inside the prose. Link titles are short: "FOMC statement, June 17", not the full page title.
- Separate multiple sources with a middot.
- No "how it has aged" section, no market pricing table, no "what it means" breakdown, no uncertainty section.

## Step 6. Write the inline chat answer (the shortened version)

Reproduce the note in chat, but shortened per these rules. This is what Turbo reads first.

- **Title and every section header carry a relevant emoji.** Example set: 🏛️ for the title, ⬆️ or ⬇️ for the conclusion, 🔥 / 📈 for reasons, 🏦 for the institutions header, 🎯 for the closing split line. Give each institution a tendency emoji: 🐂 for a hike lean, 🕊️ for a cut lean, ⚖️ for a balanced or low conviction lean. Keep it to one emoji per header or line. Do not scatter emoji inside sentences.
- **Reasons are ONE sentence each, with NO calculation steps.** State the result, not the arithmetic. "Policy sits roughly 88 bp below neutral while core PCE was revised up from 2.7 to 3.3 percent, biasing the next move toward firming." Keep the Sources line under each reason exactly as in the md.
- **Institution takes are ONE to TWO sentences each**, with the same tendency tag and the same official post meeting source link as the md.
- Keep the conclusion block and the closing one line split, same as the md.
- **After the whole note, add a horizontal rule and this marker on its own line:**

  `📄 **The full analysis (with all calculation steps and sources) is in the md.**`

- Do not narrate the shortening. Do not explain the emoji. Just produce the note then the marker.

## Step 7. Deliver

Write the full markdown file to `/Users/turboguo/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Information and knowledge/FOMC/YYYY MM DD [decision|minutes|preview].md`, creating the FOMC folder if needed.

Frontmatter:

```yaml
---
type: fomc analysis
date: YYYY MM DD
meeting: [Month] YYYY
mode: decision | minutes | preview
decision: [target range and vote, or "upcoming" for a preview]
call: POTENTIAL HIKE | POTENTIAL CUT, [earliest window], [size]
generated: YYYY MM DDTHH:MM:SS
---
```

Then present the file with `present_files`, and reproduce the shortened inline answer in chat per Step 6.

## Common failure modes

- Writing "the Fed held rates" as the conclusion. That is the decision, not the verdict. The verdict is where the next move points.
- Skipping the prior statement, so the wording diff is missed.
- Using an SEP median straight from a mangled PDF extraction without reversing and cross checking it.
- Citing an aggregator (TradingKey, HTX, Yahoo, Bloomberg, CNBC) as an institution's view. Only the bank's own site counts.
- Citing a pre meeting preview or a stale quarterly outlook as the institution's read on this meeting. It must be dated on or after the decision and be about this meeting.
- Putting the calculation steps into the inline answer. Arithmetic lives in the md only; the inline reasons are one sentence with the result.
- Forgetting the "full analysis is in the md" marker under the inline answer.
- Letting the institutions section run to five or six houses. Three.
- Burying sources inside sentences instead of on a line underneath.
- Adding sections. If it does not change the verdict, cut it.
