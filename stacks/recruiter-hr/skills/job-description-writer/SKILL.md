---
name: job-description-writer
description: "Writes inclusive, compelling job descriptions that attract strong candidates and reduce bias. Produces two versions: a full ATS version (500-700 words) and a punchy LinkedIn/job-board version (250 words), plus outreach subject lines."
triggers:
  - job description
  - write JD
  - job posting
  - job listing
  - open role
  - job ad
  - hiring for
---

## What it does

Transforms role requirements into polished, bias-checked job descriptions. Separates true must-haves from inflated wish lists (requirement inflation drives away qualified candidates, especially women and underrepresented groups). Outputs two ready-to-use versions — one optimized for ATS systems and one for social/job boards — plus three outreach subject lines for passive candidate sourcing.

## How to invoke

Describe the role you're hiring for and any details you have. The skill will ask clarifying questions if needed, then produce both versions.

Examples:
- `/job-description-writer Senior Product Manager, fintech, remote, $160-200K`
- `Write a job description for a Staff Engineer on our platform team`
- `I need a job posting for a Customer Success Manager, hybrid NYC, $80-100K`

## Workflow

### Step 1 — Role basics
Gather foundational information:
- Job title (exact title that will appear on posting)
- Team name and function
- Reporting structure (reports to whom)
- Location: remote / hybrid (days in office) / onsite + city
- Salary range (strongly recommended — postings with ranges get significantly more applicants)
- Full-time or part-time
- Employment type (FTE, contract-to-hire, contract)

If any of these are missing, ask before proceeding.

### Step 2 — Must-haves vs. nice-to-haves
Work with the hiring manager to separate true requirements from a wish list:

**Questions to ask:**
- "What would make a candidate unqualified on day 1?"
- "What skills can be learned on the job in 3-6 months?"
- "Have your best past hires for this role had X? Or did they succeed without it?"

**Common inflation patterns to challenge:**
- Degree requirements when the actual work doesn't require them
- "X years of experience" when outcomes matter more than tenure
- Tool-specific requirements when adjacent tools transfer
- "Fast-paced startup experience" when the real need is adaptability

Output: a clean list of Required (3-5 items) and Preferred (2-3 items).

### Step 3 — Bias check
Scan all language for:

- **Gendered coding**: ninja, rockstar, guru, aggressive, dominant, crushing it, killer instinct → replace with specific, outcome-focused language
- **Age-coded language**: recent grad, digital native, energetic → remove
- **Unnecessary degree requirements**: flag and suggest alternatives ("or equivalent experience")
- **Culture-fit vagueness**: "fits our vibe," "like a family" → replace with specific culture descriptors
- **Overloaded bullet lists**: >7 responsibilities signals scope creep; help trim

### Step 4 — ATS version (500-700 words)

Full job description formatted for applicant tracking systems:

**About the Role** (2-3 sentences)
What the role does, why it matters to the company, where it fits in the org.

**What You'll Do** (5-7 bullets)
Frame as outcomes, not tasks. Bad: "Attend sprint planning." Good: "Own the product roadmap for X, ensuring quarterly priorities align with company OKRs."

**What You Bring**
- Required: 3-5 bullets (true must-haves only)
- Preferred: 2-3 bullets (nice-to-haves, framed positively)

**What We Offer**
- Compensation range (salary + bonus if applicable)
- Equity if offered
- Key benefits highlights (health, PTO, 401k match)
- 1-2 culture highlights (specific, not clichéd)

**Inclusive Hiring Statement**
A genuine, specific statement — not boilerplate. Example: "We encourage applications from people of all backgrounds. If you're excited about this role but don't meet every requirement, apply anyway — we hire for potential and growth."

### Step 5 — LinkedIn version (250 words)

Same structure, compressed for attention-limited scrollers:
- Hook opening line that speaks to candidate motivation
- 3-4 punchy responsibility bullets
- 3 must-have qualifications
- Salary range
- Link/CTA

Tone: warmer, more personality, less formal than ATS version.

### Step 6 — Outreach subject lines

Three options for reaching out to passive candidates:
- **Curiosity-driven**: sparks interest without revealing everything
- **Flattery/relevance**: references something specific about the candidate's background
- **Direct/transparent**: straightforward about the role and comp

---

## Live Data Sources

- **O*NET Web Services API** (services.onetcenter.org) — occupational requirements, tasks, skills, knowledge, and abilities by SOC code. Use to validate must-have requirements and suggest role-appropriate competency language.
- **BLS Occupational Employment and Wage Statistics (OES)** (bls.gov/oes) — median and percentile wages by occupation and geographic area. Use to benchmark salary ranges and flag postings where the stated range is significantly below market.

---

## Example output

**Input**: Senior Product Manager, fintech startup, remote-first, $160-200K base, equity

**ATS Version** (excerpt):
> **About the Role**
> We're looking for a Senior Product Manager to own our payments infrastructure product — the system that processes $2B in annual volume for 40,000 merchants. You'll report to the VP of Product and work closely with Engineering, Risk, and our largest enterprise customers to ship features that directly drive revenue retention.
>
> **What You'll Do**
> - Define and own the 12-month roadmap for payments infrastructure, balancing merchant needs against regulatory requirements
> - Partner with Engineering to reduce time-to-market for payment method integrations from 6 weeks to 2
> - Synthesize qualitative customer feedback and quantitative usage data into prioritized product bets
> - Lead cross-functional reviews with Risk and Compliance to ensure new features meet PCI-DSS standards
> - Define success metrics for every launch and report outcomes to leadership quarterly

**LinkedIn Version** (excerpt):
> Tired of shipping features that don't move the needle? We're hiring a Senior PM to own the payments product at [Company] — the infrastructure behind $2B in merchant transactions. Remote-first, $160-200K + equity.
> You'll have real ownership, a clear mandate, and a team that actually ships...

**Outreach subject lines**:
1. "Your payments background + a $2B infrastructure problem"
2. "Saw your work at [Previous Company] — think you'd find this interesting"
3. "Senior PM role, remote, $160-200K — worth 15 minutes?"

## Required closing line

Every result this skill produces ends with this exact line, on its own, after all
other content:

"This is AI generated and may not be fully accurate, verify it before you use."

For a Chinese language request, use: "本分析由 AI 生成，可能不完全准确，使用前请自行核实。"

This applies to drafts, excerpts and revisions alike. Never omit it, and never
reword it. Hiring documents carry legal weight and the reader must know a machine
wrote the draft.
