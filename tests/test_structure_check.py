from app.structure_check import run_structure_check, compare_toc_to_parsed_sections
from io import BytesIO
from types import SimpleNamespace
import pytest

#Test to see if TOC structure is exactly one to one with expecteds
def test_structure_check_txt_strict_match():
    sample_txt = b"1. Introduction .................. 1\n1.2 Scope .................. 2\n"
    fake_file = BytesIO(sample_txt)
    fake_file.name = "sample.txt"

    result = run_structure_check(fake_file, is_docx=False)

    assert "1. Introduction" in result["matched"]
    assert "1.2 Scope" in result["matched"]
    
# This test assumes fuzzy or LLM comparison exists
# Currently expected to fail — tracked for roadmap

@pytest.mark.xfail(reason="Fuzzy matching not implemented yet")
def test_structure_check_txt_fuzzy_match():
    sample_txt = b"1. Introduction .................. 1\n2. Scope .................. 2\n"
    fake_file = BytesIO(sample_txt)
    fake_file.name = "sample.txt"

    result = run_structure_check(fake_file, is_docx=False)

    # This will fail with current exact matcher, pass once LLM added
    assert "2. Scope" in result["matched"]

@pytest.fixture
def monkeypatch_docx(monkeypatch):
    from app import toc_extractor

    paragraphs = [
        SimpleNamespace(text="1. Overview", style=SimpleNamespace(name="TOC 1")),
        SimpleNamespace(text="2. System Description", style=SimpleNamespace(name="TOC 2")),
        SimpleNamespace(text="3. Requirements", style=SimpleNamespace(name="TOC Heading")),
        SimpleNamespace(text="Not a TOC item", style=SimpleNamespace(name="Heading 1")),
    ]
    mock_doc = SimpleNamespace(paragraphs=paragraphs)
    monkeypatch.setattr(toc_extractor, "Document", lambda x: mock_doc)


# This test is expected to fail until LLM-based or fuzzy TOC comparison is added
@pytest.mark.xfail(reason="TOC fuzzy matching not implemented yet")
def test_structure_check_docx_fuzzy_match_placeholder(monkeypatch_docx):
    """
    Tests whether the docx TOC extractor and structure matcher can recognize
    non-standard headings like '1. Overview', which are NOT in the STANDARD_TOC
    but conceptually equivalent. This test is a placeholder for future LLM-assisted matching.
    """
    from app.structure_check import run_structure_check
    from io import BytesIO

    fake_file = BytesIO(b"dummy")
    fake_file.name = "sample.docx"

    result = run_structure_check(fake_file, is_docx=True)

    assert "1. Overview" in result["matched"]
    assert "2. System Description" in result["matched"]
    assert "3. Requirements" in result["matched"]
    assert "Not a TOC item" not in result["matched"]
    
# ✅ Matches when parsed section has only a title (no ID)
def test_compare_toc_to_parsed_sections_title_only_match():
    toc = ["Overview"]
    parsed = [
        {"id": None, "title": "Overview", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert "Overview" in result["matched"]
    assert result["missing_from_doc"] == []
    assert result["extra_in_doc"] == []

# ✅ Flags TOC line that has no matching parsed section
def test_compare_toc_to_parsed_sections_toc_missing_in_doc():
    toc = ["3. Security"]
    parsed = [
        {"id": "1", "title": "Overview", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert "3. Security" in result["missing_from_doc"]
    assert "Overview" in result["extra_in_doc"]

# ✅ Flags parsed section not listed in TOC
def test_compare_toc_to_parsed_sections_extra_in_doc():
    toc = ["1 Overview"]
    parsed = [
        {"id": "1", "title": "Overview", "body": "..."},
        {"id": "2", "title": "Scope", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert "Overview" in result["matched"]
    assert "Scope" in result["extra_in_doc"]

# ❌ Case-sensitive comparison fails for future support (xfail for now)
@pytest.mark.xfail(reason="Case-insensitive title matching not implemented in returned values")
def test_compare_toc_to_parsed_sections_case_insensitive():
    toc = ["1.2 scope"]
    parsed = [
        {"id": "1.2", "title": "Scope", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert "1.2 scope" in [m.lower() for m in result["matched"]]

# ❌ Whitespace-normalized comparison (xfail for now)
@pytest.mark.xfail(reason="Matched titles currently returned in raw form, not normalized")
def test_compare_toc_to_parsed_sections_whitespace_insensitive():
    toc = [" 1.2   Scope  "]
    parsed = [
        {"id": "1.2", "title": "Scope", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert any(m.strip().lower() == "1.2 scope" for m in result["matched"])

# ❌ Future enhancement: ID + title literal match expected from TOC
@pytest.mark.xfail(reason="Matched titles currently return title only, not full ID + title composite")
def test_compare_toc_to_parsed_sections_matches_on_id_and_title():
    toc = ["1.2 Scope", "2 Overview"]
    parsed = [
        {"id": "1.2", "title": "Scope", "body": "..."},
        {"id": "2", "title": "Overview", "body": "..."}
    ]
    result = compare_toc_to_parsed_sections(toc, parsed)
    assert "1.2 Scope" in result["matched"]
