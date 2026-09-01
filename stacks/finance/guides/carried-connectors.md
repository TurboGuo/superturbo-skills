# Stripe, Mercury and Ramp

These three arrive with the plugin. Each asks you to sign in the first time it is used, and each
grants only what your own account already allows.

| Connector | Endpoint | What it does here |
|---|---|---|
| Stripe | `https://mcp.stripe.com` | Revenue in, and the payout file every tie out starts from |
| Mercury | `https://mcp.mercury.com/mcp` | The cash side, and the bank statement a tie out reconciles to |
| Ramp | `https://mcp.ramp.com/mcp` | Cards, expenses and bill pay. The vendor spend feed |

## Trying Ramp without a Ramp account

Ramp serves sample data at `https://demo-mcp.ramp.com/mcp`. Point a custom connector at that URL
to see the shape of the data before connecting a real account.

## Scope

Grant the smallest scope that lets you run one real test: one account, one month. Widen it later.
Nothing here writes to your ledger.

Sources: [Stripe MCP](https://docs.stripe.com/mcp),
[Mercury MCP](https://docs.mercury.com/docs/connecting-mercury-mcp),
[Ramp MCP](https://agents.ramp.com/docs/mcp/overview)
