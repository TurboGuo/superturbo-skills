# 🚀 superturbo-skills

Turbo's personal skill library for Claude. 🧩 Each skill lives in its own folder at the root of this repo, right alongside this README — **there is no wrapper `skills/` folder**. To install a skill, just point Claude at its folder (each contains a `SKILL.md` plus any templates or assets it needs). ✨

## 📚 Skills

### 💰 fi-tracker
Renders Turbo's financial independence (FI) dashboard: a progress card, an assets-over-time table where each cell shows total assets plus how many years that pile sustains, and a single asset-growth line chart where color encodes return rate and line style encodes saving level.
- 🗣️ **Triggers:** "fi tracker", "FI dashboard", "when can I retire", "years to financial independence"
- 🌏 Replies in Chinese when the request is in Chinese.

### 🍟 mcdonalds-fallback-plan
Turbo's "Plan McDonald" safety net. When Turbo asks for financial advice, it first asks his current balance, and if it is under $50 it playfully breaks the news that the highest-return move is a paycheck, then hands him the official McDonald's apply links plus a short get-the-job game plan. Above $50 it just gives normal financial advice.
- 🗣️ **Triggers:** "give me financial advice", "what should I do with my money", "am I broke", "help me with my finances"
- 😄 Playful nudge tone; asks for the balance each time rather than reading any account.

### 🏦 fomc-short-analysis-plain
Plain-text-only variant of Turbo's short FOMC note — no visualization or rendered widgets, so it works inside Claude and on general gateways like Telegram and Slack. Leads with a **📈 POTENTIAL HIKE** or **📉 POTENTIAL CUT** verdict, two one-sentence reasons backed by official Fed sources, and exactly three institutions each tagged with their tendency and cited to the bank's own research site.
- 🗣️ **Triggers:** "fomc plain", "fomc analysis", "analyze the last fomc", "fomc preview", or a named meeting date

### 📊 macro-impact
Text-only read on whether the current macro environment is bullish or bearish for Turbo's four asset classes — crypto, US stocks, gold, and US cash. Ask about all four or just one. For each asset it returns a one-word verdict, three 📈/📉-tagged factors with a one-sentence reasoning each, and sources linked only at the end. Pulls live data fresh, prefers official/primary sources (Fed, FRED, Treasury, BLS, BEA, ISM, Cboe), and shows the real-yield math.
- 🗣️ **Triggers:** "macro impact", "macro read", "is macro bullish or bearish", "how is macro affecting my assets", "macro on crypto / stocks / gold / cash"
- 🔎 Uses Exa for search and cross-checks X for crypto sentiment and flows.

### 📰 news-and-knowledge-base-assistant
Builds a curated daily news brief across your chosen topics, renders an inline reading widget with text highlighting and comment notes, and files highlighted items into atomic topic notes in your knowledge base.
- 🗣️ **Triggers:** "daily news", "today's news", "morning brief", "news brief", or a fresh morning chat with no specific task
- 📦 Ships with a reader template and configurable source list.

### ✍️ turbo-x-writer
Turns raw material (insights, transcripts, research findings, on-chain data, AI workflow notes) into a ready-to-post X package: one final post, the matching image-generation prompt in Turbo's editorial vintage style, a reply, and a pre-flight QC checklist against the algorithm landmines. Built on Turbo's locked 90-day beat of AI-enhanced crypto research and agent deployment.
- 🗣️ **Triggers:** "write me an X post", "draft a tweet", "turn this into a thread", "Data Drop", "Crypto AI Stack"

### 🐦 x-writer
Analyzes any user's X/Twitter writing style and generates draft posts that sound like them. Shareable and generic (not tied to Turbo's voice).
- 🗣️ **Triggers:** "draft tweets for me", "write posts in my style", "ghostwrite", "tweet ideas", "x writer"
- 🔑 Requires a Bearer Token and X handle set in the skill config before use.

---

🛠️ Built by Turbo.
