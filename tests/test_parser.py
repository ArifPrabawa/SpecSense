from app.parser import extract_sections, is_all_caps_header, is_markdown_header, is_numbered_header

def test_extract_sections_simple():
    sample_text = "# Introduction\nSome intro text.\n\n# Requirements\nContent here."
    expected = ["Introduction", "Requirements"]
    assert extract_sections(sample_text) == expected

def test_extract_numbered_sections():
    text = "1. Introduction\nDetails.\n\n1.1 Scope\nDetails.\n\n2. Requirements\nMore details."
    expected = ["1. Introduction", "1.1 Scope", "2. Requirements"]
    assert extract_sections(text) == expected

def test_ignores_non_headers():
    text = "Some random text.\n# Functional Requirements\nDetails\nJust more text\n# Glossary\nTerms"
    expected = ["Functional Requirements", "Glossary"]
    assert extract_sections(text) == expected

def test_all_caps_headers():
    text = "INTRODUCTION\n\nSome content.\n\nREQUIREMENTS\nContent continues."
    expected = ["INTRODUCTION", "REQUIREMENTS"]
    assert extract_sections(text) == expected

def test_empty_input():
    text = ""
    expected = []
    assert extract_sections(text) == expected

def test_is_markdown_header():
    assert is_markdown_header("# Section")
    assert not is_markdown_header("Section")

def test_is_numbered_header():
    assert is_numbered_header("1. Introduction")
    assert is_numbered_header("1.2.3 Overview")
    assert not is_numbered_header("Version 1.3 applies")

def test_is_all_caps_header():
    assert is_all_caps_header("SYSTEM OVERVIEW")
    assert not is_all_caps_header("Overview")
    assert not is_all_caps_header("N/A")
