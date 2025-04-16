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

## [v0.4.0] - 2025-04-15

### Added
- Title-case fallback header detection for informal SRS sections (e.g., "Scope", "Purpose")
- TOC filtering for `.txt` files using dotted-line pattern matching (early line scan)
- TOC filtering for `.docx` files using style-based detection (e.g., "TOC 1", "TOC Heading")
- Unit tests for fallback headers and TOC behavior in both input types

### Notes
- `.docx` TOC filtering leverages paragraph styles; documents without TOC styles are currently not filtered by content — fallback detection deferred
- Optional enhancements like multiline header collapsing and smart line joining are scoped for later

## [v0.5.0] - 2025-04-16

### Added
- `header_rules.py` module for modular header detection logic (moved from `parser.py`)
- Markdown output now includes structured headings: `#`, `##`, `###`
- Clean UI rendering component (`render_section_result()`) extracted to `ui/components.py`

### Changed
- `streamlit_app.py` refactored to separate UI layout and logic
- Markdown output updated with clearer body/analysis/test sections
- Test suite updated to match new Markdown structure and refactored imports
