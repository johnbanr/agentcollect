"""Tests for research module."""

from agentcollect_audit.modules.research import research_company


def test_known_company_returns_full_shape():
    data = research_company("https://ooma.com")
    for key in (
        "name", "revenue", "ceo_name", "ceo_title", "vertical",
        "customer_count", "bbb_url", "hq_state", "employee_count", "founded_year",
    ):
        assert key in data, f"missing key: {key}"
    assert data["slug"] == "ooma"
    assert data["name"] == "Ooma Inc."


def test_unknown_company_returns_skeleton():
    data = research_company("https://totally-unknown-example-biz.com")
    assert data["slug"] == "totally-unknown-example-biz"
    assert data["name"]  # non-empty
    assert "vertical" in data
