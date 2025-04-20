from unittest.mock import patch, MagicMock
import pytest
from app.llm import analyze_requirement, suggest_tests


# ✅ Test that short input is skipped before LLM call
def test_analyze_requirement_skips_short_input():
    result = analyze_requirement("Too short.")
    assert result == "Skipped analysis — section too short or empty."


# ✅ Test that missing API key is reported as an OpenAI error
def test_analyze_requirement_returns_error_on_missing_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = analyze_requirement(
        "This requirement is long enough to trigger an LLM call."
    )
    assert result.startswith("OpenAI error: OpenAI API key not set")


# ✅ Test that a well-formed LLM response is returned correctly
def test_analyze_requirement_returns_llm_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content.strip.return_value = "Mock analysis result"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("This is a requirement long enough to analyze.")
        assert result == "Mock analysis result"


# ✅ Test that malformed response triggers fallback warning
def test_analyze_requirement_handles_malformed_response():
    mock_response = MagicMock()
    mock_response.choices = []

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("This is a requirement long enough to analyze.")
        assert result.startswith("⚠️ Unexpected LLM response format")


# ✅ Test that suggest_tests returns expected mock output
def test_suggest_tests_returns_mocked_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content.strip.return_value = (
        "- Suggested test case"
    )

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result == "- Suggested test case"


# ✅ Test that suggest_tests handles malformed response structure
def test_suggest_tests_handles_malformed_response():
    mock_response = MagicMock()
    mock_response.choices = []

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result.startswith("⚠️ Unexpected LLM response format")


# ✅ Test that suggest_tests returns error on OpenAI API failure
def test_suggest_tests_handles_openai_failure():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Mock API failure")

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("Log off after timeout.")
        assert result.startswith("OpenAI error: Mock API failure")


# ✅ Test that analyze_requirement returns error on OpenAI API failure
def test_analyze_requirement_handles_openai_failure():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Mock API failure")

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("The system shall log off.")
        assert result.startswith("OpenAI error: Mock API failure")
