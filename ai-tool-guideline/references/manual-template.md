# Manual template

Section order is fixed. Wording adapts to the client's language and depth choice.

---

## Header, always first

```
Tool: <official name>, <regional variant if any>
Version at time of writing: <version, from the official page>
Written for: <operating system> / <how far they want to get> / <depth>
Collected: <YYYY-MM-DD>
Re check after: <YYYY-MM-DD, three months later>
```

Then one short paragraph: who this manual is for, and what it does not cover. Name
the official tutorial and link it, and say plainly that this manual covers what
happens when that tutorial does not work.

---

## How to read this

Four lines, no more.

- The stages run in order. Do not skip forward.
- Each stage ends with a pass check. Do not move on until it passes.
- Every trap says where the fact came from and when it was collected.
- Any word you do not know is in the glossary at the end.

---

## Stage sections

One per surviving stage.

```
## Stage <n>, <name>

**What this is for.** <two or three sentences, plain language>

<hand held depth only: the steps, numbered, one action per step>

### Traps at this stage

<entries, or the empty line below>

### You have cleared this stage when

<one concrete observable thing>
```

If a stage produced nothing in research, write exactly this and move on:

> No publicly recorded traps found at this stage as of <date>. That does not mean
> there are none, only that nobody has written one up.

---

## Entry format

```
#### <short name of the trap>

**What you see**
> <the literal text on screen, error code included>

**What most people assume**
<the false belief, one sentence, written in the second person>

**What is actually happening**
<plain language, no unexplained terms>

**How to get out**
1. <exact click or exact command>
2. <...>

**How to avoid it next time**
<a check to run before the step, phrased as an instruction>

**Source** <link> | **Evidence** <official documentation | recurring in the official community | single second hand report | reported by you> | **Applies to** <os>, <version>, <variant>, collected <date>
```

Rules for entries:

- The "what you see" block is copied literally, never paraphrased, never translated
  if the tool prints it in another language. It is the string the reader will search for.
- "What most people assume" is mandatory. Without it the entry is a FAQ row, and the
  reader does not recognise themselves in it.
- Evidence level is never blurred. A single blog post is a single second hand report
  even when it sounds authoritative.
- One trap per entry. Two traps that share a symptom are still two entries.

---

## Glossary

```
## Words used in this manual

**<term>** <one plain sentence. What it is and why this manual mentions it.>
```

Alphabetical. Only terms that appear in the body. Any term in the body that is not
here is a defect.

---

## Closing section

```
## When this manual goes out of date

Collected <date>, against version <version>. Tools change fast and stages 4 and 6
change fastest.

If you hit something new, send this file back with what you saw on screen and what
you tried. It gets added as a new trap under the right stage, the version gets
re checked, and anything that has gone stale gets marked instead of deleted.
```
