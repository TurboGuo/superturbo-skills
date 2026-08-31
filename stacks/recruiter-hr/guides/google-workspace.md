# Google Workspace

**Tier: NECESSARY** — everyone in this role connects it
**Client cost: $0.** Free on a personal Google account. **$0 per user per month for verified
nonprofits, up to 2,000 users.**

## What it does in the hiring flow

This is the free ATS substitute, and it is why a client does not have to buy one.

- **Drive** holds the resume folder that `resume-screener` reads
- **Sheets** holds the pipeline tracker that `pipeline-health-report` reads
- **Calendar** holds the interview loop
- **Gmail** holds every candidate thread, and sends what `candidate-comms` drafts

## Install

claude.ai sidebar → **Customize** → **Connectors** → find Gmail, Google Calendar and Google Drive
→ **Connect** on each → sign in to Google → approve.
In a chat: **+** → **Connectors** → toggle each one on.

On Team and Enterprise plans an Owner must enable them at organization level first.

Three connectors, one row. The client experiences it as connecting Google once.

## Links

- Setup guide: https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
- Gmail connector page: https://claude.com/connectors/gmail
- Nonprofit $0 tier: https://www.google.com/nonprofits/workspace/compare/

## How widely used

Over 3 billion users and **more than 13 million paying customers**, per Google's own announcement,
April 2026. Alphabet's Q4 2025 earnings call gave 11 million in February 2026, so the figure moved
by 2 million in two months. Nothing on this list needs less explaining to a client.

## Open check

The Claude support article says these connectors are available to all users; the Google Drive docs
page says Drive is Pro, Max, Team and Enterprise. **Confirm which is true for the client's plan
before promising it is free.**

## What breaks without it

Everything that reads a file or sends a message. `resume-screener` falls back to pasted resumes,
`pipeline-health-report` falls back to an uploaded CSV, `candidate-comms` produces drafts the
client copies out by hand. The skills still run. The workflow gets manual.
