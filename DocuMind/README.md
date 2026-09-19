# 🧠 DocuMind — AI Document Processing

> **A modular Python automation system that extracts text from PDF/DOCX documents, sends it for structured AI analysis, validates the returned result with Pydantic, and produces machine-readable JSON plus human-readable reports.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-OpenAI-412991?logo=openai&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-16A34A?logo=pytest)
![Architecture](https://img.shields.io/badge/Architecture-Modular-CA8A04)

---

## 1. 🎯 Project Title

**DocuMind — AI Document Processing**

DocuMind is a service-specific AI automation project for turning supported PDF and DOCX documents into validated structured insights and reusable reports.

---

## 2. 📝 One-Line Description

> **PDF/DOCX → text extraction → structured AI analysis → Pydantic validation → JSON + report.**

---

## 3. 🔴 Problem

Business documents contain useful information, but extracting and structuring that information manually is repetitive.

AI-generated results also cannot simply be treated as trusted data. They need a validation boundary before being persisted or consumed by downstream workflows.

Common workflow concerns include:

- Manual document review and extraction
- Repetitive summarization
- Unstructured AI responses
- Invalid or malformed model output
- Missing or unsupported input files
- Weak operational visibility

---

## 4. 🟢 Solution

DocuMind combines document extraction, AI analysis, structured validation, persistence, reporting, and logging into one controlled workflow.

~~~text
📄 PDF / DOCX
      ↓
📖 DocumentReader
      ↓
🤖 AIProcessor
      ↓
🛡️ Pydantic Validation
      ↓
📦 JSON Result
      ↓
📄 Human-Readable Report
      ↓
📝 Operational Log
~~~

The AI integration is isolated behind `AIProcessor`, while the validation layer ensures the returned JSON conforms to the project's `DocumentAnalysis` contract.

---

## 5. ⚙️ Key Features

- 📄 PDF text extraction using `pypdf`
- 📘 DOCX text extraction using `python-docx`
- 🤖 Structured OpenAI document analysis
- 🧾 Structured fields for:
  - Summary
  - Key points
  - Action items
  - Document category
- 🛡️ Pydantic validation of AI output
- 🔐 Explicit `OPENAI_API_KEY` configuration
- 📦 Deterministic, filesystem-safe JSON output names
- 📄 Human-readable processing reports
- 📝 Centralized file logging
- ⚠️ Safe handling of missing files, unsupported formats, empty documents, missing API credentials, invalid JSON, and AI processing failures
- 🧪 **14 automated pytest tests**
- 🧩 Modular, testable component boundaries

---

## 6. 🔄 How It Works

1. **Receive** — The CLI accepts a PDF or DOCX path.
2. **Load configuration** — `.env` is loaded from the project root.
3. **Extract** — `DocumentReader` extracts text from the supported document.
4. **Analyze** — `AIProcessor` requests a JSON-formatted analysis from the OpenAI API.
5. **Validate** — The returned JSON is parsed and validated against `DocumentAnalysis`.
6. **Export** — `ResultExporter` saves the validated analysis as JSON.
7. **Report** — `ReportGenerator` creates a concise text report.
8. **Log** — Processing start, completion, and failure events are written to the application log.
9. **Return status** — The CLI reports success or failure and returns an appropriate process code.

---

## 7. 🏗️ Architecture / Workflow

~~~text
┌──────────────────────┐
│    PDF / DOCX File   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│   DocumentReader     │
│  PDF / DOCX extract  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│     AIProcessor      │
│   OpenAI analysis    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│  ResultValidator     │
│  Pydantic contract   │
└──────────┬───────────┘
           ↓
      ┌────┴─────┐
      ↓          ↓
┌───────────┐ ┌───────────────┐
│ JSON      │ │ Text Report   │
│ Export    │ │ Generation    │
└───────────┘ └───────────────┘
           ↓
      📝 Logging
~~~

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `document_reader.py` | Extract text from PDF and DOCX documents |
| `ai_processor.py` | Configure OpenAI access and request structured analysis |
| `models.py` | Define the validated `DocumentAnalysis` schema |
| `result_validator.py` | Parse and validate untrusted AI responses |
| `result_exporter.py` | Persist validated analysis as safe JSON |
| `report_generator.py` | Generate human-readable processing reports |
| `logger.py` | Configure centralized file logging |
| `main.py` | Coordinate the command-line workflow |

### Validation Boundary

The AI response is required to be a JSON object containing:

~~~json
{
  "summary": "string",
  "key_points": ["string"],
  "action_items": ["string"],
  "document_category": "string"
}
~~~

The project validates this response before exporting it.

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application implementation |
| **OpenAI SDK** | AI document analysis |
| **pypdf** | PDF text extraction |
| **python-docx** | DOCX text extraction |
| **Pydantic** | Structured result validation |
| **python-dotenv** | Environment configuration |
| **JSON** | Machine-readable result persistence |
| **pytest** | Automated verification |
| **logging** | Operational logging |

Dependencies are declared in `requirements.txt`.

---

## 9. 📁 Project Structure

~~~text
DocuMind/
├── src/
│   ├── ai_processor.py
│   ├── document_reader.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── report_generator.py
│   ├── result_exporter.py
│   └── result_validator.py
├── tests/
├── sample_documents/
├── output/
│   ├── results/
│   └── reports/
├── logs/
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
~~~

### Generated Runtime Artifacts

~~~text
output/results/
output/reports/
logs/documind.log
~~~

Generated output and log directories are excluded from version control by the repository's ignore configuration.

---

## 10. 🚀 Installation

From the `DocuMind` directory:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
~~~

The project dependencies include:

~~~text
openai
python-dotenv
pydantic
pypdf
python-docx
pytest
~~~

---

## 11. 🔧 Configuration

Create a local `.env` file based on `.env.example`:

~~~env
OPENAI_API_KEY=your_api_key_here
~~~

The application loads the environment file from the project root before processing the document.

### 🔒 Security

- Never commit `.env`.
- Never commit API keys.
- Keep credentials outside source code.
- Use `.env.example` only as a safe configuration template.

---

## 12. ▶️ Usage

### Process a PDF

~~~powershell
python src/main.py sample_documents/example.pdf
~~~

### Process a DOCX

~~~powershell
python src/main.py sample_documents/meeting-notes.docx
~~~

### Supported Formats

- 📕 `.pdf`
- 📘 `.docx`

### Successful CLI Output

The application reports the generated analysis and report paths:

~~~text
Processing complete.
Analysis JSON: output/results/<document>_analysis.json
Report: output/reports/<document>_report.txt
~~~

### Failure Behavior

Processing failures are logged and reported to the terminal. The CLI returns a non-zero process code when processing fails.

---

## 13. 🧪 Example

For an input document such as:

~~~text
sample_documents/meeting-notes.docx
~~~

DocuMind produces:

~~~text
output/results/meeting-notes_analysis.json
output/reports/meeting-notes_report.txt
logs/documind.log
~~~

### JSON Result

The validated result follows the `DocumentAnalysis` structure:

~~~json
{
  "summary": "...",
  "key_points": [
    "..."
  ],
  "action_items": [
    "..."
  ],
  "document_category": "..."
}
~~~

### Processing Report

The text report includes:

- Source document
- Processing status
- Document category
- Summary
- Number of key points
- Number of action items

### Test Verification

The current documented test result is:

~~~text
14 passed
~~~

The test suite uses mocked boundaries where appropriate, so normal testing does not require live API calls.

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- 📄 Sample PDF/DOCX input
- 🖥️ CLI processing command
- 🤖 Structured AI result
- 🛡️ Validated JSON output
- 📄 Generated processing report
- 📝 Runtime log
- 📁 Final output directory

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

~~~text
Open supported document
        ↓
Run DocuMind
        ↓
Extract text
        ↓
Send structured AI request
        ↓
Validate AI JSON
        ↓
Export JSON
        ↓
Generate report
        ↓
Show logs + final outputs
~~~

The demonstration should use a safe test document and avoid exposing any API credentials.

---

## 16. 📊 Results / Benefits

DocuMind demonstrates:

- **Automated document extraction** from PDF and DOCX.
- **Structured AI analysis** instead of free-form model output.
- **A validation boundary** between the AI provider and persisted application data.
- **Predictable machine-readable outputs** through JSON.
- **Human-readable reporting** for completed processing runs.
- **Operational logging** for processing events and failures.
- **Modular architecture** that separates document reading, AI integration, validation, export, and reporting.
- **Automated testing** with 14 documented passing tests.
- **Local CLI execution** with explicit success/failure status.

---

## 17. ⚠️ Limitations

The current implementation is intentionally focused and has several boundaries:

- Only PDF and DOCX input formats are supported.
- PDF processing extracts text; scanned/image-only PDFs do not have OCR support.
- The current AI integration is OpenAI-specific.
- Processing requires a configured `OPENAI_API_KEY` for normal live analysis.
- Processing is synchronous.
- There is no batch-processing interface.
- There is no asynchronous job queue.
- There is no database persistence layer for document history.
- Generated analysis is based on the extracted document text and model response.
- The project does not currently provide source citations inside the generated analysis.

---

## 18. 🔮 Future Improvements

Potential extensions include:

- 🔍 OCR for scanned/image-only PDFs
- 📚 Chunking and synthesis for very large documents
- ⚡ Asynchronous batch processing
- 📊 Richer report formats
- 🔄 Multiple AI-provider support
- 📌 Source citations within generated analysis
- 🗃️ Persistent document-processing history
- 📦 Batch document processing
- 🧾 Additional document formats

These are future extensions, not current implementation claims.

---

## 19. 📜 License

No dedicated `LICENSE` file is currently documented for this project.

> If the project is later distributed as open-source software, add an appropriate license file and update this section.

---

## 20. 👤 Author / Contact

**Hammad-Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For project-specific questions, use the repository's GitHub issue/discussion mechanisms where appropriate.

---

## 💼 Portfolio Positioning

**DocuMind** is a service-specific **AI Document Processing** project demonstrating:

- Python automation
- OpenAI API integration
- PDF/DOCX processing
- Structured AI outputs
- Pydantic validation
- JSON persistence
- Report generation
- Error handling
- Logging
- pytest verification
- Modular architecture

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.
