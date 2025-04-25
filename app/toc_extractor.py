from app.header_rules import is_toc_line, clean_toc_line, is_docx_toc_paragraph
from docx import Document


def extract_toc_lines_from_text(text: str) -> list[str]:
    """
    Extracts a list of TOC-style lines from plain .txt input.
    Ignores title pages and uses dotted line + page number heuristics.
    """
    toc_lines = []
    toc_started = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        if not toc_started:
            if is_toc_line(stripped):
                toc_started = True
                toc_lines.append(clean_toc_line(stripped))
            continue

        if is_toc_line(stripped):
            toc_lines.append(clean_toc_line(stripped))

    return toc_lines


def extract_toc_lines_from_docx(docx_file) -> list[str]:
    """
    Extracts TOC-style lines from a .docx file.
    Uses paragraph styles (preferred), but falls back to text pattern detection
    for documents where TOC styles are not preserved.
    """
    doc = Document(docx_file)
    toc_lines = []
    toc_started = False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Start collecting once we hit a TOC-style paragraph
        if not toc_started:
            if is_docx_toc_paragraph(para) or is_toc_line(text):
                toc_started = True
                toc_lines.append(text)
            continue

        if is_docx_toc_paragraph(para) or is_toc_line(text):
            toc_lines.append(text)

    return toc_lines
