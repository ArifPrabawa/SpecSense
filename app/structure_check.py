from app.toc_extractor import extract_toc_lines_from_text, extract_toc_lines_from_docx
from app.standard_toc import STANDARD_TOC
from app.toc_comparator import compare_toc
from app.header_rules import clean_toc_line


def run_structure_check(uploaded_file, is_docx: bool) -> dict:
    """
    Orchestrates structure conformance check.
    
    Args:
        file_text (str): Text content of the uploaded file.
        is_docx (bool): True if source is .docx, False if .txt.

    Returns:
        dict: Comparison result from compare_toc()
    """
    if is_docx:
        raw_toc_lines = extract_toc_lines_from_docx(uploaded_file)
        toc_lines = [clean_toc_line(line) for line in raw_toc_lines]
    else:
        text = uploaded_file.read().decode("utf-8")
        toc_lines = extract_toc_lines_from_text(text)

    return compare_toc(actual=toc_lines, expected=STANDARD_TOC)
