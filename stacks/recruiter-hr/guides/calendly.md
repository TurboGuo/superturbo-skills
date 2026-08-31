# Calendly

**Tier: ADDITIONAL** — connect it when the client runs more than a couple of interviews a month
**Client cost: $0 forever.** The free plan gives 1 event type and 1 calendar connection, and
Calendly confirms MCP works on **every plan including free**.

## What it does in the hiring flow

Interview scheduling, and nothing else. One event type is exactly one thing: the interview slot.
The free tier fits the job rather than being a trial of a bigger one.

Pairs with `interview-kit`, which produces the loop that has to be booked.

## Install

claude.ai → **Customize** → **Connect your tools** → search **Calendly** → Connect → sign in →
**Approve**. Then in a new chat: **+** → **Connectors** → toggle Calendly on.

Any other MCP client: server URL `https://mcp.calendly.com/`.

## Links

- Official steps: https://calendly.com/help/connect-calendly-to-your-ai-tools
- Demo and example prompts: https://calendly.com/blog/mcp-server
- Technical reference: https://developer.calendly.com/calendly-mcp-server
- Free plan limits: https://calendly.com/pricing

## How widely used

**20 million users across 230 countries**, roughly **100,000 paying companies**, and **86 per cent
of the Fortune 500** as of June 2024. $3 billion valuation in 2021. Dominant in appointment
scheduling by any measure.

Confirmed on **both Claude and ChatGPT** from Calendly's own documentation.

## What breaks without it

Google Calendar still holds the loop. The client books interviews by hand or with their own tool.
Nothing fails, the coordinator just keeps a job they were hoping to hand over.
