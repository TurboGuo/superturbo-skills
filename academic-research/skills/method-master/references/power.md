# Power and sample size — formulas with the arithmetic shown

Constants: z_{0.975} = 1.960 · z_{0.80} = 0.842 · z_{0.90} = 1.282

## Two independent means
n per group = 2 * ((z_{1-a/2} + z_{1-b}) / d)^2
At d = 0.50, alpha 0.05, power 0.80:
  2 * ((1.960 + 0.842) / 0.50)^2 = 2 * (5.604)^2 = 2 * 31.40 = 62.8 -> 63 per group

## Two proportions
n per group = ((z_{1-a/2} + z_{1-b})^2 * (p1(1-p1) + p2(1-p2))) / (p1 - p2)^2
p1 = 0.40, p2 = 0.55:
  numerator   = (2.802)^2 * (0.40*0.60 + 0.55*0.45) = 7.851 * (0.240 + 0.2475)
              = 7.851 * 0.4875 = 3.828
  denominator = (0.15)^2 = 0.0225
  n = 3.828 / 0.0225 = 170.1 -> 171 per group

## Correlation
n = ((z_{1-a/2} + z_{1-b}) / z_r)^2 + 3, where z_r = 0.5 * ln((1+r)/(1-r))
r = 0.25:  z_r = 0.5 * ln(1.25/0.75) = 0.5 * ln(1.6667) = 0.5 * 0.5108 = 0.2554
  n = (2.802 / 0.2554)^2 + 3 = (10.97)^2 + 3 = 120.3 + 3 = 123.3 -> 124

## Multiple regression, R-squared change
f2 = dR2 / (1 - R2_full)
dR2 = 0.05, R2_full = 0.35:  f2 = 0.05 / 0.65 = 0.0769  (a small effect)
Use G*Power or R `pwr::pwr.f2.test(u = <tested predictors>, f2 = 0.0769,
sig.level = 0.05, power = 0.80)`, then n = v + u + 1.

## Cluster designs
DEFF = 1 + (m - 1) * ICC, where m is the average cluster size.
n_clustered = n_simple * DEFF
40 clusters of 25, ICC 0.03:
  DEFF = 1 + 24 * 0.03 = 1.72;  a simple-random n of 400 becomes 400 * 1.72 = 688

## Interactions
For a standardized interaction effect of the same size as a main effect, budget
roughly **4x** the main-effect n. If the interaction is expected to be half the
size, budget roughly 16x. Most published moderation in social science is
underpowered and the literature's mixed findings partly reflect that.

## Minimum detectable effect, when n is fixed
MDE = (z_{1-a/2} + z_{1-b}) * SE(effect)
For two equal groups of n each with SD = 1:
  SE = sqrt(2/n);  n = 200 per group -> SE = sqrt(0.01) = 0.100
  MDE = 2.802 * 0.100 = 0.280 in standard deviations
Report this whenever the sample already exists. It is the honest version of the
question and it pre-empts the reviewer asking.

## Attrition
n_recruit = n_analysis / (1 - attrition_rate)
15% attrition on 300 analysed: 300 / 0.85 = 352.9 -> 353 recruited

## Software
Stata: `power twomeans`, `power twoproportions`, `power onecorrelation`,
       `power repeated`, `power cox`, and `simulate` for anything bespoke
R:     `pwr`, `simr` (mixed models), `WebPower`, `simsem` (SEM), `DeclareDesign`
Standalone: G*Power 3.1
For anything non-standard, **simulate**. A 500-run Monte Carlo beats a closed
form you had to distort the design to fit.

## Qualitative: information power (Malterud, Siersma & Guassora 2016)
Fewer participants are needed when the aim is narrow, the sample is specific,
established theory is applied, dialogue quality is high, and analysis is
case-focused. More are needed when any of those reverse. State a planned range,
state a stopping rule in advance, and report what actually stopped recruitment.
