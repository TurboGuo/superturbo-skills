# Causal identification in observational social science

## The question that comes before the method
**What is the counterfactual, and what makes it credible?**
If there is no answer, no estimator fixes it. Choose the estimator after the
counterfactual, never before.

## Estimand first
Say which effect is being estimated before saying how:
ATE (whole population) · ATT (the treated) · LATE (compliers, which is what IV
gives you and it is not the ATE) · CATE (conditional) · ITT (assigned, not
received). Reviewers increasingly ask for the estimand explicitly.

## The identifying assumption and how it is defended

| Design | Assumption | How it is defended | How it fails |
|---|---|---|---|
| RCT | Randomization worked | Balance table, randomization check | Attrition, non-compliance, spillover |
| DiD | Parallel trends absent treatment | Event-study pre-trends plot, placebo periods | Anticipation, differential shocks, staggered timing |
| RDD | Continuity at the cutoff | McCrary density test, covariate smoothness, bandwidth sensitivity | Manipulation of the running variable |
| IV | Relevance + exclusion + monotonicity | First-stage F and Anderson-Rubin CI; exclusion argued substantively | Weak instrument, plausible direct effect |
| Synthetic control | Good pre-period fit | Pre-period RMSPE, placebo-in-space and placebo-in-time | Short pre-period, interpolation bias |
| Matching | Selection on observables | Balance before/after, common support | The confounder you did not measure |
| Panel FE | No time-varying confounders | Robustness to unit-specific trends | Anything that varies within unit over time |

## The trap list

> Verified against the cited papers and the current Stata/R package
> documentation on **2026-08-25**. Estimator recommendations in this area have
> changed more than once in recent years — **re-check the package docs before
> relying on a specific command**, and treat the paper citations as the stable
> part and the command names as the volatile part.
- **Staggered DiD with TWFE is biased** under heterogeneous treatment effects
  (Goodman-Bacon 2021; de Chaisemartin & D'Haultfoeuille 2020; Callaway &
  Sant'Anna 2021; Sun & Abraham 2021). Use `csdid`, `did_imputation`,
  `eventstudyinteract` in Stata; `did`, `didimputation`, `fixest::sunab` in R.
- **Bad controls.** Controlling for a post-treatment variable, or for a
  collider, introduces bias rather than removing it. Draw the DAG first — this
  is exactly what theory-graph-master exists for.
- **Weak instruments.** First-stage F above 10 is a rule of thumb that does not
  survive contact with modern work (Lee et al. 2022 put the threshold far
  higher). Report Anderson-Rubin confidence sets.
- **Controlling for the mechanism** when you want the total effect. Decide
  whether the estimand is total or direct, then control accordingly.
- **p-hacking through specification search.** Report a specification curve or
  a multiverse analysis when many defensible specifications exist.
- **Clustering at the wrong level.** Cluster where treatment is assigned. With
  fewer than about 40 clusters, use wild cluster bootstrap (`boottest`,
  `fwildclusterboot`).

## When identification is not available
Say so, and say what the estimate *is*: a conditional association, a descriptive
pattern, a prediction. Then use the language ladder in insight-master. A clearly
labelled descriptive finding is publishable. A causal claim the design cannot
carry is a rejection.
