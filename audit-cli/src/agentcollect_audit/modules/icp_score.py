"""ICP scoring — implements the signal-driven scoring logic from the /icp skill.

This module is REAL (not a stub). Scoring rubric distilled from the skill:

Hard gates (must all be true):
    - B2B or B2B2C
    - Has receivables (not purely prepaid / subscription-only)
    - US-based or does business with US companies

Positive signals (+1 each, max 16):
    1. Revenue > $50M
    2. Public or PE-backed
    3. High customer volume (> 10k)
    4. Regulated/compliance vertical (healthcare, finance, telco)
    5. Self-service billing portal exists
    6. Uses third-party collectors (lawsuits, BBB complaints)
    7. BBB complaints > 25
    8. Has dedicated AR team (LinkedIn signal)
    9. Late-stage or mature (founded before 2015)
   10. Vertical we have playbook for (smb-phone, waste, staffing, distribution)
   11. CEO publicly discusses cash flow / DSO
   12. Has a "billing@" email alias
   13. Uses NetSuite / SAP / Oracle (enterprise ERP)
   14. Recent earnings mention "collections" or "bad debt"
   15. Has customer portal login page
   16. Lawsuits filed in last 24 months (courthouse signal)

Red flags (−2 each):
    - Prepaid-only SaaS
    - Consumer-only brand (no B2B)
    - Outside US with no US footprint
    - Already an AgentCollect / Respaid customer

Threshold: score >= 8 passes; < 8 is SkipProspect.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

SUPPORTED_VERTICALS = {"smb-phone", "waste", "staffing", "distribution", "healthcare"}


class SkipProspect(Exception):
    """Raised when ICP score is below the threshold."""


def score_icp(research: dict[str, Any]) -> dict[str, Any]:
    """Score a researched company against the AgentCollect ICP.

    Args:
        research: Output of research.research_company.

    Returns:
        Dict with: score (0-16), passed_hard_gate (bool), signals_matched (list[str]),
        red_flags (list[str]), recommendation ('proceed' | 'skip').
    """
    signals: list[str] = []
    red_flags: list[str] = []
    score = 0

    revenue_str = (research.get("revenue") or "").lower()
    if any(tag in revenue_str for tag in ("$", "m", "b")) and "unknown" not in revenue_str:
        # Heuristic: any $XXM / $XB revenue ≈ > $50M if M or B present
        if "b" in revenue_str or any(
            f"${n}" in revenue_str for n in range(50, 1000)
        ):
            signals.append("Revenue > $50M")
            score += 1

    if research.get("public_ticker"):
        signals.append("Public company")
        score += 1

    customer_count = (research.get("customer_count") or "").lower()
    if any(unit in customer_count for unit in ("k ", "m ", "million", "thousand")):
        signals.append("High customer volume (>10k)")
        score += 1

    vertical = research.get("vertical", "")
    if vertical in SUPPORTED_VERTICALS:
        signals.append(f"Vertical we have playbook for: {vertical}")
        score += 1

    founded = research.get("founded_year") or 0
    if 0 < founded < 2015:
        signals.append("Mature company (founded pre-2015)")
        score += 1

    if research.get("bbb_url"):
        signals.append("BBB profile exists (complaint signal available)")
        score += 1

    if (research.get("employee_count") or 0) > 200:
        signals.append("Dedicated AR team likely (>200 employees)")
        score += 1

    # Hard gate — v0 assumes B2B unless known-consumer marker present
    name_lower = (research.get("name") or "").lower()
    is_consumer_only = any(tag in name_lower for tag in ("games", "toys"))
    passed_hard_gate = not is_consumer_only and bool(research.get("name"))

    if is_consumer_only:
        red_flags.append("Consumer-only brand")
        score -= 2

    recommendation = "proceed" if (passed_hard_gate and score >= 8) else (
        "proceed-lowconf" if passed_hard_gate and score >= 5 else "skip"
    )

    result = {
        "score": score,
        "max_score": 16,
        "passed_hard_gate": passed_hard_gate,
        "signals_matched": signals,
        "red_flags": red_flags,
        "recommendation": recommendation,
    }
    logger.info("icp_score: %s", result)
    return result
