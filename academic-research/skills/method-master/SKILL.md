---
name: method-master
description: Selects, justifies and specifies social science research methods. Routes a research question to a design across quantitative, qualitative, mixed, computational and comparative-historical approaches, checks the design against the epistemic stance, sizes the sample with the arithmetic shown, and writes the methods section with Stata and R code. Use when choosing a design, defending a design to reviewers, sizing a sample, or drafting a methods section. Also carries a Stata and R operations manual: data management, merging, reshaping, missing data, survey weights, clustered standard errors, diagnostics, and exporting publication-ready tables, with runnable .do and .R templates. Also triggers on Chinese: 用什么方法, 研究设计, 研究方法怎么选, 样本量, 要多少人, 需要多少样本, 定量还是定性, 实证策略, 内生性怎么办, 方法部分怎么写, 审稿人说方法有问题, Stata 怎么写, R 怎么写, 数据怎么合并, 缺失值怎么处理, 抽样权重, 聚类标准误, 结果表怎么导出, 跑回归. 用中文提问时用中文回答.
argument-hint: "select | justify | power | specify | analyze | critique [<question or design>]"
---

# Method Master

> Shared workspace: [../academic-master/references/workspace.md](../academic-master/references/workspace.md).


## 语言 / Language

**用户用中文提问，就全程用中文回答**，包括追问、表格标题、图表标注和写进文件的正文。
用中文学术语体直接写，不要先用英文构思再翻译。术语对照表和因果表述的中文阶梯见
[LANGUAGE.md](../../LANGUAGE.md)。这条规则优先于本文件里的其他格式约定。

Reply in the language the user wrote in. Full policy and the EN/中文 terminology
table: [LANGUAGE.md](../../LANGUAGE.md).

Method choice is not tool selection. It is an argument that **this** evidence, generated **this** way, can support **that** claim. A methods section that lists techniques without that argument is why reviewers write "the design does not follow from the question."

## Modes

| Mode | Use it when |
|---|---|
| `select` | The question exists, the design does not |
| `justify` | The design exists and needs defending, usually after a reviewer hit it |
| `power` | Sample size, minimum detectable effect, or information power |
| `specify` | Write the full methods section with code |
| `analyze` | Run the analysis: Stata and R operations, from raw data to the exported table |
| `critique` | Attack an existing design before a reviewer does |

---

## Mode: select

### Step 1 — get the question into causal shape

Rewrite the question in one of five forms. This alone resolves most design confusion:

| Form | Question shape | Family |
|---|---|---|
| Descriptive | How much, how many, how distributed | Survey, administrative data, descriptive network |
| Associational | Does X co-vary with Y | Regression, correlation, SEM |
| Causal | Does X change Y | Experiment, quasi-experiment, causal inference |
| Mechanistic | How does X produce Y | Mediation, process tracing, qualitative sequence, formal model |
| Interpretive | What does X mean to whom, and how is it constituted | Ethnography, interview, discourse, narrative |

If the user cannot pick one, the question is not yet a question. Send them back to [academic-master](../academic-master/SKILL.md) `discuss`.

### Step 2 — check stance coherence, and stop if it breaks

Read field 3 of the profile. A design that contradicts the stance produces a paper that argues with itself. The common collisions:

- Interpretivist stance with a hypothesis-testing survey. One of the two has to go.
- Positivist stance claiming "we let the themes emerge" without a coding reliability statistic.
- Critical stance running a neutral descriptive design with no account of power.
- Pragmatist stance used as a licence to skip justification. Pragmatism still requires an argument for fit.

**If the stance and the candidate design collide, stop and say so.** Offer the two resolutions — change the design, or reframe the stance — and let the user choose. Do not resolve it silently.

### Step 3 — route

Use [references/design-tree.md](references/design-tree.md) for the full routing, and [references/causal-identification.md](references/causal-identification.md) whenever the question is causal. Present **two or three candidate designs**, never one, each with:

- what evidence it generates
- what claim that evidence can carry
- what it cannot rule out
- feasibility against field 7 of the profile — a design the user cannot execute is not a recommendation
- the closest published exemplar, cited, so the user can see the design working

### Step 4 — write the design memo

`.research/projects/<slug>/design.md`: question form, stance check, chosen design with the reason, the two rejected alternatives with the reason, threats to validity and what handles each, sampling plan, measurement plan, analysis plan, ethics and IRB position, and what would falsify the hypothesis.

---

## Mode: justify

Reviewers reject designs in a small number of predictable ways. Answer the actual objection, not a nearby easier one. [references/threats.md](references/threats.md) has the catalogue.

The template for each objection, and it fits in four sentences:

1. **Concede the real force of it.** A justification that starts by disagreeing loses.
2. **State what in the design addresses it** — a specific feature, not a general claim to rigor.
3. **State the residual** — what remains unaddressed, honestly.
4. **State what it would take** to close the residual, and why that is future work rather than this paper.

Never answer a design objection with a limitations paragraph. Reviewers read that as a concession that the objection is fatal.

---

## Mode: power

**Always show the arithmetic.** A power number with no working is a number the user cannot defend in a viva or a revision.

### Quantitative

Worked example — two-group comparison, and the same logic scales to every test:

```
Target power           1 - beta = 0.80
Alpha (two-tailed)     0.05
Expected effect        d = 0.35   <- SUBSTITUTE A REAL SOURCE. Take it from a
                                     meta-analytic estimate, or from the SESOI,
                                     and discount a single published estimate
                                     for publication bias. State which, and cite it.

n per group = 2 * ((z_{1-a/2} + z_{1-b}) / d)^2
            = 2 * ((1.960 + 0.842) / 0.35)^2
            = 2 * (2.802 / 0.35)^2
            = 2 * (8.006)^2
            = 2 * 64.09
            = 128.2  ->  129 per group, 258 total

Attrition 15%:  258 / (1 - 0.15) = 258 / 0.85 = 303.5  ->  304 recruited
Design effect for 20 clusters of ~15, ICC 0.05:
  DEFF = 1 + (m - 1) * ICC = 1 + (15 - 1) * 0.05 = 1 + 0.70 = 1.70
  304 * 1.70 = 516.8  ->  517 recruited
```

Then verify in software rather than trusting the closed form:

```stata
power twomeans 0 0.35, sd(1) power(0.8) alpha(0.05)
power twomeans 0 0.35, sd(1) power(0.8) k1(15) rho(0.05)   // cluster
```
```r
pwr::pwr.t.test(d = 0.35, sig.level = 0.05, power = 0.80, type = "two.sample")
```

Rules that matter more than the formula:

- **Never take the effect size from the single most cited study.** It is the most cited partly because it is the largest. Use a meta-analytic estimate, or the smallest effect that would be substantively interesting (SESOI), or discount a published estimate and say by how much.
- **For interaction terms, the required n is roughly four times the main-effect n** for the same standardized effect. Underpowered moderation is the most common quiet failure in social science.
- **Report the minimum detectable effect** when n is fixed by the data you already have. That is the honest form of the question.
- **Post-hoc "observed power" is meaningless** and reviewers know it. Never compute it.

Full formulas by design: [references/power.md](references/power.md).

### Qualitative

Not sample size — **information power** (Malterud et al., 2016): narrow aim, dense specificity, established theory, strong dialogue and case analysis all *lower* the n required. Give a defensible range with the reasoning, plus a stopping rule stated in advance and reported honestly:

> "We planned 25 to 35 interviews. Recruitment stopped at 31, after three consecutive interviews produced no new codes in the two focal categories, and we conducted four further interviews to confirm."

"Saturation was reached" with no stopping rule and no number is not a claim, it is a formula.

---

## Mode: specify

Write the methods section from the design memo. Structure by design family; see [references/methods-section.md](references/methods-section.md) for the templates and the reporting standards each family owes (CONSORT, STROBE, COREQ, SRQR, PRISMA, JARS-Quant, JARS-Qual).

Deliver runnable code stubs for the user's software. Both Stata and R by default, since the profile lists both:

```stata
* Two-way fixed effects DiD with cluster-robust SE
reghdfe y treat##post $controls, absorb(unit year) vce(cluster unit)
* Pre-trends: event study
reghdfe y ib(-1).rel_time##i.treated $controls, absorb(unit year) vce(cluster unit)
coefplot, keep(*.rel_time#1.treated) vertical yline(0) xline(4)
```
```r
fixest::feols(y ~ i(rel_time, treated, ref = -1) + controls | unit + year,
              cluster = ~unit, data = df) |> iplot()
```

**Warn on the known traps.** Two-way fixed effects with staggered adoption and heterogeneous effects is biased (Goodman-Bacon 2021; Callaway & Sant'Anna 2021) — point the user at `csdid` in Stata or `did` in R. Do not hand over a specification with a known defect and no flag.

---

## Mode: analyze

统计执行。所有命令、陷阱和代码模板在 [references/stata-r.md](references/stata-r.md)，
可直接运行的骨架在 `scripts/analysis-template.do` 和 `scripts/analysis-template.R`。

The operational half of this skill. The design memo says what to estimate; this
mode is how it actually gets run without silently corrupting the sample on the
way. Full command reference and the trap list: [references/stata-r.md](references/stata-r.md).

### 先问三件事 / Ask three things first

1. **Stata 还是 R？** 别两个都写。用户档案里的 field 7 有答案，没有就问。
2. **数据在哪一步？** 原始文件、已合并、已清洗、还是只差跑回归。从那一步接手。
3. **最终要什么？** 一张三线表、一张图、还是一个可复现的脚本。

### 八个环节 / The eight stages

按顺序走，每一步都有一个必须报告的检查值。跳过检查就是在给自己埋雷。

| 环节 | 必须报告的检查 |
|---|---|
| 读入与合并 | 合并前后样本量，`_merge` 的分布 |
| 重塑与聚合 | 分析单位变了没有，标准误该聚类到哪一层 |
| 变量构造 | 缺失值有没有被算成 0 或算成「是」 |
| 缺失值 | 缺失比例，处理方式，插补次数 m |
| 抽样权重 | 用的是 `svy:` 还是 `[pw=]`，为什么 |
| 回归 | 聚类层次，聚类数，聚类数少于 40 就换野聚类自助 |
| 诊断 | 有没有少数几个点在带整个结果 |
| 导出 | 星号规则跟哪个学科惯例，观测数对不对得上 |

### 三条硬规矩 / Three rules

- **永远不手抄系数。** 表格从 `esttab` 或 `modelsummary` 出，不从屏幕上抄。
  手抄的表格里，报告的观测数和实际回归样本对不上是最常见的错误。
- **写代码，不假装跑过。** 这个技能生成的 Stata 和 R 代码**没有被执行过**——
  云端环境和用户机器上都没装 Stata 和 R（Python 有，画图脚本是真跑过的）。
  交代码时说清楚这一点，永远不要报告一个没有真正算出来的数字。
- **报告 `e(sample)`。** 回归实际用了多少观测，和数据集有多少行，通常不是一个数。
  差额去哪了必须能解释。

### 交付 / Deliver

一个带注释的脚本，写到 `.research/projects/<slug>/analysis/`，加一段简短的说明：
每一步在做什么、哪一步的检查值需要用户自己看一眼、以及这段代码没有被运行过。

---

## Mode: critique

Run the design against every item in [references/threats.md](references/threats.md) and report only what actually bites, ranked by severity, each with: the threat, the specific way it applies here, what the design already does about it, and the cheapest fix. End with the one change that most improves the design.

## Hard rules

1. **用中文提问就用中文回答**，全程，包括表格和图注。术语见 [LANGUAGE.md](../../LANGUAGE.md)。Reply in the language the user wrote in.
2. **Show the arithmetic** for every power, sample size or effect size calculation.
3. **Never recommend a design the user cannot execute.** Check field 7 first.
4. **Stop on a stance-design collision**; do not resolve it silently.
5. **Flag known-biased estimators** rather than shipping them quietly.
6. **写了 Stata 或 R 代码就说明它没有被运行过。** 永远不报告一个没有真正算出来的数字。Never report a number from code you did not execute.
7. **Cite the method source.** Yin, Eisenhardt, Braun & Clarke, Angrist & Pischke, Malterud — a method claim is a claim and needs a citation like any other.
8. **Never compute post-hoc observed power.**
