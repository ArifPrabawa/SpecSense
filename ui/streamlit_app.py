"""
Streamlit-based UI for SpecSense.

Allows users to input SRS text and view extracted section headers and content.
"""

import streamlit as st
from app.parser import parse_sections_with_bodies
from app.formatter import format_llm_response
from app.llm import analyze_requirement

def main():
    """Renders the Streamlit UI and handles user interaction."""
    
    # Title and description
    st.title("📄 SpecSense – SRS Section Analyzer")
    st.markdown(
        "Use this tool to extract structured sections from Software Requirements Specification (SRS) documents. "
        "Paste raw text below and hit **Parse Sections** to view the breakdown."
    )


    # Placeholder input field
    user_input = st.text_area("SRS Document Text", height=300)

    # Trigger parsing on button click
    if st.button("Parse Sections"):
        if not user_input.strip():
            st.warning("Please paste some SRS content before parsing.")
            return

         # Call parser and render results
        results = parse_sections_with_bodies(user_input)
        st.success(f"Found {len(results)} sections.")
        for section in results:
            with st.expander(section["title"]):
                st.markdown(f"```\n{section['body']}\n```")
                analysis = analyze_requirement(section['body'])
                if "Skipped analysis" in analysis:
                    st.info(analysis)
                else:
                    formatted = format_llm_response(analysis)
                    st.markdown(formatted)

        # Add divider after the output
        st.divider()

if __name__ == "__main__":
    main()
