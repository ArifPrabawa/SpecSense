import pytest
from app.formatter import format_llm_response


# Test that well-formed bold headers and bullets are preserved
def test_preserves_existing_bold_headers():
    raw = "**Ambiguity:**\n- It is unclear what 'the system' refers to."
    expected = "**Ambiguity:**\n- It is unclear what 'the system' refers to."
    assert format_llm_response(raw) == expected


# Test that multiple bold markers are normalized to proper double asterisks
def test_cleans_overbolded_headers():
    raw = "****Vagueness:****\n- Lacks measurable detail."
    expected = "**Vagueness:**\n- Lacks measurable detail."
    assert format_llm_response(raw) == expected


# Test that unmatched bold markers are removed
def test_removes_unmatched_bold_markers():
    raw = "**Unmatched bold\n- Some bullet"
    expected = "Unmatched bold\n- Some bullet"
    assert format_llm_response(raw) == expected


# Test that duplicate bullet points are removed
def test_removes_duplicate_bullets():
    raw = "- Item A\n- Item A"
    expected = "- Item A"
    assert format_llm_response(raw) == expected


# Test that empty lines and excessive whitespace are stripped
def test_skips_empty_lines():
    raw = "\n\n- Valid point\n\n"
    expected = "- Valid point"
    assert format_llm_response(raw) == expected


# Test trimming of leading/trailing whitespace
def test_trims_spacing_and_indentation():
    raw = "   **Testing Challenges:**    \n    - Indented bullet    "
    expected = "**Testing Challenges:**\n- Indented bullet"
    assert format_llm_response(raw) == expected


# Test formatter behavior when looped over batch-style
def test_batch_formatter_structure():
    sections = [
        {"title": "5.1 Intro", "body": "Requirement must be fulfilled."},
        {"title": "5.2 Timeout", "body": "The system shall auto-logoff."},
    ]

    # Simulate LLM and formatter together (you could patch LLM if desired)
    results = {}
    for section in sections:
        fake_raw = f"**Clarity:**\n- {section['body']}"
        formatted = format_llm_response(fake_raw)
        results[section["title"]] = {
            "body": section["body"],
            "raw": fake_raw,
            "analysis": formatted,
        }

    assert "5.1 Intro" in results
    assert "Clarity" in results["5.2 Timeout"]["analysis"]


# Test Skipped analysis handling
def test_skipped_analysis_formatting():
    skipped_output = "Skipped analysis: too short"
    result = format_llm_response(skipped_output)

    # Make sure it doesn't crash and passes through
    assert skipped_output in result
