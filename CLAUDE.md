# AgentCollect — Website Repo

## Brand Identity (MANDATORY — read BRAND.md before ANY visual work)
- **Brand guide:** `BRAND.md` (in this repo root)
- **Also at:** `/Users/jonathanbanner/github/frontend/logos/BRAND.md`
- **Assets:** `/Users/jonathanbanner/github/frontend/logos/`

### Quick Reference
- **Primary color:** `#433196` (deep purple, matches respaid.com CTA)
- **Accent:** `#10B981` (green, success states)
- **Text:** `#0B1B3D` (dark navy)
- **Background:** `#FAFBFF` (ghost white)
- **Font display/logo:** Plus Jakarta Sans 900
- **Font body:** Inter
- **Logo:** `AgentCollect.` — wordmark with purple dot. No separate icon in nav/headers.
- **Icon (square):** A + dot on purple `#433196` background (for favicon, app icon, LinkedIn profile pic)
- **Tagline:** "The end of manual collection."

## Web Browsing & Review — Tool Hierarchy (MANDATORY)

When reviewing, scraping, QA-ing, or interacting with ANY external web page:

| Task | Tool | Why |
|------|------|-----|
| **Web research / scraping / site review** | **Browserbase** (`mcp__browserbase__*`) | Cloud Chrome, anti-detection, shadow DOM support |
| **Visual QA of our own sites** | **Chrome MCP** or **Claude Preview** | Real browser, persistent session |
| **Local dev server preview** | **Claude Preview** (`mcp__Claude_Preview__*`) | Localhost only |

**NEVER use** local Playwright, `WebFetch`, `curl`, or `wget` for web page review — these don't render JS, can't screenshot, and have no anti-detection. Use **Browserbase** for any external web browsing task.

### Positioning
- Ends manual debt collection — replaces internal teams, BPOs, agencies with AI agents
- Buyer: CFO/CEO (mid-market) or VP AR (enterprise)
- AI agents work under the CLIENT's brand
- Key message: "Build YOUR collection machine" (powered by AgentCollect)

### Pages Structure
- `index.html` — Main landing page
- `about.html`, `careers.html`, `contact.html` — Company pages
- `privacy.html`, `terms.html` — Legal
- `v2/`, `v3/` — Older versions
- `compliance/` — Compliance pages
- Prospect pages: `konica-minolta.html`, etc.

### Deploy
- Static HTML on Vercel
- Push to main = auto-deploy

## Language
- Respond in the same language as the user (French if French)
- ALL code, commits, PRs in English
