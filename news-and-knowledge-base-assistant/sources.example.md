---
type: sources
last updated: YYYY-MM-DD
purpose: canonical source list for the daily news skill. Edit this file to add or drop sources.
---

# Sources for Daily News

The daily news generator reads this file at run time and pulls from the listed sources. Add or remove entries by editing this file directly, or say "add source X" in chat.

This file ships with a few high signal web sources and newsletters across Crypto, AI, Macro, and Tech as recommended starters. X account slots are left blank since who you follow is personal taste. Fill in the X accounts you trust, or remove the X sections entirely.

---

## Crypto / DeFi / Web3

### Web (via search)
* **CoinDesk** ([coindesk.com](https://www.coindesk.com)) for breaking crypto news, price action, ETF flows, derivatives, regulatory coverage. Fully scrapeable.
* **Glassnode Insights** ([insights.glassnode.com](https://insights.glassnode.com)) for on chain analytics, Market Pulse, Week On-Chain reports, ETF flow analysis. Free tier covers all weekly research.

### X accounts
* *Add your trusted crypto accounts here, e.g. researchers, fund GPs, on chain detectives.*

---

## AI / ML

### Newsletters
* *Recommended adds: Import AI (Jack Clark), State of AI (Nathan Benaich), The Sequence. Fill in if you want.*

### X accounts
* *Add your trusted AI accounts here, e.g. lab leaders, researchers, AI engineers.*

---

## Macro / Markets

### Newsletters
* **Wall Street Breakfast** ([seekingalpha.com/author/wall-street-breakfast](https://seekingalpha.com/author/wall-street-breakfast)) for the daily premarket macro digest, published before 7:30 AM ET weekdays. Saturday "What Moved Markets This Week" for the weekly recap.
* **Global Macro Investor** ([raoulpal.substack.com](https://raoulpal.substack.com)) for free Substack excerpts of Raoul Pal's institutional macro research. Long horizon framework around liquidity, exponential age, cross asset regime.

### X accounts
* *Add your trusted macro accounts here, e.g. Fed watchers, bond market analysts, macro strategists.*

---

## Tech / Startups / VC

### Newsletters
* *Recommended adds: Newcomer (Eric Newcomer) for startup scoops, The Generalist (Mario Gabriele) for venture firm deep dives, Stratechery for tech strategy. Fill in if you want.*

### X accounts
* *Add your trusted tech / VC accounts here.*

---

## How the skill uses this file

1. The daily news task reads this file first when invoked.
2. For each web source, fresh content from the past 24 hours is fetched.
3. For each X account, recent high engagement posts are fetched.
4. Items are curated down to 5 to 10 per topic and written into the daily news markdown.
5. Sources can be added at any time. A source can be temporarily muted by prefixing the line with `~~` (strikethrough).

---

## How to edit

In chat:
* `add source @handle` or `add source https://...` to add a new source. The skill will ask which topic bucket.
* `drop source @handle` to remove.
* `mute source X` to temporarily strikethrough without removing.

Directly:
* Edit this file. Add bullet points under the right topic header. The skill picks up changes on the next run.
