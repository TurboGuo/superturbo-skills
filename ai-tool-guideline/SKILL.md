---
name: ai-tool-guideline
description: >-
  Build a beginner pitfall manual for one named AI tool, delivered as a markdown
  file the client can keep. Asks which tool, which system, how far they want to get
  and where they are stuck, then researches the official site and docs, the official
  community and public experience posts, and writes the traps nobody warns a first
  time user about, as a journey with a pass check at every stage. Every trap carries
  a source, an evidence level, the version it applies to and the date collected, so
  the manual can be re dated instead of quietly going stale. Also appends a new trap
  to a manual the client already has. Use when someone says "help me get started with
  X", "what should I watch out for with X", "make me a guide for X", "I keep getting
  stuck installing X", "写一份 X 的避坑手册", "X 有哪些坑", "帮我上手 X", "小白怎么用 X",
  "X 安装老是失败", "给我一份 X 的说明书". Do NOT trigger for choosing which tool to use,
  which is ai-tool-search, or for vetting a third party skill or connector before
  install, which is install-safety-check.
license: PolyForm-Noncommercial-1.0.0
metadata:
  author: SuperTurbo
  version: "1.0"
  last_updated: "2026-08-27"
---

# ai-tool-guideline

Every AI tool has a set of traps that the official documentation does not mention,
because the documentation was written by people who already know the answer. A
first time user hits them one at a time, alone, and quits somewhere around the
third one.

This skill produces the missing document: a manual for one tool, for one person's
actual machine and actual goal, where the traps are named up front, in plain
language, with a way to check you have cleared each stage before moving to the next.

The output is one markdown file delivered into the conversation. Nothing is written
to any connected folder unless the user asks in a separate message.

## What this is not

It is not a rewrite of the official tutorial. The official tutorial already exists
and is usually correct. This manual covers what happens when the official tutorial
does not work.

It is not a general troubleshooting bot either. If the question has nothing to do
with getting a named tool working, say so and answer it directly instead of
producing a manual.

## Step 0, intake

Ask in one round with AskUserQuestion. Four questions, no more, and do not go back
for a second round unless the tool itself could not be identified.

1. **Which tool.** Free text. If they name it vaguely, resolve it to the official
   product name and official URL before anything else, and confirm the resolution in
   one line.
2. **Which system.** macOS, Windows, Linux, not sure. If not sure, write the manual
   for macOS and Windows side by side and say so at the top.
3. **How far do you want to get.** Three options: just install it and have it work,
   get one real thing working end to end, put something online other people can use.
   This sets which checkpoints appear. Do not write checkpoints past their answer.
4. **Which depth.** Two options, and this is a real fork in the output:
   - **Quick reference.** Assumes they will follow the official tutorial and this
     manual only covers the traps and the pass checks. Dense, short, respects their
     time.
   - **Hand held.** Every step written out, traps sitting inside the step where they
     happen. For someone with genuinely no technical background.

Also capture, without asking a fifth question, whatever they already said about
where they are stuck. A stated symptom is the most valuable input in the whole
intake, because it goes straight into the manual as a solved entry.

**Regional variant.** Many AI tools ship a different product under the same name in
different regions, with different models, different pricing and different domains.
Before researching, establish which variant applies, from the official site. Getting
this wrong makes the whole manual wrong.

## Step 1, three layer research

Search in this order. The order matters because each layer is trusted for different
things. `references/research-sources.md` has the query patterns.

| Layer | Where | Trusted for |
|---|---|---|
| Official | Official site, docs, help centre, changelog, system requirements page, pricing page | Version numbers, system requirements, free tier limits, prices, supported platforms. These four facts may come from nowhere else |
| Official community | Official forum, GitHub issues, official FAQ threads | Real failures with error codes, the ones that recur |
| Public experience | Blog posts, tutorials, community sites, video transcripts, in both Chinese and English | Traps that real beginners hit. Always marked as second hand |

Search both Chinese and English sources regardless of output language. The Chinese
speaking user base and the English speaking user base of the same tool hit different
walls, because the regional builds, the default models and the network conditions
differ. A manual written from only one side is missing half the traps.

Budget roughly eight to fourteen searches. Stop when new searches stop producing new
pitfalls, and say in the manual how many stages came back empty.

## Step 2, lay out the journey

Use the nine stage skeleton in `references/checkpoints.md` as the spine, then cut and
merge stages so they fit this specific tool. A browser based tool has no install
stage. A command line tool has no login screen. Never keep an empty stage just
because the skeleton has it.

Cut every stage that sits past the answer to intake question 3.

Each stage gets three parts, in this order:

1. **What this stage is for**, in plain language, three sentences at most.
2. **The traps**, as entries in the format below.
3. **You have cleared this stage when**, a concrete observable thing. "The terminal
   prints a version number." "The chat panel replies to hello." Not "when it works."

The pass check is the part beginners are missing. Without it they carry a broken
stage forward and the failure surfaces three stages later, where it is unreadable.

## Step 3, write the entries

Every trap uses this shape. `references/manual-template.md` has the full markdown.

- **What you see.** The literal text on screen, copied exactly, error code included.
  Beginners cannot paraphrase an error correctly, so the literal string is what makes
  the manual searchable for them.
- **What most people assume.** The false belief that leads into this trap. This is the
  line that turns a checklist into something readable, and it is not optional.
- **What is actually happening.** Plain language. No term goes in unexplained, and
  every term used goes into the glossary.
- **How to get out.** Exact clicks, exact commands. Not "configure your environment."
- **How to avoid it next time.** Written as a check to run before the step, not as a
  lesson learned after it.
- **Source.** A link.
- **Evidence level.** One of: official documentation, recurring in the official
  community, single second hand report, or reported by this user. Never blur these.
- **Applies to.** Operating system, tool version, regional variant, and the date the
  fact was collected.

## Step 4, the glossary

Collect every term the manual uses that a non technical reader would not know, and
give each one a single plain sentence. Terminal, dependency, environment variable,
token, API key, path, whatever this particular tool forces on them.

Only include terms that actually appear in this manual. A generic glossary is
padding.

This section exists because the standard failure of beginner documentation is that
the author cannot remember not knowing. Treat any unexplained term in the body as a
defect.

## Step 5, deliver

Write the file, then send it into the conversation with SendUserFile. Name it after
the tool and the collection date.

The manual opens with a freshness header, always:

```
Tool: <name>, <regional variant>
Version at time of writing: <version>
Written for: <operating system>, <how far they want to get>
Collected: <date>
Re check after: <date plus three months>
```

The manual closes with the append protocol: if you hit a new trap, send this file
back with what happened, and it gets added as a new entry and the collection date
gets updated.

Do not write to any connected folder. Do not publish anything. Delivery is the file
in the conversation.

## Append mode

When someone returns with an existing manual and a new problem:

1. Read the whole manual first, including its collection date.
2. Solve the new problem, researching only as far as needed.
3. Add one entry, in the same format, under the stage it belongs to, with evidence
   level "reported by this user".
4. If the tool version in the header no longer matches reality, check the official
   changelog and flag every entry whose "applies to" version is now behind. Mark those
   entries as needing re check. Do not delete them and do not silently edit them.
5. Update the collected and re check dates.
6. Send the updated file back.

## Hard rules

**Never invent a pitfall.** Every entry traces to a source or to something the user
themselves reported. If a stage has no documented traps, write "no publicly recorded
traps found at this stage" and move on. A fabricated trap is worse than a missing one,
because the reader wastes time defending against nothing and stops trusting the rest.

**Version, price, system requirements and free tier limits come from the official site
only.** These four are the fastest to go stale and blog posts get them wrong constantly.
If the official page does not state one, write "not stated on the official page" rather
than filling it from a third party.

**Date everything.** Every entry carries the date its facts were collected. This is the
single thing that separates this manual from the static guides already on the web,
which never tell you which version they were written against.

**Never promise it will work.** The manual describes what has gone wrong for other
people and what fixed it. It does not guarantee an outcome.

**Network access and regional availability: state the official facts, give no methods.**
If the official site says the service is not offered in a region, or that a regional
build needs no extra configuration, that is a fact and it belongs in the manual, along
with alternatives that are officially available in that region. Do not write
instructions for getting around a geographic restriction, whatever the local tutorials
do. This is a client deliverable.

**Redact before writing.** API keys, tokens, passwords, and file paths carrying the
user's real name never go into the manual. Replace with a placeholder.

**Hand the extension stage to install-safety-check.** At the stage where the user
installs third party skills, plugins or MCP connectors, the manual says to run
install-safety-check on anything from a source they do not already trust. Do not write
a competing safety checklist here.

**No hyphens as punctuation** anywhere in the output. Hyphens inside product names,
commands, file names and URLs are fine and must be kept exactly.

## Language

Write the manual in the language the client used. Research in both Chinese and English
regardless. Produce one language only, unless the client asks for both.

## Related skills

- `ai-tool-search` runs before this one. It decides which tool to use.
- `install-safety-check` runs inside the extension stage of this one.
