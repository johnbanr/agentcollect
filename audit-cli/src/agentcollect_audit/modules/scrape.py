"""Portal scrape — uses Browserbase to screenshot and probe a company's billing portal.

v0 is a stub returning realistic shape data. Next agent: integrate Browserbase MCP.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def scrape_portal(url: str, dry_run: bool = False) -> dict[str, Any]:
    """Scrape a company's billing/customer portal.

    Args:
        url: Company homepage URL.
        dry_run: Skip any real HTTP and return stub.

    Returns:
        Dict: login_url, billing_url, screenshots, load_time_ms, https_valid,
        ux_issues, has_payment_interface.
    """
    parsed = urlparse(url if url.startswith("http") else f"https://{url}")
    base = f"{parsed.scheme}://{parsed.netloc}"
    logger.info("scrape: %s (dry_run=%s)", base, dry_run)

    # TODO: integrate Browserbase API — navigate, screenshot, measure load time,
    # detect login forms, detect payment interface via heuristics (iframe, stripe.js).
    return {
        "base_url": base,
        "login_url": f"{base}/login",
        "billing_url": f"{base}/billing",
        "screenshots": [
            {"filename": "homepage.png", "url": base, "viewport": "1440x900"},
            {"filename": "login.png", "url": f"{base}/login", "viewport": "1440x900"},
        ],
        "load_time_ms": 2400,
        "https_valid": parsed.scheme == "https",
        "ux_issues": [
            "Login page has no SSO option",
            "No 'pay invoice' CTA on homepage",
        ],
        "has_payment_interface": False,
        "_stub": True,
    }
