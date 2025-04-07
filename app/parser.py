"""
Section Parser for SpecSense

Parses raw SRS-style text and extracts top-level section headers.
Supports markdown-style, numbered, and all-caps formats.
"""

import re
def is_markdown_header(line):
    """Detects markdown-style headers, e.g., '# Section Title'."""
    return line.startswith("# ")

def is_numbered_header(line):
    """Matches numbered sections like '1. Introduction', '1.1 Scope'."""
    return re.match(r'^\d+(\.\d+)*[.)]?\s+', line)

def is_all_caps_header(line):
    """
    Matches uppercase-only section headers, e.g., 'REQUIREMENTS'.
    Ignores short tokens like 'N/A' or shouty paragraphs.
    """
    return re.match(r'^[A-Z\s]{5,}$', line) and len(line.split()) <= 5

def extract_sections(text):
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
    sections = []
    current_section = None
    current_body = []

    for line in text.splitlines():
        line = line.strip()

        # Check for any valid section header
        if is_markdown_header(line):
            section_title = line[2:].strip()
        elif is_numbered_header(line) or is_all_caps_header(line):
            section_title = line.strip()
        else:
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
