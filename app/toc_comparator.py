def compare_toc(actual: list[str], expected: list[str], use_llm: bool = False) -> dict:
    """
    Compares an actual TOC list against a standard expected list.

    Returns:
        dict with keys:
            - matched: list[str]
            - missing: list[str] (expected but not in actual)
            - extra: list[str] (in actual but not in expected)
    """
    matched = [item for item in actual if item in expected]
    missing = [item for item in expected if item not in actual]
    extra = [item for item in actual if item not in expected]

    result = {
        "matched": matched,
        "missing": missing,
        "extra": extra,
    }

    if use_llm:
        from app.llm import compare_toc_sections_with_llm

        llm_result = compare_toc_sections_with_llm(expected, actual)
        return {
            "strict_comparison": result,
            "llm_fuzzy_comparison": llm_result,
        }

    return result
