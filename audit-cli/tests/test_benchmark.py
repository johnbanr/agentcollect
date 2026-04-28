"""Tests for benchmark lookup."""

from agentcollect_audit.modules.benchmark import get_benchmarks


def test_default_benchmarks_exist():
    rows = get_benchmarks("smb-phone", "general")
    assert isinstance(rows, list)
    assert len(rows) >= 1
    assert "stat" in rows[0]
    assert "source_url" in rows[0]


def test_unknown_vertical_falls_back():
    rows = get_benchmarks("nonexistent", "general")
    assert isinstance(rows, list)  # should at least return default
