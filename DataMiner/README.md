# ⛏️ DataMiner — Web Data Extraction & Processing System

> **A reusable Python pipeline that fetches structured HTML, extracts product records, validates and normalizes data, exports clean CSV/JSON datasets, and generates a processing report.**

[![Python](https://img.shields.io/badge/Python-3.14%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-11%20passed-brightgreen.svg)](#-verification)
[![Status](https://img.shields.io/badge/status-complete-success.svg)](#-project-status)

---

## 1. 🎯 Project Title

**DataMiner — Web Data Extraction & Processing System**

DataMiner demonstrates a practical web-data extraction workflow for converting structured HTML into validated, cleaned, portable datasets.

---

## 2. 📝 One-Line Description

> **Fetch HTML → extract records → validate → clean → export CSV/JSON → generate a processing report.**

---

## 3. 🔴 Problem

Useful product or catalog information is often embedded in HTML while downstream workflows need structured data.

Raw HTML can contain:

- Missing fields
- Malformed product cards
- Inconsistent whitespace
- Different availability labels
- Human-formatted prices
- Records that cannot be safely converted

DataMiner isolates invalid data instead of allowing one problematic record to stop the complete workflow.

---

## 4. 🟢 Solution

DataMiner provides a modular processing pipeline:

~~~text
SOURCE_URL
    ↓
WebClient
    ↓
DataExtractor
    ↓
DataValidator
    ↓
DataCleaner
    ↓
DataExporter
    ├── CSV
    └── JSON
    ↓
ReportGenerator
    ↓
Processing Report
~~~

The included local HTML demo makes the workflow reproducible without depending on a live third-party website.

---

## 5. ⚙️ Key Features

- 🌐 HTTP fetching with configurable timeout
- 🧭 Custom User-Agent for HTTP requests
- 🛡️ Explicit network and unsuccessful HTTP-response handling
- 🔍 BeautifulSoup HTML extraction using documented CSS selectors
- 🧱 Record-level validation with invalid-record isolation
- 🧹 Whitespace normalization
- 💰 Price parsing and numeric conversion
- 🏷️ Category normalization
- 📦 Availability normalization
- 📊 CSV export
- 📦 JSON export
- 📄 Human-readable processing report
- 📝 File logging without duplicate handlers
- 🧪 **11 automated pytest tests**
- 🔁 Reproducible local end-to-end demo

---

## 6. 🔄 How It Works

1. **Fetch** — WebClient requests the configured SOURCE_URL with a timeout and User-Agent.
2. **Extract** — DataExtractor finds .product-card elements and extracts name, price, category, and availability.
3. **Validate** — DataValidator checks required fields and separates valid and invalid records.
4. **Clean** — DataCleaner normalizes text, categories, availability values, and prices.
5. **Export** — DataExporter writes cleaned records to CSV and JSON.
6. **Report** — ReportGenerator records processing counts and output locations.
7. **Log** — the application logger writes processing information to logs/dataminer.log.

Cleaning failures are isolated so successfully processable records can continue through the pipeline.

---

## 7. 🏗️ Architecture / Workflow

~~~text
SOURCE_URL
    │
    ▼
WebClient
    │
    ▼
DataExtractor
    │
    ├──────────────► Malformed cards excluded
    │
    ▼
DataValidator
    │
    ├──────────────► Invalid records reported
    │
    ▼
DataCleaner
    │
    ├──────────────► Cleaning failures isolated
    │
    ▼
DataExporter
    ├──────────────► CSV
    └──────────────► JSON
             │
             ▼
       ReportGenerator
             │
             ▼
      Processing Report
~~~

### Module Responsibilities

| Module | Responsibility |
|---|---|
| web_client.py | HTTP fetching, timeout, User-Agent, network/HTTP errors |
| data_extractor.py | HTML parsing and product-card extraction |
| data_validator.py | Required-field validation and invalid-record isolation |
| data_cleaner.py | Text, price, category, and availability normalization |
| data_exporter.py | CSV and JSON output |
| report_generator.py | Human-readable processing report |
| logger.py | File logging |
| main.py | End-to-end workflow orchestration |

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python** | Application implementation |
| **requests** | HTTP access |
| **BeautifulSoup4** | HTML parsing |
| **python-dotenv** | Optional .env configuration |
| **pytest** | Automated testing |
| **unittest.mock** | Mocked HTTP behavior |
| **CSV / JSON** | Portable data exports |
| **Python logging** | Application logging |

Dependencies are defined in requirements.txt.

---

## 9. 📁 Project Structure

~~~text
DataMiner/
├── demo/
│   └── sample_products.html
├── src/
│   ├── web_client.py
│   ├── data_extractor.py
│   ├── data_validator.py
│   ├── data_cleaner.py
│   ├── data_exporter.py
│   ├── report_generator.py
│   ├── logger.py
│   └── main.py
├── tests/
├── output/
├── reports/
├── logs/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
~~~

Generated output, reports, and logs are Git-ignored.

---

## 10. 🚀 Installation

### Prerequisites

- Python **3.14+**
- PowerShell on Windows or an equivalent shell

### Create Virtual Environment

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

### Install Dependencies

~~~powershell
pip install -r requirements.txt
~~~

---

## 11. 🔧 Configuration

DataMiner requires SOURCE_URL.

### Environment Variable

~~~text
SOURCE_URL=http://localhost:8000/sample_products.html
~~~

### Optional .env

Copy .env.example to .env:

~~~powershell
Copy-Item .env.example .env
~~~

Then run DataMiner normally.

main.py loads .env, while an explicitly supplied environment variable remains authoritative.

---

## 12. ▶️ Usage

### Start the Reproducible Local Source

From the DataMiner directory:

~~~powershell
cd demo
python -m http.server 8000
~~~

### Run DataMiner

Open another terminal in the DataMiner directory:

~~~powershell
$env:SOURCE_URL = "http://localhost:8000/sample_products.html"
python src/main.py
~~~

### Generated Outputs

~~~text
output/csv/products.csv
output/json/products.json
reports/processing_report.txt
logs/dataminer.log
~~~

### Run Tests

~~~powershell
pytest
~~~

---

## 13. 🧪 Example

### Supported HTML Structure

~~~html
<article class="product-card">
  <h2 class="product-name">Widget</h2>
  <span class="product-price">$12.50</span>
  <span class="product-category">Tools</span>
  <span class="product-availability">In Stock</span>
</article>
~~~

DataMiner uses these selectors:

| Field | Selector |
|---|---|
| Product card | .product-card |
| Name | .product-name |
| Price | .product-price |
| Category | .product-category |
| Availability | .product-availability |

### Demo Dataset

The included demo contains **five product cards**:

- 🟢 **4 records** are successfully cleaned and exported.
- 🟡 **1 record** intentionally contains Price on request, demonstrating isolated cleaning failure.

### Processing Result

~~~text
HTML source
    ↓
5 product cards
    ↓
4 valid/cleaned records
1 cleaning failure
    ↓
CSV + JSON exports
    ↓
Processing report
~~~

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- Local HTML source
- Terminal running the source server
- DataMiner execution output
- Extracted/cleaned CSV
- JSON export
- Processing report
- Log output

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

~~~text
Start local HTML server
        ↓
Configure SOURCE_URL
        ↓
Run DataMiner
        ↓
Fetch HTML
        ↓
Extract product cards
        ↓
Validate records
        ↓
Clean valid records
        ↓
Export CSV + JSON
        ↓
Generate processing report
~~~

The final demo should show the complete workflow and the intentional cleaning failure being isolated without stopping successful records.

---

## 16. 📊 Results / Benefits

DataMiner demonstrates:

- **Reusable extraction architecture** through separated modules.
- **Defensive processing** through network, HTTP, validation, and cleaning error handling.
- **Record-level fault isolation** so valid records can continue.
- **Normalized output** suitable for downstream spreadsheet or application workflows.
- **Portable exports** through CSV and JSON.
- **Reproducible execution** through the included local HTML demo.
- **Automated verification** through mocked HTTP tests.
- **Operational visibility** through reports and file logging.

The current verified test suite contains **11 passing tests**.

---

## 17. ⚠️ Limitations

The current implementation is intentionally focused on a controlled HTML extraction workflow.

Current limitations include:

- Extraction uses documented CSS selectors rather than arbitrary page discovery.
- The demo is based on a local HTML source.
- No pagination or multi-page crawling is currently implemented.
- No retry/exponential-backoff system is implemented.
- No rate-limiting mechanism is implemented.
- No database persistence is included.
- No scheduled execution is included.
- No production-scale crawling infrastructure is included.

---

## 18. 🔮 Future Improvements

Potential extensions include:

- 🔁 Pagination and multi-page crawling
- ⏱️ Retry and exponential backoff
- 🚦 Rate limiting
- ⚙️ Configurable CSS selectors
- 🔍 Duplicate detection
- 🧾 Data provenance metadata
- 📅 Scheduled execution
- 💾 Database storage
- 📊 Larger-scale extraction workflows

These are future extensions rather than claims about the current implementation.

---

## 19. 📜 License

No license file is currently included in the project.

> If this repository is later intended for open-source redistribution, add an appropriate LICENSE file and update this section accordingly.

---

## 20. 👤 Author / Contact

**Hammad-Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For project-specific questions, use the repository's GitHub issues or discussion mechanisms where appropriate.

---

## 💼 Portfolio Positioning

DataMiner demonstrates practical **web data extraction + automation** capabilities through:

- HTTP client implementation
- HTML parsing
- Structured extraction
- Data validation
- Data cleaning
- Error isolation
- CSV/JSON export
- Processing reports
- Logging
- Automated testing
- Reproducible local demonstrations

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.
