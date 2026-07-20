---
name: x-writer
description: "Analyze a user's X/Twitter writing style and generate draft posts that sound like them. Use this skill whenever the user asks to generate tweet drafts, write posts in their voice, create X content, ghostwrite tweets, or wants help with their X/Twitter posting strategy. Also triggers on phrases like \"draft tweets for me\", \"write posts in my style\", \"generate X content\", \"ghostwrite\", \"tweet ideas\", \"help me post on X\", \"analyze my posting style\", or \"x writer\". This skill is shareable. Requires Bearer Token and X handle to be set in the skill config before use."
---

# X Writer

Generate draft X/Twitter posts that match a user's authentic voice. No auto posting. Human approval always required.

## ========== USER CONFIG (EDIT THESE TWO LINES) ==========

```
BEARER_TOKEN: YOUR_BEARER_TOKEN_HERE
X_HANDLE: YOUR_X_HANDLE_HERE
```

## =========================================================

### How This Works

If the config above is already filled in, proceed directly to Step 1. No need to ask the user anything.

If the config still has placeholder values (`YOUR_BEARER_TOKEN_HERE` or `YOUR_X_HANDLE_HERE`), tell the user:

> "This skill needs your X API Bearer Token and your X handle to work. Please set them up:"
>
> 1. Open this skill file and find the `USER CONFIG` section near the top (it is clearly marked)
> 2. Replace `YOUR_BEARER_TOKEN_HERE` with your X API Bearer Token (get one at https://developer.x.com/en/portal/dashboard)
> 3. Replace `YOUR_X_HANDLE_HERE` with your X handle (no @ sign)
> 4. Save, then come back and ask me to write posts again.

Do NOT ask the user to paste their API key or handle into the chat. Do NOT proceed with the skill until the config is set. Just give the instructions above and stop.

## Step 1: Fetch Recent Posts

Pull the user's recent posts (up to 100) to build a style profile.

```bash
BEARER_TOKEN="<from config above>"
X_HANDLE="<from config above>"

# Resolve username to user ID
USER_ID=$(curl -s "https://api.twitter.com/2/users/by/username/$X_HANDLE" \
  -H "Authorization: Bearer $BEARER_TOKEN" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])")

# Fetch recent tweets (max 100 for good style analysis)
curl -s "https://api.twitter.com/2/users/$USER_ID/tweets?max_results=100&tweet.fields=text,created_at,public_metrics&exclude=retweets,replies" \
  -H "Authorization: Bearer $BEARER_TOKEN" -o /tmp/xwriter_posts.json
```

If the API returns an error, inform the user clearly:
| Code | Meaning | What to tell the user |
|------|---------|----------------------|
| 401 | Bad token | "Your Bearer Token appears invalid. Double check it at developer.x.com and update the config in SKILL.md." |
| 403 | Insufficient access | "Your API plan may not support this. Basic tier ($100/mo) or higher is needed." |
| 429 | Rate limited | "Rate limit hit. Wait 15 minutes and try again." |

## Step 2: Analyze Writing Style

Analyze the fetched posts to build a structured style profile. Compute the following from the raw post data:

**Tone and Voice**
- Formality level (casual, semi formal, formal)
- Use of humor, sarcasm, or dry wit
- Emotional register (enthusiastic, measured, provocative, chill)
- First person vs third person vs impersonal

**Structure Patterns**
- Average post length (characters and words)
- Use of line breaks and spacing
- Thread vs standalone preference
- Opening patterns (question, statement, hot take, observation)

**Vocabulary and Language**
- Common words and phrases (top 20)
- Industry jargon frequency
- Emoji usage (which ones, how often)
- Hashtag usage patterns
- Mix of English and other languages
- Abbreviations and slang

**Topic Clusters**
- Primary topics (ranked by frequency)
- Recurring themes
- What gets the most engagement

**Engagement Style**
- Call to action patterns
- Question posing habits
- How they reference other accounts (@mentions)
- Link sharing behavior

## Step 3: Ask User for Topic

After completing the style analysis, present the style profile summary to the user, then offer topic options for them to pick from.

**How to generate topic options:**

Derive 4 to 5 suggested topics based on:
1. The user's most recent posts (what they have been talking about in the last 1 to 2 weeks)
2. The user's highest engagement posts (what resonates with their audience)
3. A natural extension or follow up to a recent thread or take
4. One "fresh angle" topic that connects to their interests but they have not posted about yet

**Present the style profile summary, then the topic options using the ask_user_input tool.** Use a single select question with 4 to 5 options. Always include a final option like "Something else (I will type my own)" so the user is not locked into the suggestions.

If the user picks "Something else", ask them what topic they have in mind, then proceed.

Wait for the user to pick a topic before proceeding. Do NOT generate any drafts until the user has selected or provided a topic.

## Step 4: Research Fresh Content

Before drafting, do two rounds of research to gather fresh material:

**Round 1: Search X for high traction posts on the chosen topic.**
Use the x-reader skill (or X API search endpoint) to search X for recent posts related to the topic. Sort by engagement (likes, RTs). Note which framings, hooks, and structures get the most traction. Examples of patterns to look for:
- Concrete data/number comparisons
- "Most people dont realize..." gap framing
- "If you believe X, the best way to express it is Y" investment thesis framing
- Regulatory urgency or breaking news hooks
- Ecosystem validation posts

**Round 2: Search the web for the latest news, data, and developments on the topic.**
Use exa or web search to find:
- Fresh data points with exact sources
- Recent news (launches, regulatory updates, partnerships) from the past 2 weeks
- Original source articles (not aggregators) for every data point

**Cross check against existing posts:**
Compare all research findings against the user's fetched posts from Step 1. Remove any data point, take, or framing that already appeared in a previous post. Every draft must be genuinely new content.

**Verify every data point:**
Every number used in a draft must be traceable to a specific source article with a URL. If a data point cannot be verified, do not use it.

## Step 5: Generate 3 Draft Posts

Using the style profile from Step 2, the topic from Step 3, and the research from Step 4, generate exactly 3 draft posts.

**Generation Rules:**
- Match the user's average post length (do not suddenly write 280 char posts if they typically write 80 char posts)
- Use their actual vocabulary and phrasing patterns
- Mirror their tone exactly (if they are casual, be casual; if they mix languages, mix languages)
- Match their structural habits (line breaks, spacing, list style)
- Apply their voice and style to the requested topic, even if it is outside their usual range
- Include emoji only if and how they typically use them
- Never add hashtags if they do not use hashtags
- Never sound like a marketing bot or corporate account
- Each draft should take a different angle or framing on the same topic (e.g. hot take vs data driven vs question based)
- Drafts must NOT repeat any content, data, or framing from the user's existing posts
- Incorporate high traction patterns observed from X research in Step 4
- Every data point in the draft must come from verified sources found in Step 4

**Present each draft in this format:**

---

### Draft 1: [Short angle label, e.g. "Data driven macro take"]

[The full post text here as plain text, no blockquote, no code block. Just the raw post exactly as it would appear on X. Use line breaks as needed.]

**Why this sounds like you:** [1 sentence]

```
Sources:
[specific claim or number] — [Publication name], [date] — [full URL]
[specific claim or number] — [Publication name], [date] — [full URL]
```

---

### Draft 2: [Short angle label]

[post text as plain text]

**Why this sounds like you:** [1 sentence]

```
Sources:
[specific claim or number] — [Publication name], [date] — [full URL]
```

---

### Draft 3: [Short angle label]

[post text as plain text]

**Why this sounds like you:** [1 sentence]

```
Sources:
[specific claim or number] — [Publication name], [date] — [full URL]
```

---

**Important formatting notes:**
- The post text must be plain text with NO blockquotes, NO code blocks, NO markdown formatting. Just raw text exactly as it would appear on X so the user can copy paste directly
- Sources must be inside a code block (```) below each draft
- Each source line maps one specific data claim to one publication with a clickable URL
- Do not lump all sources together at the bottom. Each draft has its own source code block directly below it
- If a draft uses no external data (pure opinion/take), write "No external data cited" in the source block

## Step 6: Review and Iterate

After presenting drafts, ask the user:

> "Which drafts work for you? Want me to adjust any of them, change the angle, or generate fresh ones?"

**Iteration options:**
- Edit a specific draft (user provides feedback, you revise)
- Regenerate all 3 drafts with a different angle
- Adjust tone (more casual, more provocative, more technical, etc.)
- Make a draft shorter or longer
- Add or remove a specific element (emoji, question, call to action)
- Switch to a new topic entirely

**Never auto post. Always wait for explicit user approval.**

## Step 7 (Optional): Save Style Profile

If the user wants to reuse their style profile in future sessions, suggest saving it:

```bash
cp /tmp/xwriter_style_profile.json ~/x_style_profile_$X_HANDLE.json
```

Then in future sessions, the skill can load the saved profile instead of re fetching posts (though refreshing periodically is recommended to keep the style current).

## Tips for Best Results

- More posts = better style analysis. 100 posts gives a solid profile. Under 20 posts may produce generic results.
- The skill works best for accounts that post original content regularly. Accounts that mostly retweet or reply will have less data to work with.
- Bilingual accounts are fully supported. The skill detects language mixing patterns and replicates them.
- If the user wants posts about a specific topic they have not posted about before, the skill will apply their voice/style to the new topic while noting it is outside their usual range.
