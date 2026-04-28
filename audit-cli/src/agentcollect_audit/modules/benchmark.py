"""Benchmarks — looks up industry stats from a curated JSON database."""

from __future__ import annotations

import json
import logging
from typing import Any

from agentcollect_audit.config import settings

logger = logging.getLogger(__name__)


def get_benchmarks(vertical: str, finding_type: str = "general") -> list[dict[str, Any]]:
    """Return benchmarks for a vertical + finding type.

    Args:
        vertical: e.g. 'smb-phone', 'waste', 'staffing'.
        finding_type: e.g. 'dso', 'transfer-rate', 'call-abandonment'.

    Returns:
        List of {stat, source, source_url, year}.
    """
    logger.info("benchmark: vertical=%s finding_type=%s", vertical, finding_type)
    path = settings.data_dir / "benchmarks.json"
    if not path.exists():
        return []
    with open(path) as f:
        db = json.load(f)
    key = f"{vertical}:{finding_type}"
    return db.get(key, db.get(f"{vertical}:general", db.get("default", [])))
