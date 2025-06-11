# Standard library imports (always first)
import sys
import os
from flask import Blueprint, render_template, request, Response

# Add project root to sys.path for outer app/ imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Internal imports (after sys.path fix)
from app.file_reader import read_uploaded_file  # noqa: E402
from app.parser import parse_sections_with_bodies  # noqa: E402
from app.llm import analyze_requirement, suggest_tests  # noqa: E402
from app.export import format_traceability_as_markdown  # noqa:E402

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """
    Home route that renders the file upload form.
    """
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload_file():
    """
    Handles file upload from the form on the index page.
    Validates input, prepares for processing by parser and reader.
    """
    uploaded_file = request.files.get("srs_file")

    # Check if a file was actually uploaded
    if not uploaded_file or uploaded_file.filename == "":
        # Optionally use `flash()` for message passing if needed later
        return "Error: No file selected.", 400

    # Validate file extension (only .txt or .docx allowed)
    filename = uploaded_file.filename.lower()
    if not (filename.endswith(".txt") or filename.endswith(".docx")):
        return "Error: Only .txt or .docx files are supported.", 400

    # At this point, the file is valid and ready to be processed

    # Decode the uploaded file into raw text
    file_text = read_uploaded_file(uploaded_file)

    if file_text is None:
        return "Error: Could not read or decode the uploaded file.", 400

    # Parse the raw text into structured sections
    parsed_sections = parse_sections_with_bodies(file_text)

    for section in parsed_sections:
        body_text = section.get("body", "").strip()
        section["analysis"] = analyze_requirement(body_text)
        section["test_suggestions"] = suggest_tests(body_text)

    # Pass the parsed results into the parsed.html template
    return render_template(
        "parsed.html",
        sections=parsed_sections,
        filename=filename,
        file_text=file_text,  # 🆕  pass raw contents
    )


@main.route("/traceability", methods=["POST"])
def generate_traceability():
    uploaded_file = request.files.get("srs_file")
    raw_text = request.form.get("srs_text")

    if uploaded_file:
        file_text = read_uploaded_file(uploaded_file)
        filename = uploaded_file.filename.lower()
        if not (filename.endswith(".txt") or filename.endswith(".docx")):
            return "Error: Only .txt or .docx files are supported.", 400
    elif raw_text:
        file_text = raw_text
        filename = "traceability"
    else:
        return "Error: No file selected.", 400

    parsed_sections = parse_sections_with_bodies(file_text)
    trace_md = format_traceability_as_markdown(parsed_sections)

    return Response(
        trace_md,
        mimetype="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_traceability.md"
        },
    )
