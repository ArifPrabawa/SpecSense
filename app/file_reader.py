from typing import Optional
from docx import Document


def _is_docx_toc_paragraph(para) -> bool:
    """
    Returns True if the paragraph style indicates a Table of Contents entry.
    Skips styles like 'TOC 1', 'TOC Heading', etc.
    """
    style_name = para.style.name.lower()
    return style_name.startswith("toc") or "toc" in style_name


def read_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Reads text from an uploaded Streamlit file (.txt or .docx).
    Returns the text content as a single string.
    If file is unsupported or missing, returns None.
    """
    if uploaded_file is None:
        return None

    file_type = uploaded_file.name.lower()

    if file_type.endswith(".txt"):
        # Decode and return text file content
        return uploaded_file.read().decode("utf-8")

    elif file_type.endswith(".docx"):
        # Use python-docx to extract text from .docx paragraphs
        doc = Document(uploaded_file)
        return "\n".join(
            p.text for p in doc.paragraphs if not _is_docx_toc_paragraph(p)
        )

    # Fallback for unsupported types
    return None