import re


def format_llm_response(text: str) -> str:
    """
    Cleans and formats raw LLM output to ensure it's readable in Markdown or plain text.
    Removes duplicate lines, standardizes section headers, and formats bullets.
    """
    lines = text.strip().splitlines()
    cleaned = []
    seen = set()

    for line in lines:
        line = line.strip()

        if not line or line in seen:
            continue  # skip empty or duplicate lines
        seen.add(line)

        # Normalize and clean markdown bolds
        line = re.sub(r"\*{3,}", "**", line)
        if line.count("**") == 1:
            line = line.replace("**", "")

        # Match common section header format like "- Ambiguity:"
        if line.startswith("- ") and line.endswith(":") and len(line) < 30:
            label = line.lstrip("- ").rstrip(":").strip()
            cleaned.append(f"\n**{label}:**")
        else:
            cleaned.append(line)

    return "\n".join(cleaned).strip()
