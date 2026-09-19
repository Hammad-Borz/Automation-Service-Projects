# AutoFlow — Business Automation System

> **Python automation service for file intake, validation, organization, processing, reporting, and workflow logging.**

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-pytest-informational?logo=pytest&logoColor=white)](https://pytest.org/)

AutoFlow is a modular, file-based business automation system built with Python. It discovers incoming files, validates them, organizes supported files by type, extracts useful metrics from TXT and CSV inputs, generates a consolidated report, and records workflow activity in persistent logs.

The project is designed as a practical **Python Automation** service example for repetitive business file-processing workflows.

---

## 1. 📌 Project Title

**AutoFlow — Business Automation System**

**Service category:** Python Automation

---

## 2. 📝 One-Line Description

> Automatically turns incoming TXT and CSV files into a validated, organized, processed, reported, and logged workflow.

---

## 3. 🎯 Problem

Many file-based business workflows involve repetitive manual steps:

- Finding incoming files
- Checking whether files are supported and non-empty
- Sorting files into appropriate folders
- Extracting basic information from different file types
- Creating summary reports
- Keeping a record of what happened during processing

When these steps are performed manually, the workflow becomes repetitive and harder to keep consistent.

---

## 4. 💡 Solution

AutoFlow provides a single modular pipeline that automates those steps from file discovery through reporting.

**Pipeline:**

```text
Incoming Files
      ↓
File Discovery
      ↓
Validation
      ↓
File Organization
      ↓
Data Processing
      ↓
Report Generation
      ↓
Persistent Logging
```

The implementation uses small, focused Python modules so each stage can be tested and maintained independently.

---

## 5. ✨ Key Features

- 📥 **Automated file discovery** — scans the `input/` directory for incoming files.
- ✅ **File validation** — accepts `.txt` and `.csv` files and rejects unsupported or empty files.
- 📂 **Automatic organization** — moves TXT and CSV files into type-specific output folders.
- 📊 **TXT processing** — extracts file name, line count, and word count.
- 📋 **CSV processing** — extracts file name, column names, and data-row count.
- 📄 **Report generation** — creates a consolidated `automation_report.txt`.
- 📝 **Persistent logging** — records workflow activity, warnings, and errors in `logs/autoflow.log`.
- 🧩 **Modular architecture** — separates discovery, validation, organization, processing, reporting, and logging.
- 🧪 **Automated testing** — verifies the core modules with `pytest`.
- 🔒 **Repository hygiene** — runtime-generated directories and local artifacts remain outside version control.

---

## 6. ⚙️ How It Works

AutoFlow processes each file through the following sequence:

1. **Discover** files in `input/`.
2. **Validate** that each file is supported and contains data.
3. **Organize** valid files into:
   - `output/text_files/`
   - `output/csv_files/`
4. **Process** the organized file according to its extension.
5. **Collect** the extracted metrics.
6. **Generate** a consolidated report when at least one file is processed.
7. **Log** workflow events throughout execution.

If a file is invalid or cannot be organized, AutoFlow records the condition and continues processing the remaining files.

---

## 7. 🏗️ Architecture / Workflow

```text
┌───────────────────────────┐
│        input/             │
│   Incoming TXT / CSV      │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   file_discovery.py       │
│   Workflow coordinator    │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   file_validator.py       │
│ Extension + empty check   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   file_organizer.py       │
│ TXT / CSV destination     │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│   data_processor.py       │
│ TXT / CSV metrics         │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│  report_generator.py      │
│ Consolidated TXT report   │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│       logger.py           │
│ Persistent workflow log   │
└───────────────────────────┘
```

### Module responsibilities

| Module | Responsibility |
|---|---|
| `file_discovery.py` | Coordinates the end-to-end automation workflow |
| `file_validator.py` | Validates supported extensions and rejects empty files |
| `file_organizer.py` | Moves files into type-specific destination folders |
| `data_processor.py` | Extracts metrics from TXT and CSV files |
| `report_generator.py` | Generates the consolidated automation report |
| `logger.py` | Configures persistent application logging |

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.x** | Core application language |
| **pathlib** | File-system paths and directory management |
| **shutil** | File movement |
| **csv** | CSV parsing |
| **logging** | Persistent workflow logging |
| **pytest** | Automated testing |

The runtime workflow itself uses Python's standard library. The only declared external development/test dependency is `pytest>=8.0,<9.0`.

---

## 9. 📁 Project Structure

```text
AutoFlow-Business-Automation-System/
├── src/
│   ├── data_processor.py
│   ├── file_discovery.py
│   ├── file_organizer.py
│   ├── file_validator.py
│   ├── logger.py
│   └── report_generator.py
├── tests/
│   ├── test_data_processor.py
│   ├── test_file_organizer.py
│   ├── test_file_validator.py
│   ├── test_logger.py
│   └── test_report_generator.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

Runtime directories are created as needed and are intentionally excluded from version control:

```text
input/
output/
reports/
logs/
```

---

## 10. 🚀 Installation

### Prerequisites

- Python 3.x
- Git
- A terminal / PowerShell

### Clone the repository

```bash
git clone https://github.com/Hammad-Borz/Automation-Service-Projects.git
cd Automation-Service-Projects/AutoFlow-Business-Automation-System
```

### Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 11. 🔧 Configuration

AutoFlow currently has **no environment variables or external service credentials**.

The workflow uses these project-relative directories:

| Directory | Purpose |
|---|---|
| `input/` | Incoming files |
| `output/text_files/` | Organized TXT files |
| `output/csv_files/` | Organized CSV files |
| `reports/` | Generated automation report |
| `logs/` | Persistent application log |

The `input/` directory is created automatically when the application starts.

---

## 12. ▶️ Usage

### 1. Add input files

Place supported files inside:

```text
AutoFlow-Business-Automation-System/input/
```

Supported extensions:

```text
.txt
.csv
```

### 2. Run the automation

From the project directory:

```bash
python src/file_discovery.py
```

### 3. Inspect generated artifacts

After processing, review:

```text
output/
├── text_files/
└── csv_files/

reports/
└── automation_report.txt

logs/
└── autoflow.log
```

### 4. Run the test suite

```bash
pytest
```

---

## 13. 🧪 Example

### Example input

Place the following files in `input/`:

```text
input/
├── customer_notes.txt
└── sales_data.csv
```

### Example TXT processing

For a text file, AutoFlow extracts:

```text
File name
File type
Line count
Word count
```

### Example CSV processing

For a CSV file, AutoFlow extracts:

```text
File name
File type
Column names
Data-row count
```

### Resulting workflow

```text
input/customer_notes.txt
        │
        ├── validate
        ├── move → output/text_files/
        └── process → text metrics

input/sales_data.csv
        │
        ├── validate
        ├── move → output/csv_files/
        └── process → CSV metrics

                 ↓

       reports/automation_report.txt
                 +
          logs/autoflow.log
```

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

<br><br><br>

---

## 15. 🎬 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

<br><br><br>

---

## 16. 📈 Results / Benefits

AutoFlow provides a repeatable workflow for the current file-processing scope:

- Reduces manual file sorting for supported TXT and CSV inputs.
- Centralizes validation, processing, reporting, and logging into one pipeline.
- Produces a consistent report from successfully processed files.
- Keeps workflow activity available through persistent logs.
- Uses modular components that can be tested independently.
- Provides a foundation for extending the automation to additional file types and business actions.

> **Verification:** the repository includes dedicated pytest coverage for data processing, file validation, file organization, logging, and report generation.

---

## 17. ⚠️ Limitations

The current implementation intentionally keeps the scope focused:

- Only `.txt` and `.csv` inputs are supported.
- TXT processing is limited to basic line and word counts.
- CSV processing reports headers and data-row count rather than performing advanced data analysis.
- Reports are generated as plain-text files.
- Files are moved locally; there is no cloud-storage integration.
- There is no email, webhook, or external notification integration.
- There is no database or persistent business-record layer.
- Destination-name conflicts are rejected rather than automatically renamed or overwritten.
- No environment-based configuration is currently required or provided.

---

## 18. 🔮 Future Improvements

Potential extensions for a production-oriented version include:

- Additional input formats such as XLSX, JSON, and PDF.
- More advanced data validation and transformation rules.
- Duplicate-file detection and configurable conflict handling.
- Configurable workflow rules and destination mappings.
- Email or webhook notifications after processing.
- Database-backed processing history.
- Scheduled or event-driven execution.
- Structured JSON/CSV reporting in addition to TXT reports.
- Monitoring and operational metrics.
- Configuration through environment variables or a dedicated configuration file.

These are **future improvements**, not capabilities currently implemented in the project.

---

## 19. 📄 License

No dedicated license file is currently included in this project directory.

Until a license is added, treat the repository as **all rights reserved** rather than assuming an open-source license.

---

## 20. 👤 Author / Contact

**Hammad-Borz**

- GitHub: [Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For project-related discussion, use the repository's GitHub Issues or project documentation.

---

## 💼 Portfolio Positioning

**Service:** Python Automation  
**Project:** AutoFlow — Business Automation System  
**Focus:** File-based workflow automation, data processing, reporting, and operational logging.

AutoFlow demonstrates the ability to convert a repetitive file-handling process into a structured, testable Python automation workflow.

---

## 🧪 Verification

The project includes automated tests covering:

- Data processing
- File validation
- File organization
- Logging
- Report generation

Run the verification suite with:

```bash
pytest
```

---

> **Built as part of a professional automation-services portfolio.**
