from app.parser import extract_sections, _is_all_caps_header, _is_markdown_header, _is_numbered_header

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
    assert _is_markdown_header("# Section")
    assert not _is_markdown_header("Section")

def test_is_numbered_header():
    assert _is_numbered_header("1. Introduction")
    assert _is_numbered_header("1.2.3 Overview")
    assert not _is_numbered_header("Version 1.3 applies")

def test_is_all_caps_header():
    assert _is_all_caps_header("SYSTEM OVERVIEW")
    assert not _is_all_caps_header("Overview")
    assert not _is_all_caps_header("N/A")

from app.parser import parse_sections_with_bodies

def test_parse_sections_with_bodies():
    text = """# Introduction
This document describes the system.

# Requirements
The system shall allow users to log in.

# Glossary
User: a person using the system.
"""
    expected = [
        {
            "title": "Introduction",
            "body": "This document describes the system."
        },
        {
            "title": "Requirements",
            "body": "The system shall allow users to log in."
        },
        {
            "title": "Glossary",
            "body": "User: a person using the system."
        }
    ]
    assert parse_sections_with_bodies(text) == expected

def test_multiline_bodies():
    text = """# Introduction
Line one.
Line two.

# Requirements
First requirement.
Second line of same section.
"""
    expected = [
        {
            "title": "Introduction",
            "body": "Line one.\nLine two."
        },
        {
            "title": "Requirements",
            "body": "First requirement.\nSecond line of same section."
        }
    ]
    assert parse_sections_with_bodies(text) == expected
    
def test_empty_section_body():
    text = """# EmptySection

# NextSection
Has content here.
"""
    expected = [
        {
            "title": "EmptySection",
            "body": ""
        },
        {
            "title": "NextSection",
            "body": "Has content here."
        }
    ]
    assert parse_sections_with_bodies(text) == expected

def test_no_headers_returns_empty_list():
    text = """This document lacks headers.
Just some raw content.
"""
    expected = []
    assert parse_sections_with_bodies(text) == expected

def test_parse_mixed_header_formats():
    text = """# Intro
This is the intro.

1. Purpose
Details of purpose go here.

SYSTEM OVERVIEW
This section is in all caps.
"""
    expected = [
        {"title": "Intro", "body": "This is the intro."},
        {"title": "1. Purpose", "body": "Details of purpose go here."},
        {"title": "SYSTEM OVERVIEW", "body": "This section is in all caps."}
    ]
    assert parse_sections_with_bodies(text) == expected