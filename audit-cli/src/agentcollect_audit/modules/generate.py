"""Generate — render the McKinsey-style diagnostic HTML from report_data via Jinja2."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from agentcollect_audit.config import settings

logger = logging.getLogger(__name__)


def render_report(report_data: dict[str, Any], output_path: Path) -> Path:
    """Render the audit HTML and write it to output_path.

    Args:
        report_data: Merged dict from the pipeline (research + icp + hack + scrape + benchmarks).
        output_path: Destination .html file.

    Returns:
        The path written.
    """
    env = Environment(
        loader=FileSystemLoader(str(settings.templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("audit_v4.html.j2")
    html = template.render(**report_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    logger.info("generate: wrote %s (%d bytes)", output_path, len(html))
    return output_path
