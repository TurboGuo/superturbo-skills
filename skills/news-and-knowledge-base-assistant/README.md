# news-and-knowledge-base-assistant

A renamed copy of the original `daily-news-public` skill. Generates a curated daily news brief, renders an inline reading widget with text highlighting and notes, and files marked items into atomic topic notes inside your project context folder.

No personal data, no hardcoded sources, no hardcoded file paths. Bring your own source list and topic categories.

## What it does

1. **Pulls** the day's news from a user defined source list across any number of topics (Crypto, AI, Macro, Tech, anything else).
2. **Writes** a clean markdown daily brief into `news/daily/YYYY-MM-DD.md`.
3. **Renders** an inline reading widget with Readwise style highlighting. Select text, right click, add a comment, save.
4. **Files** highlighted items into atomic topic notes under `news/topics/{category}/{theme}.md`, with the source link, paragraph, excerpt, and your comment preserved.

## How to use

Install the skill folder under `~/.claude/skills/`. In chat say "daily news", "today's news", or any equivalent. The skill will:
* Read your sources from `news/_SOURCES.md`. If empty on first run, it asks you to fill it in.
* Render the reading widget inline.
* When you click "File highlights to topics", it posts the marked items back to chat and runs through them with you to propose theme buckets.

## Files in this skill

* `SKILL.md` — the runtime instructions for Claude.
* `reader_template.html` — the inline reading widget with highlight + comment + file workflow.
* `topic_note_template.md` — the atomic note skeleton for theme notes.
* `sources.example.md` — example source file to copy into your project context folder and fill in.

## Configuration

Everything is in the project context folder:
* `news/_SOURCES.md` — your source list, edited by you.
* `news/daily/` — daily briefs, archived after 30 days.
* `news/topics/` — your atomic notes per theme.
* `news/_INDEX.md` — auto refreshed index of topic notes.

The skill does not assume any specific web search tool. Exa is recommended for clean article extraction, but it adapts to whatever is available. For X content, it uses the x-reader skill if installed, or falls back to web search with `site:x.com` qualifier.

## Trigger phrases

* `daily news`, `today's news`, `morning brief` — run the full pipeline
* `open reader` — re render the widget for today's existing brief
* `file highlights` — file any pending highlights manually
* `add source @handle` or `add source URL` — append to `_SOURCES.md`
* `weekly digest` — Sunday recap synthesizing the past 7 days
* `show topic X` — open the topic note matching X
* `archive old` — move daily files older than 30 days to archive

## License

Use, fork, modify freely.
