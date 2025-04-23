"""Requirement grouping logic for SpecSense based on keyword themes."""

from typing import List, Dict


def get_requirement_categories() -> dict:
    """
    Returns a dictionary with requirement categories and their associated keywords.
    This is the single source of truth for both grouping and expected categories.
    """
    return {
        "Authentication": [
            "login",
            "authenticate",
            "password",
            "credentials",
            "access",
        ],
        "Error Handling": ["fail", "error", "retry", "invalid", "exception"],
        "Security": [
            "encrypt",
            "encryption",
            "access control",
            "confidentiality",
            "authorization",
        ],
        "Data Handling": [
            "save",
            "load",
            "store",
            "record",
            "retrieve",
            "transmit",
            "data",
            "backup",
        ],
    }


def group_requirements(requirements: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group requirements by scanning for keyword matches in the text.
    Requirements may be added to multiple groups if multiple keywords match.

    Args:
        requirements (List[Dict]): List of requirement dictionaries.

    Returns:
        dict: Grouped requirements by category.
    """
    categories = get_requirement_categories()  # Get both categories and their keywords
    grouped: Dict[str, List[Dict]] = {category: [] for category in categories}

    for req in requirements:
        text = req.get("text", "").lower()
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                grouped[category].append(req)

    return grouped


def detect_gaps(grouped_requirements: dict) -> list:
    """
    Detects missing requirement categories based on the grouped requirements.

    Args:
        grouped_requirements (dict): The current grouped requirements.

    Returns:
        list: A list of missing requirement categories.
    """
    categories = get_requirement_categories()
    expected = list(categories.keys())

    return [
        cat
        for cat in expected
        if cat not in grouped_requirements or not grouped_requirements[cat]
    ]
