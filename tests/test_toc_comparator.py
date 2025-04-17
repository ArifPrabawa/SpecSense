from app.toc_comparator import compare_toc

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