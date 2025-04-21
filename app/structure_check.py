from app.toc_extractor import extract_toc_lines_from_text, extract_toc_lines_from_docx
from app.standard_toc import STANDARD_TOC
from app.toc_comparator import compare_toc
from app.header_rules import clean_toc_line


def run_structure_check(uploaded_file, is_docx: bool, use_llm=False) -> dict:
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

    return compare_toc(actual=toc_lines, expected=STANDARD_TOC, use_llm=use_llm)


def compare_toc_to_parsed_sections(
    toc_lines: list[str], parsed_sections: list[dict]
) -> dict:
    """
    Compares TOC entries to parsed section titles.
    Returns matched titles, TOC lines missing from the body, and parsed titles missing from the TOC.

    Args:
        toc_lines (list[str]): Extracted TOC lines from .txt or .docx.
        parsed_sections (list[dict]): Parsed sections from document body.

    Returns:
        dict: {
            "matched": [...],
            "missing_from_doc": [...],
            "extra_in_doc": [...]
        }
    """
    # Normalize TOC and parsed titles for comparison
    normalized_toc = {line.strip().lower(): line for line in toc_lines}
    normalized_parsed = {get_section_key(s): s["title"] for s in parsed_sections}

    matched = []
    missing_from_doc = []
    extra_in_doc = []

    for norm_title, original in normalized_toc.items():
        if norm_title in normalized_parsed:
            matched.append(normalized_parsed[norm_title])
        else:
            missing_from_doc.append(original)

    for norm_title, original in normalized_parsed.items():
        if norm_title not in normalized_toc:
            extra_in_doc.append(original)

    return {
        "matched": matched,
        "missing_from_doc": missing_from_doc,
        "extra_in_doc": extra_in_doc,
    }


def get_section_key(section):
    """
    Generates a normalized key for comparing parsed sections to TOC entries.

    If the section has an ID (e.g., '1.2'), it is combined with the title
    (e.g., 'Scope') to form '1.2 Scope'. If no ID is present, the title alone
    is used. The result is lowercased and stripped for comparison safety.
    """

    if section.get("id"):
        return f"{section['id']} {section['title']}".strip().lower()
    return section["title"].strip().lower()
