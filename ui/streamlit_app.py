"""
Streamlit-based UI for SpecSense.

Allows users to input SRS text and view extracted section headers and content.
"""

import streamlit as st
import json
from app.parser import parse_sections_with_bodies
from app.formatter import format_llm_response
from app.llm import analyze_requirement, suggest_tests
from app.export import format_analysis_as_markdown
from app.file_reader import read_uploaded_file
from ui.components import render_section_result
from app.traceability import (
    build_traceability_index,
    export_traceability_as_json,
    export_traceability_as_csv,
)


def main():
    """Renders the Streamlit UI and handles user interaction."""

    # Title and instructions at top of app
    st.title(" SpecSense – SRS Section Analyzer")
    st.markdown(
        "_Upload a file or paste text below. If both are provided, the uploaded file will be used._"
    )

    # Button to enable the TOC comparison
    with st.sidebar:
        st.header("Settings")
        use_llm_fuzzy = st.checkbox(
            " Enable LLM fuzzy TOC comparison",
            value=False,
            help="Uses GPT-4 to identify approximate matches between your document's TOC and a known standard. May be slower.",
        )

    # Upload option first
    uploaded_file = st.file_uploader(
        "Upload a .txt or .docx SRS file", type=["txt", "docx"]
    )
    if uploaded_file:
        is_docx = uploaded_file.name.lower().endswith(".docx")

    # Allow user to run a structural conformance check (TOC vs standard template)
    # This is a shallow structure check, not content-based or semantic yet
    if st.button("Run Structure Check"):
        from app.structure_check import run_structure_check

        # Dispatch to structure_check.py, which extracts TOC lines and compares to STANDARD_TOC
        toc_result = run_structure_check(uploaded_file, is_docx, use_llm=use_llm_fuzzy)
        display_structure_check_results(toc_result)
        # Rewind the file stream so it can be re-used later by read_uploaded_file()
        uploaded_file.seek(0)
    document_text = read_uploaded_file(uploaded_file)

    # Paste fallback only if no file uploaded
    if document_text is None:
        document_text = st.text_area("SRS Document Text", height=300)

    # Run parser + analysis on button click
    if st.button("Analyze"):
        if not document_text or not document_text.strip():
            st.warning("Please provide SRS content either via upload or paste.")
            return

        # Step 1: Parse SRS into sections (headers + body content)
        results = parse_sections_with_bodies(document_text)
        st.session_state["parsed_sections"] = results
        st.success(f"Found {len(results)} sections.")

        # Step 2: Analyze each section via LLM and format results
        analysis_results = {}
        for section in results:
            body = section["body"]

            # Run analysis first
            analysis = analyze_requirement(body)
            formatted = format_llm_response(analysis)

            # Only call suggest_tests if analysis was actually performed
            if "Skipped analysis" in analysis:
                test_suggestions = "⚠️ Skipped: section too short or empty."
            else:
                test_suggestions = suggest_tests(body)

            analysis_results[section["title"]] = {
                "id": section.get("id"),
                "title": section["title"],
                "body": body,
                "analysis": formatted,
                "raw": analysis,
                "tests": test_suggestions,
            }
        st.session_state["analysis_results"] = analysis_results
        # Optional: View raw analysis result dictionary
        with st.expander(" Debug: Raw Analysis Output"):
            st.json(analysis_results)

        # Step 3: Render each section + analysis
        st.markdown("###  Analyzed Sections")

        # Loop over analyzed sections
        for title, result in analysis_results.items():
            render_section_result(title, result)

        # Summary teaser (still in main content flow)
        st.markdown("###  Summary (Coming Soon)")
        st.info(
            "We're working on a cross-section analysis view to summarize risks and themes."
        )

        # === Export Section ===
        st.markdown("### Download Analysis Output")

        # Generate Markdown + JSON content
        markdown_output = format_analysis_as_markdown(analysis_results)
        json_output = json.dumps(analysis_results, indent=2)

        # Markdown download button
        st.download_button(
            label="Download as Markdown",
            data=markdown_output,
            file_name="specsense_output.md",
            mime="text/markdown",
        )

        # JSON download button
        st.download_button(
            label="Download as JSON",
            data=json_output,
            file_name="specsense_output.json",
            mime="application/json",
        )

        st.markdown("---")
    # === Traceability Export Button Flow ===
    if st.button("Generate Traceability Export"):
        if "parsed_sections" in st.session_state:
            trace_index = build_traceability_index(st.session_state["parsed_sections"])
            trace_json = export_traceability_as_json(trace_index)
            trace_csv = export_traceability_as_csv(trace_index)

            st.markdown("### Download Requirement Traceability")

            st.download_button(
                label="Download Traceability (JSON)",
                data=trace_json,
                file_name="traceability.json",
                mime="application/json",
            )

            st.download_button(
                label="Download Traceability (CSV)",
                data=trace_csv,
                file_name="traceability.csv",
                mime="text/csv",
            )
        else:
            st.warning("Please run analysis first to extract requirements.")

        # Visual end-of-analysis divider
        st.divider()


def display_structure_check_results(result: dict):
    """
    Render the TOC comparison results in a collapsible UI format.
    Sections are grouped as:
      - matched (found in both doc and standard)
      - missing (expected but not present)
      - extra (present but not expected)
    """
    st.subheader("📋 TOC Conformance Result")
    if "strict_comparison" in result:
        strict_result = result["strict_comparison"]
    else:
        strict_result = result

    with st.expander("✅ Matched Sections"):
        if strict_result["matched"]:
            for line in strict_result["matched"]:
                st.markdown(f"- {line}")
        else:
            st.info("No matching sections found.")

    with st.expander("⚠️ Missing Sections"):
        if strict_result["missing"]:
            for line in strict_result["missing"]:
                st.markdown(f"- {line}")
        else:
            st.success("No missing sections.")

    with st.expander("❗ Extra Sections"):
        if strict_result["extra"]:
            for line in strict_result["extra"]:
                st.markdown(f"- {line}")
        else:
            st.success("No extra sections found.")

    if "llm_fuzzy_comparison" in result:
        with st.expander("🧠 LLM Fuzzy Match Results"):
            st.markdown(result["llm_fuzzy_comparison"])


# execute main UX code
if __name__ == "__main__":
    main()
