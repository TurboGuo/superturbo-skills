# Design routing tree

## A. Causal question, you control assignment
- **Lab experiment** — high internal validity, weak external. Report per CONSORT.
- **Field experiment / RCT** — the gold standard where ethics and budget allow.
  Pre-register. Watch spillover, attrition, non-compliance (report ITT and LATE).
- **Survey experiment** — vignette, conjoint, list experiment, endorsement
  experiment. Best for sensitive attitudes and for measuring multi-dimensional
  preferences. Conjoint: Hainmueller, Hopkins & Yamamoto (2014); AMCE estimands.
- **Lab-in-the-field** — behavioral games with a non-student population.

## B. Causal question, you do not control assignment
See causal-identification.md. In rough order of credibility when the assumptions
hold: RDD > DiD with a credible parallel-trends story > IV with a genuinely
excludable instrument > matching or weighting on observables > selection models.
- **Difference-in-differences** — needs parallel pre-trends, shown not asserted.
  Staggered adoption requires csdid / did / did2s, not plain TWFE.
- **Regression discontinuity** — a cutoff with local randomization. Report the
  McCrary density test, bandwidth sensitivity, donut specifications.
- **Instrumental variables** — relevance is testable (first-stage F, and the
  weak-IV threshold is far above 10 for inference; use Anderson-Rubin).
  Exclusion is not testable and must be argued substantively.
- **Synthetic control** — one treated unit, many donors, long pre-period.
- **Matching / weighting** — PSM, CEM, entropy balancing, IPW. Only controls
  observables; report balance before and after and the common-support region.
- **Panel fixed effects** — removes time-invariant unobservables only.
- **Event study** — the visual test that the identifying assumption holds.

## C. Associational or descriptive
- **Cross-sectional survey** — sampling frame and response rate are the whole
  ballgame. Report AAPOR response rate 1-6 and say which.
- **Panel survey** — attrition analysis is mandatory.
- **Multilevel / hierarchical models** — individuals in groups. Report ICC,
  justify random slopes, and note that under ~30 level-2 units the level-2
  standard errors are unreliable.
- **SEM** — CFA first, then structural. Report chi-square, CFI above 0.95,
  TLI, RMSEA below 0.06, SRMR below 0.08, and the full measurement model.
  Sample: roughly 10 cases per free parameter, or run a Monte Carlo power study.
- **PLS-SEM** — for prediction, formative constructs, or small n. Report
  composite reliability, AVE above 0.50, HTMT below 0.85. It is not a
  small-sample loophole for covariance SEM, whatever the software marketing says.

## D. Mechanistic question
- **Mediation** — causal steps are obsolete. Use the potential-outcomes
  framework (Imai, Keele & Tingley), report ACME, ADE, total effect, and a
  sensitivity analysis for sequential ignorability (rho). Stata `medeff` /
  `causalmed`, R `mediation`. Cross-sectional mediation is nearly always
  uninterpretable; say so.
- **Moderation** — always plot the marginal effect across the moderator range,
  never rely on the interaction coefficient alone. Stata `margins, dydx()` and
  `marginsplot`; R `marginaleffects`. Check common support in the interaction.
- **Process tracing** — within-case causal inference. Four test types: straw in
  the wind, hoop, smoking gun, doubly decisive (Beach & Pedersen; Collier 2011).
- **Formal model plus empirical test** — the model generates a comparative
  static, the data tests it.

## E. Interpretive question
- **Semi-structured interviews** — thematic analysis (Braun & Clarke 2006; use
  the reflexive-TA restatement in Braun & Clarke 2019, which explicitly rejects
  inter-rater reliability as a quality criterion for reflexive TA), framework analysis, or
  IPA for lived experience.
- **Grounded theory** — Glaserian, Straussian, or constructivist (Charmaz).
  Pick one and follow it; theoretical sampling and constant comparison are
  requirements, not options.
- **Abductive analysis** — Timmermans & Tavory. Theory first, then surprises.
- **Ethnography** — prolonged engagement, fieldnotes, thick description,
  reflexivity on the researcher's position.
- **Discourse and content analysis** — qualitative content analysis (Mayring)
  needs inter-coder reliability: Cohen's kappa above 0.70 for two coders,
  Krippendorff's alpha above 0.80 for more or for ordinal data.
- **Narrative analysis** — structure, plot, and positioning within accounts.

## F. Comparative and historical
- **Comparative case study** — most similar, most different, deviant, typical,
  crucial. State the case-selection logic; never select on the dependent
  variable and then explain the variation.
- **QCA (crisp or fuzzy set)** — set-theoretic, for medium-N configurational
  questions. Report consistency and coverage, and the truth table.
- **Historical institutionalism** — critical junctures, path dependence,
  sequencing. Archival sourcing standards apply.

## G. Computational
- **Text as data** — dictionary, supervised classification, topic models (LDA,
  STM), embeddings, LLM-assisted coding. **Validation against human coding is
  mandatory**; report agreement on a held-out set. Grimmer & Stewart (2013).
- **Network analysis** — centrality, community detection, ERGM, SAOM (RSiena)
  for dynamics. Boundary specification is the first and most consequential
  decision.
- **Agent-based modeling** — verification, validation, sensitivity sweeps,
  report per ODD protocol.
- **Digital trace data** — platform bias, API coverage limits, and the fact
  that the population is platform users, not people.

## H. Mixed methods
Name the design and its notation (Creswell & Plano Clark):
- Convergent parallel — QUAN + QUAL, merged at interpretation
- Explanatory sequential — QUAN -> qual, the qual explains the quan
- Exploratory sequential — QUAL -> quan, the quan tests what the qual found
- Embedded, multiphase

Specify the **point of integration** and what a divergence between strands would
mean. "Triangulation" without naming the type (data, method, theory,
investigator) and without saying what convergence proves is a documented failure
mode, not a design.

## I. Consensus and elicitation
- **Delphi** — rounds, panel selection criteria, consensus defined in advance
  (Kendall's W, or a percentage-agreement threshold), stability across rounds.
- **Expert elicitation** — structured, with calibration questions.
