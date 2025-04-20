from unittest.mock import patch, MagicMock
from app.llm import analyze_requirement, suggest_tests
import pytest

# ✅ Test that analyze_requirement returns mocked LLM response
def test_analyze_requirement_returns_mocked_llm_response():
    mock_response_text = "This requirement is ambiguous due to vague language."

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content.strip.return_value = mock_response_text

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("The system shall always be secure.")
        assert result == mock_response_text


# ✅ Test that empty input is skipped from LLM analysis
def test_analyze_requirement_skips_empty_input():
    assert analyze_requirement("   ") == "Skipped analysis — section too short or empty."


# ✅ Test that suggest_tests returns mocked LLM response
def test_suggest_tests_returns_mocked_llm_response():
    mock_response_text = "- Test user logout after 10 minutes"

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content.strip.return_value = mock_response_text

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result == mock_response_text


# ✅ Test handling of missing API key
def test_missing_api_key_raises_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OpenAI API key not set"):
        analyze_requirement("This is a test requirement.")


# ✅ Test LLM failure fallback for analyze_requirement
def test_analyze_requirement_handles_openai_failure():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Mock API failure")

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("The system shall log off.")
        assert result.startswith("OpenAI error: Mock API failure")


# ✅ Test LLM failure fallback for suggest_tests
def test_suggest_tests_handles_openai_failure():
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("Mock API failure")

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("Log off after timeout.")
        assert result.startswith("OpenAI error: Mock API failure")


# ✅ Handles malformed response for analyze_requirement
def test_analyze_requirement_handles_malformed_response():
    mock_client = MagicMock()
    malformed_response = MagicMock()
    malformed_response.choices = []

    mock_client.chat.completions.create.return_value = malformed_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("Secure login")
        assert result.startswith("⚠️ Unexpected LLM response format")


# ✅ Handles malformed response for suggest_tests
def test_analyze_requirement_handles_malformed_response():
    mock_client = MagicMock()
    mock_response = MagicMock()

    # Force .choices[0] to raise IndexError
    def raise_index_error():
        raise IndexError("No choices")

    mock_response.choices.__getitem__.side_effect = raise_index_error
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("The system shall perform a secure login.")
        assert result.startswith("⚠️ Unexpected LLM response format")
