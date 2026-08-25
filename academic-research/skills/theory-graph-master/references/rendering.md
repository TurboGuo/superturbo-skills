# Rendering paths

| Path | Install cost | Use it when |
|---|---|---|
| Mermaid | none | Drafting, chat, GitHub, slides, anything iterative |
| Python (`scripts/`) | matplotlib, networkx | A journal file: SVG, PDF, 300 dpi PNG from one source |
| R | ggdag, dagitty, DiagrammeR, semPlot | The analysis is already in R, or you want dagitty's checks |
| Stata | limited | Stata has no general diagram engine; see the note below |

**Default to Mermaid while the model is still changing.** Move to a script only
when the structure is settled, because every re-render of a scripted figure
costs more than an edit to five lines of Mermaid.

## Mermaid patterns

Conceptual framework, left to right:
```
flowchart LR
    IV["Construct A"] -->|"H1 (+)"| MED["Mediator"]
    MED -->|"H2 (+)"| DV["Outcome"]
    IV -.->|"H3 indirect"| DV
    MOD["Moderator"] --> P(( ))
    P -.- IV
    CTRL["Controls: a, b, c"] --> DV
    classDef ctrl fill:#f5f5f5,stroke:#999,stroke-dasharray:3 3
    class CTRL ctrl
```

Cross-level model — use subgraphs as level bands:
```
flowchart TB
    subgraph L2["Organization level"]
        CLIM["Climate"]
    end
    subgraph L1["Individual level"]
        ATT["Attitude"] --> BEH["Behavior"]
    end
    CLIM -.->|"cross-level moderation, H3"| ATT
```

PRISMA 2020 flow:
```
flowchart TB
    A["Records identified<br/>Databases n=1,204<br/>Registers n=18"] --> B["Duplicates removed<br/>n=311"]
    B --> C["Records screened<br/>n=911"]
    C --> D["Excluded<br/>n=742"]
    C --> E["Reports sought<br/>n=169"]
    E --> F["Not retrieved<br/>n=12"]
    E --> G["Assessed for eligibility<br/>n=157"]
    G --> H["Excluded n=118<br/>wrong population 54<br/>no outcome 39<br/>not empirical 25"]
    G --> I["Studies included<br/>n=39"]
```

Gioia data structure:
```
flowchart LR
    A1["'they just decide<br/>without asking us'"] --> B1["Exclusion from<br/>decision rights"]
    A2["'we find out after'"] --> B1
    B1 --> C1["Eroded procedural<br/>standing"]
```

## Python scripts

`scripts/render_framework.py` — conceptual frameworks. JSON spec:

| Field | Meaning |
|---|---|
| `nodes[].id` | Reference used by edges |
| `nodes[].label` | Text; `\n` breaks lines, long text auto-wraps |
| `nodes[].col`, `.row` | Grid position; col is left to right, row is bottom to top |
| `nodes[].kind` | `construct` `outcome` `latent` `moderator` `control` `unobserved` |
| `nodes[].mediator` | `true` turns on the both-legs validation check |
| `edges[].from`, `.to` | A directed path |
| `edges[].onto` | `[a, b]` makes it a moderator terminating on the a→b path |
| `edges[].label` | Hypothesis number and sign, e.g. `H2a (+)` |
| `edges[].style` | `solid` `dashed` `dotted` |
| `edges[].curve` | Arc, e.g. `-0.38` to route an indirect path over a mediator |
| `note` | The figure note, printed under the figure |

```
uv run --with matplotlib scripts/render_framework.py spec.json --out fig1
uv run --with matplotlib scripts/render_framework.py spec.json --out fig1 --strict
```
`--strict` exits non-zero on a validation warning. Use it in a build script.

`scripts/render_dag.py` — DAG plus identification report. It prints every
backdoor path, marks colliders, computes minimal sufficient adjustment sets over
**measured** variables, and says NOT IDENTIFIED when no such set exists.

```
uv run --with networkx --with matplotlib scripts/render_dag.py dag.json --out fig2
uv run --with networkx scripts/render_dag.py dag.json --no-render   # report only
```

## R

```r
# DAG with formal checks
library(dagitty); library(ggdag)
g <- dagitty('dag { X [exposure] Y [outcome] U [latent]
                    U->X U->Y X->M M->Y Z->X Z->Y }')
adjustmentSets(g, exposure="X", outcome="Y")
impliedConditionalIndependencies(g)
ggdag(g) + theme_dag()

# SEM path diagram
library(lavaan); library(semPlot)
fit <- sem(model, data = df)
semPaths(fit, whatLabels="std", layout="tree2", edge.color="black",
         sizeMan=7, sizeLat=9, nCharNodes=0)

# PRISMA flow from counts
library(PRISMA2020)
PRISMA_flowdiagram(PRISMA_data(read.csv("prisma.csv")), interactive = FALSE)
```

## Stata

Stata has no general node-and-arrow engine outside the SEM Builder GUI, and the
Builder cannot be scripted reproducibly. The honest paths:

1. Build the model in the SEM Builder, then `graph export fig.eps, replace`.
2. Estimate in Stata, export the coefficients, and render the figure with
   `scripts/render_framework.py`. This is the reproducible option.
3. For coefficient and marginal-effect plots, which Stata does well:
   `coefplot`, `marginsplot`, `graph export fig.pdf, replace`.

Do not tell a Stata user their diagram is a `graph twoway` problem. It is not.
