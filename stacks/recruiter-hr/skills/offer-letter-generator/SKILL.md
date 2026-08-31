---
name: offer-letter-generator
description: "Drafts professional, warm offer letters that make candidates feel excited to join while covering all legally necessary elements. Produces a formal PDF-ready version and an email version. Reduces back-and-forth with legal."
triggers:
  - offer letter
  - write offer
  - job offer
  - compensation offer
  - employment offer
  - offer package
---

## What it does

Transforms a compensation package into a polished offer letter that makes the candidate feel genuinely celebrated — not just processed. Many candidates read their offer letter as a preview of company culture. A warm, clear letter increases acceptance rates; a cold, legalistic one raises doubts.

Produces two ready-to-use versions:
1. **Formal letter** — PDF-ready, letterhead format, complete legal coverage
2. **Email version** — lighter tone, same key terms, ideal for initial send before formal letter follows

Includes a legal checklist so nothing is missed before it goes to the candidate.

> **Important**: Always have HR/legal review before sending. Requirements vary by state and country — particularly around at-will language, final pay, and non-compete enforceability.

## How to invoke

Provide the compensation details and candidate/role basics. The skill will draft both versions.

Examples:
- `/offer-letter-generator Engineering Manager, $175K base, 15% bonus, 50K RSUs, start April 7`
- `Write an offer letter for Sarah Chen, Senior Designer, $140K, fully remote, starts May 1`
- `I need an offer letter for a Sales Director — $200K base + commission, relocation package`

## Workflow

### Step 1 — Role and candidate basics
Collect:
- **Candidate full name** (as it will appear on the letter)
- **Job title** (exact title, matches what was posted)
- **Department / team**
- **Reports to** (hiring manager full name and title)
- **Start date** (or "to be mutually agreed")
- **Work location**: remote / hybrid (office address) / onsite (office address)
- **Employment type**: full-time / part-time
- **At-will statement**: standard in most US states (note: Montana is not at-will; consult legal for other jurisdictions)

### Step 2 — Compensation details
Be precise — the offer letter is a legal document:

**Base salary**:
- Annual amount (e.g., $175,000/year)
- Pay frequency (bi-weekly, semi-monthly)
- Overtime eligibility (exempt vs. non-exempt under FLSA)

**Bonus** (if applicable):
- Target percentage (e.g., 15% of base = $26,250)
- Metrics / triggers (company performance, individual performance, or purely discretionary)
- Payout timing (annually, semi-annually)
- Prorated for partial year? (specify)
- **Caution**: avoid language that "guarantees" the bonus — it should be contingent and discretionary unless intentionally otherwise

**Equity** (if applicable):
- Number of shares or options
- Equity type: RSUs / ISOs / NSOs
- Vesting schedule (e.g., 4 years, 1-year cliff)
- Grant date (usually board approval after start date — note this clearly)
- Strike price if options (may not be known at offer time)

**Sign-on bonus** (if applicable):
- Amount
- Clawback terms (typical: repay if departure within 12-24 months, prorated or full)

**Other comp**: car allowance, phone stipend, relocation package — itemize each.

### Step 3 — Benefits summary
Include highlights only — do not try to list every benefit (creates legal liability if details change):

- Medical/dental/vision: carrier name or just "comprehensive coverage," effective date (day 1 or first of month after start)
- 401(k): company match amount, vesting schedule for match
- PTO: total days, or "flexible/unlimited" policy description
- Parental leave: paid weeks if competitive/differentiating
- Other notable benefits: equity purchase plan, learning budget, remote work stipend

Add: "Full benefits details are provided in [benefits guide / onboarding materials]."

### Step 4 — Contingencies
List all offer contingencies clearly:

- **Background check**: standard language ("offer contingent on satisfactory completion")
- **Reference check**: if applicable
- **I-9 / work authorization verification**: required by law (Form I-9 within 3 business days of start)
- **Drug screening**: if applicable (note state laws vary — cannabis particularly complex)
- **Non-compete / NDA / IP assignment agreement**: note that signing these is a condition of employment (provide docs separately)
- **Education verification**: if role requires specific credentials

### Step 5 — Letter tone
Set the right emotional register:

- **Opening**: warm, celebratory — acknowledge the candidate specifically, express genuine excitement
- **Terms section**: clear and precise without being cold
- **Closing**: enthusiastic, forward-looking, invite questions

Avoid: overly corporate boilerplate, excessive legalese in the narrative sections (save precise language for the terms), anything that sounds like a form letter.

### Step 6 — Two versions

**Formal letter** (PDF-ready):
- Company letterhead placeholder [COMPANY LOGO]
- Date
- Candidate name and address
- Formal greeting
- Full terms, all sections
- Signature block: [Hiring Manager name/title] and [HR/People Ops name/title]
- Candidate acceptance signature line + date

**Email version**:
- Subject line: "[Candidate first name] — Your offer from [Company]"
- Shorter, warmer opening
- Key terms in a clear summary block (salary, title, start date, equity)
- Link or attachment reference for formal letter
- Clear CTA: "Please let us know by [deadline]" with both acceptance and decline paths

### Step 7 — Response deadline
- Standard: 3-5 business days (give candidates time; rushing creates bad impression)
- Exploding offers (24-48 hours) are widely considered poor practice — flag this if requested
- Include graceful decline path: "If this offer isn't the right fit, we completely understand — please let [recruiter name] know at [email]."

---

## Legal checklist (review before sending)

- [ ] At-will language present (if US)
- [ ] No implied contract language (e.g., avoid "permanent employment," "as long as you perform well")
- [ ] Bonus described as discretionary/contingent unless intentionally guaranteed
- [ ] Equity grant is described as subject to board approval
- [ ] Clawback terms for sign-on are clear
- [ ] I-9 verification requirement mentioned
- [ ] Non-compete/NDA/IP assignment listed as contingency if applicable
- [ ] State-specific requirements reviewed (CA, NY, IL, WA have notable differences)

---

## Live Data Sources

- **BLS OES Wage Percentiles by SOC Code** (bls.gov/oes) — 10th/25th/50th/75th/90th percentile wages by occupation and metro area. Use to validate that offer compensation is competitive and to flag offers below the 25th percentile for the role and geography.
- **State Minimum Wage Database** (dol.gov/agencies/whd/minimum-wage/state) — current minimum wage by state, including scheduled increases. Use to verify base salary and any hourly conversions meet state requirements before the letter is sent.

---

## Example output

**Input**: Engineering Manager offer — Sarah Chen, $175K base, 15% target bonus, 50K RSUs (4yr/1yr cliff), $10K sign-on (12-month clawback), 4 weeks PTO, remote, start April 14

**Formal letter opening excerpt**:
> March 21, 2026
>
> Sarah Chen
> [Address]
>
> Dear Sarah,
>
> On behalf of the entire team at [Company], I'm thrilled to offer you the position of Engineering Manager. From your first conversation with us, it was clear you bring exactly the combination of technical depth, people leadership, and product thinking we've been looking for — and we can't wait for you to join.
>
> Below you'll find the details of your offer. Please don't hesitate to reach out with any questions — we want you to feel completely informed and excited before you sign.

**Terms summary block**:
> - **Title**: Engineering Manager
> - **Start Date**: April 14, 2026
> - **Base Salary**: $175,000/year (paid bi-weekly)
> - **Annual Bonus**: Target 15% of base ($26,250), based on company and individual performance, paid annually
> - **Equity**: 50,000 RSUs, vesting over 4 years with a 1-year cliff, subject to board approval
> - **Sign-On Bonus**: $10,000, subject to 12-month repayment agreement
> - **PTO**: 4 weeks per year
> - **Location**: Remote

**Email version subject line**: "Sarah — Your offer from [Company] 🎉"

## Required closing line

Every result this skill produces ends with this exact line, on its own, after all
other content:

"This is AI generated and may not be fully accurate, verify it before you use."

For a Chinese language request, use: "本分析由 AI 生成，可能不完全准确，使用前请自行核实。"

This applies to drafts, excerpts and revisions alike. Never omit it, and never
reword it. Hiring documents carry legal weight and the reader must know a machine
wrote the draft.
