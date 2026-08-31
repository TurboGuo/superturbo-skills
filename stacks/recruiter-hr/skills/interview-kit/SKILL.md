---
name: interview-kit
description: "Generates a complete structured interview kit for any role — behavioral questions mapped to competencies, technical/skills questions, scoring rubrics, and a debrief guide. Ensures legal, consistent, bias-reduced interviews."
triggers:
  - interview questions
  - interview kit
  - interview guide
  - candidate interview
  - structured interview
  - behavioral questions
  - interview prep
---

## What it does

Builds a complete, ready-to-use interview kit that every interviewer can pick up without briefing. Structured interviewing (same questions, same rubric, for every candidate) is the single highest-impact change most hiring teams can make — it reduces bias, improves predictive validity, and protects against legal risk. This skill does the design work so your team doesn't have to.

Outputs: behavioral questions with STAR format + follow-up probes, technical/skills scenarios, a 1-4 scoring rubric with behavioral anchors, illegal question reference, and a debrief facilitation guide.

## How to invoke

Name the role and level, and optionally the competencies you want to assess.

Examples:
- `/interview-kit Senior Software Engineer, IC4`
- `Build me an interview guide for a Marketing Director`
- `I need interview questions for a mid-level Customer Success Manager focused on problem-solving and communication`

## Workflow

### Step 1 — Role and level
Establish scope:
- **Job title**: exact role
- **Seniority level**: use IC levels (IC1=entry, IC2=junior, IC3=mid, IC4=senior, IC5=staff/principal) or management levels (Manager, Director, VP)
- **3-5 core competencies** to assess — if not provided, suggest defaults based on role type:
  - ICs: technical depth, problem-solving, communication, collaboration, ownership/initiative
  - Managers: leadership, strategic thinking, communication, developing others, execution
  - Customer-facing: customer empathy, communication, resilience, problem-solving, process rigor

Ask: "Are there any competencies you've seen past hires struggle with that you want to specifically probe?"

### Step 2 — Interview structure
Map who assesses what across rounds:

For each round, define:
- Round name (e.g., "Recruiter Screen," "Hiring Manager," "Technical," "Panel," "Executive")
- Duration (30 / 45 / 60 min)
- Interviewers
- Competencies assessed in that round (avoid duplication)
- Format (behavioral only / technical + behavioral / case / presentation)

Output a clean interview plan table.

### Step 3 — Behavioral questions
For each competency, generate 2-3 STAR-format behavioral questions.

**Format for each question**:

> **Question**: "Tell me about a time you [specific scenario]."
>
> **What you're assessing**: [1-2 sentences on the underlying competency signal]
>
> **Strong answer indicators**:
> - Specific situation with clear stakes
> - Candidate owned the problem, not just contributed
> - Clear, measurable outcome described
> - Reflection or learning noted
>
> **Weak answer indicators**:
> - Vague or hypothetical ("I would usually...")
> - Only describes team accomplishment without personal role
> - No outcome or negative outcome without learning
>
> **Follow-up probes**:
> - "What would you do differently now?"
> - "How did others react?"
> - "What was the hardest part?"

### Step 4 — Technical / skills questions (if applicable)
For technical or specialized roles, generate 2-3 scenario-based assessments:

- Live coding / take-home / system design (specify format)
- What to look for at each level (IC3 vs. IC4 should see different depth)
- Time box recommendations
- What "good" looks like vs. "excellent" vs. "concerning"

For non-technical roles: substitute role-specific scenarios (e.g., case study for consulting, writing sample review for content roles, pipeline review for sales).

### Step 5 — Illegal questions to avoid
Quick-reference card for all interviewers. Clearly list what NOT to ask and why:

| Topic | Illegal / Risky to Ask | Legal Alternative |
|---|---|---|
| Marital/family status | "Do you have kids?" "Are you married?" | — (don't ask) |
| Pregnancy / parental plans | "Do you plan to have children?" | — (don't ask) |
| Age | "When did you graduate?" "How old are you?" | "Are you authorized to work in the US?" |
| Religion | "Do you go to church?" "What holidays do you observe?" | "This role sometimes requires weekend work — is that workable for you?" |
| National origin / citizenship | "Where are you from originally?" "Is that a foreign accent?" | "Are you authorized to work in the US?" |
| Disability | "Do you have any health conditions?" | "Can you perform the essential functions of this role with or without accommodation?" |
| Arrest record | "Have you ever been arrested?" | "Have you been convicted of [relevant offense]?" (check state law) |

Note: these vary by jurisdiction. Always consult HR/legal for local requirements.

### Step 6 — Scoring rubric
A 1-4 scale for each competency with behavioral anchors (not adjectives).

**Template**:

> **Competency: [Name]**
>
> | Score | Label | Behavioral Description |
> |---|---|---|
> | 4 | Exceptional | [Specific behaviors that distinguish outstanding performance at this level] |
> | 3 | Strong | [Solid demonstration of the competency; meets bar for this level] |
> | 2 | Mixed | [Some evidence but inconsistent; gaps that are noticeable at this level] |
> | 1 | Insufficient | [Little or no evidence; would be a concern at this level] |

Calibration note: Interviewers should complete scorecards independently before the debrief. A 3 from one interviewer and a 3 from another should reflect the same bar — calibrate on the first few uses.

### Step 7 — Debrief guide
Instructions for running the post-interview debrief:

**Before the debrief**:
- All scorecards submitted before meeting starts (no peeking at others' scores first)
- Debrief owner (usually hiring manager or recruiter) prepares candidate summary

**Debrief structure (45 min)**:
1. (5 min) Recruiter reads scorecard summary: average scores by competency, range
2. (5 min) Each interviewer shares one highlight and one concern — **no overall recommendation yet**
3. (20 min) Discussion by competency, starting with lowest-scored. Interviewer who assessed it speaks first.
4. (10 min) Calibration: is the bar being applied consistently? Any demographic patterns in feedback that warrant a pause?
5. (5 min) Decision: hire / no-hire / strong hire. Recruiter documents rationale.

**Groupthink prevention**:
- Most senior person speaks last, not first
- If one interviewer is very strong (positive or negative), ask: "What specific behavior led to that score?"
- If the team agrees too quickly (all 4s or all 1s), push back: "What's the weakest signal we saw today?"

**Documentation**: Every decision must be documented in the ATS with behavioral rationale. "Didn't seem like a culture fit" is not a documented reason. "Scored 1 on communication — gave vague answers to two structured questions with no specific examples" is.

---

## Live Data Sources

- **O*NET Competency Models API** (services.onetcenter.org) — structured competency frameworks by occupation and industry. Use to map role-appropriate behavioral competencies and calibrate question depth to seniority level.
- **SHRM Behavioral Interviewing Research** (shrm.org) — evidence-based STAR method guidance and structured interview best practices from the Society for Human Resource Management.

---

## Example output

**Input**: Senior Software Engineer, IC4 level, 5 competencies: technical depth, system design, collaboration, communication, ownership

**Interview plan**:
| Round | Duration | Interviewers | Competencies |
|---|---|---|---|
| Recruiter Screen | 30 min | Recruiter | Motivation, logistics, comp alignment |
| Hiring Manager | 45 min | HM | Ownership, communication |
| Technical | 60 min | 2 ICs | Technical depth (live coding) |
| System Design | 60 min | Staff Eng | System design |
| Panel | 45 min | PM + EM | Collaboration, communication |

**Sample behavioral question** (Ownership competency):
> "Tell me about a time you took on a problem that was technically outside your scope because you could see it was going to block your team."
>
> **Strong indicators**: proactively identified the risk, communicated the tradeoff clearly, delivered a solution while managing their core work, team unblocked as a result.
>
> **Follow-up**: "How did you decide this was your problem to solve vs. escalating it?"

**Scoring rubric excerpt** (System Design, IC4):
| Score | Description |
|---|---|
| 4 | Designs scalable systems unprompted, considers failure modes, trade-offs between consistency/availability, data modeling depth; could present this to an engineering all-hands |
| 3 | Solid high-level design with reasonable component choices; identifies 1-2 trade-offs when prompted; appropriate for IC4 expectations |
| 2 | Gets the basic structure right but misses key considerations (e.g., doesn't think about scale, ignores error handling); would need mentorship at IC4 |
| 1 | Struggles with component decomposition; unclear on how services communicate; not ready for IC4 scope |

## Required closing line

Every result this skill produces ends with this exact line, on its own, after all
other content:

"This is AI generated and may not be fully accurate, verify it before you use."

For a Chinese language request, use: "本分析由 AI 生成，可能不完全准确，使用前请自行核实。"

This applies to drafts, excerpts and revisions alike. Never omit it, and never
reword it. Hiring documents carry legal weight and the reader must know a machine
wrote the draft.
