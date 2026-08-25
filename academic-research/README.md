# Academic Research Plugin

A research partner for social science, built as six skills that share one
workspace. It learns how you think, hunts literature ranked against that rather
than against generic relevance, teaches and drafts the review, chooses and
defends the method, draws the theory, enforces the citation style, and turns
results into a contribution.

**Fully bilingual.** Ask in Chinese and the skills trigger on Chinese phrasing
and answer in Chinese — 学术语体, not translated English. Covers 文献综述
conventions (述 + 评, 国内外研究现状), GB/T 7714-2015, and the 学位论文 template
rules that outrank the national standard. See [LANGUAGE.md](LANGUAGE.md).

## Install

```bash
claude plugins add academic-research
```

Or drop the folder into `.claude/plugins/` in your project.

## The six skills

| Skill | What it does | Modes |
|---|---|---|
| `academic-master` | Learns your research preferences into a durable profile, then discusses ideas and hunts literature ranked against it | `calibrate` `discuss` `hunt` `profile` |
| `literature-review-master` | Teaches what a review is, plans the type and structure, builds the synthesis matrix, drafts and critiques | `teach` `plan` `matrix` `draft` `critique` |
| `method-master` | Routes question to design, checks stance coherence, sizes samples with the arithmetic shown, writes the methods section, and carries a Stata/R operations manual with runnable templates | `select` `justify` `power` `specify` `analyze` `critique` |
| `theory-graph-master` | Conceptual frameworks, causal DAGs with identification checks, SEM paths, PRISMA flows, coding trees, timelines | `framework` `dag` `path` `prisma` `codetree` `timeline` |
| `format-master` | APA 7, ASA, APSA, Chicago, MLA 9, Harvard, AMA, IEEE, GB/T 7714-2015. Format, convert, audit, fix in place | `format` `convert` `audit` `manuscript` `journal` |
| `insight-master` | Result to finding to contribution. Causal language ladder, effect size interpretation, discussion, limitations, abstract | `interpret` `contribute` `discussion` `limitations` `abstract` `critique` |

## What makes it one plugin rather than six tools

**The researcher profile.** `academic-master calibrate` interviews you across
eleven fields — theoretical commitments, what evidence convinces you, what bores
you, the papers you want to be compared to — and writes it to
`.research/profile.md`. Every search is then scored against that profile with
the arithmetic shown, not against generic topical relevance. Every other skill
reads it: the review drafts in your language and register, the method skill will
not recommend a design you cannot execute, the format skill knows your default
style.

**The shared workspace.** All six skills read and write one `.research/`
directory, so the matrix the review builds is the matrix the insight skill reads,
and the citation the hunt found is the citation the format skill renders.

```
.research/
  profile.md
  library/references.bib · references.json · notes/
  projects/<slug>/
    idea.md · hunt-<date>.md · matrix.csv · screening.csv
    design.md · figures/ · draft/ · insights.md
```

## Typical path

```
/academic-master calibrate            once, about fifteen minutes
/academic-master discuss <your idea>  pressure-test before you commit
/academic-master hunt <question>      scored literature, snowballed
/literature-review-master matrix      the artifact everything comes from
/method-master select                 two or three designs, with the trade-offs
/theory-graph-master framework        the figure, validated then rendered
/method-master power                  sample size, arithmetic shown
   ... you run the study ...
/insight-master interpret             what it means, at the right rung
/insight-master contribute            the contribution sentence
/insight-master discussion            the section
/format-master audit                  before submission
```

## 中文快速上手

直接用中文说就行，技能会自己触发，回答也是中文。

| 你说 | 触发 |
|---|---|
| 帮我找一下关于……的文献 | `academic-master hunt` |
| 我有个想法，你觉得行不行 | `academic-master discuss` |
| 帮我写文献综述 / 国内外研究现状 | `literature-review-master` |
| 这个题目用什么方法比较好 / 样本量要多少 | `method-master` |
| 帮我画个理论模型图 / 变量关系图 | `theory-graph-master` |
| 参考文献改成 APA / 国标格式 | `format-master` |
| 这个结果说明什么 / 理论贡献怎么写 | `insight-master` |
| Stata 怎么合并数据 / 聚类标准误 / 结果表怎么导出 | `method-master analyze` |

三个例外：引文格式跟着目标期刊走，不跟着提问语言走；代码和变量名保持英文；
方法名和统计量第一次出现时中英并列。完整规则和术语对照表在
[LANGUAGE.md](LANGUAGE.md)。

**中文因果表述**特别提醒：横截面数据不能写「显著影响」。「影响」在学术中文里被读作
因果动词，`insight-master` 会按设计逐句检查。

## Requirements

- Nothing required. Every skill works with no connector and no install.
- Optional: `matplotlib` and `networkx` for the diagram scripts; `pandoc` for
  CSL-based citation rendering; R or Stata to **run** the analysis code the
  method skill writes. The plugin writes that code, it does not execute it —
  and it says so every time it hands you a script.
- Optional connectors: see [CONNECTORS.md](CONNECTORS.md). The single
  highest-value addition for social science is an OpenAlex-backed paper search.

## Seven rules the plugin will not break

1. **It answers in the language you asked in.** 中文提问，中文回答，全程。
2. **No fabricated citations.** Every reference resolves to a DOI or a stable
   URL, or it is tagged `[UNVERIFIED]`.
3. **The causal verb matches the design.** Every sentence, in every skill.
4. **Arithmetic is shown** for every ranking, power calculation and effect size.
5. **Gaps are pointed at, never asserted.**
6. **Nothing is written outside your project root**, and nothing overwrites a
   file of yours without showing you the diff.
7. **It disagrees with you.** A research partner that agrees is worth nothing.

## Licence

[PolyForm Noncommercial 1.0.0](LICENSE). Free for your own research, your
teaching, your thesis, and for any university, charity or public body regardless
of funding — which is most of the people who will ever open this. Commercial use
needs a licence, see [COMMERCIAL.md](COMMERCIAL.md).

Not an OSI-approved licence, so GitHub shows it as "unrecognized". That is
expected.

Original work throughout; see [NOTICE](NOTICE).
