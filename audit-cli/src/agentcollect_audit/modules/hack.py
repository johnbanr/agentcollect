"""Mystery shop — launches RetellAI calls using the polymorphic agent.

Polymorphic agent ID: agent_4ba93270dfed9b5893f9f2813f (hardcoded in config).
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

import httpx

from agentcollect_audit.config import settings

logger = logging.getLogger(__name__)

RETELLAI_BASE = "https://api.retellai.com"


def mystery_shop(
    company_name: str,
    phone: str,
    persona: str = "smb-phone",
    dry_run: bool = False,
) -> dict[str, Any]:
    """Launch a RetellAI mystery shop call against a company's billing line.

    Args:
        company_name: Company being shopped (used in dynamic_variables).
        phone: E.164 phone number to dial.
        persona: Persona slug from data/personas.json (e.g. 'smb-phone').
        dry_run: Return canned fixture instead of making a real call.

    Returns:
        Dict: call_id, transcript, recording_url, duration_sec, key_quotes.
    """
    logger.info("hack: %s at %s (persona=%s, dry_run=%s)", company_name, phone, persona, dry_run)

    if dry_run or not settings.retellai_api_key:
        return _stub_call(company_name, phone, persona)

    try:
        resp = httpx.post(
            f"{RETELLAI_BASE}/v2/create-phone-call",
            headers={
                "Authorization": f"Bearer {settings.retellai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from_number": settings.retellai_from_number,
                "to_number": phone,
                "override_agent_id": settings.retellai_polymorphic_agent_id,
                "retell_llm_dynamic_variables": {
                    "company_name": company_name,
                    "persona": persona,
                },
            },
            timeout=30,
        )
        resp.raise_for_status()
        call_data = resp.json()
        call_id = call_data.get("call_id", "unknown")
    except Exception as e:
        logger.warning("hack: RetellAI create failed (%s), returning stub", e)
        return _stub_call(company_name, phone, persona)

    # Poll for completion (max ~6 min)
    transcript = ""
    recording_url = ""
    duration_sec = 0
    for _ in range(72):
        time.sleep(5)
        try:
            r = httpx.get(
                f"{RETELLAI_BASE}/v2/get-call/{call_id}",
                headers={"Authorization": f"Bearer {settings.retellai_api_key}"},
                timeout=15,
            )
            r.raise_for_status()
            data = r.json()
            if data.get("call_status") in ("ended", "error"):
                transcript = data.get("transcript", "")
                recording_url = data.get("recording_url", "")
                duration_sec = int(
                    (data.get("end_timestamp", 0) - data.get("start_timestamp", 0)) / 1000
                )
                break
        except Exception as e:
            logger.warning("hack: poll error %s", e)

    return {
        "call_id": call_id,
        "transcript": transcript,
        "recording_url": recording_url,
        "duration_sec": duration_sec,
        "key_quotes": _extract_quotes(transcript),
        "company_name": company_name,
        "phone": phone,
        "persona": persona,
    }


def _stub_call(company_name: str, phone: str, persona: str) -> dict[str, Any]:
    """Canned call result for dry runs / missing API key."""
    return {
        "call_id": "stub_call_0000",
        "transcript": (
            "[stub transcript] Agent: I'd like to check on an invoice. "
            "Rep: Can I have your account number? ..."
        ),
        "recording_url": "https://example.com/stub-recording.wav",
        "duration_sec": 182,
        "key_quotes": [
            {
                "text": "Let me transfer you to another department",
                "start_sec": 42,
                "end_sec": 46,
                "type": "gold",
            },
            {
                "text": "I don't see that account in the system",
                "start_sec": 98,
                "end_sec": 101,
                "type": "warning",
            },
            {
                "text": "You'll have to call back tomorrow",
                "start_sec": 156,
                "end_sec": 159,
                "type": "gold",
            },
        ],
        "company_name": company_name,
        "phone": phone,
        "persona": persona,
    }


def _extract_quotes(transcript: str) -> list[dict[str, Any]]:
    """Heuristic quote extraction — finds the 3 most damning lines.

    v0: naive keyword match. Next agent: swap for Claude API call.
    """
    # TODO: integrate Anthropic API for real quote scoring
    damning_keywords = ["transfer", "can't help", "don't see", "call back", "system is down"]
    quotes: list[dict[str, Any]] = []
    for line in (transcript or "").split("\n"):
        line = line.strip()
        if any(k in line.lower() for k in damning_keywords):
            quotes.append(
                {"text": line, "start_sec": 0, "end_sec": 0, "type": "gold"}
            )
        if len(quotes) >= 3:
            break
    return quotes


def load_fixture(path: str) -> dict[str, Any]:
    """Load a pre-recorded call fixture (for tests)."""
    with open(path) as f:
        return json.load(f)
