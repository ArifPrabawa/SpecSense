from typing import Optional
from docx import Document
from app.header_rules import is_docx_toc_paragraph


def read_uploaded_file(uploaded_file) -> Optional[str]:
    """
    Reads text from an uploaded Streamlit file (.txt or .docx).
    Returns the text content as a single string.
    If file is unsupported or missing, returns None.
    """
    if uploaded_file is None:
        return None

    file_type = getattr(uploaded_file, "filename", None) or getattr(
        uploaded_file, "name", None
    )

    if file_type:
        file_type = file_type.lower()
    else:
        return None

    if file_type.endswith(".txt"):
        # Decode and return text file content
        raw = uploaded_file.read()
        print("🔍 TXT raw byte length:", len(raw))
        return raw.decode("utf-8")

    elif file_type.endswith(".docx"):
        # Use python-docx to extract text from .docx paragraphs
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs if not is_docx_toc_paragraph(p))

    # Fallback for unsupported types
    return None
