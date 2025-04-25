import pytest
from unittest.mock import patch, MagicMock
from app.llm import (
    analyze_requirement,
    suggest_tests,
    compare_toc_sections_with_llm,
    llm_group_requirement,
    summarize_analysis,
)


@pytest.fixture(autouse=True)
def mock_all_llm(monkeypatch):
    import app.llm

    monkeypatch.setattr(
        app.llm, "analyze_requirement", lambda text: "🧪 Mocked analysis"
    )
    monkeypatch.setattr(
        app.llm, "suggest_tests", lambda text: "🧪 Mocked test suggestion"
    )
    monkeypatch.setattr(
        app.llm,
        "compare_toc_sections_with_llm",
        lambda a, b: "🧪 Mocked fuzzy comparison",
    )


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
    mock_response.choices[0].message.content = "Mock analysis result"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("This is a requirement long enough to analyze.")
        assert result == "Mock analysis result"


# ✅ Test that suggest_tests returns expected mock output
def test_suggest_tests_returns_mocked_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "- Suggested test case"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result == "- Suggested test case"


# ✅ Test that malformed (non-string) response triggers fallback warning
def test_analyze_requirement_handles_non_string_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = 123  # not a string

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("This is a requirement long enough to analyze.")
        assert result.startswith("⚠️ Unexpected LLM response format")


# ✅ Test that malformed (missing .choices[0]) response triggers OpenAI error
def test_analyze_requirement_handles_exception_response():
    mock_response = MagicMock()
    mock_response.choices = []  # causes IndexError

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = analyze_requirement("This is a requirement long enough to analyze.")
        assert result.startswith("OpenAI error: list index out of range")


# ✅ Test that malformed (non-string) response triggers fallback warning
def test_suggest_tests_handles_non_string_response():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = None  # triggers format warning

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result.startswith("⚠️ Unexpected LLM response format")


# ✅ Test that malformed (missing .choices[0]) response triggers OpenAI error
def test_suggest_tests_handles_exception_response():
    mock_response = MagicMock()
    mock_response.choices = []  # causes IndexError

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("app.llm.get_client", return_value=mock_client):
        result = suggest_tests("The system shall log off after 10 minutes.")
        assert result.startswith("OpenAI error: list index out of range")


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


# ✅ Test that compare_toc_sections_with_llm returns Markdown on normal fuzzy input
@patch("app.llm.get_client")
def test_compare_toc_sections_with_llm_valid_input(mock_get_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = (
        "- Scope\n- Functional Requirements\n- Introduction"
    )

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = compare_toc_sections_with_llm(
        ["Introduction", "Scope", "Functional Requirements"],
        ["Intro", "System Scope", "Features"],
    )

    assert isinstance(result, str)
    assert "Scope" in result or "Missing Sections" in result


# ✅ Test that compare_toc_sections_with_llm skips if any list is empty
def test_compare_toc_sections_with_llm_empty_input():
    result = compare_toc_sections_with_llm([], ["Some Section"])
    assert result.startswith("⚠️ Skipped")

    result = compare_toc_sections_with_llm(["Some Section"], [])
    assert result.startswith("⚠️ Skipped")

    result = compare_toc_sections_with_llm([], [])
    assert result.startswith("⚠️ Skipped")


# Should simulate semantic fuzzy match result (mocked, no LLM)
def test_compare_toc_sections_with_llm_semantic_equivalence():
    standard = ["User Interface Requirements"]
    document = ["GUI Specs"]

    # Mocking get_client to avoid calling the LLM
    with patch("app.llm.get_client") as mock_get_client:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[
            0
        ].message.content = """
            Matched Sections:
            - None

            Fuzzy Matched Sections:
            - User Interface Requirements (Fuzzy match to: 'GUI Specs')

            Missing Sections:
            - None
        """

        # Set mock response for the get_client mock
        mock_get_client.return_value.chat.completions.create.return_value = (
            mock_response
        )

        # Now call the function with the mock in place
        result = compare_toc_sections_with_llm(standard, document)

    # Assert based on the mocked string that includes "Fuzzy Matched Sections"
    assert "Fuzzy Matched Sections" in result
    assert "User Interface Requirements" in result
    assert "GUI Specs" in result


# ✅ Test LLM group assignment with mocked valid JSON array response
@patch("app.llm.get_client")
def test_llm_group_requirement_valid_response(mock_get_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '["Authentication", "Security"]'

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = llm_group_requirement("The system shall authenticate users securely.")
    assert "Authentication" in result
    assert "Security" in result


# ✅ Test that a malformed (non-JSON) response is caught
@patch("app.llm.get_client")
def test_llm_group_requirement_malformed_response(mock_get_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Oops, not a JSON array"

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = llm_group_requirement("REQ-1 Something vague")
    assert result == ["⚠️ Unexpected format"]


# ✅ Test fallback on OpenAI failure
@patch("app.llm.get_client")
def test_llm_group_requirement_handles_openai_exception(mock_get_client):
    mock_get_client.side_effect = Exception("Simulated API failure")
    result = llm_group_requirement("REQ-99 Simulated crash")
    assert result[0].startswith("OpenAI error:")


# ✅ Test skip logic for short input
def test_llm_group_requirement_skips_short_input():
    result = llm_group_requirement("Too short.")
    assert result == []


# ✅ Test fallback for missing API key
def test_llm_group_requirement_no_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = llm_group_requirement("REQ-7 The system shall log errors.")
    assert result == ["⚠️ No API Key"]


# ✅ Test that summarize_analysis handles missing API key gracefully
def test_summarize_analysis_skips_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = summarize_analysis({"5.1": {"analysis": "Some analysis here."}})
    assert result.startswith("⚠️ Summary skipped")


# ✅ Test that summarize_analysis handles empty analysis_results cleanly
def test_summarize_analysis_handles_empty_input():
    result = summarize_analysis({})
    assert result.startswith("⚠️ No analysis content")


# ✅ Test that summarize_analysis filters out 'Skipped' sections
def test_summarize_analysis_ignores_skipped_sections():
    input_data = {
        "5.1": {"analysis": "Skipped analysis — section too short or empty."},
        "5.2": {"analysis": ""},
    }
    result = summarize_analysis(input_data)
    assert result.startswith("⚠️ No analysis content")


# ✅ Test that summarize_analysis returns LLM result when analysis exists
@patch("app.llm.get_client")
def test_summarize_analysis_returns_llm_response(mock_get_client):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked summary output."

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_get_client.return_value = mock_client

    input_data = {
        "5.1": {"analysis": "Authentication requires clarification on user roles."},
        "5.2": {"analysis": "Encryption methods are not clearly specified."},
    }

    result = summarize_analysis(input_data)

    assert result == "Mocked summary output."
