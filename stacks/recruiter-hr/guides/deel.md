# Deel

**Tier: ADDITIONAL** — connect it when the client employs people, not just interviews them
**Client cost: $0 for companies under 200 employees** (Deel HR). $5 per employee per month above
that. EOR and payroll are separate paid products the client does not need for these skills.

## What it does in the hiring flow

The free HRIS, and the source of the one number nobody else can produce.

- Employee records, PTO, org chart, onboarding workflows
- **Employment cost by country**, which is what turns a salary figure into a real budget line
- EOR versus own entity comparison, for a client hiring across borders

Feeds `offer-and-cost-pack`. Without it that skill falls back to a US formula and labels the total
estimated.

## Install

claude.ai → **Customize** → **Connect your tools** → search **Deel** → Connect → sign in → approve.

General questions work with **no login at all**; only account data needs authentication.
For Claude Code or another client: `https://api.letsdeel.com/mcp` over HTTP with OAuth.

## Links

- Directory listing: https://claude.ai/directory/connectors/deel
- Connector announcement: https://www.deel.com/blog/deel-mcp-claude/
- Client setup docs: https://developer.deel.com/mcp/connecting-clients
- Free HRIS tier: https://www.deel.com/blog/meet-the-new-deel/

## How widely used

Crossed **$1.5 billion ARR in the first half of 2026**, **40,000+ businesses**, roughly
**$22 billion in annual payroll processed**, across 150+ countries. $17.3 billion valuation on a
$300 million Series E.

One conflict on record: the tracker GetLatka lists 4,500 customers against Deel's own 40,000+.
A tenfold gap. Use Deel's figure and the August 2026 press coverage, not the tracker.

## What breaks without it

`offer-and-cost-pack` still runs on its own arithmetic, but every total is labelled estimated and
the country by country comparison is gone.
