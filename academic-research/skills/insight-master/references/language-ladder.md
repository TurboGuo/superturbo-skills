# The causal language ladder

The verb is a claim. Reviewers read it as one. Match it to what the design can
carry, in every sentence of the abstract, results, discussion and conclusion.

## Rung 0 — description
`X percent of respondents reported...` · `the distribution is skewed toward...`
· `three patterns appear in the data`
Licensed by: any sample, with the sampling frame stated.

## Rung 1 — association
`is associated with` · `co-varies with` · `is correlated with` · `differs
between` · `is higher among`
Licensed by: cross-sectional data, any observational correlation.
**Not licensed**: any statement about what would happen if X changed.

## Rung 2 — prediction
`predicts` · `is a significant predictor of` · `accounts for X percent of the
variance in`
Licensed by: the same as rung 1, plus temporal precedence for a forecasting
claim. Note that "predicts" is heard as causal by non-methodologists, so pair
it with an explicit disclaimer at first use.

## Rung 3 — conditional association
`is associated with, conditional on observed confounders` · `after adjusting
for` · `among otherwise similar respondents`
Licensed by: regression with controls, matching, weighting, entropy balancing.
Requires: a balance table, the common-support region, and a sensitivity analysis
for unobserved confounding (Rosenbaum bounds, E-value, or a Cinelli-Hazlett
sensitivity contour). Without the sensitivity analysis, stay at rung 1.

## Rung 4 — identified causal effect, local
`causes, among compliers` · `the effect at the cutoff is` · `for units induced
to treatment by the instrument`
Licensed by: IV (LATE), fuzzy RDD, RDD at the cutoff.
**The generalization is the error here**, not the causal verb. A LATE is not
an ATE, and saying so in one sentence pre-empts the reviewer.

## Rung 5 — identified causal effect, population
`causes` · `increases` · `reduces` · `leads to`
Licensed by: randomized experiment, or a quasi-experiment whose identifying
assumption has been defended and tested.
Still bounded by: the population studied, the setting, the treatment variant,
the outcome measure and the period.

## Qualitative claims, a separate ladder
`participants described` · `the account suggests` · `in this setting, X operated
through Y` · `the case demonstrates that X is possible` · `the mechanism
appeared as`
**Not licensed**: `most participants`, `X percent`, `this shows that generally`.
Qualitative work generalizes to theory, not to populations, and saying so is a
strength, not a hedge.

## The laundering list
These are causal verbs wearing a hedge. Reviewers do not accept them as softer:
`impacts` · `drives` · `shapes` · `affects` · `influences` · `determines` ·
`contributes to` · `translates into` · `results in` · `produces` · `fosters` ·
`enhances` · `improves` · `promotes` · `boosts` · `undermines` · `erodes`
If the design supports a causal claim, say `causes`. If it does not, say
`is associated with`. The middle ground is where papers get rejected.

## The construction that hides a causal claim
`Given the positive relationship between X and Y, organizations should increase
X.` The recommendation is a causal claim regardless of how the sentence started.
Practical implications inherit the rung of the evidence.
