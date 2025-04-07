# SpecSense

**SpecSense** is an AI-powered analyzer for Software/System Requirements Specifications (SRS).  
It helps engineers detect vague, ambiguous, or non-testable requirements using large language models.

Built by a systems/test engineer rebuilding automation and development capability from the ground up.

---

## Features (In Progress)

- [x] Extract section headers from raw SRS documents (Markdown, Numbered, ALL CAPS)
- [x] Return structured section data with titles and body content
- [ ] Identify ambiguity or missing test coverage  
- [ ] Suggest tests based on requirement language  
- [ ] Optional Flask-based UI or API  

---

## Setup

```bash
# Create virtual environment (Windows)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

```bash
pytest
```

---

## Environment Variables

Create a `.env` file in the project root with the following:

```
OPENAI_API_KEY=your-api-key-here
```

A sample file is available as `.env.example`.

---
## Example Usage

```python
from app.parser import parse_sections_with_bodies

sample = """# Introduction
This document outlines the system.

1. Purpose
The system shall provide user authentication.

SYSTEM OVERVIEW
This section defines system boundaries.
"""

output = parse_sections_with_bodies(sample)

# Output:
[
    {"title": "Introduction", "body": "This document outlines the system."},
    {"title": "1. Purpose", "body": "The system shall provide user authentication."},
    {"title": "SYSTEM OVERVIEW", "body": "This section defines system boundaries."}
]
```
---
## Project Structure

```
SpecSense/
├── app/                  # Core logic (parsers, AI tools)
├── tests/                # Unit tests
├── .env.example          # Template for required secrets
├── .gitignore
├── requirements.txt
├── run.py                # Entry point (optional dev use)
├── README.md
└── .venv/                # Virtual environment (not committed)
```

---

## License

MIT License — free to use, adapt, and extend.

