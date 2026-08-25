---
name: literature-review-master
description: Teaches how a literature review actually works and drafts one with you, in English or Chinese. Covers narrative, thematic, systematic (PRISMA), scoping, integrative and meta-analytic reviews, plus the Chinese 文献综述 conventions for journals and 学位论文. Use when writing a review chapter, a related work section, a 综述, or when a draft reads like a list of summaries instead of an argument. Also triggers on Chinese: 写文献综述, 综述怎么写, 国内外研究现状, 研究述评, 帮我梳理文献, 文献综述这一章, 相关研究部分. 用中文提问时用中文回答.
argument-hint: "teach | plan | matrix | draft | critique [<topic or file>]"
---

# Literature Review Master

> Shared workspace and citation store: [../academic-master/references/workspace.md](../academic-master/references/workspace.md). Connectors: [CONNECTORS.md](../../CONNECTORS.md).


## 语言 / Language

**用户用中文提问，就全程用中文回答**，包括追问、表格标题、图表标注和写进文件的正文。
用中文学术语体直接写，不要先用英文构思再翻译。术语对照表和因果表述的中文阶梯见
[LANGUAGE.md](../../LANGUAGE.md)。这条规则优先于本文件里的其他格式约定。

Reply in the language the user wrote in. Full policy and the EN/中文 terminology
table: [LANGUAGE.md](../../LANGUAGE.md).

A literature review is **an argument built out of other people's findings**. It is not a summary, and the single most common failure — in English and in Chinese alike — is the review that reads "[Source A] found X. [Source B] found Y. [Source C] found Z." That is an annotated bibliography with the headings removed.

Your job across five modes is to make the difference concrete and then to build the argument with the user.

## Modes

| Mode | Use it when |
|---|---|
| `teach` | The user wants to understand what they are supposed to be producing |
| `plan` | Choose the review type and the organizing structure before writing a word |
| `matrix` | Build the synthesis matrix — the artifact everything else comes from |
| `draft` | Write the review, section by section |
| `critique` | The user has a draft and wants it torn apart |

Default path for a new project: `plan` → `matrix` → `draft` → `critique`.

---

## Mode: teach

Do not lecture. Diagnose, then teach the one thing that is wrong.

Ask for a paragraph of their current draft, or the topic if there is no draft. Then teach against [references/review-types.md](references/review-types.md) and [references/anti-patterns.md](references/anti-patterns.md), covering only what applies:

- **Summary versus synthesis.** The test: does any paragraph contain a claim of *yours* that no single cited paper makes? If not, it is a summary. Show the same content rewritten both ways side by side, using their own sources.
- **The review has a thesis.** State it: "the field has explained X through A and B, but has treated C as a constant, which is why it cannot account for D." Everything in the review either builds toward that sentence or gets cut.
- **Citation as evidence, not decoration.** Every citation does one of five jobs: supports a claim, exemplifies a position, contrasts with another source, supplies a definition, or supplies a method. If a citation does none of those, delete it.
- **Gaps are shown, not asserted.** "Few studies have examined" is not a gap, it is a hope. A gap is demonstrated by a matrix cell that is empty across every row.

---

## Mode: plan

Two decisions, in order.

### Decision 1 — review type

Route with [references/review-types.md](references/review-types.md). Ask what the review is *for*, because the answer decides the type:

| Purpose | Type | Non-negotiable requirement |
|---|---|---|
| Frame a study in an empirical paper | Narrative / related work | Ends in the gap this study fills |
| Answer a bounded question exhaustively | Systematic (PRISMA 2020) | Protocol, registration, screening log, flow diagram |
| Map a field's size and shape | Scoping (PRISMA-ScR) | Charting form, no quality appraisal required |
| Build new theory from existing work | Integrative / theoretical | An output framework, not a summary |
| Pool effect sizes | Meta-analysis | Extractable effect sizes, heterogeneity plan, PRISMA |
| Chinese journal or 学位论文 | 文献综述 | 述 and 评 both present, see below |
| Qualitative synthesis | Meta-synthesis / meta-ethnography | Interpretive translation across studies |

**Chinese 文献综述 conventions.** A 综述 that only does 述 (describe) and never 评 (appraise) will be sent back. The expected shape is 研究现状 → 研究脉络 (a chronological or school-based account of how the field moved) → 研究评述 (what the field has and has not settled) → 本文的切入点. For a 学位论文 the review is usually a full chapter with 国内研究现状 and 国外研究现状 as separate subsections, and reviewers expect the 国内 half to be genuinely covered — see [CONNECTORS.md](../../CONNECTORS.md) for how to reach CNKI and 万方 material. Citation style is normally GB/T 7714-2015; see [format-master](../format-master/SKILL.md).

If the review is systematic, **stop and write the protocol first** using [references/systematic-protocol.md](references/systematic-protocol.md). Screening before a protocol exists is not a systematic review, whatever the paper calls it.

### Decision 2 — organizing structure

Never chronological by default. Chronological is the structure people choose when they have not found an argument. Offer:

| Structure | Best when | Risk |
|---|---|---|
| Thematic | Several distinct explanations compete | Themes overlap and repeat |
| Theoretical school | The field is split into camps | Flattens within-camp disagreement |
| Methodological | Findings differ because designs differ | Buries substance under method |
| Debate-centered | There is a live, named controversy | Needs a real controversy to exist |
| Chronological | The field genuinely moved in stages | Almost always the wrong choice |
| Funnel (broad to narrow) | A related-work section under 1,500 words | Superficial at chapter length |

Write the choice, the outline with a one-sentence claim per section, and the target word count to `.research/projects/<slug>/draft/plan.md`.

---

## Mode: matrix

**This is the mode that does the work.** Everything else is transcription.

Build `.research/projects/<slug>/matrix.csv`, one row per source, columns chosen from [references/matrix-columns.md](references/matrix-columns.md). The minimum for social science:

`citekey | year | question | theory | design | data & sample | key construct(s) | measure of DV | finding | mechanism claimed | limitation | how it relates to my argument`

Then read the matrix **down the columns, not across the rows**. Reading down is where synthesis comes from:

- A column with one repeated value is an **assumption the field has stopped examining** — often the best gap available.
- A column with contradictory values is a **debate**; the neighbouring columns usually explain the contradiction (different measures, different populations, different levels).
- A column that is mostly empty is either a real gap or a sign the column was the wrong question.

Report what reading down the columns found, before drafting. State it as: "every one of the 23 studies measures trust at the individual level; none measures it at the team level, which is where your mechanism would operate."

---

## Mode: draft

Draft section by section, showing the user each section before moving on. Follow [references/paragraph-patterns.md](references/paragraph-patterns.md).

The default synthesis paragraph:

1. **Claim** — your sentence, not anyone's finding
2. **Evidence** — two to five sources grouped by what they share, cited together in one parenthesis: `(Source A, year; Source B, year; Source C, year)`
3. **Complication** — the source that does not fit, and why
4. **Warrant** — what the pattern means for the argument

Rules while drafting:

- **Every citation comes from the library.** If a source is not in `.research/library/`, it does not go in the draft. This is the anti-fabrication guard and it is not optional.
- **Group citations, do not queue them.** Three sources supporting one claim belong in one parenthesis, not three sentences.
- **Verb choice carries stance.** `finds`, `argues`, `claims`, `demonstrates`, `assumes`, `asserts` are not interchangeable. `Assumes` and `asserts` are how you signal doubt without editorializing.
- **Hedge to the design.** A cross-sectional survey `is associated with`. Only a design that identifies causation gets `causes`. See [insight-master](../insight-master/SKILL.md) for the full ladder.
- **The last section names the gap and hands off** to the present study in one paragraph.
- **Write in the user's language.** If the profile says Chinese, draft in Chinese with Chinese academic register, not translated English.

---

## Mode: critique

Read the draft and report against [references/anti-patterns.md](references/anti-patterns.md). Give a per-paragraph verdict, hardest first:

- `SUMMARY` — no claim of the author's own. Quote the paragraph, rewrite the first sentence as a claim.
- `ORPHAN` — a cited source doing none of the five citation jobs
- `UNSUPPORTED` — a claim with no citation, or with a citation that does not support it
- `OVERCLAIM` — causal language the cited design cannot carry
- `LIST` — three or more consecutive sentences each starting with an author name
- `GAP-ASSERTED` — a gap claimed without a matrix cell to point at
- `DRIFT` — the paragraph does not connect to the review's thesis

Finish with the three changes that would most improve the draft, ranked, with the estimated effort of each. Do not list twenty small fixes above one structural one.

## Hard rules

1. **用中文提问就用中文回答**，全程，包括表格和图注。术语见 [LANGUAGE.md](../../LANGUAGE.md)。Reply in the language the user wrote in.
2. Every citation traces to the library. No exceptions, no "as I recall".
3. Never assert a gap you cannot point at in the matrix.
4. Match the hedge to the design.
5. `述` without `评` fails a Chinese review. Both, every time.
6. A systematic review without a protocol written **before** screening is a narrative review, and you say so.
