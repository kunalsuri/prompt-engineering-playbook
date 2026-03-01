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

import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any

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

DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 2


@dataclass
class _MockFunction:
    name: str
    arguments: str


@dataclass
class _MockToolCall:
    function: _MockFunction


@dataclass
class _MockMessage:
    content: str | None = None
    tool_calls: list[_MockToolCall] | None = None


@dataclass
class _MockChoice:
    message: _MockMessage


@dataclass
class _MockResponse:
    choices: list[_MockChoice]


def _extract_product_data(text: str) -> dict[str, Any]:
    name = text.split(".")[0].strip()
    price_match = re.search(r"\$\s*([0-9]+(?:\.[0-9]+)?)", text)
    price_usd = float(price_match.group(1)) if price_match else 0.0

    lowered = text.lower()
    if any(word in lowered for word in ["iphone", "headphones", "kindle"]):
        category = "Electronics"
    elif any(word in lowered for word in ["lego", "toy"]):
        category = "Toys"
    elif any(word in lowered for word in ["book", "paperback"]):
        category = "Books"
    elif any(word in lowered for word in ["vacuum", "appliance", "dyson"]):
        category = "Appliances"
    else:
        category = "Other"

    specs = []
    for chunk in text.split("."):
        chunk = chunk.strip()
        if chunk and any(char.isdigit() for char in chunk):
            specs.append(chunk)
        if len(specs) == 4:
            break

    if not specs:
        specs = ["Specification unavailable", "See full product details"]

    return {
        "name": name,
        "price_usd": price_usd,
        "category": category,
        "key_specs": specs[:4],
    }


def _mock_sentiment(prompt: str) -> str:
    lowered = prompt.lower()
    if any(w in lowered for w in ["love", "best", "incredible", "superb"]):
        return "Positive"
    if any(w in lowered for w in ["waste", "broke", "disappointed", "returned"]):
        return "Negative"
    return "Neutral"


def _mock_math_response(prompt: str, with_trace: bool) -> str:
    mappings = {
        "23 apples": "33",
        "60 km/h": "270",
        "Maria has $50": "20",
        "rectangular garden": "44",
        "class of 30 students": "9",
    }
    answer = "42"
    for marker, value in mappings.items():
        if marker in prompt:
            answer = value
            break
    if with_trace:
        return f"Step 1: Parse values.\nStep 2: Compute arithmetic.\nANSWER: {answer}"
    return answer


def _mock_judge_json() -> str:
    return json.dumps(
        {
            "relevance": 4,
            "clarity": 4,
            "engagement": 4,
            "criteria_met": 4,
            "conciseness": 4,
        }
    )


def _mock_specificity_eval() -> str:
    return json.dumps(
        {
            "structure": 4,
            "detail": 4,
            "code_quality": 4,
            "completeness": 4,
            "overall": 4,
        }
    )


def _mock_plan() -> str:
    return "1. Define core concepts\n2. Compare approaches\n3. Provide concrete examples\n4. Summarize practical takeaways"


def _mock_text_response(system: str, user: str) -> str:
    system_lower = system.lower()
    user_lower = user.lower()

    if "sentiment classifier" in system_lower:
        return _mock_sentiment(user)

    if "math tutor" in system_lower:
        return _mock_math_response(user, with_trace="answer:" in user_lower)

    if "strict technical writing evaluator" in system_lower:
        return _mock_specificity_eval()

    if "strict email marketing evaluator" in system_lower:
        return _mock_judge_json()

    if "product data extraction assistant" in system_lower and "json" in user_lower:
        desc_match = re.search(r"product description:\n(.*)$", user, re.IGNORECASE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else user
        return json.dumps(_extract_product_data(description))

    if "planning agent" in system_lower:
        return _mock_plan()

    if "execution agent" in system_lower:
        return "This step is executed with concrete details and practical examples for the target audience."

    if "synthesis agent" in system_lower:
        return "## Synthesized Answer\n\nThis response combines the planned steps into a coherent, practical final answer."

    if "helpful writing assistant" in system_lower:
        return "## Python Testing Guide\n\nUse pytest for unit and integration tests with clear Arrange-Act-Assert structure."

    return "Mock response generated for deterministic CI validation."


class _MockCompletions:
    def create(self, *, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None = None, **_: Any) -> _MockResponse:
        system = ""
        user = ""
        for message in messages:
            if message.get("role") == "system":
                system = str(message.get("content", ""))
            if message.get("role") == "user":
                user = str(message.get("content", ""))

        if tools:
            data = _extract_product_data(user)
            tool_call = _MockToolCall(function=_MockFunction(name="extract_product", arguments=json.dumps(data)))
            return _MockResponse(choices=[_MockChoice(message=_MockMessage(content=None, tool_calls=[tool_call]))])

        content = _mock_text_response(system, user)
        return _MockResponse(choices=[_MockChoice(message=_MockMessage(content=content, tool_calls=None))])


class _MockChat:
    def __init__(self) -> None:
        self.completions = _MockCompletions()


class _MockClient:
    def __init__(self) -> None:
        self.chat = _MockChat()


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


def resolve_model(default_fallback: str = "gpt-4o-mini") -> str:
    """Resolve the model with provider-aware defaults and env override."""
    explicit = os.getenv("LLM_MODEL")
    if explicit:
        return explicit

    try:
        _, _, provider_default = _detect_provider()
        return provider_default
    except EnvironmentError:
        return default_fallback


def ensure_sandbox_environment() -> None:
    """Ensure labs run in an isolated/sandboxed environment."""
    if os.getenv("VIRTUAL_ENV"):
        return

    if os.getenv("CONDA_PREFIX"):
        return

    if os.getenv("COLAB_RELEASE_TAG") or "google.colab" in sys.modules:
        return

    if os.getenv("CI", "").lower() == "true":
        return

    if os.getenv("PEP_ALLOW_NO_VENV") == "1":
        return

    if getattr(sys, "base_prefix", sys.prefix) != sys.prefix:
        return

    raise EnvironmentError(
        "This lab must run in an isolated environment (recommended: .venv).\n"
        "Run:\n"
        "  python3 -m venv .venv\n"
        "  source .venv/bin/activate\n"
        "  python -m pip install -r learn/labs/requirements.txt\n"
        "Or run the notebook in Google Colab."
    )


def get_client() -> OpenAI | _MockClient:
    """Return an OpenAI-compatible client configured from environment variables."""
    ensure_sandbox_environment()
    if os.getenv("LABS_SKIP_API") == "1":
        return _MockClient()

    api_key, base_url, _ = _resolve_config()

    timeout = DEFAULT_TIMEOUT_SECONDS
    max_retries = DEFAULT_MAX_RETRIES

    try:
        timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)))
    except ValueError:
        pass

    try:
        max_retries = int(os.getenv("LLM_MAX_RETRIES", str(DEFAULT_MAX_RETRIES)))
    except ValueError:
        pass

    kwargs: dict = {
        "api_key": api_key,
        "timeout": timeout,
        "max_retries": max_retries,
    }
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def complete(
    prompt: str,
    *,
    system: str = "",
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
    client: OpenAI | _MockClient | None = None,
) -> str:
    """Send a chat completion request and return the response text."""
    if client is None:
        client = get_client()
    if model is None:
        model = resolve_model()

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

    if not response.choices:
        raise RuntimeError("LLM returned no completion choices.")

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("LLM completion content was empty.")

    return content


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
