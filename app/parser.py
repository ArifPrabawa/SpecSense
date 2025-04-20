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
            sections.append(
                {
                    "id": current_section["id"] if current_section else None,
                    "title": current_section["title"] if current_section else "",
                    "body": "\n".join(current_body).strip(),
                }
            )
            current_body = []

        current_section = {"id": section_id, "title": section_title}

    # Add the final section after loop ends
    if current_section:
        sections.append(
            {
                "id": current_section["id"],
                "title": current_section["title"],
                "body": "\n".join(current_body).strip(),
            }
        )

    return sections
