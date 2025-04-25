"""
Parser module for SpecSense.

Public functions:
- extract_sections(text): returns list of section titles
- parse_sections_with_bodies(text): returns list of dicts {title, body}
"""

import re

from app.header_rules import (
    is_markdown_header,
    is_numbered_header,
    is_all_caps_header,
    is_fallback_header,
    extract_id_and_title,
    is_toc_line,
)


def extract_sections(text):
    """
    Extracts section titles from unstructured SRS-style text.

    Args:
        text (str): Raw string input representing an SRS document.

    Returns:
        List[str]: A list of section titles (headers only).
    """
    sections = []
    for line in text.splitlines():
        line = line.strip()

        # Markdown-style header
        if is_markdown_header(line):
            # Remove the "# " from the start
            sections.append(line[2:].strip())
            continue

        # Numbered section: 1. Title, 1.1 Subsection, etc.
        if is_numbered_header(line):
            sections.append(line.strip())
            continue

        # All-caps (at least 2 words, 5+ chars total)
        if is_all_caps_header(line):
            sections.append(line.strip())
            continue

    return sections


def is_title_block_line(line: str) -> bool:
    """
    Determines whether a line is part of a document's title block.

    Title block lines typically appear at the top of SRS documents and include
    metadata such as project name, version, and date. These lines are not actual
    section headers and should be excluded from requirement parsing.

    Args:
        line (str): A single line from the input document.

    Returns:
        bool: True if the line is part of the title block, False otherwise.
    """
    stripped = line.strip().lower()

    known_exact = {
        "software requirements specification",
        "table of contents",
    }

    known_prefixes = ["project:", "version:", "date:"]

    for prefix in known_prefixes:
        if stripped.startswith(prefix):
            return True

    return stripped in known_exact


def strip_title_block(lines: list[str]) -> list[str]:
    """
    Removes the document's initial title block from a list of lines.

    Many SRS documents begin with metadata such as project title, version, date,
    and a "Table of Contents" heading before the actual requirements begin.
    This function removes those lines to prevent them from being misclassified
    as section headers.

    The title block is assumed to appear only at the top of the document.
    Filtering stops as soon as the first line is encountered that does not match
    known title block patterns.

    Args:
        lines (list[str]): Raw lines from the input document.

    Returns:
        list[str]: The remaining lines after removing the title block.
    """
    filtered = []
    in_title_block = True

    for line in lines:
        if in_title_block and is_title_block_line(line):
            continue
        if in_title_block and not line.strip():
            continue  # skip blank lines right after title metadata
        in_title_block = False
        filtered.append(line)

    return filtered


def parse_sections_with_bodies(text):
    """
    Extracts section headers and their corresponding body text from raw input.

    Args:
        text (str): Raw SRS-style text input with headers and body content.

    Returns:
        List[dict]: A list of dictionaries with 'title' and 'body' keys.
    """
    sections = []
    current_section = None
    current_body = []

    lines = text.splitlines()
    lines = strip_title_block(lines)
    for i, line in enumerate(lines):
        line = line.strip()

        if i < 40 and is_toc_line(line):
            continue  # skip TOC-style line

        # Look at previous and next lines to confirm isolation
        prev_line = lines[i - 1].strip() if i > 0 else ""
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

        # Only treat ALL CAPS as header if visually separated
        is_isolated_all_caps = is_all_caps_header(line) and (
            prev_line == "" or next_line == ""
        )
        # Check for any valid section header
        if is_markdown_header(line):
            section_id, section_title = extract_id_and_title(line[2:].strip())
        elif is_numbered_header(line) or is_isolated_all_caps:
            section_id, section_title = extract_id_and_title(line.strip())
        elif is_fallback_header(line):
            section_id, section_title = None, line.strip()
        else:
            # Accumulate body lines under current section
            if current_section:
                current_body.append(line)
            continue

        # Save previous section before starting a new one
        if current_section or current_body:
            section_body = "\n".join(current_body).strip()
            sections.append(
                {
                    "id": current_section["id"] if current_section else None,
                    "title": current_section["title"] if current_section else "",
                    "body": section_body,
                    "requirements": extract_requirement_statements(section_body),
                }
            )
            current_body = []

        current_section = {"id": section_id, "title": section_title}

    # Add the final section after loop ends
    if current_section:
        section_body = "\n".join(current_body).strip()
        sections.append(
            {
                "id": current_section["id"],
                "title": current_section["title"],
                "body": section_body,
                "requirements": extract_requirement_statements(section_body),
            }
        )

    return sections


def extract_requirement_statements(text: str) -> list[dict]:
    """
    Scans body text line-by-line and returns a list of
    {'id': ..., 'text': ...} mappings for each line containing a requirement ID.
    """
    if not text:
        return []

    patterns = [
        r"\bREQ-\d+\b",  # REQ-001
        r"\bID:\s*[A-Z0-9\-]{2,}\b",  # ID: ABC-45
    ]

    results = []
    lines = text.splitlines()

    for line in lines:
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                results.append({"id": match.group().strip(), "text": line.strip()})
                break  # Stop at first match per line

    return results
