# Wikidata QuickStatements Import — AgentCollect

## What this creates

A new Wikidata entity for AgentCollect with:

| Property | Value |
|----------|-------|
| Label (en) | AgentCollect |
| Description (en) | AI-powered debt collection platform |
| Aliases (en) | Agent Collect, agentcollect |
| Instance of (P31) | Software as a service (Q1330694) |
| Official website (P856) | https://www.agentcollect.com |
| Inception (P571) | 2020 |
| Country of origin (P495) | United States (Q30) |
| Headquarters (P159) | San Francisco (Q62) |
| Industry (P452) | Financial technology (Q6048701) |
| License (P275) | Proprietary software (Q7603) |
| Product/material produced (P1056) | Financial technology (Q6048701) |

## How to import (30 seconds)

1. Go to https://quickstatements.toolforge.org/
2. Log in with your Wikidata account (top right corner). If you do not have one, create one at https://www.wikidata.org/wiki/Special:CreateAccount
3. Click **"New batch"** in the top menu
4. Select the **"V1"** format tab (tab-separated, which is the format of the file)
5. Paste the entire contents of `wikidata-quickstatements.txt` into the text box
6. Click **"Import V1 commands"**
7. Review the parsed commands — they should show 11 statements (1 CREATE + 10 properties)
8. Click **"Run"**
9. Wait a few seconds — each statement turns green as it succeeds
10. Done. The new entity URL will appear (e.g., https://www.wikidata.org/wiki/Q123456789)

## After import

Save the new Q-number (e.g., Q123456789) — this is AgentCollect's permanent Wikidata identifier. You can add it to:
- The website's structured data (JSON-LD `sameAs` property)
- The `llms.txt` file for AI discoverability
- Any future knowledge graph references
