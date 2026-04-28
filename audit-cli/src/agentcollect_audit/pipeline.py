"""Pipeline orchestrator — runs modules in order, saves snapshots after each step."""

from __future__ import annotations

import concurrent.futures
import json
import logging
from pathlib import Path
from typing import Any

from rich.console import Console

from agentcollect_audit.config import settings, slugify
from agentcollect_audit.modules import benchmark, draft_email, generate, hack, icp_score, publish, research, scrape

logger = logging.getLogger(__name__)
console = Console()


class SkipProspect(Exception):
    """Pipeline aborted because ICP score was too low."""


def run_pipeline(
    url: str,
    dry_run: bool = False,
    publish_page: bool = False,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Run the full audit pipeline end-to-end.

    Steps:
      1. research + icp_score (FAIL FAST if score too low)
      2. scrape + hack (parallel)
      3. benchmark
      4. generate (HTML)
      5. draft_email
      6. publish (optional)

    Args:
        url: Prospect company URL.
        dry_run: Stub all external API calls.
        publish_page: If True, push HTML to agentcollect.com.
        output_dir: Override the default output dir.

    Returns:
        Complete report_data dict.
    """
    slug = slugify(url)
    out = (output_dir or settings.output_dir) / slug
    out.mkdir(parents=True, exist_ok=True)

    report_data: dict[str, Any] = {"url": url, "slug": slug, "dry_run": dry_run}

    def snapshot(step: str) -> None:
        (out / "report_data.json").write_text(
            json.dumps(report_data, indent=2, default=str), encoding="utf-8"
        )
        logger.debug("snapshot after %s", step)

    # Step 1 — research + ICP (fail fast)
    console.print(f"[bold cyan][1/6][/bold cyan] Researching {url}...")
    report_data["research"] = research.research_company(url)
    snapshot("research")

    console.print("[bold cyan][1/6][/bold cyan] Scoring against ICP...")
    report_data["icp"] = icp_score.score_icp(report_data["research"])
    snapshot("icp")
    icp = report_data["icp"]
    if icp["recommendation"] == "skip":
        console.print(
            f"[bold red]SkipProspect[/bold red]: score={icp['score']}/{icp['max_score']} — "
            f"red_flags={icp['red_flags']}"
        )
        raise SkipProspect(f"ICP score {icp['score']} below threshold")
    console.print(
        f"  [green]PASS[/green] score={icp['score']}/{icp['max_score']} "
        f"signals={len(icp['signals_matched'])}"
    )

    # Steps 2+3 — scrape + hack (parallel)
    console.print("[bold cyan][2/6][/bold cyan] Scraping portal + mystery shop (parallel)...")
    company_name = report_data["research"].get("name", slug)
    persona = report_data["research"].get("vertical", "smb-phone")
    phone = "+18669396662"  # v0 placeholder; next agent pulls from research

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        scrape_future = ex.submit(scrape.scrape_portal, url, dry_run)
        hack_future = ex.submit(hack.mystery_shop, company_name, phone, persona, dry_run)
        report_data["scrape"] = scrape_future.result()
        report_data["hack"] = hack_future.result()
    snapshot("scrape+hack")

    # Step 4 — benchmarks
    console.print("[bold cyan][3/6][/bold cyan] Loading industry benchmarks...")
    report_data["benchmarks"] = benchmark.get_benchmarks(persona, "general")
    snapshot("benchmarks")

    # Step 5 — generate HTML
    console.print("[bold cyan][4/6][/bold cyan] Rendering McKinsey-style HTML...")
    html_path = out / f"audit-{slug}.html"
    generate.render_report(report_data, html_path)
    report_data["html_path"] = str(html_path)
    snapshot("generate")

    # Step 6 — draft email
    console.print("[bold cyan][5/6][/bold cyan] Drafting CEO email...")
    email = draft_email.draft_email(report_data)
    report_data["email"] = email
    (out / "email.txt").write_text(
        f"To: {email['to_email']}\nSubject: {email['subject']}\n\n{email['body']}",
        encoding="utf-8",
    )
    snapshot("email")

    # Step 7 — publish (optional)
    if publish_page:
        console.print("[bold cyan][6/6][/bold cyan] Publishing to agentcollect.com...")
        report_data["published_url"] = publish.publish_page(html_path, slug)
        snapshot("publish")
    else:
        console.print("[bold cyan][6/6][/bold cyan] Publish skipped (--publish not set)")

    console.print(f"\n[bold green]Done.[/bold green] Artifacts: {out}")
    return report_data
