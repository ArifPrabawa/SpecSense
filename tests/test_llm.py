# Tests that analyze_requirement() correctly parses LLM response using a mocked OpenAI call


from unittest.mock import patch
from app.llm import analyze_requirement

def test_analyze_requirement_mocked():
    mock_response = "This requirement is ambiguous due to vague language."
    
    with patch("app.llm.client.chat.completions.create") as mock_create:
        mock_create.return_value.choices[0].message.content = mock_response
        result = analyze_requirement("The system should be secure.")
        
        assert result == mock_response

def test_analyze_requirement_empty_input():
    assert analyze_requirement("   ") == "Skipped analysis — section too short or empty."