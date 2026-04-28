"""End-to-end dry-run test of the pipeline."""

from pathlib import Path

from agentcollect_audit.pipeline import run_pipeline


def test_full_pipeline_dry_run(tmp_path: Path):
    result = run_pipeline("https://ooma.com", dry_run=True, output_dir=tmp_path)
    assert result["slug"] == "ooma"
    assert "research" in result
    assert "icp" in result
    assert "hack" in result
    assert "scrape" in result
    assert "benchmarks" in result
    assert "html_path" in result
    assert "email" in result
    # HTML written
    html_path = Path(result["html_path"])
    assert html_path.exists()
    assert "Ooma" in html_path.read_text()
    # Snapshot written
    assert (tmp_path / "ooma" / "report_data.json").exists()
    assert (tmp_path / "ooma" / "email.txt").exists()
