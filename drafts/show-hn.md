# Show HN: AgentCollect -- AI agents that recover past-due invoices (~50% in 20 days)

We built AgentCollect because traditional collection agencies are broken. They assign 1 human to 250+ accounts. Most accounts get 2 emails and 1 call, then get ignored for months. The industry average is 20-30% recovery over 6 months.

**What it does:** 1 AI agent per unpaid invoice. Each agent calls, emails, resolves disputes, and negotiates payment plans autonomously.

**How it works:**
1. Upload a spreadsheet of past-due accounts
2. AI researches each debtor -- company financials, LinkedIn profiles, industry context, decision-maker identification
3. Contacts with the right tone and channel for each debtor (some need a firm attorney letter, others need a gentle payment plan)
4. Follows up persistently for up to 12 months -- no account gets forgotten

**Results:** ~50% recovery rate within 20 days. 0 compliance incidents across all accounts processed.

**Tech stack:** Laravel backend, RetellAI for voice calls, Claude for intelligence/research/decision-making. The voice agent handles real phone conversations -- negotiates payment plans, answers questions about the debt, handles disputes.

**Why this matters:** The collection industry hasn't changed in 30 years. Agencies charge 25-50% fees and recover less than a third of what they're given. We charge 5-15% and recover more, faster, because every single account gets dedicated attention from an AI agent that never forgets to follow up.

**Background:** YC S23. We've been running this in production for over a year with real clients and real money.

**Try it:** Go to https://agentcollect.com -- enter your company domain and see a branded AI agent for your business in 30 seconds. No signup required.

Happy to answer questions about the voice AI stack, compliance challenges, or how we handle edge cases like disputes and payment plans.

-- John Banner (j@respaid.com)
