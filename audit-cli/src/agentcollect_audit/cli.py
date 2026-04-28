"""click CLI — entry points for the agentcollect-audit command."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import click
from rich.console import Console
from rich.logging import RichHandler

from agentcollect_audit import __version__
from agentcollect_audit.config import settings, slugify
from agentcollect_audit.modules import generate as generate_mod
from agentcollect_audit.modules import hack as hack_mod
from agentcollect_audit.modules import scrape as scrape_mod
from agentcollect_audit.pipeline import SkipProspect, run_pipeline

console = Console()


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
    )


@click.group()
@click.version_option(__version__, prog_name="agentcollect-audit")
def cli() -> None:
    """AgentCollect Audit CLI — automated AR diagnostic reports for B2B prospects."""


@cli.command("run")
@click.argument("url")
@click.option("--dry-run", is_flag=True, help="Stub external API calls.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose logging.")
@click.option("--publish", is_flag=True, help="Push HTML to agentcollect.com after render.")
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Override output directory (default: ./output).",
)
def run(url: str, dry_run: bool, verbose: bool, publish: bool, output_dir: Path | None) -> None:
    """Run the full audit pipeline for a company URL."""
    _setup_logging(verbose)
    console.rule(f"[bold]agentcollect-audit {__version__} — {url}[/bold]")
    try:
        run_pipeline(url, dry_run=dry_run, publish_page=publish, output_dir=output_dir)
    except SkipProspect as e:
        console.print(f"[yellow]Skipped: {e}[/yellow]")
        raise SystemExit(2) from e


@cli.command("hack")
@click.argument("company_name")
@click.option("--phone", required=True, help="E.164 phone number to dial.")
@click.option("--persona", default="smb-phone", help="Persona slug (default: smb-phone).")
@click.option("--dry-run", is_flag=True)
@click.option("--verbose", "-v", is_flag=True)
def hack_cmd(
    company_name: str, phone: str, persona: str, dry_run: bool, verbose: bool
) -> None:
    """Run just the mystery shop module."""
    _setup_logging(verbose)
    result = hack_mod.mystery_shop(company_name, phone, persona, dry_run=dry_run)
    console.print_json(json.dumps(result, default=str))


@cli.command("scrape")
@click.argument("url")
@click.option("--dry-run", is_flag=True)
@click.option("--verbose", "-v", is_flag=True)
def scrape_cmd(url: str, dry_run: bool, verbose: bool) -> None:
    """Run just the portal scrape module."""
    _setup_logging(verbose)
    result = scrape_mod.scrape_portal(url, dry_run=dry_run)
    console.print_json(json.dumps(result, default=str))


@cli.command("generate")
@click.argument("report_data_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output",
    type=click.Path(path_type=Path),
    default=None,
    help="Output HTML path (default: next to report_data.json).",
)
@click.option("--verbose", "-v", is_flag=True)
def generate_cmd(report_data_path: Path, output: Path | None, verbose: bool) -> None:
    """Re-render the HTML page from a saved report_data.json."""
    _setup_logging(verbose)
    with open(report_data_path) as f:
        report_data = json.load(f)
    slug = report_data.get("slug") or slugify(report_data.get("url", "unknown"))
    out = output or (report_data_path.parent / f"audit-{slug}.html")
    generate_mod.render_report(report_data, out)
    console.print(f"[green]Wrote[/green] {out}")


if __name__ == "__main__":
    cli()
