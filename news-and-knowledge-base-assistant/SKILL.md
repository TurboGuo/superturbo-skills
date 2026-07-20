---
name: news-and-knowledge-base-assistant
description: Generate a curated daily news brief across user defined topics, render an inline reading widget that supports text highlighting and comment notes, and file highlighted items into atomic topic notes inside the project context folder. Use whenever the user says "daily news", "today's news", "morning brief", "news brief", "what is happening today", "give me the news", "open reader", "show me my news", or any equivalent phrase requesting a curated daily roundup. Also use when the user opens a fresh chat in the morning with no specific task, since the implicit ask is often the daily brief.
---

# News and Knowledge Base Assistant Skill

End to end news pipeline: pull sources, write a daily news markdown into the project context folder, render an inline reading widget with right click highlighting, then file the user's marked highlights into atomic topic notes.

The pipeline is configurable. All paths and source lists live inside the project context folder and can be edited by the user at any time.

---

## Step 0: Setup (first run only)

On the first invocation, check if the project context folder exists at `./news/` (or wherever the user's project context folder is mounted). If not, create the folder skeleton:

```
news/
├── _SYSTEM.md           the spec (this file, copied in for reference)
├── _SOURCES.md          user defined source list (start blank, prompt user to fill)
├── _INDEX.md            living index of topic notes (auto regenerated)
├── daily/               daily news markdown files
│   └── archive/         daily files older than 30 days move here
└── topics/              atomic notes per theme
    ├── crypto/
    ├── ai/
    ├── macro/
    ├── tech-and-vc/
    └── (other categories created on demand)
```

If `_SOURCES.md` is missing in the project folder, copy the seed `_SOURCES.md` from this skill folder into `news/_SOURCES.md`. The seed ships with four recommended web defaults (CoinDesk, Glassnode Insights, Wall Street Breakfast, Global Macro Investor) and blank X slots, ready for the user to fill in their personal picks.

If the project folder's `_SOURCES.md` has only defaults and no X accounts yet, optionally prompt the user (once) to add a couple of X accounts via AskUserQuestion so the daily X Pulse section has content.

---

## Step 1: Run the daily pipeline

When the user invokes the skill:

1. Get today's date. Format the target daily file as `YYYY-MM-DD.md` (or however the user has configured).
2. Read `_SOURCES.md` to load the canonical source list.
3. Run TaskCreate to track the pipeline steps so progress is visible.

---

## Step 2: Pull sources (research first)

For each source listed in `_SOURCES.md`, fetch fresh content from the past 24 hours.

The skill ships with a few high signal web sources and newsletters as recommended starters that work for most users:

* **Crypto**: CoinDesk (coindesk.com), Glassnode Insights (insights.glassnode.com)
* **Macro**: Wall Street Breakfast (seekingalpha.com/author/wall-street-breakfast), Global Macro Investor Substack excerpts (raoulpal.substack.com)

X accounts and other personal picks should be added by the user to `_SOURCES.md`.

Tool guidance:
* Web sources (news sites, newsletters, Substacks): use the user's preferred web search tool. Exa search is recommended for clean article extraction; web_fetch is the alternative.
* X / Twitter accounts: use the x-reader skill if available, or web search with `site:x.com from:HANDLE` qualifier.
* Research feeds (HuggingFace Papers, GitHub Trending, HackerNews): use direct fetches or relevant search.

For any product or company name surfaced in a story, cross check on X for additional context unless the user has opted out.

Aim for 5 to 10 items per topic. Cap at about 24 items total. Highly curated, no filler.

---

## Step 3: Write the daily news markdown

Write to `news/daily/YYYY-MM-DD.md` with this exact frontmatter and structure:

```markdown
---
type: daily news
date: YYYY-MM-DD
generated: YYYY-MM-DDTHH:MM:SS
sources: [list of sources pulled this run]
total items: N
---

# Daily News YYYY-MM-DD

> [day of week] edition · about [N] min read · [N] items

[1 to 2 sentence lede summarizing the day]

---

## [Topic 1 emoji] [Topic 1 name]

### 1. [Headline]
> Source: [name] · [date] · [link](url)
> [2 to 3 sentence excerpt from the source]

**Why it matters**: [one line synthesis]

---

### 2. ...

## [Topic 2 emoji] [Topic 2 name]

### N. ...

(... continue for each topic the user has sources for ...)

---

## X Pulse (top 2 to 3 must read tweets)

1. @account · "tweet" · [link]
2. ...

## Long reads of the day (1 to 2 max)

> ...
```

Topic emojis and names match the user's `_SOURCES.md` categorization. Default examples:
* Crypto / DeFi / Web3
* AI / ML
* Macro / Markets
* Tech / Startups / VC

---

## Step 4: Render the reading widget

After writing the markdown, render the inline reading widget by calling `mcp__visualize__show_widget` with a unique title per day (e.g. `daily_news_reader_YYYY_MM_DD`).

The widget code is in `reader_template.html` in this skill folder. Substitute these placeholders before rendering:
* `__DN_TITLE__` with the day's title (e.g. "Daily News, Saturday May 23 2026")
* `__DN_SUBTITLE__` with a short subtitle (sources, item count, edition type)
* `__DN_ITEMS__` with a JSON array of the day's items in this shape:

```js
[
  {
    id: 1,
    topic: 'crypto',           // matches one of the topic keys
    headline: '...',
    source: '...',
    url: 'https://...',
    excerpt: '...',
    why: '...'
  },
  ...
]
```

The widget gives the user:
* Topic filter chips at the top
* Card layout per item with topic chip, headline, source, excerpt, "why it matters" callout
* Right click or text select on any card opens a highlight popup
* Highlights save to a sidebar tray with a comment field
* A "File highlights to topics" button that posts the marked items back to chat via `sendPrompt`

After rendering, tell the user the news is ready and they can highlight any paragraph and click File when done.

Note: `sendPrompt` only exists inside `mcp__visualize__show_widget` widgets, not inside `mcp__cowork__create_artifact` artifacts. Always use the widget for the daily flow so the file action posts to chat directly.

---

## Step 5: Filing workflow (triggered by the widget File button)

When the widget posts a "Please file these N highlight(s)" message to chat:

1. **Read** existing topic notes in `news/topics/` to learn what theme buckets already exist.
2. **Detect duplicates**: for each incoming highlight, check whether the same headline plus source pair already appears as an entry in any existing topic note. If yes, ask the user via AskUserQuestion how to handle: skip, append fresh entry, replace, or move to a different theme.
3. **Propose a theme bucket** for each non duplicate highlight using AskUserQuestion. Use existing themes when they fit. Propose a new one when nothing fits.
4. **Write or append** to the topic note at `news/topics/{category}/{theme}.md`. If the note exists, append a new entry under `## Entries` (newest on top). If it does not exist, create it with the template from `topic_note_template.md`.

Entry format:

```markdown
### YYYY-MM-DD · [headline]
**Source**: [name] · [date] · [link](url)
**Marked paragraph**: "[the paragraph the user highlighted]"
**Source excerpt**: "[2 to 3 sentence context from the original source]"
**Note**: [the user's comment]
```

5. **Confirm in chat** with a short summary: file paths created or updated and entry count. Present the files so the user can open them.
6. **Link related notes**: if the new entry mentions an entity that has its own existing note, add a `[[wikilink]]`. If a theme cross references another theme, add a `related:` entry in the frontmatter.

---

## Step 6: Maintenance (run weekly or on demand)

* Refresh `_INDEX.md` listing all topic notes.
* Move daily news files older than 30 days to `daily/archive/`.
* On Sundays, optionally generate a weekly digest by synthesizing the past 7 daily notes.

---

## Trigger phrases reference

| Phrase | Behavior |
|---|---|
| daily news, today's news, morning brief, news brief | Full pipeline, steps 1 to 4 |
| open reader | Re render the widget for today's existing daily news note without regenerating |
| file highlights | Force file pending highlights if the user pasted them manually |
| add source X | Append to `_SOURCES.md` |
| weekly digest | Synthesize past 7 daily notes into a Sunday recap |
| show topic X | Open the topic note matching X |
| archive old | Move daily news older than 30 days to archive |

---

## Configuration notes

The skill is designed to be portable across users. To customize:

1. Edit `_SOURCES.md` in the project context folder. Sources are grouped by topic. Add or remove freely.
2. Topic categories are inferred from `_SOURCES.md` section headers. Add a new section to introduce a new topic.
3. The reader widget's topic colors and labels can be customized by editing `reader_template.html` (CSS rules `.dn-topic.crypto`, `.dn-topic.ai`, etc.).
4. The default daily file location is `news/daily/YYYY-MM-DD.md`. If the user prefers a different location, ask once and remember.
5. The skill does not assume any specific web search tool, file storage system, or note format. It defaults to Exa for search and markdown for storage but adapts to whatever the user has configured.
