"""
Shared utilities for prompt engineering labs.

Provides a configured LLM client and helper functions for running
prompt experiments.  Supports multiple FREE providers out of the box:

  1. Google Gemini  (GOOGLE_API_KEY)  — recommended free tier
  2. Groq           (GROQ_API_KEY)    — free tier
  3. OpenAI         (OPENAI_API_KEY)  — paid
  4. Any OpenAI-compatible endpoint   (OPENAI_API_BASE + OPENAI_API_KEY)

The first available key wins (in the order above).
"""

from __future__ import annotations

import os
import textwrap

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ---------------------------------------------------------------------------
# Provider auto-detection
# ---------------------------------------------------------------------------
# Each entry: (env_var, base_url, default_model)
_PROVIDERS: list[tuple[str, str, str]] = [
    ("GOOGLE_API_KEY",  "https://generativelanguage.googleapis.com/v1beta/openai/", "gemini-2.0-flash"),
    ("GROQ_API_KEY",    "https://api.groq.com/openai/v1",                          "llama-3.1-8b-instant"),
    ("OPENAI_API_KEY",  "",                                                         "gpt-4o-mini"),
]


def _detect_provider() -> tuple[str, str, str]:
    """Return (api_key, base_url, default_model) for the first available provider."""
    for env_var, base_url, default_model in _PROVIDERS:
        key = os.getenv(env_var)
        if key:
            return key, base_url, default_model
    raise EnvironmentError(
        "No LLM API key found.  Set one of these environment variables:\n"
        "  • GOOGLE_API_KEY   — free at https://aistudio.google.com/apikey\n"
        "  • GROQ_API_KEY     — free at https://console.groq.com\n"
        "  • OPENAI_API_KEY   — https://platform.openai.com/api-keys\n"
    )


def _resolve_config() -> tuple[str, str, str]:
    """Resolve API key, base URL, and model from env with override support."""
    api_key, base_url, default_model = _detect_provider()
    # Allow explicit overrides
    base_url = os.getenv("OPENAI_API_BASE", base_url)
    model = os.getenv("LLM_MODEL", default_model)
    return api_key, base_url, model


_API_KEY, _BASE_URL, DEFAULT_MODEL = _resolve_config()


def get_client() -> OpenAI:
    """Return an OpenAI-compatible client configured from environment variables."""
    kwargs: dict = {"api_key": _API_KEY}
    if _BASE_URL:
        kwargs["base_url"] = _BASE_URL
    return OpenAI(**kwargs)


def complete(
    prompt: str,
    *,
    system: str = "",
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 1024,
    client: OpenAI | None = None,
) -> str:
    """Send a chat completion request and return the response text."""
    if client is None:
        client = get_client()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content or ""


def print_header(title: str) -> None:
    """Print a formatted lab header."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width + "\n")


def print_comparison_table(
    headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None
) -> None:
    """Print a simple ASCII comparison table."""
    if col_widths is None:
        col_widths = [max(len(str(row[i])) for row in [headers] + rows) + 2 for i in range(len(headers))]

    header_line = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"
    separator = "|-" + "-|-".join("-" * w for w in col_widths) + "-|"

    print(header_line)
    print(separator)
    for row in rows:
        print("| " + " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths)) + " |")
    print()
