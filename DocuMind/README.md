# DocuMind — AI Document Processing System

DocuMind is a portfolio-ready Python automation project that turns PDFs and Word documents into validated, structured insights. It separates document extraction, AI interaction, validation, persistence, and reporting into clear, testable components.

## Features

- Extracts text from PDF and DOCX files
- Uses OpenAI to classify and summarize documents into a strict schema
- Validates every model response with Pydantic before saving it
- Produces predictable JSON analysis files and readable processing reports
- Handles missing files, unsupported types, empty documents, missing credentials, AI failures, and invalid responses safely
- Writes operational events to a dedicated log without duplicate handlers
- Includes a fully mocked pytest suite—no API key or network requests are needed to test it

## Architecture

```text
Document → DocumentReader → AIProcessor → ResultValidator → ResultExporter
                                      └──────────────────→ ReportGenerator
```

| Component | Responsibility |
| --- | --- |
| `document_reader` | Extract text independently from PDF/DOCX files. |
| `ai_processor` | Isolate OpenAI client setup and structured AI requests. |
| `models` / `result_validator` | Define and enforce the analysis contract. |
| `result_exporter` | Save validated output as safe JSON filenames. |
| `report_generator` | Create concise human-readable reports. |
| `logger` | Configure file logging once per process. |

## Project structure

```text
DocuMind/
├── src/                    # Application modules and CLI entry point
├── tests/                  # Mocked unit tests
├── sample_documents/       # Optional local input documents
├── output/results/         # Generated analysis JSON (gitignored)
├── output/reports/         # Generated reports (gitignored)
├── logs/                   # Runtime logs (gitignored)
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

```bash
cd DocuMind
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env`, then set a real key. Never commit `.env`.

```env
OPENAI_API_KEY=your_api_key_here
```

## Usage

Run the CLI from the project root with a PDF or DOCX input:

```bash
python src/main.py sample_documents/example.pdf
```

On success, DocuMind prints the resulting JSON and report paths. It writes analysis to `output/results/`, reports to `output/reports/`, and events to `logs/documind.log`.

## Example workflow

1. Place a supported source document anywhere accessible to the command.
2. DocuMind extracts its text and requests an analysis with `summary`, `key_points`, `action_items`, and `document_category`.
3. Pydantic validates that response.
4. The validated analysis is saved as JSON and summarized in a text report.

## Testing

```bash
pytest
```

Tests inject mock OpenAI clients and mock document-library boundaries where appropriate, so they do not make real API calls.

## Output

For `meeting-notes.docx`, typical output files are:

- `output/results/meeting-notes_analysis.json` — machine-readable validated analysis
- `output/reports/meeting-notes_report.txt` — source, status, category, summary, and item counts

## Limitations and future improvements

- Scanned/image-only PDFs require OCR, which is intentionally outside the current text-extraction scope.
- Very long documents may need chunking and synthesis before a single provider call.
- Future versions could add asynchronous batch processing, richer report formats, provider selection, and source citations.
