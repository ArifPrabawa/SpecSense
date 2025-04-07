"""
Parser module for SpecSense.

Public functions:
- extract_sections(text): returns list of section titles
- parse_sections_with_bodies(text): returns list of dicts {title, body}
"""

import re
def _is_markdown_header(line)-> bool:
    """Returns True if the line is a Markdown-style header (e.g., '# Section')."""
    return line.startswith("# ")

def _is_numbered_header(line)-> bool:
    """Returns True if the line starts with a numbered pattern (e.g., '1.', '2.1.3')."""
    return re.match(r'^\d+(\.\d+)*[.)]?\s+', line)

def _is_all_caps_header(line)-> bool:
    """Returns True if the line is in ALL CAPS and reasonably short (likely a section)."""
    return re.match(r'^[A-Z\s]{5,}$', line) and len(line.split()) <= 5

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
        if _is_markdown_header(line):
            # Remove the "# " from the start
            sections.append(line[2:].strip())
            continue

        # Numbered section: 1. Title, 1.1 Subsection, etc.
        if _is_numbered_header(line):
            sections.append(line.strip())
            continue
        
        # All-caps (at least 2 words, 5+ chars total)
        if _is_all_caps_header(line):
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

    for line in text.splitlines():
        line = line.strip()

        # Check for any valid section header
        if _is_markdown_header(line):
            section_title = line[2:].strip()
        elif _is_numbered_header(line) or _is_all_caps_header(line):
            section_title = line.strip()
        else:
            # Accumulate body lines under current section
            if current_section:
                current_body.append(line)
            continue

        # Save previous section before starting a new one
        if current_section or current_body:
            sections.append({
                "title": current_section,
                "body": "\n".join(current_body).strip()
            })
            current_body = []

        current_section = section_title


    # Add the final section after loop ends
    if current_section:
        sections.append({
            "title": current_section,
            "body": "\n".join(current_body).strip()
        })

    return sections
