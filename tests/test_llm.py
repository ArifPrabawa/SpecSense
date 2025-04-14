from unittest.mock import patch, MagicMock
from app.llm import analyze_requirement, suggest_tests
import pytest

# Test that analyze_requirement returns the expected LLM response when mocked
def test_analyze_requirement_returns_mocked_llm_response():
    mock_response = "This requirement is ambiguous due to vague language."
    
    # Create a mocked OpenAI completion response with nested structure
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = mock_response

    # Patch the OpenAI call and assert that our function returns the mock
    with patch("app.llm.client.chat.completions.create", return_value=mock_completion):
        result = analyze_requirement("The system should be secure.")
        assert result == mock_response


# Test that empty or whitespace-only input is skipped from LLM analysis
# This prevents unnecessary API calls and avoids noise in the output
def test_analyze_requirement_skips_empty_input():
    assert analyze_requirement("   ") == "Skipped analysis — section too short or empty."
    


#Test that suggest_tests returns the expected LLM response when mocked
def test_suggest_tests_returns_mocked_llm_response():
    mock_response = "- Test user logout after 10 minutes"

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = mock_response

    with patch("app.llm.client.chat.completions.create", return_value=mock_completion):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result == mock_response


#Test for missing API key
def test_missing_api_key_raises_error(monkeypatch):
    """
    Should raise a ValueError if OPENAI_API_KEY is not set.
    """
    # Simulate missing API key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OpenAI API key not set"):
        analyze_requirement("This is a test requirement that should be analyzed.")
        

#Test handling of OpenAI API errors in analyze_requirement
def test_analyze_requirement_handles_openai_failure():
    """
    Simulates an OpenAI API failure and verifies fallback behavior.
    """
    # Simulate an exception being raised by the OpenAI client
    with patch("app.llm.client.chat.completions.create", side_effect=Exception("Mock API failure")):
        result = analyze_requirement("The system shall allow user login via fingerprint.")
        assert result.startswith("OpenAI error: Mock API failure")


#Test handling of OpenAI API errors in suggest_tests
def test_suggest_tests_handles_openai_failure():
    """
    Simulates an OpenAI API failure and verifies fallback behavior.
    """
    # Simulate an exception being raised by the OpenAI client
    with patch("app.llm.client.chat.completions.create", side_effect=Exception("Mock API failure")):
        result = suggest_tests("The system shall allow user login via fingerprint.")
        assert result.startswith("OpenAI error: Mock API failure")
   
        
#Handles case where OpenAI response is missing expected fields in analyze_requirement
def test_analyze_requirement_handles_malformed_response():
    """
    Simulates a malformed OpenAI response (e.g., missing choices/message).
    """
    # Return an object missing .choices[0].message.content
    malformed_response = MagicMock()
    malformed_response.choices = []

    with patch("app.llm.client.chat.completions.create", return_value=malformed_response):
        result = analyze_requirement("The system shall perform a secure login.")
        assert result.startswith("⚠️ Unexpected LLM response format")
        
        
#Handles case where OpenAI response is missing expected fields in suggest_tests
def test_suggest_tests_handles_malformed_response():
    """
    Simulates a malformed OpenAI response (e.g., missing choices/message).
    """
    # Return an object missing .choices[0].message.content
    malformed_response = MagicMock()
    malformed_response.choices = []

    with patch("app.llm.client.chat.completions.create", return_value=malformed_response):
        result = suggest_tests("The system shall perform a secure login.")
        assert result.startswith("⚠️ Unexpected LLM response format")