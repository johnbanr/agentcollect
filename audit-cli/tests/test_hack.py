"""Tests for the mystery-shop hack module (stub mode)."""

from agentcollect_audit.modules.hack import load_fixture, mystery_shop


def test_stub_returns_full_shape():
    result = mystery_shop("Ooma", "+18669396662", "smb-phone", dry_run=True)
    for key in ("call_id", "transcript", "recording_url", "duration_sec", "key_quotes"):
        assert key in result
    assert isinstance(result["key_quotes"], list)
    assert len(result["key_quotes"]) >= 1


def test_fixture_loads(tmp_path):
    # sanity check: the shipped fixture parses
    import json
    from pathlib import Path
    fixture = Path(__file__).parent / "fixtures" / "ooma_call.json"
    data = load_fixture(str(fixture))
    assert data["call_id"].startswith("call_")
    assert len(data["key_quotes"]) == 3
