"""Company research — pulls company metadata from web sources.

v0 returns stub data for known companies and a generic skeleton for unknown ones.
Next agent: wire up Serper API + homepage scrape + BBB lookup.
"""

from __future__ import annotations

import logging
from typing import Any

from agentcollect_audit.config import slugify

logger = logging.getLogger(__name__)

# Canned data for known prospects — lets the pipeline run end-to-end without API keys.
_KNOWN: dict[str, dict[str, Any]] = {
    "ooma": {
        "name": "Ooma Inc.",
        "revenue": "$256M ARR",
        "ceo_name": "Eric Stang",
        "ceo_title": "Chairman & CEO",
        "vertical": "smb-phone",
        "customer_count": "1.2M users",
        "bbb_url": "https://www.bbb.org/us/ca/sunnyvale/profile/voip-providers/ooma-inc",
        "hq_state": "CA",
        "employee_count": 700,
        "founded_year": 2004,
        "public_ticker": "OOMA",
    },
}


def research_company(url: str) -> dict[str, Any]:
    """Research a company given its URL.

    Args:
        url: Company homepage URL (e.g. 'https://ooma.com').

    Returns:
        Dict with keys: name, revenue, ceo_name, ceo_title, vertical, customer_count,
        bbb_url, hq_state, employee_count, founded_year.
    """
    slug = slugify(url)
    logger.info("research: %s (slug=%s)", url, slug)

    if slug in _KNOWN:
        data = dict(_KNOWN[slug])
        data["url"] = url
        data["slug"] = slug
        return data

    # TODO: integrate Serper API + homepage HTTP fetch + BBB scraper
    return {
        "url": url,
        "slug": slug,
        "name": slug.title(),
        "revenue": "unknown",
        "ceo_name": "unknown",
        "ceo_title": "CEO",
        "vertical": "unknown",
        "customer_count": "unknown",
        "bbb_url": "",
        "hq_state": "",
        "employee_count": 0,
        "founded_year": 0,
        "public_ticker": "",
    }
