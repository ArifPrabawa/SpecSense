"""
Tests for keyword-based requirement grouping logic.
"""

from app.requirement_grouper import group_requirements, detect_gaps


# Should group requirements into expected categories based on keyword matches
def test_group_requirements_keyword_match():
    requirements = [
        {
            "requirement_id": "REQ-1",
            "text": "The system shall allow users to login securely.",
        },
        {
            "requirement_id": "REQ-2",
            "text": "The system must retry if an error occurs.",
        },
        {
            "requirement_id": "REQ-3",
            "text": "All data shall be stored with encryption.",
        },
        {"requirement_id": "REQ-4", "text": "The system shall save user records."},
        {
            "requirement_id": "REQ-5",
            "text": "This is unrelated and should not be grouped.",
        },
    ]

    grouped = group_requirements(requirements)

    assert "REQ-1" in [r["requirement_id"] for r in grouped["Authentication"]]
    assert "REQ-2" in [r["requirement_id"] for r in grouped["Error Handling"]]
    assert "REQ-3" in [r["requirement_id"] for r in grouped["Security"]]
    assert "REQ-4" in [r["requirement_id"] for r in grouped["Data Handling"]]
    assert all(
        "REQ-5" not in [r["requirement_id"] for r in group]
        for group in grouped.values()
    )


def test_group_requirements_and_gaps():
    requirements = [
        {"id": "REQ-1", "text": "The system shall authenticate users securely."},
        {"id": "REQ-2", "text": "The system must retry on error."},
        {"id": "REQ-3", "text": "Data shall be saved securely."},
    ]

    # Group the requirements
    grouped = group_requirements(requirements)

    # Detect gaps
    gaps = detect_gaps(grouped)

    # Assertions
    assert "Security" in grouped
    assert "Error Handling" in grouped
    assert "Data Handling" in grouped
    assert "Authentication" in grouped

    # No missing categories should be found
    assert gaps == []
