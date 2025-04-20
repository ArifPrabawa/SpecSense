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
        md += f"### Raw Section Body\n\n"
        md += f"```\n{data.get('body', '').strip()}\n```\n\n"

        # LLM analysis
        md += f"### LLM Analysis\n\n"
        if "Skipped" in data.get("raw", ""):
            md += f"> ⚠️ {data.get('raw', 'Analysis skipped.')}\n\n"
        else:
            md += f"{data.get('analysis', '').strip()}\n\n"

        # Test suggestions
        md += f"### Suggested Tests\n\n"
        if "Skipped" in data.get("tests", ""):
            md += f"> ⚠️ {data.get('tests', 'Tests skipped.')}\n\n"
        else:
            md += f"{data.get('tests', '').strip()}\n\n"

        md += "---\n\n"

    return md.strip()
