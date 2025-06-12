# Standard library imports (always first)
import sys
import os
from flask import Blueprint, render_template, request, Response

# Add project root to sys.path for outer app/ imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Internal imports (after sys.path fix)
from app.parser import parse_sections_with_bodies  # noqa: E402
from app.llm import analyze_requirement, suggest_tests  # noqa: E402
from app.export import format_traceability_as_markdown  # noqa:E402
from app.utils import validate_and_read_upload  # noqa:E402

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
    try:
        filename, file_text = validate_and_read_upload(request)
    except ValueError as e:
        return f"Error: {e}", 400

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
    try:
        filename, file_text = validate_and_read_upload(request)
    except ValueError as e:
        return f"Error: {e}", 400

    parsed_sections = parse_sections_with_bodies(file_text)
    trace_md = format_traceability_as_markdown(parsed_sections)

    return Response(
        trace_md,
        mimetype="text/markdown",
        headers={
            "Content-Disposition": f"attachment; filename={filename}_traceability.md"
        },
    )
