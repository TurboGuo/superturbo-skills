# DAG rules, with the cases that actually bite

## The three building blocks
| Structure | Shape | Association flows when |
|---|---|---|
| Chain (mediator) | A → B → C | B is NOT conditioned on |
| Fork (confounder) | A ← B → C | B is NOT conditioned on |
| Collider | A → B ← C | B IS conditioned on — the reverse of the other two |

The collider rule is the counter-intuitive one and it is the source of most
harm done by "controlling for everything available".

## Backdoor criterion
Z is sufficient to identify the effect of X on Y if:
1. No member of Z is a descendant of X, **and**
2. Z blocks every path from X to Y that begins with an arrow into X.

Equivalently: delete every arrow leaving X, then check that Z d-separates X
from Y in what remains. That is exactly what `render_dag.py` computes.

## Six failures, in the order they occur in real papers

**1. Adjusting for a collider.** Selecting on, or controlling for, a common
effect of X and Y creates an association where none existed. Classic case:
studying only hospitalized patients, only employed workers, only surviving
firms. Selection into the sample is conditioning on a collider, and it is
invisible in the regression output.

**2. Adjusting for a mediator when you want the total effect.** The coefficient
that comes back is a direct effect, and the paper usually calls it the total
effect. Decide the estimand before choosing the controls.

**3. The kitchen-sink regression.** "We control for everything available" is not
conservative. It is a specification chosen at random with respect to the causal
structure, and it can add bias.

**4. M-bias.** X ← U1 → Z ← U2 → Y. Z is a pre-treatment variable, it is not a
descendant of X, and adjusting for it still opens a path. Pre-treatment is not
a sufficient reason to control.

**5. The unmeasured confounder.** The honest outcome of many DAGs. When the
adjustment set requires a variable you do not have, the effect is not identified
by adjustment and you need a different design. Say this in the paper rather than
reporting the regression and hoping.

**6. Reverse arrows drawn by convenience.** Ask for every arrow whether the
reverse is equally plausible. If it is, the DAG encodes an assumption that needs
defending in the text, not a fact.

## Testable implications
A DAG implies conditional independencies you can check in the data. `dagitty`'s
`impliedConditionalIndependencies()` lists them; `localTests()` tests them.
A DAG whose implications fail in the data is a DAG that is wrong, and finding
that out before the reviewer does is worth the ten minutes.

## What a DAG cannot do
It carries no functional form, no effect sizes, no interactions, and no
guarantee of correctness — a DAG is your assumptions drawn neatly, and drawing
them neatly does not make them true. Its value is that it makes them arguable.
