"""Tests for portal scrape stub."""

from agentcollect_audit.modules.scrape import scrape_portal


def test_scrape_shape():
    r = scrape_portal("https://ooma.com", dry_run=True)
    for key in (
        "login_url", "billing_url", "screenshots", "load_time_ms",
        "https_valid", "ux_issues", "has_payment_interface",
    ):
        assert key in r
    assert r["https_valid"] is True
    assert isinstance(r["screenshots"], list)
