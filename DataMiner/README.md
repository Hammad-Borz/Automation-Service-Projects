# ⛏️ DataMiner — Web Data Extraction & Processing System

> **A reusable Python data pipeline that transforms structured HTML into validated, cleaned, and export-ready datasets.**

[![Python](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-11%20passed-brightgreen.svg)](#-testing)
[![Status](https://img.shields.io/badge/status-complete-success.svg)](#-project-status)

---

## 🎯 The Business Problem

Businesses often have useful catalog or product information embedded in HTML, while their downstream workflows need **clean CSV or JSON data** for analysis, migration, reporting, or automation.

**DataMiner** demonstrates a reliable and testable pipeline that:

```text
Fetch HTML → Extract Records → Validate Data → Clean Records → Export Results → Generate Report
```

The project uses a controlled and reproducible HTML demo rather than depending on a third-party website whose structure may change.

---

## ⚙️ Core Workflow

```text
                         SOURCE_URL
                             │
                             ▼
                      🌐 WebClient
                             │
                             ▼
                    🔍 DataExtractor
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
         Validated Records          Malformed / Invalid
                │                         │
                ▼                         ▼
            🧹 DataCleaner             Log & Skip
                │
          ┌─────┴─────┐
          ▼           ▼
     CSV Export    JSON Export
          │           │
          └─────┬─────┘
                ▼
         📄 Processing Report
```

---

## ✨ Key Capabilities

- 🌐 **HTTP fetching** with configurable timeout and a custom User-Agent
- 🛡️ **Clear error handling** for network and unsuccessful HTTP responses
- 🔍 **BeautifulSoup extraction** using documented CSS selectors
- ✅ **Record-level validation** with invalid-record isolation
- 🧹 **Data cleaning and normalization** for whitespace, prices, categories, and availability
- 📊 **CSV export** for spreadsheet-friendly workflows
- 📦 **JSON export** for application and API workflows
- 📄 **Human-readable processing reports**
- 📝 **File logging** without duplicate handlers
- 🧪 **11 automated pytest tests** with mocked HTTP behavior
- 🔁 **Reproducible local end-to-end demo** with no dependency on a live third-party website

---

## 🏗️ Project Architecture

```text
SOURCE_URL
    │
    ▼
WebClient
    │
    ▼
DataExtractor ──────► Malformed cards safely excluded
    │
    ▼
DataValidator ──────► Invalid records reported
    │
    ▼
DataCleaner ────────► Cleaning failures isolated
    │
    ▼
DataExporter ───────► CSV + JSON
    │
    ▼
ReportGenerator ────► Processing summary
```

---

## 📁 Project Structure

```text
DataMiner/
│
├── demo/
│   └── sample_products.html    # Reproducible local HTML catalog
│
├── src/
│   ├── web_client.py           # HTTP access
│   ├── data_extractor.py       # HTML extraction
│   ├── data_validator.py       # Record validation
│   ├── data_cleaner.py         # Data normalization
│   ├── data_exporter.py        # CSV and JSON output
│   ├── report_generator.py     # Processing reports
│   ├── logger.py               # Application logging
│   └── main.py                 # Workflow entry point
│
├── tests/                      # Automated test suite
├── output/                     # Generated data (Git-ignored)
├── reports/                    # Generated reports (Git-ignored)
├── logs/                       # Generated logs (Git-ignored)
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🛠️ Technology Stack

| Area | Technology |
|---|---|
| 🐍 Language | Python |
| 🌐 HTTP | `requests` |
| 🔍 HTML Parsing | `BeautifulSoup4` |
| 🔐 Configuration | `python-dotenv` |
| 🧪 Testing | `pytest` + `unittest.mock` |
| 📊 Data Formats | CSV + JSON |
| 📝 Logging | Python `logging` |

---

## 🚀 Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🧪 Run the Reproducible End-to-End Demo

The included demo contains **five product cards**:

- 🟢 **4 records** are successfully cleaned and exported
- 🟡 **1 record** intentionally contains `Price on request`, demonstrating how a cleaning failure is isolated without stopping the workflow

### Terminal 1 — Start the local source server

From the `DataMiner` directory:

```powershell
cd demo
python -m http.server 8000
```

### Terminal 2 — Run DataMiner

Open another PowerShell window in the `DataMiner` directory:

```powershell
$env:SOURCE_URL = "http://localhost:8000/sample_products.html"
python src/main.py
```

The workflow generates:

```text
output/csv/products.csv
output/json/products.json
reports/processing_report.txt
```

### Optional `.env` configuration

Copy `.env.example` to `.env` and run:

```powershell
python src/main.py
```

`main.py` automatically loads `.env`. A normal environment variable takes precedence when one is already set.

---

## 🔍 Supported HTML Structure

DataMiner intentionally uses explicit selectors for predictable extraction:

```html
<article class="product-card">
  <h2 class="product-name">Widget</h2>
  <span class="product-price">$12.50</span>
  <span class="product-category">Tools</span>
  <span class="product-availability">In Stock</span>
</article>
```

---

## 🧪 Testing

Run the complete test suite:

```powershell
pytest
```

### Latest verified result

```text
11 passed
```

The suite covers:

- Successful HTTP requests
- Network and HTTP failures
- HTML extraction
- Malformed cards
- Data validation
- Data cleaning and price conversion
- CSV and JSON exports
- Report generation

The tests use mocked HTTP behavior, so **internet access is not required**.

---

## 💼 Skills Demonstrated

`Python` • `Web Data Extraction` • `BeautifulSoup` • `requests` • `Data Validation` • `Data Cleaning` • `CSV` • `JSON` • `Error Handling` • `Logging` • `pytest` • `Automation Pipelines`

---

## 🔮 Future Improvements

A production version could add:

- 🔁 Pagination and multi-page crawling
- ⏱️ Retry and exponential backoff
- 🚦 Rate limiting
- ⚙️ Configurable CSS selectors
- 🔍 Duplicate detection
- 🧾 Data provenance metadata
- 📅 Scheduled execution
- 💾 Database storage

---

## 🟢 Project Status

**Completed — Portfolio Ready** 🚀

This project demonstrates a practical web data extraction workflow designed around a realistic client need: transforming controlled HTML data into clean, portable, automation-ready datasets.
