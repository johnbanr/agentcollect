# agentcollect-audit

**Automated AR diagnostic reports for B2B prospects.** A Python CLI that runs the full AgentCollect audit pipeline from a single command.

```bash
agentcollect-audit run https://ooma.com
```

Out comes: a McKinsey-style diagnostic HTML page, mystery-shop call recordings with timestamped damning quotes, a CEO email draft, and a `report_data.json` snapshot ready to publish.

## Why this exists

JB has been running the AgentCollect audit playbook manually via Claude Code skills (`/icp`, `/hack`, `/neo`). It works but it's fragile — directives get forgotten between sessions, quotes are transcribed inconsistently, the HTML template drifts, and every new prospect costs 2-3 hours of human orchestration. The CLI encodes the entire playbook as code, so the next audit is one command away from a publishable page.

The CLI is the **automation layer**. The skills are the **source of truth**. When a skill evolves, we port the directive into the CLI modules here.

## Install

```bash
cd /Users/jonathanbanner/github/agentcollect/audit-cli
pip install -e .
cp .env.example .env
# Fill in RETELLAI_API_KEY, BROWSERBASE_API_KEY, etc.
```

## Usage

```bash
# Full pipeline (research → ICP → scrape + hack in parallel → benchmark → generate → draft email)
agentcollect-audit run https://ooma.com

# Dry run (no API calls, stubs only)
agentcollect-audit run https://ooma.com --dry-run --verbose

# Just the mystery shop
agentcollect-audit hack "Ooma" --phone "+18669396662" --persona smb-phone

# Just the portal scrape
agentcollect-audit scrape https://ooma.com

# Re-generate HTML from an existing report_data.json
agentcollect-audit generate ./output/ooma/report_data.json
```

All artifacts land in `./output/{slug}/`:

```
output/ooma/
├── report_data.json    # full pipeline snapshot
├── audit-ooma.html     # final McKinsey-style page
├── email.txt           # CEO cold email draft
├── screenshots/        # portal screenshots from Browserbase
└── recordings/         # RetellAI call recordings
```

## Architecture

```
 ┌─────────┐
 │  CLI    │  click commands: run / hack / scrape / generate
 └────┬────┘
      │
 ┌────▼──────┐
 │ pipeline  │  orchestrates, saves report_data.json after each step
 └─┬─┬─┬─┬─┬─┘
   │ │ │ │ │
   │ │ │ │ └──> draft_email  (jinja → email.txt + mailto)
   │ │ │ └────> generate     (jinja → audit-{slug}.html)
   │ │ └──────> benchmark    (vertical lookup → benchmarks.json)
   │ └────────> hack         (RetellAI call → transcript + quotes)
   │            scrape       (Browserbase → portal screenshots)
   └──────────> research → icp_score (FAIL FAST if score < 8)
```

## v0 scope

The scaffolding is done; most modules return realistic stub data so the pipeline runs end-to-end. Next agent integrates the actual APIs. Search the code for `# TODO` to find the 5 integration points.

## License

Proprietary — AgentCollect / Respaid.
