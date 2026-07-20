# superturbo-skills

Turbo's personal skill library for Claude. Each skill lives in its own folder at the root of this repo, right alongside this README. There is no wrapper `skills/` folder, so to install a skill just point Claude at its folder (each contains a `SKILL.md` plus any templates or assets it needs).

## Skills

### fi-tracker
Renders Turbo's financial independence (FI) dashboard: a progress card, an assets over time table where each cell shows total assets plus how many years that pile sustains, and a single asset growth line chart where color encodes return rate and line style encodes saving level. Triggers on "fi tracker", "FI dashboard", "when can I retire", "years to financial independence", and similar. Replies in Chinese when the request is in Chinese.

### fomc-short-analysis-plain
Plain text only variant of Turbo's short FOMC note, no visualization or rendered widgets, so it works inside Claude and on general gateways like Telegram and Slack. Leads with a POTENTIAL HIKE or POTENTIAL CUT verdict, two one sentence reasons backed by official Fed sources, and exactly three institutions each tagged with their tendency and cited to the bank's own research site. Triggers on "fomc plain", "fomc analysis", "analyze the last fomc", "fomc preview", or a named meeting date.

### news-and-knowledge-base-assistant
Builds a curated daily news brief across your chosen topics, renders an inline reading widget with text highlighting and comment notes, and files highlighted items into atomic topic notes in your knowledge base. Triggers on "daily news", "today's news", "morning brief", "news brief", or a fresh morning chat with no specific task. Ships with a reader template and configurable source list.

### turbo-x-writer
Turns raw material (insights, transcripts, research findings, on-chain data, AI workflow notes) into a ready to post X package: one final post, the matching image generation prompt in Turbo's editorial vintage style, a reply, and a pre-flight QC checklist against the algorithm landmines. Built on Turbo's locked 90 day beat of AI enhanced crypto research and agent deployment. Triggers on "write me an X post", "draft a tweet", "turn this into a thread", "Data Drop", "Crypto AI Stack", and similar.

### x-writer
Analyzes any user's X/Twitter writing style and generates draft posts that sound like them. Shareable and generic (not tied to Turbo's voice). Triggers on "draft tweets for me", "write posts in my style", "ghostwrite", "tweet ideas", or "x writer". Requires a Bearer Token and X handle set in the skill config before use.

---

Built by Turbo.
