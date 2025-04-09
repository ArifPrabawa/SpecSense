"""
Handles communication with OpenAI's API for analyzing requirement clarity.
"""
from openai import OpenAI
import os, re
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_requirement(text: str) -> str:
    """
    Sends a requirement string to the OpenAI API and returns its analysis.
    """
    text = text.strip()
    if not text or len(text.strip()) < 20:
        return "Skipped analysis — section too short or empty."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're an expert in software and systems engineering. "
                        "Analyze the following requirement for ambiguity, vagueness, or anything that would make it hard to test."
                        "provide the explanation concisely and in plain terms, with bullet points as necessary."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.2,
            max_tokens=300
        )   

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"OpenAI error: {str(e)}"

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

        # Remove all bolding asterisks safely (beginning or inline)
        line = re.sub(r"\*{2,}", "", line)

        # Match common section header format like "- Ambiguity:"
        if line.startswith("- ") and line.endswith(":") and len(line) < 30:
            label = line.lstrip("- ").rstrip(":").strip()
            cleaned.append(f"\n**{label}:**")
        else:
            cleaned.append(line)

    return "\n".join(cleaned).strip()
