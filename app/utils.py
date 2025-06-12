# app/utils.py
from flask import Request
from app.file_reader import read_uploaded_file


def validate_and_read_upload(request: Request):
    """
    Consolidated upload + raw-text handling.

    Returns:
        tuple[str, str]  -> (filename, file_text)
    Raises:
        ValueError with message for any validation failure.
    """
    uploaded_file = request.files.get("srs_file")
    raw_text = request.form.get("srs_text")

    if uploaded_file:
        filename = uploaded_file.filename.lower()
        if not (filename.endswith(".txt") or filename.endswith(".docx")):
            raise ValueError("Only .txt or .docx files are supported.")
        file_text = read_uploaded_file(uploaded_file)
        if file_text is None:
            raise ValueError("Could not read or decode the uploaded file.")
        return filename, file_text

    if raw_text:
        return "traceability", raw_text

    raise ValueError("No file selected.")
