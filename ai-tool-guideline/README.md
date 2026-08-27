# ai-tool-guideline

**A manual for the traps nobody warns a first time user about.**

Name an AI tool. This produces a markdown manual for that tool, cut to your operating
system and how far you actually want to get, where every trap carries a source link,
an evidence level, the version it applies to, and the date it was collected.

## Why not just read the official docs

You should read the official docs. They are usually correct. This covers what happens
when following them does not work, which is the part they cannot cover, because they
were written by people who already know the answer.

## Why not just search the web

For a popular tool, go ahead. Good trap lists exist. This beats them on three things
only:

1. It is cut to your system and your goal, not written for everyone
2. Every fact is dated and sourced, so you know when it went stale instead of finding
   out the hard way
3. You can send it back and add your own traps, so it grows instead of rotting

For a new, obscure or recently changed tool, nothing public exists to compare against,
and that is where it earns its keep.

## What you get

A journey, in stages, from choosing a version through to keeping it running. Each stage
has what it is for, the traps, and a concrete pass check so you know you actually
cleared it before moving on. Plus a glossary of every technical word the manual used,
one plain sentence each.

Each trap reads:

> **What you see:** the literal error, copied exactly
> **What most people assume:** the false belief that leads you in
> **What is actually happening:** plain language
> **How to get out:** exact clicks, exact commands
> **How to avoid it next time:** a check to run before the step

## Install

Drop the folder into your skills directory, or hand over the `.skill` file.

## Use

- "help me get started with <tool>"
- "what should I watch out for with <tool>"
- "写一份 <tool> 的避坑手册"
- "<tool> 有哪些坑"
- Or send an existing manual back with a new problem, and it gets added

## Boundaries

It never invents a trap. Version numbers, prices, system requirements and free tier
limits come from the official site only. It never promises an outcome. It states
official facts about regional availability and gives no methods for getting around a
geographic restriction.

## Related

- `ai-tool-search` runs before this. It decides which tool to use.
- `install-safety-check` runs inside the extension stage of this.

Licence: PolyForm Noncommercial 1.0.0. See `COMMERCIAL.md`.
