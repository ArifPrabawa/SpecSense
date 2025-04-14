## [v0.3.0] - 2025-04-14

### Added
- Upload support for `.txt` and `.docx` SRS files via Streamlit UI
- Utility function `read_uploaded_file()` for clean decoding and fallback
- LLM test suggestion logic now respects skipped analysis cases
- Unit tests for all file upload scenarios (valid, invalid, none)

### Fixed
- Removed hallucinated test cases for empty or malformed sections
- JSON and Markdown outputs now cleanly reflect analysis skips

### Known Issues
- Parser does not yet detect informal title-case headers (e.g., "Scope", "Purpose") — fix scheduled for next release