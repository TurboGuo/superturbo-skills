# Toolfit: Finance

An accounts receivable desk where the arithmetic is done by a script, not by a language model,
plus the three finance connectors that carry a public endpoint.

## Skill

| Skill | Use it for |
|---|---|
| `/toolfit-finance:ar-collections-desk` | Aged receivables that cross foot, DSO with a reliability check, late fee schedules, customer statements, a ranked call sheet, and fact checked briefs for chase emails |

Point it at a QuickBooks, Xero or CSV invoice export. Every figure is computed by
`scripts/ar.py`, and every output states its source, its as at date, its control total and its
exceptions. A DSO longer than its own measurement window is refused rather than printed.

`python3 tests/test_ar.py` runs 92 checks against three fixtures if you want to see the maths
verified before you trust it.

## Connectors carried by this stack

Stripe, Mercury and Ramp. Endpoints and scope guidance in
[`guides/carried-connectors.md`](./guides/carried-connectors.md).

## Connectors you switch on yourself

QuickBooks and Google Workspace. Neither can be carried by a plugin: QuickBooks installs from the
connector directory, and Google Workspace is managed by Anthropic. See
[`guides/`](./guides).

## Honest install promise

One install. The skill works immediately. Stripe, Mercury and Ramp need one sign in each.
QuickBooks and Google Workspace you switch on yourself, once.

## Check every figure

This skill is built with AI assistance and may contain mistakes. Check every figure against the
ledger before sending, charging or filing. That warning appears at the top of the HTML pack and
at the foot of every command; do not remove it from either.

## Licence and attribution

MIT. Derived from [Denymbird/accounts-receivable-skills](https://github.com/Denymbird/accounts-receivable-skills),
copyright (c) 2026 Paidnice. `LICENSE` and `NOTICE.md` must travel with every copy, including
every client copy. `NOTICE.md` lists exactly what SuperTurbo changed.
