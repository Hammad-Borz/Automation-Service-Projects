# 🧠 DocuMind — AI Document Processing System

> **An AI-powered Python automation system that transforms PDF and Word documents into validated, structured insights, machine-readable results, and human-readable reports.**

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![AI Automation](https://img.shields.io/badge/Focus-AI%20Automation-purple)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Modular-yellow)

---

## ✨ Overview

DocuMind is a modular **AI document-processing pipeline** designed to turn supported documents into structured, validated outputs. It separates document extraction, AI analysis, validation, persistence, reporting, and logging into focused, testable components.

```text
PDF / DOCX Document
        ↓
📖 Extract Text
        ↓
🤖 AI Analysis
        ↓
✅ Validate Structured Result
        ↓
📦 Export JSON
        ↓
📄 Generate Report
```

---

## 🚀 Key Capabilities

- 📄 Extract text from **PDF** and **DOCX** files
- 🤖 Perform structured AI-powered document analysis
- 🧾 Produce summaries, key points, action items, and document categories
- 🛡️ Validate model responses with **Pydantic** before persistence
- 📦 Export validated analysis as predictable JSON files
- 📊 Generate concise, human-readable processing reports
- ⚠️ Handle missing files, unsupported formats, empty documents, missing credentials, AI failures, and invalid responses safely
- 📝 Record operational events through centralized logging
- 🧪 Include a fully mocked **pytest suite with 14 passing tests**

---

## 🏗️ System Architecture

```text
                    ┌──────────────────┐
                    │  PDF / DOCX File │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ DocumentReader   │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │   AIProcessor    │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ ResultValidator  │
                    └────────┬─────────┘
                             ▼
                    ┌──────────────────┐
                    │ ResultExporter   │──► 📦 JSON Output
                    └────────┬─────────┘
                             └──► 📄 ReportGenerator ──► Text Report
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `document_reader` | Extract text independently from PDF and DOCX files. |
| `ai_processor` | Isolate AI client setup and structured analysis requests. |
| `models` | Define the structured document-analysis contract. |
| `result_validator` | Validate AI-generated results before persistence. |
| `result_exporter` | Save validated analysis using safe JSON filenames. |
| `report_generator` | Create concise human-readable reports. |
| `logger` | Configure centralized operational logging. |
| `main` | Coordinate the end-to-end command-line workflow. |

---

## 📁 Project Structure

```text
DocuMind/
│
├── src/
│   ├── ai_processor.py
│   ├── document_reader.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── report_generator.py
│   ├── result_exporter.py
│   └── result_validator.py
│
├── tests/                  # Automated test suite
├── sample_documents/       # Optional local input documents
├── output/
│   ├── results/            # Generated analysis JSON
│   └── reports/            # Generated reports
├── logs/                   # Runtime logs
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## ⚙️ Installation

From the `DocuMind` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🔐 Configuration

Copy `.env.example` to `.env` and add your API key:

```env
OPENAI_API_KEY=your_api_key_here
```

> 🔒 **Security:** Never commit your `.env` file or API key to GitHub.

---

## ▶️ Usage

Run the application from the project directory with a supported document:

```powershell
python src/main.py sample_documents/example.pdf
```

### Supported Formats

- 📕 PDF
- 📘 DOCX

### Processing Flow

```text
Document → Text Extraction → AI Analysis → Pydantic Validation
                                     ↓
                        JSON Result + Text Report
```

---

## 📤 Output

For a document such as `meeting-notes.docx`, DocuMind can generate:

```text
output/results/meeting-notes_analysis.json
```

A machine-readable, validated analysis containing structured insights.

```text
output/reports/meeting-notes_report.txt
```

A human-readable processing report containing source information, document category, summary, and item counts.

Operational events are written to:

```text
logs/documind.log
```

---

## 🧪 Testing

Run the complete automated test suite:

```powershell
pytest
```

### Current Verified Result

```text
14 passed
```

The tests use mocked boundaries where appropriate, including mocked AI interactions, so the normal test suite does **not require live API calls**.

---

## 🎯 Example Workflow

1. 📥 Provide a PDF or DOCX document.
2. 📖 Extract the document text.
3. 🤖 Request structured AI analysis.
4. 🛡️ Validate the returned result.
5. 📦 Export the validated analysis as JSON.
6. 📄 Generate a readable processing report.
7. 📝 Record operational events in logs.

---

## 🛠️ Skills Demonstrated

`Python` • `AI Automation` • `OpenAI API` • `Document Processing` • `PDF` • `DOCX` • `Pydantic` • `Structured Data` • `JSON` • `Error Handling` • `Logging` • `pytest` • `Modular Architecture`

---

## 🔮 Future Improvements

- 🔍 OCR support for scanned or image-only PDFs
- 📚 Chunking and synthesis for very large documents
- ⚡ Asynchronous batch processing
- 📊 Richer report formats
- 🔄 Multiple AI-provider support
- 📌 Source citations within generated analysis

---

## 🟢 Project Status

**Complete · Tested · Portfolio Ready**

> **14 automated tests passing.**

DocuMind demonstrates a practical AI document-processing workflow built with modular architecture, validation, automated testing, and production-oriented error handling.
