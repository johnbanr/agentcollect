"""Tests for HTML generation."""

from pathlib import Path

from agentcollect_audit.modules.generate import render_report


def test_render_produces_html(tmp_path):
    report_data = {
        "url": "https://ooma.com",
        "slug": "ooma",
        "version": "0.1.0",
        "research": {
            "name": "Ooma Inc.",
            "url": "https://ooma.com",
            "ceo_name": "Eric Stang",
            "ceo_title": "CEO",
            "vertical": "smb-phone",
            "revenue": "$256M",
            "customer_count": "1.2M users",
            "hq_state": "CA",
        },
        "icp": {"score": 9, "max_score": 16, "signals_matched": [], "red_flags": []},
        "hack": {
            "call_id": "stub",
            "recording_url": "https://example.com/x.wav",
            "duration_sec": 180,
            "persona": "smb-phone",
            "key_quotes": [
                {"text": "transfer you", "start_sec": 10, "end_sec": 12, "type": "gold"}
            ],
        },
        "scrape": {
            "base_url": "https://ooma.com",
            "load_time_ms": 2400,
            "https_valid": True,
            "ux_issues": ["No pay CTA"],
            "has_payment_interface": False,
        },
        "benchmarks": [
            {"stat": "DSO is 44 days", "source": "Atradius", "source_url": "https://x", "year": 2024}
        ],
    }
    out = tmp_path / "audit-ooma.html"
    render_report(report_data, out)
    assert out.exists()
    html = out.read_text()
    assert "Ooma Inc." in html
    assert "transfer you" in html
    assert "DSO is 44 days" in html
