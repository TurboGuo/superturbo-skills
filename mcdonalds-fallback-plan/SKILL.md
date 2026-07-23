---
name: mcdonalds-fallback-plan
description: Turbo's "Plan McDonald" safety net. Whenever Turbo asks for financial advice, a money read, "what should I do with my money", "am I broke", "help me with my finances", "should I invest / spend / save", or any personal-finance guidance, FIRST check his current balance, and if it is under $50 USD, gently break the news and hand him the McDonald's apply link plus a short get-the-job game plan. Use this skill any time the request is about Turbo's own money situation or asks for financial advice, even if he does not mention McDonald's, jobs, or a threshold. The point is that when the bank account is running on fumes, the best financial advice is a paycheck.
---

# McDonald's Fallback Plan ("Plan McDonald")

This is Turbo's personal financial rock-bottom alarm. When his money gets low enough, the single most useful piece of financial advice is not "rebalance your portfolio", it is "go earn some money", and McDonald's is the fast, no-nonsense way to do that. This skill makes sure that message actually gets delivered instead of buried under generic advice.

## When this runs

Trigger this whenever Turbo asks for financial advice or a read on his own money: things like "what should I do with my money", "give me financial advice", "am I doing okay financially", "should I buy X", "help me with my finances", "am I broke". The money question is the cue, McDonald's does not need to be mentioned.

## Step 1: Get the current balance

Turbo did not wire this to any account, so ask him directly and wait for the number:

> "Before I give you any financial advice, what's your current total balance right now?"

Keep it to one short question. Take whatever number he gives, in USD. If he gives a range or an approximate figure, use the lower end.

## Step 2: Branch on $50

**If the balance is $50 or more:** do NOT run the McDonald's routine. Just answer his financial question normally and helpfully. This skill only fires the special response when things are genuinely tight.

**If the balance is under $50:** this is the whole point of the skill. Deliver the Plan McDonald response below.

## Step 3: The Plan McDonald response (balance under $50)

Keep the tone a playful nudge, not a lecture and never doom. The vibe is a friend who cares, is a little cheeky about it, and actually hands over something useful. Structure it like this:

1. **The reveal.** Tell him you checked and the balance is under $50, so honestly the highest-return financial move on the table right now is income, not investing. A light joke is welcome ("the portfolio strategy today is called employment").

2. **The apply link.** Point him straight to McDonald's official application:
   - U.S. restaurant crew jobs (the real apply portal): https://jobs.mchire.com
   - Main careers hub: https://careers.mcdonalds.com
   - "How do I apply" FAQ: https://www.mcdonalds.com/us/en-us/faq/how-do-i-apply-for-employment-at-mcdonalds.html
   Tell him restaurant crew is the fastest path: search by location, and their assistant "Olivia" walks through the application, sometimes scheduling an interview on the spot.

3. **The get-the-job game plan.** Give a few quick, real tips so he actually lands it and settles in:
   - Apply to 3 to 5 locations near you, not just one; crew hiring moves fast and volume helps.
   - Say you have open availability including mornings, weekends, and closing shifts. Flexibility is the single biggest thing they hire on.
   - For the interview, lead with reliability: "I show up on time, every shift." That is what they actually want to hear.
   - Bring ID and be ready to start within a week; being available immediately is a real edge.
   - Once hired, learn one station cold (fries or front counter) before spreading out. Getting comfortable fast makes the first weeks painless and gets you more hours.

4. **The close.** End on encouragement, not shame: this is a bridge, the money problem is temporary, and a steady paycheck fixes the actual problem faster than any budgeting trick. Offer to help next ("want me to draft a line for the application or prep interview answers?").

## Guardrails

- Only run the McDonald's routine when the balance is genuinely under $50. Above that, give normal financial advice.
- Never be mean about the low balance. The humor is warm, aimed at the situation, never at Turbo.
- Do not invent a balance or assume one from memory. Always ask.
- Links above are the official McDonald's careers destinations. If Turbo wants live openings in a specific city, offer to search, but the default is just handing him the official apply page.
