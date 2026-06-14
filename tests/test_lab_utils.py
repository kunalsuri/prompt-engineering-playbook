"""Unit tests for learn/labs/lab_utils.py.

lab_utils is the deterministic mock + client layer that the notebook smoke
tests depend on. It was previously untested. These tests lock in:
  * the mock's product-extraction / sentiment / math / dispatch behaviour
    (so a regression silently changing notebook outputs is caught — issue #5),
  * provider auto-detection + env overrides,
  * sandbox enforcement,
  * the public complete() contract against the mock client.
"""

from __future__ import annotations

import json

import pytest

import lab_utils as lu


# --------------------------------------------------------------------------- #
# Product extraction
# --------------------------------------------------------------------------- #
def test_extract_product_data_parses_price_and_category():
    data = lu._extract_product_data("Apple iPhone 15. Costs $999.50. 128GB storage.")
    assert data["name"] == "Apple iPhone 15"
    assert data["price_usd"] == 999.50
    assert data["category"] == "Electronics"
    assert data["key_specs"]  # non-empty


@pytest.mark.parametrize(
    "text,category",
    [
        ("LEGO Star Wars set. $50.", "Toys"),
        ("A paperback book. $12.", "Books"),
        ("Dyson vacuum appliance. $400.", "Appliances"),
        ("Generic widget. $5.", "Other"),
    ],
)
def test_extract_product_data_categories(text, category):
    assert lu._extract_product_data(text)["category"] == category


def test_extract_product_data_defaults_when_no_price():
    data = lu._extract_product_data("Mystery item with no price")
    assert data["price_usd"] == 0.0
    assert data["key_specs"]  # falls back to placeholder specs


# --------------------------------------------------------------------------- #
# Sentiment + math mocks
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "prompt,expected",
    [
        ("I love this, the best ever", "Positive"),
        ("What a waste, it broke", "Negative"),
        ("It is a chair", "Neutral"),
    ],
)
def test_mock_sentiment(prompt, expected):
    assert lu._mock_sentiment(prompt) == expected


def test_mock_math_response_trace_and_answer():
    traced = lu._mock_math_response("Tom has 23 apples ...", with_trace=True)
    assert "ANSWER: 33" in traced
    assert lu._mock_math_response("Tom has 23 apples ...", with_trace=False) == "33"


# --------------------------------------------------------------------------- #
# Dispatch table
# --------------------------------------------------------------------------- #
def test_mock_text_response_routes_sentiment():
    out = lu._mock_text_response("You are a Sentiment Classifier Bot", "I love it")
    assert out == "Positive"


def test_mock_text_response_routes_product_json():
    out = lu._mock_text_response(
        "You are a product data extractor",
        "Return JSON.\nProduct description:\nApple iPhone. $999.",
    )
    assert json.loads(out)["category"] == "Electronics"


def test_mock_text_response_default_fallback():
    assert "Mock response" in lu._mock_text_response("unmatched system", "hi")


# --------------------------------------------------------------------------- #
# Client + complete()
# --------------------------------------------------------------------------- #
def test_complete_with_mock_client_text():
    client = lu._MockClient()
    out = lu.complete(
        "I love it",
        system="You are a sentiment classifier",
        client=client,
        model="mock",
    )
    assert out == "Positive"


def test_complete_raises_on_empty_choices():
    class _Empty:
        class chat:
            class completions:
                @staticmethod
                def create(**_):
                    return lu._MockResponse(choices=[])

    with pytest.raises(RuntimeError):
        lu.complete("x", client=_Empty(), model="m")


def test_get_client_returns_mock_when_skip_api(monkeypatch):
    monkeypatch.setenv("LABS_SKIP_API", "1")
    monkeypatch.setenv("PEP_ALLOW_NO_VENV", "1")  # don't depend on outer env
    assert isinstance(lu.get_client(), lu._MockClient)


def test_mock_tool_call_path():
    client = lu._MockClient()
    resp = client.chat.completions.create(
        messages=[{"role": "user", "content": "Apple iPhone. $999."}],
        tools=[{"type": "function"}],
    )
    call = resp.choices[0].message.tool_calls[0]
    assert call.function.name == "extract_product"
    assert json.loads(call.function.arguments)["category"] == "Electronics"


# --------------------------------------------------------------------------- #
# Provider detection / model resolution / sandbox
# --------------------------------------------------------------------------- #
def _clear_provider_env(monkeypatch):
    for var in ("GOOGLE_API_KEY", "GROQ_API_KEY", "OPENAI_API_KEY", "LLM_MODEL", "OPENAI_API_BASE"):
        monkeypatch.delenv(var, raising=False)


def test_detect_provider_prefers_google(monkeypatch):
    _clear_provider_env(monkeypatch)
    monkeypatch.setenv("GOOGLE_API_KEY", "g")
    monkeypatch.setenv("OPENAI_API_KEY", "o")
    key, _, model = lu._detect_provider()
    assert key == "g" and model == "gemini-2.0-flash"


def test_detect_provider_raises_without_keys(monkeypatch):
    _clear_provider_env(monkeypatch)
    with pytest.raises(EnvironmentError):
        lu._detect_provider()


def test_resolve_model_env_override_wins(monkeypatch):
    _clear_provider_env(monkeypatch)
    monkeypatch.setenv("LLM_MODEL", "my-model")
    assert lu.resolve_model() == "my-model"


def test_resolve_model_fallback_without_keys(monkeypatch):
    _clear_provider_env(monkeypatch)
    assert lu.resolve_model(default_fallback="fallback-x") == "fallback-x"


def test_ensure_sandbox_environment_allows_explicit_flag(monkeypatch):
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)
    monkeypatch.delenv("CONDA_PREFIX", raising=False)
    monkeypatch.setenv("PEP_ALLOW_NO_VENV", "1")
    lu.ensure_sandbox_environment()  # must not raise


def test_print_comparison_table(capsys):
    lu.print_comparison_table(["A", "B"], [["1", "2"], ["3", "4"]])
    out = capsys.readouterr().out
    assert "A" in out and "B" in out and "3" in out
