"""Publish — push the generated page to agentcollect.com via git.

v0 is a stub. Next agent: git add/commit/push + poll Vercel for deploy URL.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def publish_page(html_path: Path, slug: str) -> str:
    """Publish an audit HTML page to agentcollect.com.

    Args:
        html_path: Local path to the rendered HTML file.
        slug: Page slug (e.g. 'ooma' → agentcollect.com/audit-ooma).

    Returns:
        Vercel preview URL (or placeholder in v0).
    """
    logger.info("publish: would push %s to agentcollect.com/audit-%s", html_path, slug)
    # TODO: copy html_path into settings.agentcollect_repo_path, git add/commit/push,
    # then poll Vercel API for the latest deployment URL.
    return f"https://agentcollect.com/audit-{slug}"
