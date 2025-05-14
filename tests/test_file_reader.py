from io import BytesIO
from app.file_reader import read_uploaded_file
from app.header_rules import is_docx_toc_paragraph
from types import SimpleNamespace
from docx import Document


# Test that simulates uploading a .txt file and verifies decoded output.
def test_read_uploaded_txt_file():
    fake_txt = BytesIO(b"The system shall start within 10 seconds.")
    fake_txt.name = "example.txt"  # simulate file name

    result = read_uploaded_file(fake_txt)
    assert "The system shall start" in result


# Test if no file is uploaded returns None
def test_read_uploaded_file_none():

    result = read_uploaded_file(None)
    assert result is None


# Test if unsupported file types (e.g., .pdf) returns None
def test_read_unsupported_file_type():

    fake_pdf = BytesIO(b"%PDF-1.4 content here")
    fake_pdf.name = "example.pdf"

    result = read_uploaded_file(fake_pdf)
    assert result is None


# Test uploading a .docx file and verifies the extracted paragraph text
def test_read_uploaded_docx_file():

    # Create a temporary Word document in memory
    doc = Document()
    doc.add_paragraph("The system shall log off after 10 minutes.")
    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)  # reset pointer to the beginning
    doc_io.name = "sample.docx"  # simulate uploaded file name

    result = read_uploaded_file(doc_io)
    assert "log off after 10 minutes" in result


# Test docx TOC detection logic
def test_is_docx_toc_paragraph_detection():
    toc_mock = SimpleNamespace(style=SimpleNamespace(name="TOC 1"))
    real_mock = SimpleNamespace(style=SimpleNamespace(name="Heading 1"))

    assert is_docx_toc_paragraph(toc_mock) is True
    assert is_docx_toc_paragraph(real_mock) is False


# Test .txt file upload using Flask-style `.filename` instead of `.name`
def test_read_uploaded_txt_file_flask_style():
    fake_txt = BytesIO(b"The system shall shut down securely.")
    fake_txt.filename = "example.txt"  # simulate Flask-style upload
    result = read_uploaded_file(fake_txt)
    assert "shut down securely" in result
