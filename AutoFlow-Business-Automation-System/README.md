# AutoFlow — Business Automation System

> **Primary service demonstrated: 🐍 Python Automation**

AutoFlow is a modular Python business-automation system that automatically discovers incoming business files, validates them, organizes them by type, extracts useful information, generates a consolidated report, and records the workflow in structured logs.

## 🎯 What This Project Demonstrates

This project is designed as a practical portfolio example of **Python automation for repetitive business workflows**.

It demonstrates:

- Automated file discovery
- File validation and basic data-quality checks
- Automated folder organization
- TXT and CSV data processing
- Automated report generation
- Persistent application logging
- Modular Python design
- Automated testing with `pytest`

## 🔄 Workflow

```text
📥 Input Files
      ↓
🔍 File Discovery
      ↓
✅ Validation
      ↓
📂 File Organization
      ↓
📊 Data Processing
      ↓
📄 Report Generation
      ↓
📝 Activity Logging
```

## 🧩 Project Structure

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

Runtime directories such as `input/`, `output/`, `reports/`, and `logs/` are intentionally excluded from version control because they contain generated or local runtime data.

## ⚙️ Modules

| Module | Responsibility |
|---|---|
| `file_discovery.py` | Detects files in the input directory and coordinates the workflow |
| `file_validator.py` | Validates supported extensions and rejects empty files |
| `file_organizer.py` | Moves files into type-specific output folders |
| `data_processor.py` | Extracts metrics from TXT and CSV files |
| `report_generator.py` | Creates a consolidated automation report |
| `logger.py` | Records workflow events to a persistent log file |

## 📄 Supported Input Types

### TXT
Extracts:
- Line count
- Word count
- File name

### CSV
Extracts:
- Column names
- Data-row count
- File name

Currently supported extensions are `.txt` and `.csv`.

## 🧪 Testing

The project uses `pytest` for automated verification.

Run:

```bash
pytest
```

The implemented test suite covers validation, TXT/CSV processing, organization, report generation, and logging.

## ▶️ Running AutoFlow

From the project directory:

```bash
python src/file_discovery.py
```

Place supported `.txt` or `.csv` files in the `input/` directory before running the automation.

The workflow creates or updates runtime artifacts in:

```text
output/
reports/
logs/
```

## 🔐 Repository Hygiene

Generated runtime files and local environment data are excluded through `.gitignore`. No secrets or credentials are required by the current implementation.

## 🛠️ Tech Stack

- Python 3
- Standard library: `pathlib`, `shutil`, `csv`, `logging`
- `pytest`

## 📈 Current Scope

AutoFlow currently provides the foundational automation pipeline for file-based business workflows. The architecture is intentionally modular so capabilities such as email notifications, archiving, stronger duplicate handling, and additional data-processing rules can be added without replacing the core workflow.

## 💼 Portfolio Context

**Service:** Python Automation  
**Project:** AutoFlow — Business Automation System  
**Goal:** Demonstrate a practical, modular automation solution for repetitive business file workflows.
