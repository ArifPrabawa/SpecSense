from app.header_rules import is_toc_line, clean_toc_line, is_docx_toc_paragraph
from docx import Document

def extract_toc_lines_from_text(text: str) -> list[str]:
    """
    Extracts a list of TOC-style lines from plain .txt input using existing
    TOC detection and cleaning logic.
    """
    toc_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if is_toc_line(stripped):
            toc_lines.append(clean_toc_line(stripped))
    return toc_lines


def extract_toc_lines_from_docx(docx_path: str) -> list[str]:
    """
    Extracts TOC lines from a .docx file based on paragraph styles that match
    known TOC indicators (e.g., 'TOC 1', 'toc heading').
    """
    doc = Document(docx_path)
    toc_lines = []
    for para in doc.paragraphs:
        if is_docx_toc_paragraph(para):
            cleaned = para.text.strip()
            if cleaned:
                toc_lines.append(cleaned)
    return toc_lines