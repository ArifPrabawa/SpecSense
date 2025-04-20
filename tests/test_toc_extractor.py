from app.toc_extractor import extract_toc_lines_from_text, extract_toc_lines_from_docx
from app.header_rules import clean_toc_line, is_toc_line
from types import SimpleNamespace
from docx import Document
import tempfile
import os



# Ensures TOC entries in .txt format are correctly extracted and cleaned
def test_extract_toc_lines_from_text():
    sample_text = """
    1. Introduction ................... 1
    1.1 Purpose ....................... 2
    2. Scope ......................... 3

    1. Introduction
    This is the actual section.
    """

    expected = [
        "1. Introduction",
        "1.1 Purpose",
        "2. Scope"
    ]

    result = extract_toc_lines_from_text(sample_text)
    assert result == expected


# Ensures TOC-styled paragraphs in a .docx file are correctly extracted
def test_extract_toc_lines_from_docx():
    # Fake paragraphs with mock style names
    mock_paragraphs = [
        SimpleNamespace(text="1. Overview", style=SimpleNamespace(name="TOC 1")),
        SimpleNamespace(text="2. System Description", style=SimpleNamespace(name="TOC 1")),
        SimpleNamespace(text="3. Requirements", style=SimpleNamespace(name="TOC 1")),
        SimpleNamespace(text="Not a TOC", style=SimpleNamespace(name="Heading 1")),
    ]

    # Fake Document object
    mock_doc = SimpleNamespace(paragraphs=mock_paragraphs)

    # Patch Document() to return our mock
    import app.toc_extractor as toc_module
    def fake_doc_loader(path: str):
        return mock_doc
    toc_module.Document = fake_doc_loader

    expected = ["1. Overview", "2. System Description", "3. Requirements"]
    result = extract_toc_lines_from_docx("fake_path.docx")

    assert result == expected


# Verifies dotted leaders and page numbers are removed from TOC lines
def test_clean_toc_line_removes_dotted_leader():
    raw = "1. Overview ..................... 2"
    cleaned = clean_toc_line(raw)
    assert cleaned == "1. Overview"


# Confirms that is_toc_line detects TOC-style lines and ignores non-TOC lines
def test_is_toc_line_identifies_valid_line():
    assert is_toc_line("2. Scope ............. 3") is True
    assert is_toc_line("Just some paragraph text.") is False
