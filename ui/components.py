import streamlit as st

def render_section_result(title: str, result: dict):
    """
    Renders a parsed section and its LLM analysis in an expandable Streamlit block.
    
    Args:
        title (str): Section title (e.g., '5.1.2 Overview')
        result (dict): Output from parser + LLM, with keys:
            - id
            - title
            - body
            - analysis
            - raw (original LLM output)
            - tests (suggested tests)
    """
    st.markdown("---")  # Divider line
    section_title = f"{result['id']} {title}" if result.get("id") else title

    with st.expander(section_title):
        st.markdown("#### Raw Section Body")
        st.markdown(f"```\n{result['body']}\n```")

        st.markdown("#### LLM Analysis")
        if "Skipped analysis" in result["raw"]:
            st.info(result["raw"])
        else:
            st.markdown(result["analysis"])
        

        st.markdown("#### Suggested Tests")
        if "Skipped analysis" in result["raw"]:
            st.info("Tests not generated due to skipped analysis.")
        else:
            st.markdown(result["tests"])