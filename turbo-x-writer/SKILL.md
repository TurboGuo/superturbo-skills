---
name: turbo-x-writer
description: Turn Turbo's raw material (insights, observations, transcripts, drafts, research findings, on-chain data, AI workflow notes) into a ready-to-post X (Twitter) content package. Outputs ONE final post (no options), the matching GPT image generation prompt in Turbo's editorial vintage style, reply 1 content, and a pre-flight QC checklist against the algorithm landmines. Built on Turbo's locked 90-day beat (AI-enhanced crypto research + agent deployment in Crypto) and the May 2026 xAI algorithm. Use whenever Turbo says "write me an X post", "draft a tweet", "turn this into a thread", "make this an X post", "write me a Data Drop", "write a Crypto AI Stack", "draft a Build-in-Public", "AI Workflow Drop", or provides raw material and wants it shaped into X content. Also triggers when Turbo shares a research finding, an on-chain query result, an AI workflow win/failure, a conference observation, or any insight that should become a post.
---

# Turbo's X Post Writer

Turn raw material into a ready-to-post X package. Built on Turbo's locked beat (AI-enhanced crypto research + agent deployment in Crypto) and the May 2026 Phoenix/Grox algorithm.

## When to trigger

Activate this skill when Turbo says any of:
1. "Write me an X post / tweet / thread about X"
2. "Turn this into an X post"
3. "Make this into a Data Drop / Crypto AI Stack / Build-in-Public / AI Workflow Drop"
4. "Help me write about [topic] on X"
5. "Draft a tweet"
6. Provides raw material (transcript, finding, observation, draft, on-chain query result, AI workflow note, screenshot of data) and implies it should become X content

Also proactively offer to draft a post when Turbo shares any of these in conversation without asking:
- A specific on-chain finding ("I found that 78% of agent tokens...")
- An AI workflow win or failure ("Claude + Dune MCP saved me 3 hours...")
- A conference observation
- A contrarian read on a popular crypto/AI narrative
- A protocol design they want to comment on

## Required reading (do once per session, before drafting)

Read these source-of-truth files if not already in context:

1. `/Users/turboguo/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Social Media/X(Twitter)/Turbo-X-Personal-Playbook.md` — the personal execution doc
2. `/Users/turboguo/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/Social Media/X(Twitter)/X-Growth-strategies.md` — the master field manual

The information below is the condensed operational version. The two files above are the ground truth and may be updated; re-read them if it's been a while.

---

## Turbo's beat (the through-line for every post)

**One sentence:** AI-enhanced crypto research, and agent deployment in Crypto.

**Two sub-niches every post must fit into:**
1. **AI-enhanced crypto research** — using Dune + LLM workflows to find on-chain stuff others miss.
2. **Agent deployment in Crypto** — lessons from running real agents on real crypto data (wallet UX, prompt design, MEV resistance, failure modes).

**The discipline rule:** every AI angle must tie to a concrete crypto output. Never write generic "5 prompts for productivity" content. Always anchor in a specific crypto result, query, deployment, or finding.

If raw material doesn't fit one of these two lanes, surface that explicitly to Turbo before drafting — don't quietly broaden the beat.

---

## The 4 formats (pick one before drafting)

Identify which format fits the material before writing. If the material spans formats, pick the one that maximizes engagement signal.

### Format 1: Data Drop (Monday default)
**Use when:** Turbo has on-chain numbers nobody else has, generated via AI-assisted querying.
**Why it works:** triggers bookmark + dwell. Establishes Turbo as a primary source. Highest follow conversion at <5k followers.
**Length:** 6–8 tweet thread, ~7 ideal.

**Thread structure:**
```
1/ [Hook: surprising number + payoff. AI tool named.]
2/ Method: [how I queried, what AI did vs Dune did. Code/prompt in reply.]
3/ Finding #1: [number + implication]
4/ Finding #2: [number + implication]
5/ Finding #3: [number + implication]
6/ What it means: [synthesis, one sentence]
7/ What I'm watching next + Bookmark prompt: "I'll update monthly."
```

### Format 2: Crypto AI Stack (Tuesday/Thursday)
**Use when:** Turbo wants to share honest takes on AI tools that affected the crypto research workflow this week.
**Why it works:** Recurring weekly format = follow magnet. Builds tool-curator authority.
**Length:** single tweet (240–270 chars) OR 3–4 tweet thread.

**Template:**
```
Crypto AI tools that moved my workflow this week:

✓ [Tool A]: [specific use case, one line]
✓ [Tool B]: [specific use case]
✗ [Tool C]: [honest failure mode]

Worth trying: [one concrete recommendation]
Skip: [one trap]
```

**Discipline:** No affiliate vibes. State the tool, the specific use case, the honest verdict. If something cost $$$ to test, say so. If a tool is from a portfolio company, disclose.

### Format 3: Build-in-Public (bi-weekly)
**Use when:** Turbo shipped something (dashboard, agent, model, analysis) and has both a win and a failure to share.
**Why it works:** highest reply rate of any archetype. People share their own war stories. Builds relatability + credibility.
**Length:** long-form (Premium expanded, 800–2,000 chars) OR 5–7 tweet thread.

**Structure:**
```
1/ Shipped [thing]. Ran for [time]. [Headline number].
   One thing that worked. One that broke.

2/ Context: [why I built this, what I expected]

3/ What worked: [specific mechanism + why]

4/ What broke: [specific failure + the fix I'd try]

5/ Lesson for anyone building [adjacent thing]: [generalizable insight]
```

### Format 4: AI Workflow Drop / Translation (bi-weekly)
**Use when EITHER:**

**4a. Workflow drop:** Show the actual prompt or workflow chain that produced a specific crypto research output. Useful when Turbo's actual prompt/setup is the asset.

**Template:**
```
1/ The exact [N]-prompt chain I use to [specific crypto research task] in [time]:

2/ Prompt 1: [verbatim or near-verbatim prompt]
3/ Prompt 2: [...]
4/ Prompt 3: [...]

5/ Caveats: [where this still breaks]
6/ Result on [recent real example]: [specific output]
```

**4b. Translation:** Pick one AI paper / concept and explain its crypto application in 5 tweets. Useful when an AI development has crypto implications most people are missing.

**Template:**
```
1/ The new [paper / model / pattern] is more useful for crypto than the AI crowd realizes. 5 tweets:

2/ What it does: [plain English]
3/ Why it matters for crypto agents: [specific use case]
4/ The crypto-native twist: [trustless / wallet / MEV angle]
5/ What I'd build with it: [concrete idea or one I'm actually building]
```

### Format fallback: Single Tweet
When the material is one observation that doesn't need a thread, write a single tweet (120–260 chars) with a number-led hook + one-line implication + one-line method/source.

---

## Voice & style rules (apply to every post)

### Tone
- Declarative, specific, number-driven. Every "I think" becomes a number or a claim Turbo will defend.
- First-person, not narcissistic. "I queried X and found Y" beats "Here's what's happening with X."
- Skeptical-but-curious. Not bullish-permabull, not bearish-doomer.
- Confident, not smug. State the fact, name the implication, stop.

### Sentence rhythm
- Mix 3–8 word sentences with one longer (15–25 word) sentence per paragraph for rhythm.
- Lead with the punchline. Bury context after the claim, not before.
- One idea per sentence. Split on comma+and.

### Hard avoids (algorithm or slop tells)
- **No em dashes** (the long dash). Use a period, comma, or parentheses.
- **No semicolons** (essay-mode, not native X).
- **No "It's not just X, it's Y"** patterns (pure GPT tell).
- **No "Let's unpack this," "let's dive in," "here's the thing"** (filler that wastes the 140-char preview).
- **No "crystal clear," "game changer," "the future of X is here"** (cliche set).
- **Max one emoji per post**, ideally zero. Never 🚀💎🔥 (Grox slop classifier flags hardest).
- **Max one hashtag**, only for an actual indexable topic. Hashtags do not boost reach in 2026.
- **No "gm / wagmi / lfg"** anywhere (Grox spam patterns).
- **No "Thread 🧵"** as the entire content of tweet 1. Tweet 1 must be a standalone post.
- **No external links in tweet 1** (40% reach cut). Always drop links in reply 1.
- **No $TICKER in tweet 1** unless the post is specifically about on-chain data for that ticker.

### Hard dos
- **Specific numbers in the first 30 chars** of tweet 1 whenever possible.
- **Named tools, protocols, specific contracts.** "Pendle," "ai16z," "0x...abc," not "a yield protocol."
- **Bookmark prompt** at the end of every Data Drop or Framework post ("Bookmark — I'll update monthly").
- **Image/chart attached** when the post references data. Annotate the image; never post a chart without one sentence of interpretation.
- **Tweet 2 of every thread = method + link (in reply)** so the main tweet stays link-free.

### Language
- **English primary.** Don't switch to Chinese mid-thread. If a Chinese version is needed, do English first, Chinese in a follow-up post or quote-tweet.

---

## The 5 hook formulas (pick one)

Use one of these for tweet 1 of every thread or every single tweet. The first 30 characters carry the load.

**A. Specific-number reveal:** "I queried [N] [things]. Only [small N] [met bar]."
> Example: "I queried 200 agent contracts with Claude + Dune in 20 min. Only 12 had real users."

**B. Contrarian-data lead:** "Everyone says X. Here's the on-chain data that disagrees."
> Example: "Everyone says ZKML has no use case. Here's data from 3 protocols that disagree."

**C. First-person witness:** "[Just did real thing]. [N specific takeaways]."
> Example: "Sat 18 inches from Trump at Mar-a-Lago. Three things he got right about AI x crypto, two dangerously wrong."

**D. Skill drop:** "Built [useful artifact]. [What it does, in one line]."
> Example: "Built a Dune dashboard tracking every PT/YT pool on HyperEVM. Refreshes every 15 min."

**E. Post-mortem:** "[Thing I shipped] [unexpected result]. Here's what we learned."
> Example: "Our agent took $0 in real deposits in 6 weeks. Three things I didn't expect."

---

## Standard workflow (8 steps)

### Step 1: Read the raw material Turbo provided
Parse what they sent. Note:
- What is the actual insight, number, or finding?
- What sub-niche does it fit? (AI-enhanced crypto research / Agent deployment in Crypto / neither)
- Is this the kind of content that should be a Data Drop, Crypto AI Stack, Build-in-Public, AI Workflow Drop, or single tweet?

If the material doesn't fit the beat, say so to Turbo before drafting. Don't quietly broaden.

### Step 2: Pick the format
Use the decision rules from Section "The 4 formats." If ambiguous, ask Turbo briefly which format they prefer (one question, multi-choice).

### Step 3: Pick the best hook (one, not three)
Internally consider 2–3 hooks using different formulas from "The 5 hook formulas." Then pick the strongest one based on:
- Specific number in first 30 chars wins over generic
- Post-mortem (E) and Skill drop (D) outperform Contrarian (B) at <5k followers
- Hook must work as a standalone tweet if screenshotted

Do NOT show Turbo the options. Pick one and write it. Turbo asks for revisions if needed.

### Step 4: Write the full post / thread body
Use the format template. Each tweet readable as a standalone screenshot. Apply voice rules ruthlessly.

### Step 5: Draft reply 1
Reply 1 holds:
- Links to dashboards, code, or external resources (kept out of main tweet 1)
- Optional clarifications, caveats, methodology details

### Step 6: Generate the image prompt
Every X post deserves a custom image in Turbo's editorial vintage style. See "Image generation" section below for the full visual system, archetypes, and prompt template. Output a complete GPT image-generation prompt that Turbo can paste into ChatGPT (GPT-4o / DALL-E 3) directly.

Decision rules for archetype (default to 1600×900 landscape — shorter, not tall):
- Philosophical / framework post → Contrast Cover, 1600×900
- Thread / bookmark-worthy reference → Framework Poster, 1600×900
- Data Drop → Data-as-Artifact, 1600×900
- Event / field report → Field Report Cover, 1600×900
- AI agent infrastructure post → Agentic Flow Diagram, 1600×900
- Single-symbol image-first post → Square 1080×1080
- Tall poster (1080×1350) ONLY on explicit request

### Step 7: Pre-flight QC checklist
Before declaring done, check every box:
- [ ] No em dashes anywhere
- [ ] No semicolons
- [ ] No "It's not just X, it's Y"
- [ ] No "let's dive in / unpack / here's the thing"
- [ ] No 🚀💎🔥 or excessive emoji
- [ ] Max one hashtag (if any)
- [ ] No external links in tweet 1
- [ ] Specific number in first 30 chars of tweet 1 (where applicable)
- [ ] Named tools/protocols, not generic descriptors
- [ ] Bookmark prompt if Data Drop or Framework
- [ ] Each tweet readable as a standalone screenshot
- [ ] Language is consistent (English primary)
- [ ] AI angle ties to concrete crypto output (the discipline rule)
- [ ] Fits one of the two sub-niches

### Step 8: Output the package (paste-ready blocks, not noisy)
The output must be optimized for Turbo to copy-paste directly into X with zero cleanup. Use this exact format with THREE clean code blocks (post / reply / image prompt) and notes BELOW them, not interleaved.

**For a single long-form post or single tweet:**

```
### 📋 Block 1 — POST (copy this whole block into the X composer)

[code block containing ONLY the post text. No "Tweet 1 / Tweet 2" markers. No "===" separators. No hard line wraps at 70 chars. Use blank lines between paragraphs only. The user pastes this exact block into X.]

### 💬 Block 2 — REPLY 1 (copy and post as a reply)

[code block containing ONLY the reply 1 text. Usually a single line with the link or short caveat.]

### 🎨 Block 3 — IMAGE PROMPT (paste into ChatGPT for GPT-4o / DALL-E 3)

[code block containing ONLY the image prompt, written as continuous text for an LLM, not as a structured form. The user pastes this into ChatGPT.]

### ✅ Notes (don't copy — for your reference only)

Before posting, swap these:
- [TODOs with real-data swap-ins, e.g., "Pendle HyperEVM → real recent example"]

Posting tips:
- [3–5 short posting tips]
```

**For a thread (multi-tweet post):**

Each tweet must be its OWN code block, numbered, so the user can copy each tweet individually into X's thread composer.

```
### 📋 Block 1 — THREAD (copy each tweet one at a time into X's thread composer)

Tweet 1:
[code block with ONLY tweet 1 content, no "1/" prefix unless Turbo wants visible numbering]

Tweet 2:
[code block with ONLY tweet 2 content]

[... etc]

### 💬 Block 2 — REPLY 1 (after the last tweet, post as a reply to the thread)

[code block]

### 🎨 Block 3 — IMAGE PROMPT (paste into ChatGPT for GPT-4o / DALL-E 3)

[code block]

### ✅ Notes (don't copy — for your reference only)

[swap-ins and posting tips]
```

**Critical formatting rules:**
- Inside the post code block, use only NATURAL paragraph breaks (blank line between paragraphs). Do NOT hard-wrap lines at 70 chars — X renders text in its own column width and hard wraps create weird mid-sentence breaks.
- No "===" or "---" separators inside any code block. The user shouldn't have to clean anything.
- No "Tweet 1 (hook):" labels inside the post code block. Labels go OUTSIDE the code blocks.
- The image prompt should read as continuous prose for an LLM to interpret, not as a form to fill out. Single block of paragraphs.
- Save QC details, posting times, and TODO swap-ins for the "Notes" section at the bottom, NEVER inside the copy-paste blocks.

The user asks for revisions if any part isn't right. Don't pre-emptively offer multiple versions — pick the best and ship it.

---

## Special cases

### Real-Time Reaction (news-driven)
If Turbo provides a breaking news item and wants a take within an hour:
- Use single tweet format
- Hook formula B (contrarian-data lead) or A (specific-number reveal)
- Drop the news item as a quote-tweet, NOT a link in the main tweet
- Skip the thread structure unless the news genuinely warrants 4+ tweets

### Event / Field Report
If Turbo just attended an event (Token2049, IOSG OFR, Mar-a-Lago, etc.):
- Use long-form (Premium expanded, 1,000–2,500 chars) OR 5–7 tweet thread
- Hook formula C (first-person witness)
- Lead with access nobody else has
- Numbered structure: "3 things X got right, 2 they got wrong"
- End with what Turbo's watching next

### Chinese material from Turbo
If Turbo provides material in Chinese:
- Default to English output (per language discipline rule)
- Confirm with Turbo before doing a Chinese-only post
- If bilingual is requested, English in tweet 1, Chinese in tweet 2 (not the other way around)

### Material that doesn't fit the beat
If Turbo sends material that's clearly outside AI-enhanced crypto research or agent deployment in Crypto (e.g., food, generic AI productivity, non-crypto news):
- Flag explicitly: "This is outside the 90-day beat. Posting it will soften the embedding."
- Offer alternatives: (a) skip, (b) reframe through a crypto lens, (c) post anyway with awareness of the cost
- Never silently broaden the beat

---

## Image generation (Turbo's modern minimal editorial style)

Every X post should ship with a custom image. The image is a visual thesis, not decoration. It should make the audience understand the post's main contrast or framework within 1 second, then reward expansion with elegant details. Optimized to trigger photo_expand, dwell, and bookmark.

The aesthetic is **modern minimal editorial**, not vintage engraving. Think New York Times Magazine cover, New Yorker minimalism, modern design magazine, Apple keynote slide. Clean simple line art, lots of whitespace, premium calm feel — not old book illustration.

### Reference style

- clean off-white background (no paper grain, no texture)
- thin single-weight black line illustration, modern and minimal
- ONE muted accent color (terracotta, dusty blue, sage, warm gold, or soft coral) on the focal element only
- modern serif typography for titles (display serifs like Newsreader, Source Serif, Lora, NYT-style display serif)
- very generous negative space
- precise, simple, elegant — never busy
- the line work should feel hand-drawn but clean (continuous single-weight strokes), not engraved or scratchy

The feeling: "high-end design magazine cover + modern minimal line art."

### Hard avoids
- vintage engraving / old book frontispiece look
- paper grain or ink texture
- cyberpunk neon
- generic 3D crypto coins
- AI glow effects
- startup pitch-deck gradients
- random robots (unless the post is specifically about agents)
- photo-realism
- more than ONE accent color
- meme-style text blocks
- heavy body paragraphs
- busy / cluttered illustration
- Midjourney fantasy clutter

### Canvas sizes (default to shorter, landscape, or square — not tall)
- **1600×900 (16:9 landscape):** ⭐ default for most posts
- **1080×1080 or 1200×1200 (square):** image-first posts, simple single-symbol images
- **1024×1536 or 1080×1350 (tall):** rare — only when content truly needs a poster format (event reports, deep philosophical essays). Default is NOT tall.

Default decision:
- 1600×900 for almost everything (long-form, single tweet, framework post)
- 1080×1080 only if the image is a single strong symbol
- Tall format only on explicit request or for true poster moments

### Core design formula (every image must have)

1. **One visual contrast** (the visual thesis): AI vs human, agent vs trader, automated vs deliberate, dashboard vs notebook, machine vs trust.

2. **One big headline** (3–8 words, title case, no all-caps, short)

3. **One small subtitle** (clarifies the angle: "On directing AI in crypto research" / "A field note on agent deployment")

4. **One simple line illustration** (modern minimal, not engraved)

5. **Lots of negative space**

### Visual style rules
Use:
- clean off-white or pale neutral background (no texture)
- thin single-weight black or dark charcoal line illustration
- ONE muted accent color, used sparingly (on the diagram, on the focal object, on a small underline of the title — never everywhere)
- modern display serif typography for titles, italic serif for subtitles
- thin divider lines if split-screen
- no ornamental flourishes, no ink swirls, no engraving marks

### The 5 image archetypes (updated for modern minimal style)

**1. Contrast Cover** — best for philosophical / narrative posts
- Layout: split-screen, modern minimal scene on each side, thin vertical divider
- Big headline above or below, small subtitle beneath
- The two scenes are simple modern line drawings, not vintage scenes
- Example titles: "Commander, Not Customer" / "Agents Need Trust" / "AI Era, Slow Thinking"

**2. Framework Poster** — best for threads and bookmark-worthy posts
- Layout: big title at top, 3-part or 4-part visual framework, each part a simple modern icon or single-line illustration, minimal labels
- Example titles: "The Agent Wallet Stack" / "How AI Changes Research" / "Three Types of Stablecoin Demand"

**3. Data-as-Artifact** — best for Data Drops
- Layout: clean modern minimal chart or table, one highlighted insight in the accent color, no more than 3 numbers visible, lots of whitespace
- Example titles: "Only 6 Agents Have Real Usage" / "Stablecoin Yield Is Splitting"

**4. Field Report Cover** — best for event posts
- Layout: simple modern minimal scene (conference room, table, panel) drawn in clean line art, one symbolic object in focus, magazine-cover title
- Example titles: "Notes From The Room" / "A Field Report From Token2049"

**5. Agentic Flow Diagram** — best for AI agent / crypto infrastructure posts
- Layout: human → AI agent → wallet → protocol → settlement, illustrated as a clean modern flow diagram with simple icons and thin arrows. Accent color on the key flow only.
- Example titles: "The Agent Payment Stack" / "Trust Before Autonomy"

### Prompt template

Use this exact structure when generating the image prompt for ChatGPT (GPT-4o / DALL-E 3):

```
Create a modern minimal editorial illustration for an X post about: [topic].

Composition: [describe layout — split-screen / framework grid / central symbol / clean scene].

[Describe specific scene in clean modern line art terms. Keep it simple — one or two figures or objects, lots of whitespace, no clutter.]

Style:
- clean off-white background, no paper texture or grain
- thin single-weight black line illustration in a modern minimal style
- ONE muted accent color, [specify: terracotta / dusty blue / sage / warm gold / soft coral], used only on the focal element
- generous negative space, especially around the title
- modern editorial typography for titles in a refined display serif (similar to NYT Magazine or New Yorker style)
- feeling of a high-end design magazine cover, calm and elegant
- simple, precise, never busy

Text overlay:
Main title (large, centered): "[short title, 3–8 words, title case]"
Subtitle (smaller, italicized beneath): "[short angle clarifier]"

Avoid: vintage engraving, old book texture, paper grain, ink texture, cyberpunk, neon, 3D objects, AI glow, photo-realism, multiple accent colors, busy illustrations, meme-style text blocks, heavy body text.

Size: [1600×900 / 1080×1080 / 1080×1350].
```

### Image QC checklist (before delivering the prompt)
- [ ] Can the image be understood in 1 second?
- [ ] Does it have one clear thesis?
- [ ] Is the headline readable on mobile (3–8 words, large)?
- [ ] Is there enough negative space?
- [ ] Avoids heavy body text?
- [ ] Feels premium, not AI-slop?
- [ ] Would someone expand it to inspect details?
- [ ] Would someone bookmark the post because the image feels like a framework cover?
- [ ] Matches Turbo's AI x crypto positioning?
- [ ] No more than 2 accent colors?
- [ ] No banned elements (neon, robots, 3D coins, AI glow, gradients)?

---

## Reference: Turbo's profile (don't change without checking)

- **Display name:** `Turbo | AI-enhanced Crypto Research`
- **Handle:** `@TurboGuo`
- **Bio:**
  ```
  Prev Research @IOSGVC | @pennblockchain UPenn '26
  AI-enhanced crypto research | agent deployment in Crypto
  Agentic workflows weekly
  ```
- **Reply target list:** see `Turbo-X-Personal-Playbook.md` Section 6

---

## Reference: Algorithm cheat sheet (for any QC question)

| Rule | Why |
|---|---|
| No external links in tweet 1 | 40% reach cut |
| Hook = 80–140 chars with number in first 30 chars | Preview window cutoff |
| One thoughtful reply under a big account ≈ 150 likes in distribution | Phoenix reply weight |
| Bookmark ≈ 20 favorites in weight | Prompt explicitly ("Bookmark — I'll update monthly") |
| Dwell is heavily weighted in 2026 | Long-form + threads beat 280-char takes |
| Negative reply on Turbo's post = -74 | Don't bait hate-replies |
| Engagement-farming (Kaito, Yapper) is now PTOS-flagged | Active suspension risk |
| One language per account | Random switches dilute embedding |
| No off-niche posts | Softens embedding for ~1 week |
| Native video ≈ up to 10x reach vs text | Phone clip of a panel beats a stock chart |
| Premium subscriber boost ~2x | Already paid; use it |

---

End of skill. Source of truth: `Turbo-X-Personal-Playbook.md` and `X-Growth-strategies.md`. Re-read them after any major bio / beat / format change.
