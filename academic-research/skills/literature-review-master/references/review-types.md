# Review types and what each one owes the reader

## Narrative / related work
The review inside an empirical paper. 800 to 2,500 words. Selective by design,
and that is legitimate as long as selection is by argument, not by convenience.
Owes the reader: a thesis, a structure, and a final paragraph that makes the
present study inevitable.

## Systematic review (PRISMA 2020)
A protocol-first, reproducible answer to a bounded question. Owes the reader:
a registered or at least pre-written protocol, the exact search string per
database with the date run, inclusion and exclusion criteria fixed in advance,
dual screening with an agreement statistic, a risk-of-bias appraisal, and the
four-stage flow diagram. If any of these are missing, it is a narrative review.
Reporting checklist: PRISMA 2020, 27 items.

## Scoping review (PRISMA-ScR)
Maps how much work exists, of what kinds, and where the concentration and the
holes are. Quality appraisal is optional; charting is not. Use when the question
is "what is out there" rather than "what is the answer".

## Rapid review
A systematic review with declared shortcuts (one database, one screener, a date
cut). Legitimate only if every shortcut is stated. Undeclared shortcuts are just
a bad systematic review.

## Integrative / theoretical review
Builds a new framework out of existing work. The output is a framework — a
figure, a typology, a set of propositions — not a summary. Torraco (2005) and
Webster & Watson (2002) are the standard method references in management and IS.
Pair with theory-graph-master to draw the resulting framework.

## Meta-analysis
Pools effect sizes. Requires extractable effects with variances, a chosen model
(fixed versus random, and random is almost always right in social science),
heterogeneity reported as Q, I-squared and tau-squared, moderator analysis, and
publication-bias assessment (funnel plot, Egger's test, p-curve, or selection
models). Report per PRISMA. Software: R `metafor` or `meta`, Stata `meta`.

## Meta-synthesis / meta-ethnography
Qualitative synthesis across studies. Noblit & Hare's reciprocal, refutational
and line-of-argument translation. Report per ENTREQ. The output is a new
interpretation, not a frequency count of themes.

## Bibliometric / science mapping
Co-citation, bibliographic coupling, co-word analysis over a corpus of thousands.
Tools: VOSviewer, CiteSpace, R `bibliometrix`. Describes a field's structure;
it does not substitute for reading the papers, and reviewers know the difference.

## 文献综述 (Chinese convention)
Expected shape:
1. 引言 — why this topic, why now
2. 研究现状 — 国外研究现状 and 国内研究现状, usually as separate subsections
3. 研究脉络 — how the field moved, by stage or by school
4. 研究评述 — the appraisal half. What is settled, what is contested, what is
   untouched, and what the existing work cannot explain
5. 本文的切入点 / 研究展望 — the opening this paper takes

The 评 half is what distinguishes a 综述 from a 综述性的罗列. A review that
stops after 研究现状 will be returned. For a 学位论文 this is a full chapter,
typically 8,000 to 15,000 characters, and reviewers check that 国内 sources are
genuinely covered rather than token.
