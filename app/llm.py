"""
Handles communication with OpenAI's API for analyzing requirement clarity.
"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def get_client():

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key is None or api_key.strip() == "":
        raise ValueError("OpenAI API key not set")

    return OpenAI(api_key=api_key)


def analyze_requirement(text: str) -> str:
    """
    Sends a requirement string to the OpenAI API and returns its analysis.
    """

    # Skip empty input
    text = text.strip()
    if not text or len(text.strip()) < 20:
        return "Skipped analysis — section too short or empty."

    # LLM call to generate analysis
    try:
        response = get_client().chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're an expert in software and systems engineering. "
                        "Analyze the following requirement for ambiguity, vagueness, or anything that would make it hard to test."
                        "provide the explanation concisely and in plain terms, with bullet points as necessary."
                    ),
                },
                {"role": "user", "content": text},
            ],
            temperature=0.2,
            max_tokens=300,
        )

        content = response.choices[0].message.content
        if not content or not isinstance(content, str):
            return "⚠️ Unexpected LLM response format"
        return content.strip()

    except Exception as e:
        return f"OpenAI error: {str(e)}"


def suggest_tests(section_text: str) -> str:
    """
    Calls the LLM to suggest test ideas for a given requirement section.
    """
    prompt = (
        "Based on the following software requirement, suggest test cases. "
        "Be concise. Use bullet points.\n\n"
        f"Requirement:\n{section_text}"
    )

    try:
        response = get_client().chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
        )

        content = response.choices[0].message.content
        if not content or not isinstance(content, str):
            return "⚠️ Unexpected LLM response format"
        return content.strip()

    except Exception as e:
        return f"OpenAI error: {str(e)}"


def compare_toc_sections_with_llm(
    standard_sections: list[str], document_sections: list[str]
) -> str:
    """
    Use an LLM to compare the document's TOC sections against a known standard TOC structure,
    allowing for fuzzy matching. This helps detect sections that are semantically similar but
    differ in naming, order, or phrasing.

    Args:
        standard_sections (list of str): The expected section titles from a standard TOC (e.g., ISO/IEC 29148).
        document_sections (list of str): The section titles extracted from the user's document.

    Returns:
        str: A Markdown-formatted string describing alignment, mismatches, and approximate matches,
             or an error message if the LLM call fails.
    """
    try:
        if not standard_sections or not document_sections:
            return "⚠️ Skipped: one or both TOC lists are empty."

        prompt = (
            "You are reviewing a software requirements document.\n\n"
            "Compare the user's Table of Contents (TOC) against the provided standard structure.\n"
            "Classify each standard section as:\n"
            "- **Matched**: appears identically in the document TOC\n"
            "- **Fuzzy Matched**: meaning is close but the wording, numbering, or spelling differs\n"
            "- **Missing**: not present or not reasonably aligned\n\n"
            "Be tolerant of spelling mistakes (e.g., 'Pupose' vs 'Purpose') and section number differences (e.g., '5.1.1' vs '1.1').\n\n"
            "**Each standard section must appear in exactly one category. If a section is fuzzy matched, do not include it in the Missing list.**\n\n"
            "Only output the grouped results using the following Markdown structure:\n\n"
            "Matched Sections:\n"
            "- section name\n\n"
            "Fuzzy Matched Sections:\n"
            "- section name (Fuzzy match to: 'document section name')\n\n"
            "Missing Sections:\n"
            "- section name\n\n"
            f"Standard TOC:\n{chr(10).join(f'- {s}' for s in standard_sections)}\n\n"
            f"Document TOC:\n{chr(10).join(f'- {s}' for s in document_sections)}"
        )

        response = get_client().chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful requirements engineering assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content
        if not content or not isinstance(content, str):
            return "⚠️ Unexpected LLM response format"
        return content.strip()
    except Exception as e:
        return f"OpenAI error: {str(e)}"
