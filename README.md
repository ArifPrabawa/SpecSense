# SpecSense

**SpecSense** is an AI-powered analyzer for Software/System Requirements Specifications (SRS).  
It helps engineers detect vague, ambiguous, or non-testable requirements using large language models.

Built by a systems/test engineer rebuilding automation and development capability from the ground up.

---

## Features (Coming Soon)

- [ ] Extract structured sections from raw SRS docs  
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

