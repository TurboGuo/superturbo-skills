# Systematic review protocol template

Write this BEFORE any screening. Save to
`.research/projects/<slug>/protocol.md`. Register it where the field expects:
PROSPERO for health-adjacent work, OSF Registries or RIDIE for social science.

```markdown
# Protocol: <title>
Written: YYYY-MM-DD   Registered: <ID or "not registered">

## 1. Question
PICO / PICo / SPIDER as fits the design:
  Population:
  Intervention or Exposure or phenomenon of Interest:
  Comparator:
  Outcome:
  Context:
  Study design(s):

## 2. Eligibility criteria
Include:
Exclude:
Date range:            and the justification for it
Languages:             and what is lost by that limit
Publication types:     peer-reviewed only, or grey literature included

## 3. Sources
| Database | Interface | Search string | Date run | Hits |
|---|---|---|---|---|

Supplementary: backward and forward citation chasing from included studies,
hand search of <named journals>, contact with <named authors>.

## 4. Screening
Stage 1 title and abstract, stage 2 full text.
Screeners: two independent. Agreement: Cohen's kappa, target above 0.70.
Disagreement resolution: discussion, then a third reader.
Software: Rayyan, Covidence, or a spreadsheet.

## 5. Data extraction
Form piloted on 5 studies before full extraction. Fields: <list>.
Extracted by: <one with a check on 20 percent, or two independent>.

## 6. Risk of bias
Tool: RoB 2 (trials), ROBINS-I (non-randomized), MMAT (mixed methods),
CASP (qualitative), or a named custom rubric with its items listed.

## 7. Synthesis
Narrative synthesis, or meta-analysis with:
  model: random effects (justify if fixed)
  heterogeneity: Q, I-squared, tau-squared, prediction interval
  moderators: <pre-specified list>
  publication bias: funnel plot, Egger's test, p-curve or selection model

## 8. Deviations
Any departure from this protocol is recorded here with its date and reason.
```

## The PRISMA 2020 flow numbers to track from day one

```
Identification:  records from databases (n = , by source)
                 records from other methods (n = )
                 duplicates removed (n = )
Screening:       records screened (n = )     excluded (n = )
                 reports sought for retrieval (n = )   not retrieved (n = )
                 reports assessed for eligibility (n = )
                 excluded with reasons (n = , reason 1 = , reason 2 = )
Included:        studies included (n = )   reports of those studies (n = )
```

theory-graph-master renders this as the four-stage flow diagram.
