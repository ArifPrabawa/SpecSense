from app.export import (
    format_analysis_as_markdown,
    generate_requirement_summary,
    extract_requirement_lines,
    generate_requirement_summary_from_sections,
)

# tests/test_export.py  (append)
from app.export import format_traceability_as_markdown


# Test that format_analysis_as_markdown returns correctly structured Markdown
# for a single analyzed section, including all required headers and content blocks.
def test_format_analysis_as_markdown_output():
    # Minimal mock data
    mock_data = {
        "5.1 Auto Log-Off": {
            "id": "5.1",
            "title": "Auto Log-Off",
            "body": "The system shall log off after 10 minutes.",
            "analysis": "This is a time-based session control requirement.",
            "tests": "- Verify auto log-off after 10 min\n- Check session is cleared",
        }
    }

    markdown = format_analysis_as_markdown(mock_data)

    assert "# SpecSense Analysis" in markdown
    assert "## 5.1 Auto Log-Off" in markdown
    assert "### Raw Section Body" in markdown
    assert "The system shall log off after 10 minutes." in markdown
    assert "### Suggested Tests" in markdown
    assert "- Verify auto log-off" in markdown
    assert "---" in markdown  # Divider line


# Test that format_analysis_as_markdown works for multiple sections.
def test_format_analysis_as_markdown_multiple_sections():
    sample = {
        "5.1 Auto Log-Off": {
            "id": "5.1",
            "title": "Auto Log-Off",
            "body": "Logs out after 10 minutes.",
            "analysis": "Covers session timeout behavior.",
            "tests": "- Trigger inactivity\n- Confirm logout",
        },
        "5.2 Password Policy": {
            "id": "5.2",
            "title": "Password Policy",
            "body": "Passwords must be at least 8 characters.",
            "analysis": "Requirement enforces minimal complexity.",
            "tests": "- Try 7-char password\n- Try 8-char password",
        },
    }

    markdown = format_analysis_as_markdown(sample)

    # Check both sections are included
    assert "## 5.1 Auto Log-Off" in markdown
    assert "## 5.2 Password Policy" in markdown

    # Check that both sets of content made it in
    assert "Logs out after 10 minutes." in markdown
    assert "Passwords must be at least 8 characters." in markdown

    # Check both dividers are there (should be one per section)
    assert markdown.count("---") == 2


# Test that format_analysis_as_markdown works with empty fields.
def test_format_analysis_handles_empty_fields():
    sample = {
        "5.3 Incomplete": {
            "id": "5.3",
            "title": "Incomplete",
            "body": "Some requirement text.",
            "analysis": "",
            "tests": "",
        }
    }

    markdown = format_analysis_as_markdown(sample)

    assert "## 5.3 Incomplete" in markdown
    assert "Some requirement text." in markdown
    assert "### LLM Analysis" in markdown
    assert "### Suggested Tests" in markdown
    assert markdown.count("---") == 1


# ✅ Test summary output when all expected groups are present and no gaps exist
def test_generate_summary_with_all_groups_and_no_gaps():
    grouped = {
        "Authentication": [{"id": "REQ-1"}, {"id": "REQ-2"}],
        "Security": [{"id": "REQ-3"}],
    }
    gaps = []

    summary = generate_requirement_summary(grouped, gaps)

    assert "Authentication" in summary
    assert "Security" in summary
    assert "✅ All expected categories are present." in summary


# ✅ Test summary output when some expected categories are missing
def test_generate_summary_with_missing_categories():
    grouped = {"Authentication": [{"id": "REQ-1"}]}
    gaps = ["Security", "Error Handling"]

    summary = generate_requirement_summary(grouped, gaps)

    assert "Authentication" in summary
    assert "Security" in summary
    assert "Error Handling" in summary
    assert "⚠️ Missing Requirement Categories" in summary


# ✅ Test summary output when no requirements were grouped at all
def test_generate_summary_with_no_grouped_requirements():
    grouped = {}
    gaps = ["Authentication", "Security"]

    summary = generate_requirement_summary(grouped, gaps)

    assert "No grouped requirements found." in summary
    assert "Authentication" in summary
    assert "Security" in summary


# ✅ Test for REQ-xxx extraction from section bodies
def test_extract_requirement_lines():
    sections = [
        {"body": "REQ-1 The system shall authenticate.\nREQ-2 The system shall retry."},
        {"body": "No requirements here."},
    ]
    extracted = extract_requirement_lines(sections)
    assert len(extracted) == 2
    assert extracted[0]["id"] == "REQ-1"
    assert "authenticate" in extracted[0]["text"]


# ✅ Test the full top-level UI-facing function
def test_generate_summary_from_sections():
    sections = [
        {
            "body": "REQ-1 The system shall authenticate users.\nREQ-2 The system must handle errors."
        }
    ]
    summary = generate_requirement_summary_from_sections(sections)
    assert "Authentication" in summary
    assert "Error Handling" in summary


def test_format_traceability_as_markdown_basic():
    sections = [
        {
            "id": None,
            "title": "Login",
            "requirements": [{"id": "REQ-1", "text": "Login shall..."}],
        },
        {
            "id": None,
            "title": "Logout",
            "requirements": [{"id": "REQ-2", "text": "Logout shall..."}],
        },
    ]
    md = format_traceability_as_markdown(sections)
    assert "| REQ-1 | Login |" in md
    assert "| REQ-2 | Logout |" in md
