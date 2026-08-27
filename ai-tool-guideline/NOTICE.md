# NOTICE

`ai-tool-guideline` is **original SuperTurbo work**. No upstream skill or repository
was copied, forked or adapted, so no third party licence obligation travels with it.

## Prior art that was read, and how it relates

The problem this skill addresses has two existing camps. Both were surveyed on
27 August 2026 before this skill was written. Nothing below was copied. Two ideas were
consciously borrowed at the level of concept, and they are named here rather than
passed off as original.

### Camp one, failure memory tools for developers

| Tool | Licence | Relationship |
|---|---|---|
| `satvikxbansal/debug-log-skill` | see repo | Not used. The obsolete tombstone idea, marking a stale entry rather than deleting it, is a deliberate borrow at concept level |
| `nicoalbo0/never-again` | see repo | Not used. Its redaction before write rule is a deliberate borrow at concept level |
| `polyxmedia/mnemos` | see repo | Not used |
| `kurikomi-labs/komi-learn` | see repo | Not used |
| `Yingqi-Han/learning-retrospective-skill` | see repo | Not used |
| `wuisabel-gif/MemWhale` | see repo | Not used |
| `creanlab/agent-genome-lab` | see repo | Not used |
| `livlign/claude-skills-pitfalls` | see repo | Not used. Its graded evidence labels, verified against documented, are a deliberate borrow at concept level |

All of these assume a git repository, a developer who reads stack traces, and a
willingness to install a CLI or an MCP server. The audience this skill serves meets
none of those conditions.

### Camp two, static beginner guides

Public tutorials and paid courses covering beginner traps in AI coding tools, in
Chinese and English. They are the closest thing to this skill's output. Every one of
them shares the same two structural weaknesses: the traps are the author's, not the
reader's, and the document carries no version stamp, so it silently misleads after the
next release.

Those two weaknesses are exactly what this skill's freshness header, per entry
environment stamp and append protocol exist to fix. No text from any of them is
reproduced. Where such a source supplies a fact for a generated manual, the manual
cites its URL and marks it as a second hand report.

## Honest limitation, recorded here rather than buried

For a popular tool, good public trap lists already exist. A manual produced by this
skill beats them on three things only: it is cut to the client's system and goal, every
fact is dated and sourced, and it can be extended with the client's own traps later. If
those three do not matter to a given client, a web search will serve them just as well,
and the honest thing is to say so.

The value is highest on new, obscure or recently changed tools, where nothing public
exists to compare against.
