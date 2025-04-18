import re


def is_markdown_header(line)-> bool:
    """Returns True if the line is a Markdown-style header (e.g., '# Section')."""
    return line.startswith("# ")

def is_numbered_header(line)-> bool:
    """Returns True if the line starts with a numbered pattern (e.g., '1.', '2.1.3')."""
    return re.match(r'^\d+(\.\d+)*[.)]?\s+', line)

def is_all_caps_header(line)-> bool:
    """Returns True if the line is in ALL CAPS and reasonably short (likely a section)."""
    return re.match(r'^[A-Z\s]+$', line) is not None and len(line.split()) <= 5

def extract_id_and_title(line: str) -> tuple[str | None, str]:
    """
    Extracts a section ID (like '5.1.9') and title from a header line.
    If no ID is found, returns (None, line).
    """
    match = re.match(r'^(\d+(?:\.\d+)*)(?:[.)]?)\s+(.*)', line)
    if match:
        return match.group(1), match.group(2).strip()
    return None, line.strip()


def is_fallback_header(line: str) -> bool:
    """
    Detects informal fallback section headers based on formatting.
    Matches short, title-case lines (1–4 words) like 'Scope' or 'System Overview',
    typically found in unstructured or loosely formatted SRS files.

    Args:
        line (str): A single line of text from the input document.

    Returns:
        bool: True if the line looks like a fallback header, False otherwise.
    """
    words = line.strip().split()
    if not (1 <= len(words) <= 4):
        return False
    if not line.strip().istitle():
        return False
    return True

def is_toc_line(line: str) -> bool:
    """
    Returns True if the line resembles a Table of Contents entry.
    Matches patterns like '1. Introduction .......... 2'
    """
    line = line.strip()
    if "..." in line or re.search(r"\.{4,}", line):  # 4+ dots
        if re.search(r"\d+$", line):  # ends in a number
            return True
    return False

def is_docx_toc_paragraph(para) -> bool:
    """
    Returns True if the .docx paragraph uses a style associated with a Table of Contents.
    """
    style_name = para.style.name.lower() if para.style else ""
    return style_name.startswith("toc") or "toc" in style_name

def clean_toc_line(line: str) -> str:
    """
    Cleans a TOC line by removing dotted leaders and trailing page numbers.
    Example:
        '1. Introduction .......... 2' → '1. Introduction'
    """
    line = re.split(r'\.{3,}\s*\d*$', line.strip())[0].strip()
    line = re.sub(r"(\d+\.\d+)\.\s+", r"\1 ", line)  # Normalize '1.2. Title' → '1.2 Title'
    return line