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