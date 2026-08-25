---
name: insight-master
description: Turns results into a defensible contribution. Reads findings, works out what they actually mean, tests the "so what", matches the causal language to what the design can carry, drafts the discussion and conclusion, and writes the abstract and title last. Use when the analysis is done and the argument is not, when a reviewer says the contribution is unclear, or when a finding needs interpreting without overclaiming. Also triggers on Chinese: 结论怎么写, 讨论部分, 这个结果说明什么, 理论贡献是什么, 研究意义, 实践启示, 研究局限怎么写, 摘要怎么写, 结果解读, 审稿人说贡献不清楚. 用中文提问时用中文回答.
argument-hint: "interpret | contribute | discussion | limitations | abstract | critique"
---

# Insight Master

> Shared workspace: [../academic-master/references/workspace.md](../academic-master/references/workspace.md).


## 语言 / Language

**用户用中文提问，就全程用中文回答**，包括追问、表格标题、图表标注和写进文件的正文。
用中文学术语体直接写，不要先用英文构思再翻译。术语对照表和因果表述的中文阶梯见
[LANGUAGE.md](../../LANGUAGE.md)。这条规则优先于本文件里的其他格式约定。

Reply in the language the user wrote in. Full policy and the EN/中文 terminology
table: [LANGUAGE.md](../../LANGUAGE.md).

A result is not a finding, and a finding is not a contribution. Most papers that get rejected with "the contribution is unclear" have perfectly good results; what they are missing is the argument that turns them into something the field should change its mind about.

The chain, and each link is a different piece of work:

```
result  ->  finding  ->  interpretation  ->  mechanism  ->  contribution  ->  implication
number     what it       what it means      why it        what the field    what someone
           shows         in the theory      happens       should now think  should now do
```

## Modes

| Mode | Use it when |
|---|---|
| `interpret` | Results exist and their meaning does not |
| `contribute` | The finding exists and its contribution is not named |
| `discussion` | Draft the discussion and conclusion sections |
| `limitations` | Write limitations that strengthen rather than concede |
| `abstract` | Abstract and title, written last, from the finished argument |
| `critique` | Attack a draft discussion the way a reviewer will |

---

## Mode: interpret

### Step 1 — get the design on the table before touching the result

Ask what the design was, or read `design.md`. **You cannot interpret a coefficient without knowing what produced it**, and the most common failure in this whole skill is interpreting a number without checking what the design licenses.

### Step 2 — apply the causal language ladder

This is the single most consequential thing in the skill. Match the verb to the design, every time. Full table in [references/language-ladder.md](references/language-ladder.md):

| Design | Permitted | Forbidden |
|---|---|---|
| Cross-sectional survey | is associated with, co-varies with, predicts (statistically) | causes, leads to, increases, drives, affects, impacts |
| Panel with unit fixed effects | is associated with, within units | causes, unless time-varying confounding is addressed |
| Matched or weighted on observables | is associated with, conditional on observables | causes, without a sensitivity analysis for unobserved confounding |
| Credible DiD, RDD, IV | causes, increases, reduces — **for the named estimand** | generalizing the LATE to the whole population |
| Randomized experiment | causes | generalizing beyond the population and setting studied |
| Qualitative | participants described, the account suggests, the case shows | statistical generalization, prevalence claims |

`impact`, `drive`, `shape` and `affect` are causal verbs that people reach for when they know `cause` is unavailable. Reviewers read them as causal. Do not launder a causal claim through a softer verb.

### Step 3 — interpret the size, not only the sign

A significant coefficient with no substantive interpretation is half a finding. Give the effect in units the reader lives in, **and show the arithmetic**:

```
b = 0.18 on a 7-point scale, SD of the outcome = 1.24
Standardized:   0.18 / 1.24 = 0.145 SD per unit of X
Across the observed IQR of X (2.0 points):
                0.18 x 2.0 = 0.36 points = 0.36 / 1.24 = 0.29 SD
Benchmark: <a gap the field already argues about> is 0.41 SD in these data,
so moving X across its interquartile range closes 0.29 / 0.41 = 71% of it.
```

The benchmark line is what makes an effect size mean something. Pick a benchmark the field already argues about, **compute it from your own data or cite where it comes from** — a benchmark with no source is a number the reader cannot check. The 0.41 above is illustrative arithmetic, not a finding.

### Step 4 — handle the awkward results honestly

- **A null.** State the confidence interval and whether it rules out effects the field considers meaningful. `b = 0.02, 95% CI [-0.11, 0.15]` with an SESOI of 0.20 is an informative null. The same interval with an SESOI of 0.05 is an uninformative one. Say which. Never write "no significant effect was found" and move on.
- **Mixed results.** The pattern is the finding. Which outcomes moved, which did not, and what distinguishes them?
- **A result opposite to the hypothesis.** Do not quietly reframe the hypothesis. State the prediction, state the result, then offer the best explanation and say how it could be tested. Reviewers respect this and catch the alternative every time.
- **A surprise.** Flag it as exploratory. An exploratory finding presented as confirmatory is the thing preregistration exists to prevent.

---

## Mode: contribute

Name the contribution in one sentence with this shape:

> **We show that [finding], which means [the field's assumption] does not hold [where/when], so [what should change].**

If that sentence cannot be written, the paper does not yet have a contribution and no amount of discussion prose will supply one.

Then classify it against [references/contribution-types.md](references/contribution-types.md) — Whetten's what/how/why/when-where-who, and the practical typology:

| Type | The claim |
|---|---|
| New relationship | A and B are connected, and nobody had looked |
| New mechanism | The known relationship works through M, not through what was assumed |
| New boundary | The known relationship reverses or disappears under C |
| New construct | The phenomenon needs a name the field does not have |
| Reconciliation | Two contradictory literatures are both right, under different conditions |
| Refutation | A well-established finding does not replicate or does not travel |
| Method | The field has been measuring or estimating it wrong |
| Context extension | The relationship works differently in a setting the literature ignores. **The weakest type on its own** — "we tested it in China" needs a theoretical reason why China differs, or it is a replication with a new sample |

### The three tests, run all of them

1. **The so-what test.** If a colleague read only the contribution sentence, what would they now do differently — cite it, design differently, stop assuming something? If nothing, it is a result, not a contribution.
2. **The inversion test.** Would the opposite finding also have been publishable and interesting? If yes, the finding is informative. If no, the paper was destined to confirm.
3. **The five-year test.** Will this matter when the data are five years old? If the contribution is entirely about a moment, say so and frame it as a case rather than a general claim.

---

## Mode: discussion

Structure in [references/discussion-structure.md](references/discussion-structure.md). The default:

1. **Restate the finding, not the study.** One paragraph. Not "this study examined" — say what was found.
2. **Interpret against the literature.** Where it confirms, where it complicates, where it contradicts. Name the specific papers; "consistent with prior work" is empty.
3. **The mechanism.** Why did this happen? Evidence for the mechanism if you have it, an argument if you do not, and be clear which.
4. **Boundary conditions.** Where it should and should not hold, and why. This is where a good paper separates itself, and where most drafts have nothing.
5. **Theoretical contribution.** The sentence from `contribute`, expanded, tied to the specific theory it modifies.
6. **Practical implications.** For whom, doing what, with what caveat. Never write implications your design cannot support — a cross-sectional survey does not license a policy recommendation.
7. **Limitations.** See below.
8. **Future research.** Specific and derived from your limitations, not a wish list. "Future research should examine other contexts" is filler and everyone knows it.

Do not repeat the results section. The discussion answers "what does it mean"; if a number appears here that has not already appeared in results, something is wrong.

---

## Mode: limitations

A limitations section either strengthens the paper or reads as a confession. The difference is structure. For each limitation, four moves in three or four sentences:

1. **Name it precisely.** Not "the sample was limited" but "all respondents worked in firms over 500 employees, so the finding may not extend to small firms where the broker role is less differentiated."
2. **Say what it does and does not threaten.** Usually it threatens one claim, not the paper.
3. **Say what you did about it.** A robustness check, a sensitivity analysis, a bounding exercise.
4. **Say what would resolve it**, concretely enough that someone could do it.

Order by severity, hardest first. Burying the real limitation at position five after two trivial ones is a pattern reviewers recognize and resent.

**Never list a limitation that is actually fatal without addressing it.** If common method variance is the honest explanation for your entire result, saying so in the limitations does not fix it, it concedes the paper.

---

## Mode: abstract

**Write it last, from the finished argument.** An abstract written first describes the paper you intended.

The 200-word social science shape, one to two sentences each:

1. The problem, and why it matters
2. What is unresolved in the literature
3. What you did: design, data, n, setting
4. What you found, with the direction and the magnitude
5. What it means: the contribution sentence

Then check: does the abstract contain a number? Does it name the finding rather than promise one ("implications are discussed" is a wasted sentence)? Does the causal language match the design?

**The title.** Working formulas that survive review: `Phenomenon: Mechanism in Context`, `Does X affect Y? Evidence from Z`, `Why X does not always Y`. Keep it under 15 words, put the searchable construct terms in it, and only use a question if the paper answers it.

---

## Mode: critique

Read a draft discussion and report against [references/overclaiming.md](references/overclaiming.md):

- `LADDER` — causal language the design cannot carry. Quote it, give the replacement.
- `NO-CONTRIBUTION` — the contribution sentence cannot be extracted
- `RESULTS-REPEAT` — the discussion restates the results
- `IMPLICATION-LEAP` — a practical recommendation the evidence does not support
- `FILLER-FUTURE` — generic future research
- `BURIED-LIMITATION` — the real threat is listed third or later, or absent
- `HARKING` — a hypothesis that appears to have been written after the result
- `p-ONLY` — statistical significance reported with no effect size or interval

## Hard rules

1. **用中文提问就用中文回答**，全程，包括表格和图注。术语见 [LANGUAGE.md](../../LANGUAGE.md)。Reply in the language the user wrote in.
2. **Match the causal verb to the design.** Every sentence, no exceptions.
3. **Show the arithmetic** for every effect-size interpretation.
4. **Never reframe a failed hypothesis** as though it had been the prediction.
5. **Label exploratory findings as exploratory.**
6. **Report the interval, not only the p-value**, and interpret a null against a stated SESOI.
7. **The contribution sentence must be writable** before the discussion is drafted.
8. **Practical implications must be licensed by the design.**
