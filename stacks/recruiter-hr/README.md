# Toolfit: Recruiter / HR

Three skills for the person who owns hiring without owning an HR department, plus the
two connectors that stack actually needs.

## Skills

| Skill | Use it for |
|---|---|
| `/toolfit-recruiter-hr:job-description-writer` | An ATS version and a job board version of the same role, plus outreach subject lines |
| `/toolfit-recruiter-hr:interview-kit` | Behavioural and technical questions mapped to competencies, a scoring rubric, a debrief guide |
| `/toolfit-recruiter-hr:offer-letter-generator` | A formal offer letter and its email version, with the legally necessary elements covered |

You can also just describe the task. Each skill triggers on its own description.

## Connectors carried by this stack

These arrive with the install. Each asks you to sign in the first time it is used.

| Connector | Endpoint | What it is for | Cost |
|---|---|---|---|
| Deel | `https://api.letsdeel.com/mcp` | Employee records, PTO, org chart, onboarding | Free under 200 employees |
| Calendly | `https://mcp.calendly.com` | Interview scheduling, and nothing else | Free forever, 1 event type |

## Connectors you switch on yourself

A plugin cannot carry these. Turn them on in **Customize > Connectors**. Setup notes are
in [`guides/`](./guides).

| Connector | Why it is separate |
|---|---|
| Google Workspace | Managed by Anthropic, no public MCP endpoint to point at. Resumes in Drive, pipeline tracker in Sheets |
| ZipRecruiter | No public MCP endpoint. What comparable roles pay in your market |

## Honest install promise

One install. The three skills work immediately. Deel and Calendly need one sign in each.
Google Workspace and ZipRecruiter you switch on yourself, once.

## Grant the minimum

When a connector asks for access, give it the smallest scope that lets you run one real
test: one folder, one calendar, one workspace. Widen it later if you need to.

## Licence

MIT. See `LICENSE` and `NOTICE.md` beside each skill for attribution.
