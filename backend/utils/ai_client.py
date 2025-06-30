from __future__ import annotations

"""Thin wrapper around Google Gemini (Generative AI) SDK.

Usage example::
    from utils.ai_client import gemini_chat

    reply = gemini_chat([
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ])
    print(reply)

The module autoloads environment variables from a .env file (if present).
It will raise ``RuntimeError`` at import-time if *GEMINI_API_KEY* is not found.
"""

import os
from typing import List, Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai

# ---------------------------------------------------------------------------
# Environment & client configuration
# ---------------------------------------------------------------------------

# Load variables from .env file (if it exists) _before_ reading GEMINI_API_KEY.
load_dotenv()

_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not _GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Create a .env file or export it in your shell."
    )

# Configure the global client.
# `genai` handles authentication internally once this is done.
genai.configure(api_key=_GEMINI_API_KEY)

# Allow overriding the model via environment variable for flexibility. Default
# to the newer versioned model names. If that fails at runtime, the helper
# later tries a legacy fallback.
_DEFAULT_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.0-pro")

# Attempt to instantiate the model; if it is not found, fall back to the legacy
# name used in earlier SDK examples ("gemini-pro"). This keeps the code working
# across different SDK / API versions without forcing users to keep track.
try:
    _model = genai.GenerativeModel(_DEFAULT_MODEL_NAME)
except Exception as _e:  # pragma: no cover
    if "not found" in str(_e).lower() and _DEFAULT_MODEL_NAME != "gemini-pro":
        _model = genai.GenerativeModel("gemini-pro")
    else:
        raise

# ---------------------------------------------------------------------------
# Public helper functions
# ---------------------------------------------------------------------------

def _safe_generate(model, prompt, *, temperature: float = 0.7, **kwargs):
    """Helper that tries generation and falls back to legacy model names if needed."""
    try:
        return model.generate_content(prompt, generation_config={"temperature": temperature, **kwargs}).text
    except Exception as e:
        msg = str(e).lower()
        if "not found" in msg and model.model_name != "gemini-pro":
            legacy = genai.GenerativeModel("gemini-pro")
            return legacy.generate_content(prompt, generation_config={"temperature": temperature, **kwargs}).text
        raise


def gemini_chat(messages: List[Dict[str, str]], *, temperature: float = 0.7, **kwargs: Any) -> str:  # noqa: D401
    """Send a chat-style conversation to Gemini and return the text reply.

    ``messages`` must be a list of dicts with *role* ("system" | "user" | "model")
    and *content* keys, similar to OpenAI's Chat API.
    """
    # Gemini expects either plain strings or *content blocks*. We'll concatenate
    # messages into a single prompt. For richer multi-modal input you may switch
    # to the official chat format in the future.
    prompt_parts = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        prompt_parts.append(f"[{role.upper()}] {content}")

    prompt = "\n".join(prompt_parts)

    return _safe_generate(_model, prompt, temperature=temperature, **kwargs)


def gemini_generate(prompt: str, *, temperature: float = 0.7, **kwargs: Any) -> str:
    """Shortcut for single-prompt content generation."""
    return _safe_generate(_model, prompt, temperature=temperature, **kwargs)


# ---------------------------------------------------------------------------
# Module test (executed only when run directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":  # pragma: no cover
    print("Testing Gemini client…")
    reply = gemini_generate("Say hello to NYUAD Budgetly users in one sentence.")
    print("Gemini reply:", reply) 