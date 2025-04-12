from unittest.mock import patch, MagicMock
from app.llm import analyze_requirement, suggest_tests

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
def test_analyze_requirement_skips_empty_input():
    assert analyze_requirement("   ") == "Skipped analysis — section too short or empty."
    

#test that suggest_tests returns the expected LLM response when mocked
def test_suggest_tests_returns_mocked_llm_response():
    mock_response = "- Test user logout after 10 minutes"

    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock()]
    mock_completion.choices[0].message.content = mock_response

    with patch("app.llm.client.chat.completions.create", return_value=mock_completion):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result == mock_response