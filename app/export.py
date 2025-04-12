def format_analysis_as_markdown(results: dict) -> str:
    """
    Converts the analyzed results into Markdown format for export.
    """
    output = ["# SpecSense Analysis\n"]

    # Loop through each section and format its content
    for title, data in results.items():
        output.append(f"## {title}\n")
        output.append("### Raw Requirement\n")
        output.append(f"```\n{data['body']}\n```\n")

        output.append("### LLM Analysis\n")
        output.append(f"{data['analysis']}\n")

        output.append("### Suggested Test Cases\n")
        output.append(f"{data['tests']}\n")

        output.append("---\n")

    return "\n".join(output)