"""Tests for email drafting."""

from agentcollect_audit.modules.draft_email import draft_email


def test_draft_email_shape():
    report_data = {
        "research": {
            "slug": "ooma",
            "name": "Ooma Inc.",
            "ceo_name": "Eric Stang",
        },
        "hack": {
            "key_quotes": [
                {"text": "You'll have to call back tomorrow", "start_sec": 180, "end_sec": 183, "type": "gold"}
            ]
        },
        "scrape": {"ux_issues": []},
    }
    email = draft_email(report_data)
    assert "subject" in email
    assert "body" in email
    assert "to_email" in email
    assert "mailto_url" in email
    assert "Eric" in email["body"]
    assert "Ooma Inc." in email["body"]
    assert "call back tomorrow" in email["body"]
