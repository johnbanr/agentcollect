"""Tests for ICP scoring."""

from agentcollect_audit.modules.icp_score import score_icp


def test_scores_known_ooma_as_proceed():
    research = {
        "name": "Ooma Inc.",
        "revenue": "$256M ARR",
        "vertical": "smb-phone",
        "customer_count": "1.2M users",
        "bbb_url": "https://bbb.org/ooma",
        "employee_count": 700,
        "founded_year": 2004,
        "public_ticker": "OOMA",
    }
    result = score_icp(research)
    assert result["score"] >= 5
    assert result["passed_hard_gate"] is True
    assert result["recommendation"] in ("proceed", "proceed-lowconf")
    assert "max_score" in result
