"""
Handles communication with OpenAI's API for analyzing requirement clarity.
"""
from openai import OpenAI
import os, re
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

        try:
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Unexpected LLM response format: {str(e)}"
    
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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
        )

        try:
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Unexpected LLM response format: {str(e)}"
    
    except Exception as e:
        return f"OpenAI error: {str(e)}"

