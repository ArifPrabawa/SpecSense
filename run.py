"""
Manual dev script to test parser and LLM integration.
"""

from app.parser import parse_sections_with_bodies
from app.llm import analyze_requirement, format_llm_response


def main():
    sample_text = """# Introduction
This document outlines the system.

1. Purpose
The system shall allow access via fingerprint or password.

SYSTEM OVERVIEW
The system should be fast and user-friendly.
"""

    print("Parsing sections...\n")
    sections = parse_sections_with_bodies(sample_text)

    for section in sections:
        print(f"== {section['title']} ==")
        print(section['body'])
        print()

        print("-- LLM Analysis --")
        try:
            result = analyze_requirement(section["body"])
            formatted = format_llm_response(result)
            print(formatted)

        except Exception as e:
            print(f"[ERROR] Failed to analyze section: {e}")
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()