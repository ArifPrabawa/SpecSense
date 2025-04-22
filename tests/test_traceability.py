from app.traceability import (
    build_traceability_index,
    export_traceability_as_csv,
    export_traceability_as_json,
)
import json


# Test that build_traceability_index correctly maps requirement IDs to section context
def test_build_traceability_index():
    # Simulate the output from parse_sections_with_bodies
    sections = [
        {
            "id": "5.1",
            "title": "Authentication",
            "body": "REQ-1 The system shall log out after 10 minutes.",
            "requirements": [
                {
                    "id": "REQ-1",
                    "text": "REQ-1 The system shall log out after 10 minutes.",
                }
            ],
        },
        {
            "id": "5.2",
            "title": "Persistence",
            "body": "REQ-2 User settings shall persist.",
            "requirements": [
                {"id": "REQ-2", "text": "REQ-2 User settings shall persist."}
            ],
        },
    ]

    # Call the function you're testing
    index = build_traceability_index(sections)

    # Assertions
    assert "REQ-1" in index
    assert "REQ-2" in index

    assert index["REQ-1"]["section_id"] == "5.1"
    assert index["REQ-1"]["section_title"] == "Authentication"
    assert index["REQ-1"]["text"] == "REQ-1 The system shall log out after 10 minutes."

    assert index["REQ-2"]["section_id"] == "5.2"
    assert index["REQ-2"]["section_title"] == "Persistence"
    assert index["REQ-2"]["text"] == "REQ-2 User settings shall persist."


# Test that traceability export produces valid JSON with expected structure
def test_export_traceability_as_json():
    index = {
        "REQ-1": {
            "section_id": "5.1",
            "section_title": "Authentication",
            "text": "REQ-1 The system shall log out after 10 minutes.",
        },
        "REQ-2": {
            "section_id": "5.2",
            "section_title": "Persistence",
            "text": "REQ-2 User settings shall persist.",
        },
    }

    output = export_traceability_as_json(index)

    # Ensure it's valid JSON
    parsed = json.loads(output)
    assert "REQ-1" in parsed
    assert parsed["REQ-1"]["section_title"] == "Authentication"
    assert parsed["REQ-2"]["text"] == "REQ-2 User settings shall persist."


# Test that traceability export produces a valid CSV with header and rows
def test_export_traceability_as_csv():
    index = {
        "REQ-1": {
            "section_id": "5.1",
            "section_title": "Authentication",
            "text": "REQ-1 The system shall log out after 10 minutes.",
        },
        "REQ-2": {
            "section_id": "5.2",
            "section_title": "Persistence",
            "text": "REQ-2 User settings shall persist.",
        },
    }

    output = export_traceability_as_csv(index)

    # Split into lines and check headers and row content
    lines = output.strip().splitlines()
    assert lines[0] == "requirement_id,section_id,section_title,text"
    assert "REQ-1" in lines[1]
    assert "REQ-2" in lines[2]
