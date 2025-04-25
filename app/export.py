import re
from app.requirement_grouper import group_requirements, detect_gaps
from app.llm import llm_group_requirement


def format_analysis_as_markdown(analysis_results: dict) -> str:
    """
    Formats the full analysis result as Markdown.
    Uses Markdown heading levels for clean export and structured viewing.
    """
    md = "# SpecSense Analysis\n\n"

    for title, data in analysis_results.items():
        display_title = (
            f"{data['id']} {data['title']}" if data.get("id") else data["title"]
        )
        md += f"## {display_title}\n\n"

        # Body block
        md += "### Raw Section Body\n\n"
        md += f"```\n{data.get('body', '').strip()}\n```\n\n"

        # LLM analysis
        md += "### LLM Analysis\n\n"
        if "Skipped" in data.get("raw", ""):
            md += f"> ⚠️ {data.get('raw', 'Analysis skipped.')}\n\n"
        else:
            md += f"{data.get('analysis', '').strip()}\n\n"

        # Test suggestions
        md += "### Suggested Tests\n\n"
        if "Skipped" in data.get("tests", ""):
            md += f"> ⚠️ {data.get('tests', 'Tests skipped.')}\n\n"
        else:
            md += f"{data.get('tests', '').strip()}\n\n"

        md += "---\n\n"

    return md.strip()


def extract_requirement_lines(sections: list[dict]) -> list[dict]:
    """
    Extracts individual REQ-xxx lines from section bodies.
    Returns a list of dicts like {"id": "REQ-1", "text": "..."}
    """
    reqs = []
    for section in sections:
        lines = section.get("body", "").splitlines()
        for line in lines:
            if match := re.match(r"(REQ-\d+)\s+(.*)", line.strip()):
                reqs.append({"id": match.group(1), "text": match.group(2)})
    return reqs


def generate_requirement_summary_from_sections(parsed_sections: list[dict]) -> str:
    """
    UI-facing summary generator.
    Accepts parsed sections and processes internally.
    """
    reqs = extract_requirement_lines(parsed_sections)
    grouped = group_requirements(reqs)
    gaps = detect_gaps(grouped)
    return generate_requirement_summary(grouped, gaps)


def generate_requirement_summary(grouped: dict, gaps: list) -> str:
    """
    Logic-facing summary generator for grouped requirements and detected gaps.
    Keeps testability and separation of concerns.
    """
    lines = []

    if grouped:
        lines.append("### 📊 Grouped Requirements:")
        for category, items in grouped.items():
            lines.append(f"- **{category}**: {len(items)} requirement(s)")
    else:
        lines.append("No grouped requirements found.")

    lines.append("")

    if gaps:
        lines.append("### ⚠️ Missing Requirement Categories:")
        for gap in gaps:
            lines.append(f"- {gap}")
    else:
        lines.append("✅ All expected categories are present.")

    return "\n".join(lines)


def group_requirements_with_llm(parsed_sections: list[dict]) -> list[dict]:
    """
    Extracts REQ lines and assigns LLM-based semantic groupings.

    Args:
        parsed_sections (list[dict]): Parsed section data with body text.

    Returns:
        list[dict]: List of REQs with LLM-assigned groups (id, text, llm_group).
    """
    reqs = extract_requirement_lines(parsed_sections)
    enriched = []

    for req in reqs:
        groups = llm_group_requirement(req["text"])
        enriched.append({"id": req["id"], "text": req["text"], "llm_group": groups})

    return enriched
