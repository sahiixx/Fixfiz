"""
Agency Engine — bridges the curated agency-agents persona library to the
live Ollama runtime so NOWHERE.ai agents are real LLM agents, not status
objects.

Design choice: a lightweight HTTP bridge to Ollama (/api/chat), NOT an
import of agency-agents' Python (langchain-ollama + deepagents). That
keeps the live backend's venv untouched (no new heavy deps) and avoids
coupling the running server to the agency-agents repo on disk. The
valuable IP — the persona system prompts — is copied into
backend/agency_personas/ so the backend is self-contained.

Honest degradation: if Ollama is unreachable or the model is missing,
run_agent returns a clear offline/error dict instead of raising, so the
backend never crashes on the agent engine's account.
"""
from __future__ import annotations

import asyncio
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp

logger = logging.getLogger(__name__)

_BACKEND_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> Dict[str, str]:
    """Minimal KEY=VALUE parser (no python-dotenv dependency). Ignores
    comments and blank lines, strips surrounding quotes. Used for
    .agency.env so the cloud creds never enter os.environ — config.py's
    pydantic Settings use extra=forbid and would crash on unknown
    AGENCY_OLLAMA_* keys if they leaked into the process environment."""
    out: Dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


_AGENCY_ENV = _load_env_file(_BACKEND_ROOT / ".agency.env")


def _cfg(name: str, fallback: str = "") -> str:
    """Precedence: .agency.env -> process env -> fallback."""
    return _AGENCY_ENV.get(name) or os.getenv(name) or fallback


# --- config: AGENCY_* preferred; fall back to OLLAMA_*/JARVIS_OLLAMA_MODEL so
#     the sahiixx-os Ollama Cloud env also works if exported into the process. ---
_OLLAMA_URL = (_cfg("AGENCY_OLLAMA_URL") or _cfg("OLLAMA_URL") or "http://localhost:11434").rstrip("/")
_DEFAULT_MODEL = _cfg("AGENCY_OLLAMA_MODEL") or _cfg("JARVIS_OLLAMA_MODEL") or "llama3.2:1b"
_API_KEY = _cfg("AGENCY_OLLAMA_API_KEY") or _cfg("OLLAMA_API_KEY") or ""
_TIMEOUT = float(_cfg("AGENCY_OLLAMA_TIMEOUT", "120") or "120")


def _auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_API_KEY}"} if _API_KEY else {}

# Personas live one level up from services/ -> backend/agency_personas/
_PERSONAS_DIR = Path(__file__).resolve().parent.parent / "agency_personas"

# Map the existing 5 operational agent slots to a primary persona, so the
# frontend agents page can associate each running agent with a real LLM
# persona. Keys are persona filenames (without .md).
SLOT_TO_PERSONA: Dict[str, str] = {
    "sales": "sales-outbound-strategist",
    "marketing": "marketing-social-media-strategist",
    "content": "marketing-content-creator",
    "analytics": "sales-pipeline-analyst",
    "ops": "marketing-growth-hacker",
}


def _parse_persona(path: Path) -> Optional[Dict[str, Any]]:
    """Parse a persona .md: YAML-ish frontmatter + body system prompt."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning("Could not read persona %s: %s", path, e)
        return None

    # Frontmatter is delimited by leading --- ... --- on its own lines.
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not m:
        # No frontmatter — treat whole file as the system prompt.
        return {
            "key": path.stem,
            "name": path.stem,
            "description": "",
            "color": "#8b5cf6",
            "emoji": "",
            "tools": "",
            "system_prompt": raw.strip(),
            "file": path.name,
        }

    frontmatter, body = m.group(1), m.group(2)
    meta: Dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip().lower()] = v.strip().strip('"').strip("'")

    return {
        "key": path.stem,
        "name": meta.get("name", path.stem),
        "description": meta.get("description", ""),
        "color": meta.get("color", "#8b5cf6"),
        "emoji": meta.get("emoji", ""),
        "tools": meta.get("tools", ""),
        "system_prompt": body.strip(),
        "file": path.name,
    }


def _load_all() -> Dict[str, Dict[str, Any]]:
    personas: Dict[str, Dict[str, Any]] = {}
    if not _PERSONAS_DIR.exists():
        logger.warning("Agency personas dir missing: %s", _PERSONAS_DIR)
        return personas
    for p in sorted(_PERSONAS_DIR.glob("*.md")):
        parsed = _parse_persona(p)
        if parsed:
            personas[parsed["key"]] = parsed
    return personas


_PERSONAS: Dict[str, Dict[str, Any]] = _load_all()


def list_roster() -> List[Dict[str, Any]]:
    """Public roster metadata (no system prompts) for the frontend."""
    out: List[Dict[str, Any]] = []
    for key, p in _PERSONAS.items():
        slot = next((s for s, pk in SLOT_TO_PERSONA.items() if pk == key), None)
        out.append({
            "key": key,
            "name": p["name"],
            "description": p["description"],
            "color": p["color"],
            "emoji": p["emoji"],
            "tools": p["tools"],
            "slot": slot,
        })
    return out


def get_persona(key: str) -> Optional[Dict[str, Any]]:
    return _PERSONAS.get(key)


def persona_for_slot(slot: str) -> Optional[Dict[str, Any]]:
    pk = SLOT_TO_PERSONA.get(slot)
    return _PERSONAS.get(pk) if pk else None


async def _ollama_chat(system_prompt: str, task: str, model: str) -> Dict[str, Any]:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ],
        "stream": False,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{_OLLAMA_URL}/api/chat",
            json=payload,
            headers=_auth_headers(),
            timeout=aiohttp.ClientTimeout(total=_TIMEOUT),
        ) as resp:
            data = await resp.json()
            if resp.status >= 400:
                return {"error": f"ollama status {resp.status}", "detail": str(data)[:500]}
            msg = (data.get("message") or {}).get("content", "")
            return {
                "response": msg.strip(),
                "model": data.get("model", model),
                "eval_count": data.get("eval_count"),
                "total_duration_ns": data.get("total_duration"),
            }


async def run_agent(agent_key: str, task: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Run a curated persona against the user task via Ollama.

    Returns a StandardResponse-friendly dict. Never raises — on any
    failure returns {"error": ...} so callers can surface it honestly.
    """
    persona = _PERSONAS.get(agent_key)
    if not persona:
        return {"error": f"Unknown agent '{agent_key}'", "available": list(_PERSONAS.keys())}
    if not task or not task.strip():
        return {"error": "A task prompt is required"}

    model = model or _DEFAULT_MODEL
    started = time.time()
    try:
        result = await asyncio.wait_for(_ollama_chat(persona["system_prompt"], task, model), timeout=_TIMEOUT)
    except asyncio.TimeoutError:
        return {"error": "agent engine timed out", "timeout_s": _TIMEOUT}
    except aiohttp.ClientConnectorError as e:
        return {"error": "agent engine offline — Ollama not reachable", "ollama_url": _OLLAMA_URL, "detail": str(e)[:200]}
    except Exception as e:
        logger.exception("agency_engine.run_agent failed")
        return {"error": f"agent run failed: {type(e).__name__}", "detail": str(e)[:300]}

    took_ms = int((time.time() - started) * 1000)
    if "error" in result:
        result["agent"] = agent_key
        result["name"] = persona["name"]
        result["took_ms"] = took_ms
        result["ollama_url"] = _OLLAMA_URL
        return result

    return {
        "agent": agent_key,
        "name": persona["name"],
        "model": result.get("model", model),
        "response": result.get("response", ""),
        "eval_count": result.get("eval_count"),
        "took_ms": took_ms,
        "ollama_url": _OLLAMA_URL,
    }


async def health() -> Dict[str, Any]:
    """Probe Ollama reachability + available models (for /api/agency/health)."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{_OLLAMA_URL}/api/tags", headers=_auth_headers(), timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                models = [m.get("name") for m in data.get("models", [])]
                return {
                    "reachable": True,
                    "ollama_url": _OLLAMA_URL,
                    "default_model": _DEFAULT_MODEL,
                    "cloud": bool(_API_KEY),
                    "models": models,
                    "persona_count": len(_PERSONAS),
                }
    except Exception as e:
        return {
            "reachable": False,
            "ollama_url": _OLLAMA_URL,
            "default_model": _DEFAULT_MODEL,
            "cloud": bool(_API_KEY),
            "error": str(e)[:200],
            "persona_count": len(_PERSONAS),
        }