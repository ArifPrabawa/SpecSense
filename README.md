# SpecSense

**SpecSense** is an AI-powered analyzer for Software Requirements Specifications (SRS).  
It helps engineers detect vague, ambiguous, or non-testable requirements using GPT-based models (GPT-3.5 / GPT-4).  
The tool also supports requirement grouping, traceability export, and project-level summaries — all from a single document upload.

---

## 💡 Use Case

Engineers, testers, and compliance reviewers can use SpecSense to:

- Detect unclear requirements early
- Auto-suggest tests for each SRS section
- Group requirements by functionality (e.g. Security, Authentication)
- Export traceable requirement IDs to JSON/CSV
- Summarize systemic risks or strengths in the specification

---

## 🚀 Features

### 🔍 Section Parser
- Supports Markdown, numbered headers, and ALL CAPS detection
- Skips known TOC and metadata sections
- Supports `.txt` and `.docx` input

### 🤖 LLM-Based Analysis
- GPT-powered analysis of each requirement section
- Flags ambiguity, vagueness, implicit behavior, or untestability
- Can confirm when a section is clear and testable
- GPT-powered summary of document-wide risks and themes

### 📊 Requirement Grouping & Gap Detection
- Inline detection of REQ-IDs from section bodies
- Grouping based on functional keywords or LLM classification
- Warns if key requirement categories (e.g. Security, Error Handling) are missing

### 📁 Traceability Export
- Export all REQ-IDs with their section, body, and analysis to JSON or CSV
- Compatible with tools like DOORS, ReqView, Excel, and audit pipelines

### 🧪 Full Test Coverage
- 80+ pytest tests
- All OpenAI calls are mocked
- Includes failure tests for malformed inputs, empty sections, and API edge cases

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🖥️ Run the App

```bash
streamlit run ui/streamlit_app.py
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
OPENAI_API_KEY=your-key-here
```

A sample is available in `.env.example`.

---

## 🗂️ Project Structure

```
SpecSense/
├── app/                  # Core logic (parser, LLM, grouping, summaries)
├── ui/                   # Streamlit UI
├── tests/                # Pytest unit tests
├── .env.example          # Example env file
├── README.md
├── requirements.txt
└── run.py                # Optional CLI/dev runner
```

---

## 📄 License

MIT License — free to use, modify, and extend.

