def format_analysis_as_markdown(results: dict) -> str:
    """
    Converts the analyzed results into Markdown format for export.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    output = [f"# SpecSense Analysis\n\n_Exported {timestamp}_\n"]

    # Loop through each section and format its content
    for title, data in results.items():
        display_title = f"{data['id']} {data['title']}" if data['id'] else data['title']
        output.append(f"## {display_title}\n")
        output.append("### Raw Requirement\n")
        output.append(f"```\n{data['body']}\n```\n")

        output.append("### LLM Analysis\n")
        output.append(f"```\n{data['analysis']}\n```\n")

        output.append("### Suggested Test Cases\n")
        output.append(f"```\n{data['tests']}\n```\n")

        output.append("---\n")

    return "\n".join(output)

