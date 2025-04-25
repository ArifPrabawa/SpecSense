import textwrap
from app.parser import extract_sections, parse_sections_with_bodies, strip_title_block
from app.header_rules import is_all_caps_header, is_markdown_header, is_numbered_header


# Test basic markdown headers are correctly extracted
def test_extract_sections_simple():
    sample_text = "# Introduction\nSome intro text.\n\n# Requirements\nContent here."
    expected = ["Introduction", "Requirements"]
    assert extract_sections(sample_text) == expected


# Test extraction of numbered headers (e.g., 1., 1.1, 2.)
def test_extract_numbered_sections():
    text = "1. Introduction\nDetails.\n\n1.1 Scope\nDetails.\n\n2. Requirements\nMore details."
    expected = ["1. Introduction", "1.1 Scope", "2. Requirements"]
    assert extract_sections(text) == expected


# Test that body text not acting as a header is ignored
def test_ignores_non_headers():
    text = "Some random text.\n# Functional Requirements\nDetails\nJust more text\n# Glossary\nTerms"
    expected = ["Functional Requirements", "Glossary"]
    assert extract_sections(text) == expected


# Test detection of ALL CAPS headers as section titles
def test_all_caps_headers():
    text = "INTRODUCTION\n\nSome content.\n\nREQUIREMENTS\nContent continues."
    expected = ["INTRODUCTION", "REQUIREMENTS"]
    assert extract_sections(text) == expected


# Test that empty input returns an empty list
def test_empty_input():
    text = ""
    expected = []
    assert extract_sections(text) == expected


# Test detection logic for markdown-style headers
def testis_markdown_header():
    assert is_markdown_header("# Section")
    assert not is_markdown_header("Section")


# Test detection logic for numbered-style headers
def testis_numbered_header():
    assert is_numbered_header("1. Introduction")
    assert is_numbered_header("1.2.3 Overview")
    assert not is_numbered_header("Version 1.3 applies")


# Test detection logic for all-caps-style headers
def testis_all_caps_header():
    assert is_all_caps_header("SYSTEM OVERVIEW")
    assert not is_all_caps_header("Overview")
    assert not is_all_caps_header("N/A")


# Test full section parsing with markdown headers and body content
def test_parse_sections_with_bodies():
    text = textwrap.dedent(
        """# Introduction
This document describes the system.

# Requirements
The system shall allow users to log in.

# Glossary
User: a person using the system.
"""
    )

    result = parse_sections_with_bodies(text)

    assert len(result) == 3

    assert result[0]["title"] == "Introduction"
    assert result[0]["body"] == "This document describes the system."

    assert result[1]["title"] == "Requirements"
    assert result[1]["body"] == "The system shall allow users to log in."

    assert result[2]["title"] == "Glossary"
    assert result[2]["body"] == "User: a person using the system."


# Test multiline bodies are preserved under a single section
def test_multiline_bodies():
    text = textwrap.dedent(
        """# Introduction
Line one.
Line two.

# Requirements
First requirement.
Second line of same section.
"""
    )

    result = parse_sections_with_bodies(text)

    assert len(result) == 2

    assert result[0]["title"] == "Introduction"
    assert "Line one." in result[0]["body"]
    assert "Line two." in result[0]["body"]

    assert result[1]["title"] == "Requirements"
    assert "First requirement." in result[1]["body"]
    assert "Second line of same section." in result[1]["body"]


# Test behavior when a header has no body content
def test_empty_section_body():
    text = textwrap.dedent(
        """# EmptySection

# NextSection
Has content here.
"""
    )

    result = parse_sections_with_bodies(text)

    assert len(result) == 2

    assert result[0]["title"] == "EmptySection"
    assert result[0]["body"] == ""

    assert result[1]["title"] == "NextSection"
    assert result[1]["body"] == "Has content here."


# Test parsing returns empty list when no valid headers exist
def test_no_headers_returns_empty_list():
    text = textwrap.dedent(
        """This document lacks headers.
Just some raw content.
"""
    )
    expected = []
    assert parse_sections_with_bodies(text) == expected


# Test mixed header formats are parsed with correct IDs and bodies
def test_parse_mixed_header_formats():
    text = textwrap.dedent(
        """# Intro
This is the intro.

1. Purpose
Details of purpose go here.

SYSTEM OVERVIEW
This section is in all caps.

5.2. Purpose
Details of purpose go here.
"""
    )

    result = parse_sections_with_bodies(text)

    assert len(result) == 4

    assert result[0]["title"] == "Intro"
    assert "This is the intro." in result[0]["body"]

    assert result[1]["title"] == "Purpose"
    assert "Details of purpose go here." in result[1]["body"]

    assert result[2]["title"] == "SYSTEM OVERVIEW"
    assert "This section is in all caps." in result[2]["body"]

    assert result[3]["title"] == "Purpose"
    assert "Details of purpose go here." in result[3]["body"]


# Test all-caps headers are recognized and associated with their bodies
def test_all_caps_header_detection():
    text = textwrap.dedent(
        """Intro paragraph.

TEST
This is a test section.

SYSTEM OVERVIEW
This section defines system boundaries.
"""
    )

    result = parse_sections_with_bodies(text)

    assert len(result) == 2

    assert result[0]["title"] == "TEST"
    assert "This is a test section." in result[0]["body"]

    assert result[1]["title"] == "SYSTEM OVERVIEW"
    assert "This section defines system boundaries." in result[1]["body"]


# Test the short title-case lines like 'Scope' or 'Purpose' fallback
def test_fallback_headers_detected():

    raw_text = textwrap.dedent(
        """\
    Purpose
    This document defines the project scope.

    Scope
    The lighting system will allow remote control.

    System Overview
    Uses mobile, cloud, and Wi-Fi.
    """
    )

    results = parse_sections_with_bodies(raw_text)
    titles = [section["title"] for section in results]

    assert "Purpose" in titles
    assert "Scope" in titles
    assert "System Overview" in titles


# Test the removal of TOC style text in .txt files
def test_toc_lines_are_skipped():
    text = textwrap.dedent(
        """\
        1. Introduction .................... 1
        2. Scope ........................ 2
        3. Requirements ...................... 3

        # Introduction
        Actual body starts here.
    """
    )
    results = parse_sections_with_bodies(text)
    titles = [section["title"] for section in results]
    assert "1. Introduction .................... 1" not in titles
    assert "Introduction" in titles


# Test that requirement IDs and full traceable lines are extracted correctly
def test_requirement_id_extraction():
    text = textwrap.dedent(
        """# Test Section
REQ-1 The system shall power on within 2 seconds.
REQ-2 The system shall log out after 10 minutes.
This line has no ID.
"""
    )

    result = parse_sections_with_bodies(text)
    assert len(result) == 1

    section = result[0]
    assert section["title"] == "Test Section"

    requirement_map = {req["id"]: req["text"] for req in section["requirements"]}
    assert "REQ-1" in requirement_map
    assert "REQ-2" in requirement_map
    assert (
        requirement_map["REQ-1"] == "REQ-1 The system shall power on within 2 seconds."
    )
    assert (
        requirement_map["REQ-2"] == "REQ-2 The system shall log out after 10 minutes."
    )


# ✅ Test that strip_title_block removes known title metadata lines at the top
def test_strip_title_block_removes_metadata_lines():
    lines = [
        "Software Requirements Specification",
        "Project: SpecSense AI Tool",
        "Version: 1.0",
        "Date: 2025-04-22",
        "",
        "1 Introduction",
        "This is the actual first section.",
    ]

    result = strip_title_block(lines)

    assert "Software Requirements Specification" not in result
    assert "Project: SpecSense AI Tool" not in result
    assert "Version: 1.0" not in result
    assert "Date: 2025-04-22" not in result
    assert result[0] == "1 Introduction"
    assert result[1] == "This is the actual first section."
