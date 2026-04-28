"""Central config — loads env vars, defines defaults, exposes a Settings singleton."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DATA_DIR = PROJECT_ROOT / "data"


class Settings(BaseModel):
    """Runtime settings pulled from env vars with sensible defaults."""

    retellai_api_key: str = os.getenv("RETELLAI_API_KEY", "")
    retellai_polymorphic_agent_id: str = os.getenv(
        "RETELLAI_POLYMORPHIC_AGENT_ID", "agent_4ba93270dfed9b5893f9f2813f"
    )
    retellai_from_number: str = os.getenv("RETELLAI_FROM_NUMBER", "+18557700000")

    browserbase_api_key: str = os.getenv("BROWSERBASE_API_KEY", "")
    browserbase_project_id: str = os.getenv("BROWSERBASE_PROJECT_ID", "")

    serper_api_key: str = os.getenv("SERPER_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")

    output_dir: Path = Path(os.getenv("AUDIT_OUTPUT_DIR", "./output")).resolve()
    agentcollect_repo_path: Path = Path(
        os.getenv("AGENTCOLLECT_REPO_PATH", "/Users/jonathanbanner/github/agentcollect")
    )

    templates_dir: Path = TEMPLATES_DIR
    data_dir: Path = DATA_DIR


settings = Settings()


def slugify(url_or_name: str) -> str:
    """Turn 'https://ooma.com' or 'Ooma Inc' into 'ooma'."""
    s = url_or_name.lower().strip()
    for prefix in ("https://", "http://", "www."):
        if s.startswith(prefix):
            s = s[len(prefix):]
    s = s.split("/")[0]
    s = s.replace(".com", "").replace(".io", "").replace(".net", "").replace(".co", "")
    s = "".join(c if c.isalnum() else "-" for c in s).strip("-")
    while "--" in s:
        s = s.replace("--", "-")
    return s or "unknown"
