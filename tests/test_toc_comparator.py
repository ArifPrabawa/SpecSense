from app.toc_comparator import compare_toc
from unittest.mock import patch


# Test when actual TOC perfectly matches expected TOC
def test_compare_toc_perfect_match():
    expected = ["1. Intro", "2. Scope", "3. References"]
    actual = ["1. Intro", "2. Scope", "3. References"]

    result = compare_toc(actual, expected)
    assert result["matched"] == expected
    assert result["missing"] == []
    assert result["extra"] == []


# Test when actual TOC is missing entries from expected
def test_compare_toc_missing_entries():
    expected = ["1. Intro", "2. Scope", "3. References"]
    actual = ["1. Intro"]

    result = compare_toc(actual, expected)
    assert result["matched"] == ["1. Intro"]
    assert result["missing"] == ["2. Scope", "3. References"]
    assert result["extra"] == []


# Test when actual TOC contains unexpected (extra) entries
def test_compare_toc_with_extra_entries():
    expected = ["1. Intro", "2. Scope"]
    actual = ["1. Intro", "2. Scope", "4. Appendix"]

    result = compare_toc(actual, expected)
    assert result["matched"] == ["1. Intro", "2. Scope"]
    assert result["missing"] == []
    assert result["extra"] == ["4. Appendix"]


# ✅ Test that compare_toc returns both strict and fuzzy results if use_llm is enabled
@patch("app.llm.compare_toc_sections_with_llm", return_value="*Mocked fuzzy result*")
def test_compare_toc_with_llm_enabled(mock_llm):
    standard = ["Introduction", "Scope", "System Overview"]
    document = ["Intro", "System Scope", "Features"]

    result = compare_toc(document, standard, use_llm=True)

    assert "strict_comparison" in result
    assert "llm_fuzzy_comparison" in result
    assert isinstance(result["llm_fuzzy_comparison"], str)
    assert result["llm_fuzzy_comparison"] == "*Mocked fuzzy result*"
