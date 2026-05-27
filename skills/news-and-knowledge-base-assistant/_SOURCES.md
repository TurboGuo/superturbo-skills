---
type: sources
created: YYYY-MM-DD
last updated: YYYY-MM-DD
purpose: canonical source list for the daily news skill
---

# Sources for Daily News

This is the seed file. On first run, the skill copies it to `news/_SOURCES.md` in your project context folder, where it becomes your canonical, editable source list.

Four web sources ship as defaults. X account slots are blank since who you follow is personal taste.

---

## Crypto / DeFi / Web3

### Web (via search)
* **CoinDesk** ([coindesk.com](https://www.coindesk.com)) for breaking crypto news, price action, ETF flows, derivatives, regulatory coverage.
* **Glassnode Insights** ([insights.glassnode.com](https://insights.glassnode.com)) for on chain analytics, Market Pulse, Week On-Chain, ETF flow analysis. Free tier covers all weekly research.

### X accounts
*(add your trusted crypto accounts here)*

---

## AI / ML

### Newsletters
*(add your AI newsletters here; suggested adds: Import AI by Jack Clark, State of AI by Nathan Benaich, The Sequence by Jesus Rodriguez)*

### X accounts
*(add your trusted AI accounts here)*

---

## Macro / Markets

### Newsletters
* **Wall Street Breakfast** ([seekingalpha.com/author/wall-street-breakfast](https://seekingalpha.com/author/wall-street-breakfast)) for the daily premarket macro digest, published before 7:30 AM ET weekdays. Saturday "What Moved Markets This Week" for the weekly recap.
* **Global Macro Investor** ([raoulpal.substack.com](https://raoulpal.substack.com)) for free Substack excerpts of Raoul Pal's institutional macro research.

### X accounts
*(add your trusted macro accounts here)*

---

## Tech / Startups / VC

### Newsletters
*(add your tech / VC newsletters here; suggested adds: Newcomer by Eric Newcomer, The Generalist by Mario Gabriele, Stratechery by Ben Thompson)*

### X accounts
*(add your trusted tech / VC accounts here)*

---

## How the skill uses this file

1. The daily news task reads this file at run time.
2. For each web source, fresh content from the past 24 hours is fetched.
3. For each X account, recent high engagement posts are fetched.
4. Items are curated down to 5 to 10 per topic and written into the daily news markdown.

## How to edit

In chat:
* `add source @handle` or `add source https://...` to add a new source. The skill will ask which topic bucket.
* `drop source @handle` to remove.
* `mute source X` to temporarily strikethrough without removing.

Directly:
* Edit this file in your project context folder. Add bullet points under the right topic header. The skill picks up changes on the next run.

## How to add a new topic

Just add a new section header (e.g. `## Health / Biotech` or `## Energy / Commodities`). The skill infers topics from section headers, so any new category appears in the daily brief automatically.
