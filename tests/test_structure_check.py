from app.structure_check import run_structure_check
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