"""
Handles communication with OpenAI's API for analyzing requirement clarity.
"""
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_requirement(text: str) -> str:
    """
    Sends a requirement string to the OpenAI API and returns its analysis.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're an expert in software and systems engineering. "
                    "Analyze the following requirement for ambiguity, vagueness, or anything that would make it hard to test."
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
