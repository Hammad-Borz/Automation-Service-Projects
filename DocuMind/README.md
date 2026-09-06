# 🧠 DocuMind — AI Document Processing System

> **An AI-powered Python automation system that transforms PDF and Word documents into validated, structured insights, machine-readable results, and human-readable reports.**

---

## ✨ What DocuMind Does

DocuMind processes supported documents through a modular pipeline:

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

The project separates document extraction, AI interaction, validation, persistence, and reporting into clear, testable components.

---

## 🚀 Key Capabilities

- 📄 Extracts text from **PDF and DOCX** files
- 🤖 Uses OpenAI for structured document analysis
- 🧾 Produces summaries, key points, action items, and document categories
- 🛡️ Validates model responses with **Pydantic** before saving them
- 📦 Exports validated analysis as predictable JSON files
- 📊 Generates concise, human-readable processing reports
- ⚠️ Handles missing files, unsupported types, empty documents, missing credentials, AI failures, and invalid responses safely
- 📝 Writes operational events to a dedicated log
- 🧪 Includes a fully mocked pytest suite with **14 passing tests**

---

# 🏗️ Architecture

```text
Document
   ↓
DocumentReader
   ↓
AIProcessor
   ↓
ResultValidator
   ↓
ResultExporter
   ↓
Validated JSON Output

        └──→ ReportGenerator → Processing Report
```

| Component | Responsibility |
|---|---|
| `document_reader` | Extract text independently from PDF and DOCX files. |
| `ai_processor` | Isolate OpenAI client setup and structured AI requests. |
| `models` | Define the structured document-analysis contract. |
| `result_validator` | Validate AI-generated results before persistence. |
| `result_exporter` | Save validated analysis using safe JSON filenames. |
| `report_generator` | Create concise human-readable reports. |
| `logger` | Configure file logging once per process. |
| `main` | Coordinate the end-to-end command-line workflow. |

---

# 📁 Project Structure

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

# ⚙️ Installation

From the repository's `DocuMind` directory:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Configuration

Copy `.env.example` to `.env` and provide your OpenAI API key:

```env
OPENAI_API_KEY=your_api_key_here
```

> 🔒 Never commit your `.env` file or API key to GitHub.

---

# ▶️ Usage

Run the application from the DocuMind project directory with a supported document:

```bash
python src/main.py sample_documents/example.pdf
```

Supported document formats:

- 📕 PDF
- 📘 DOCX

On successful processing, DocuMind produces:

```text
Document
   ↓
Text Extraction
   ↓
AI Analysis
   ↓
Pydantic Validation
   ↓
JSON Result + Text Report
```

---

# 📤 Output

For a document such as `meeting-notes.docx`, DocuMind can generate:

```text
output/results/meeting-notes_analysis.json
```

Machine-readable validated analysis containing structured insights.

```text
output/reports/meeting-notes_report.txt
```

A human-readable processing report containing source information, document category, summary, and item counts.

Operational events are written to:

```text
logs/documind.log
```

---

# 🧪 Testing

Run the complete automated test suite:

```bash
pytest
```

### Current verified result

```text
14 passed
```

The tests use mocked boundaries where appropriate, including mocked OpenAI interactions, so the suite does **not require real API calls**.

---

# 🎯 Example Workflow

1. 📥 Provide a PDF or DOCX document.
2. 📖 DocuMind extracts the document text.
3. 🤖 The AI processor requests structured analysis.
4. 🛡️ Pydantic validates the returned result.
5. 📦 The validated analysis is exported as JSON.
6. 📄 A readable processing report is generated.
7. 📝 Operational events are recorded in logs.

---

# 🛠️ Skills Demonstrated

`Python` • `AI Automation` • `OpenAI API` • `Document Processing` • `PDF` • `DOCX` • `Pydantic` • `Structured Data` • `JSON` • `Error Handling` • `Logging` • `pytest` • `Modular Architecture`

---

# 🔮 Limitations & Future Improvements

The current version intentionally focuses on text-based PDF and DOCX processing. Potential future improvements include:

- 🔍 OCR support for scanned or image-only PDFs
- 📚 Chunking and synthesis for very large documents
- ⚡ Asynchronous batch processing
- 📊 Richer report formats
- 🔄 Multiple AI provider support
- 📌 Source citations within generated analysis

---

## 🟢 Project Status

**Complete — 14 automated tests passing.**

DocuMind demonstrates a practical AI document-processing workflow built with modular architecture, validation, automated testing, and production-oriented error handling.
