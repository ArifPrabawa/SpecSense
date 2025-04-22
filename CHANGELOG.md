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

## [v0.6.0] - TOC Conformance Comparison

### Added
- `toc_extractor.py`: Functions to extract TOC-style lines from `.txt` and `.docx` inputs using shared detection logic.
- `standard_toc.py`: Central definition of standard TOC structure for structural comparison.
- `toc_comparator.py`: Logic to compare extracted TOC against standard structure with reporting of matched, missing, and extra sections.
- Unit tests for all TOC extraction and comparison utilities.

### Changed
- Moved `is_docx_toc_paragraph()` from `file_reader.py` to `header_rules.py` for shared access across parser, extractor, and test logic.

### Notes
- All tests pass (including mocked `.docx` TOC tests for style matching).
- Lays foundation for structural conformance UI/export and future user-uploaded standard comparison.

## [v0.7.0] – TOC Conformance Check Added (Day 17)
### Added
- Structural conformance check: compare document TOC to `STANDARD_TOC`
- `structure_check.py` orchestration module
- `extract_toc_lines_from_docx()` supports both style and text-pattern detection
- `clean_toc_line()` normalization: handles dotted numbering (e.g., `1.2. Scope`)
- `test_structure_check.py` covering `.txt` and `.docx` logic
- Streamlit UI section: "Run Structure Check" with matched/missing/extra display
- `@pytest.mark.xfail` tests for LLM-based fuzzy matching (future feature placeholder)

### Fixed
- TOC parser now correctly detects malformed `.docx` TOC entries styled as `"Normal"`
- TOC matching logic adjusted to avoid false negatives from formatting quirks

## [v0.8.0] – TOC vs Parsed Structure Comparison
### Added
- `compare_toc_to_parsed_sections()` compares extracted TOC lines to actual parsed section titles
- Normalized comparison using `section['id'] + title` for stronger structural validation
- Identifies matched, missing, and extra sections between TOC and document body
- Unit tests for title-only match, extra section detection, case and whitespace normalization
- `@pytest.mark.xfail` coverage for ID+title composite matching and non-normalized return behavior (to be addressed in future)

### Fixed
- Clarified matching behavior by returning parsed section titles (not raw TOC lines) in matched results
- Adjusted test case inputs to reflect normalized structure for strict mode

### Notes
- Matching logic is deterministic and robust; fuzzy matching will be added separately in `v0.10.0+`
- README update deferred to v1.0 polish

## [v0.9.0] – LLM Error Handling & Test Coverage Alignment

### Added
- Centralized `get_client()` logic for OpenAI API key management
- Full test coverage for `analyze_requirement()` and `suggest_tests()` with correct mocking and input handling
- Support for OpenAI failure fallback logic and malformed response detection

### Fixed
- Removed invalid `pytest.raises()` tests that conflicted with catch-all exception logic
- Corrected monkeypatch behavior by moving `load_dotenv()` back to top of `llm.py`
- CI environment now reflects correct API key behavior during tests

### Known Issues
- Assistant guidance during test implementation phase was inconsistent and caused unnecessary rework
- Additional test validation should be applied in final polish phase to ensure return-based testing is consistent

## [v0.9.1] – LLM TOC Comparison + Lint Compliance

### Added
- `compare_toc_sections_with_llm()` function in `llm.py` for fuzzy TOC-to-standard comparison using GPT-4
- Full test suite for the new function, including:
  - Valid input test
  - Empty/malformed response handling
  - `xfail` test for semantic equivalence
- `use_llm` toggle in `compare_toc()` (`toc_comparator.py`) to enable LLM fallback without affecting strict comparison
- Mocked test in `test_toc_comparator.py` to validate LLM integration

### Fixed
- Removed all unused imports (`F401`) across app and test files
- Replaced unnecessary f-strings missing placeholders (`F541`)
- Fixed spacing/blank line issues flagged by `flake8` (`E302`, `E303`)
- Split multi-import lines for clarity and `E401` compliance
- Resolved `F811` redefinition warning in `streamlit_app.py`

### Configuration
- Added `.flake8` config file with project-wide linting rules:
  - `max-line-length = 100`
  - `ignore = E203, W503` for compatibility with `black`
  - Excluded `.venv`, `__pycache__`, and build directories

### Notes
- LLM fuzzy TOC logic is complete and test-covered, but not yet surfaced in the UI
- Codebase now passes both `flake8` and `black`
- CI and local lint behavior are now consistent and enforceable

## [v0.10.0] – LLM Fuzzy TOC Comparison (UI Integration)

### Added
- Streamlit sidebar checkbox to enable **LLM fuzzy TOC comparison**
- `use_llm` toggle passed from UI → `structure_check.py` → `compare_toc()`
- Support for optional fuzzy match results from GPT-4 alongside strict structure check
- New expandable section in UI: **"🧠 LLM Fuzzy Match Results"**, rendered using Markdown
- Dynamic fallback handling: strict vs. fuzzy results display correctly based on toggle

### Fixed
- `display_structure_check_results()` updated to support both old and new result formats (with or without `strict_comparison`)
- Eliminated crash when LLM output structure differed from default TOC comparison return

### Notes
- This completes full UI surfacing of the LLM fuzzy comparison logic implemented in `v0.9.1`
- First version where users can visibly benefit from AI-enhanced structural analysis

## [v0.11.0] – Traceability Export & Inline Requirement ID Detection

### Added
- Implemented inline requirement ID detection for sections.
- Added traceability export functionality (JSON/CSV) based on parsed SRS sections.
- Integrated a "Generate Traceability Export" button to Streamlit UI, enabling traceability downloads.
- Session state used to preserve parsed sections and analysis results across reruns.
- Tests for `build_traceability_index()`, `export_traceability_as_json()`, and `export_traceability_as_csv()` added and verified.

### Notes
- The summary section for cross-section analysis remains a future task.