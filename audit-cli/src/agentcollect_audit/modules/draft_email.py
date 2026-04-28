"""Draft the CEO cold email using the NEO-approved pattern.

Reference: ~/.claude/skills/neo/SKILL.md cold email patterns A/B.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader

from agentcollect_audit.config import settings

logger = logging.getLogger(__name__)


def draft_email(report_data: dict[str, Any], ceo_first_name: str = "") -> dict[str, Any]:
    """Draft the CEO email from the full report_data.

    Args:
        report_data: Output of the pipeline.
        ceo_first_name: Override first name. If empty, derived from research.ceo_name.

    Returns:
        Dict: subject, body, to_email, mailto_url.
    """
    research = report_data.get("research", {})
    if not ceo_first_name:
        ceo_first_name = (research.get("ceo_name") or "").split(" ")[0] or "there"

    slug = research.get("slug", "unknown")
    company = research.get("name", slug.title())
    killer = _killer_finding_one_liner(report_data)

    env = Environment(
        loader=FileSystemLoader(str(settings.templates_dir)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("email_v4.txt.j2")
    body = template.render(
        ceo_first_name=ceo_first_name,
        company_name=company,
        slug=slug,
        killer_finding_one_line=killer,
        audit_url=f"https://agentcollect.com/audit-{slug}",
    )

    subject = f"called {company} today"
    # We don't know the email yet — placeholder address
    to_email = f"{ceo_first_name.lower()}@{slug}.com"
    mailto_url = (
        f"mailto:{to_email}"
        f"?subject={quote(subject)}"
        f"&body={quote(body)}"
    )

    logger.info("draft_email: to=%s subject=%s", to_email, subject)
    return {
        "subject": subject,
        "body": body,
        "to_email": to_email,
        "mailto_url": mailto_url,
    }


def _killer_finding_one_liner(report_data: dict[str, Any]) -> str:
    """Pick the most damning single-sentence finding from hack + scrape."""
    hack = report_data.get("hack", {})
    quotes = hack.get("key_quotes", [])
    if quotes:
        return quotes[0].get("text", "your billing line transferred me three times")
    scrape = report_data.get("scrape", {})
    issues = scrape.get("ux_issues", [])
    if issues:
        return issues[0]
    return "your AR process has some rough edges that are costing you real money"
