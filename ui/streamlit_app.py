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
    
    # Title and instructions at top of app
    st.title("📄 SpecSense – SRS Section Analyzer")
    st.markdown(
        "Use this tool to extract structured sections from Software Requirements Specification (SRS) documents. "
        "Paste raw text below and hit **Parse Sections** to view the breakdown."
    )


    # Placeholder input field
    user_input = st.text_area("SRS Document Text", height=300)

    # Run parser + analysis on button click
    if st.button("Analyze"):
        if not user_input.strip():
            st.warning("Please paste some SRS content before parsing.")
            return

         # Step 1: Parse SRS into sections (headers + body content)
        results = parse_sections_with_bodies(user_input)
        st.success(f"Found {len(results)} sections.")
        
        # Step 2: Analyze each section via LLM and format results
        analysis_results = {}
        for section in results:
            body = section["body"]
            analysis = analyze_requirement(body)
            formatted = format_llm_response(analysis)
            analysis_results[section["title"]] = {
                "body": body,
                "analysis": formatted,
                "raw": analysis
            }
            
        # Optional: View raw analysis result dictionary
        with st.expander("🔍 Debug: Raw Analysis Output"):
            st.json(analysis_results)
            
        # Step 3: Render each section + analysis
        st.markdown("### ✅ Analyzed Sections")
        
        # Loop over analyzed sections
        for title, result in analysis_results.items():
            st.markdown(f"---")  # Divider line
            with st.expander(f"📘 {title}"):
                st.markdown("#### 📄 Raw Section Body")
                st.markdown(f"```\n{result['body']}\n```")

                #Check for skipped analysis
                st.markdown("#### 🤖 LLM Analysis")
                if "Skipped analysis" in result["raw"]:
                    st.info(result["raw"])
                else:
                    st.markdown(result["analysis"])
                    
        # Summary teaser (still in main content flow)
        st.markdown("### 🧠 Summary (Coming Soon)")
        st.info("We're working on a cross-section analysis view to summarize risks and themes.")
        
        # Visual end-of-analysis divider
        st.divider()

#execute main UX code
if __name__ == "__main__":
    main()
