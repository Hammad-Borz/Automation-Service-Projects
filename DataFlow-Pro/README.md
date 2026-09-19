
# 📊 DataFlow Pro — Business Data Processing Pipeline

> **A deterministic local business-data pipeline that ingests CSV transaction data, validates and normalizes records, detects duplicates, calculates trusted business metrics, persists canonical data in SQLite, and generates operational reports through both a direct pipeline and FastAPI.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-37-16A34A?logo=pytest)

---

## 1. 🎯 Project Title

**DataFlow Pro — Business Data Processing Pipeline**

DataFlow Pro is a modular Python data-processing system for turning inconsistent business transaction exports into validated, canonical records, quality intelligence, business analytics, SQLite data, and shareable reports.

---

## 2. 📝 One-Line Description

> **Validate, normalize, analyze, persist, and report business transaction data through one deterministic local pipeline.**

---

## 3. 🔴 Problem

Business transaction CSV exports can contain:

- Missing required values
- Inconsistent capitalization and whitespace
- Malformed email addresses
- Invalid quantities or prices
- Invalid dates
- Unsupported statuses
- Duplicate order_id values
- Untrusted source totals

Passing these records directly into downstream systems can produce unreliable analytics and inconsistent business data.

**DataFlow Pro makes validation, cleaning, duplicate handling, trusted calculations, and data quality reporting explicit and repeatable.**

---

## 4. 🟢 Solution

DataFlow Pro provides an end-to-end processing workflow:

~~~text
Business CSV
    ↓
Ingestion
    ↓
Cleaning & Normalization
    ↓
Validation
    ↓
Duplicate Detection
    ↓
Canonical Transformation
    ↓
Quality Analysis + Business Analytics
    ↓
SQLite Persistence
    ↓
CSV / JSON / TXT / XLSX Reports
    ↓
FastAPI Operational API
~~~

The same core Pipeline orchestration is used by direct Python execution and the FastAPI layer, keeping processing behavior centralized and testable.

---

## 5. ⚙️ Key Features

- 📥 CSV ingestion with required-column validation
- 🧱 Pydantic-backed canonical data modeling
- 🧹 Whitespace, case, null, email, currency, status, region, and date normalization
- 🛡️ Row-level business validation with structured validation results
- ♻️ Deterministic duplicate detection using order_id
- 🧮 Trusted total_amount = quantity × unit_price calculation
- 💎 Configurable high-value transaction classification
- 📊 Data-quality scoring and validation-error reporting
- 📈 Revenue, order, quantity, status, region, product, category, and monthly analytics
- 🗄️ SQLite persistence with parameterized SQL
- 🔄 Order-level SQLite upsert behavior
- 📑 CSV, JSON, TXT, and XLSX report generation
- 🌐 FastAPI operational endpoints
- 🔒 Safe input-path handling restricted to the project data/ directory
- 🧪 **37 isolated pytest tests**

---

## 6. 🔄 How It Works

1. **Ingest** — Reads the selected CSV and verifies required columns.
2. **Clean** — Normalizes whitespace, casing, nulls, emails, currency, status, region, and dates.
3. **Validate** — Evaluates row-level business constraints and records validation errors.
4. **Deduplicate** — Uses order_id as the business key and preserves the first valid occurrence.
5. **Transform** — Builds canonical records and calculates trusted totals and derived fields.
6. **Analyze** — Calculates data-quality statistics and business KPIs.
7. **Persist** — Upserts canonical records into SQLite and stores the processing run.
8. **Report** — Generates CSV, JSON, text, and Excel outputs.

Invalid records remain represented in the quality report but are excluded from canonical persistence.

---

## 7. 🏗️ Architecture / Workflow

~~~mermaid
flowchart TD
    API[FastAPI] --> Pipeline[Pipeline Orchestrator]
    CLI[Direct Python Caller] --> Pipeline

    Pipeline --> Ingestion[CSV Ingestion]
    Ingestion --> Cleaning[Cleaning]
    Cleaning --> Validation[Validation]
    Validation --> Duplicate[Duplicate Detection]
    Duplicate --> Transform[Canonical Transformation]

    Transform --> Quality[Quality Analysis]
    Transform --> Analytics[Business Analytics]
    Transform --> Repository[SQLite Repository]

    Quality --> Reports[Reporting Service]
    Analytics --> Reports

    Repository --> API
    Reports --> API
~~~

### Architecture Responsibilities

| Component | Responsibility |
|---|---|
| ingestion_service.py | CSV loading, existence checks, and required-column validation |
| cleaner.py | Normalization and cleaning rules |
| validator.py | Row-level business validation |
| quality.py | Quality statistics, valid-row selection, and duplicate counts |
| transformer.py | Trusted totals and derived business fields |
| analytics.py | Operational KPI calculations |
| repository.py | SQLite persistence and upsert behavior |
| reporting_service.py | CSV, JSON, TXT, and Excel outputs |
| pipeline.py | End-to-end orchestration and processing-run persistence |
| api/routes.py | FastAPI operational endpoints |

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application and pipeline implementation |
| **pandas** | Tabular ingestion and transformation |
| **Pydantic 2** | Canonical models and API schemas |
| **FastAPI** | Operational REST API |
| **Uvicorn** | Local ASGI server |
| **SQLite** | Local persistence |
| **openpyxl** | Excel report generation |
| **pytest** | Automated testing |
| **httpx** | API test support |

Dependencies are defined in requirements.txt.

---

## 9. 📁 Project Structure

~~~text
DataFlow-Pro/
├── data/
│   ├── input/
│   └── output/
├── docs/
│   ├── architecture/
│   └── setup/
├── src/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   └── services/
├── tests/
├── requirements.txt
└── README.md
~~~

### Important Runtime Files

~~~text
data/
├── input/
│   └── sample_business_data.csv
├── output/
│   ├── clean_business_data.csv
│   ├── data_quality_report.json
│   ├── business_analytics.json
│   ├── business_summary.txt
│   └── business_report.xlsx
└── dataflow.sqlite3
~~~

---

## 10. 🚀 Installation

### Prerequisites

- Python **3.11+**
- PowerShell on Windows or an equivalent shell

### Create Virtual Environment

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

### Install Dependencies

~~~powershell
python -m pip install -r requirements.txt
~~~

---

## 11. 🔧 Configuration

DataFlow Pro uses environment variables for optional runtime configuration.

| Variable | Purpose | Default |
|---|---|---|
| DATAFLOW_DATABASE_PATH | SQLite database location | data/dataflow.sqlite3 |
| DATAFLOW_HIGH_VALUE_THRESHOLD | High-value transaction threshold | 1000 |
| DATAFLOW_ENVIRONMENT | Runtime environment label | development |
| DATAFLOW_LOGGING_LEVEL | Logging level | INFO |

No .env file is required for the default local setup.

---

## 12. ▶️ Usage

### Run the Pipeline Directly

~~~powershell
python -c "from src.config import Settings; from src.core.pipeline import Pipeline; print(Pipeline(Settings.for_project()).run())"
~~~

### Start the FastAPI Application

~~~powershell
python -m src.main
~~~

The local API runs at:

http://127.0.0.1:8000

### Open Swagger UI

http://127.0.0.1:8000/docs

### Run Tests

~~~powershell
pytest
~~~

### Process Another CSV

Place the CSV under the project's data/ directory and send a project-relative path:

~~~powershell
$body = '{"input_path":"data/input/my_business_data.csv"}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/pipeline/run -Method Post -ContentType 'application/json' -Body $body
~~~

The API rejects paths outside the project's data/ directory.

---

## 13. 🧪 Example

### API Request

~~~powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/pipeline/run -Method Post -ContentType 'application/json' -Body '{}'
~~~

### Example Processing Flow

~~~text
24 input rows
      ↓
Validation
      ↓
19 valid records
5 invalid records
1 duplicate detected
      ↓
Canonical transformation
      ↓
SQLite persistence
      ↓
Quality + analytics
      ↓
CSV / JSON / TXT / XLSX reports
~~~

The repository's sample dataset currently produces **24 input rows, 19 valid records, 5 invalid records, and 1 duplicate**; these values are calculated dynamically by the pipeline.

### Available API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Health check |
| POST | /pipeline/run | Execute the pipeline |
| GET | /pipeline/runs | List processing runs |
| GET | /pipeline/runs/{run_id} | Retrieve a processing run |
| GET | /analytics/overview | View business analytics |
| GET | /records | List canonical records |
| GET | /records/{order_id} | Retrieve an order |
| GET | /quality/latest | View the latest quality report |

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- Swagger/OpenAPI interface
- Pipeline execution response
- Data-quality report
- Canonical SQLite records
- Business analytics output
- Generated Excel report
- Input → validation → transformation evidence

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

~~~text
CSV Input
   ↓
Ingestion
   ↓
Cleaning
   ↓
Validation
   ↓
Duplicate Detection
   ↓
Canonical Transformation
   ↓
Quality + Analytics
   ↓
SQLite Persistence
   ↓
Reports
   ↓
FastAPI Visibility
~~~

The final demo should show the complete workflow from raw business data to validated records, analytics, persistence, and generated reports.

---

## 16. 📊 Results / Benefits

DataFlow Pro provides:

- **Deterministic processing** — the same input follows the same processing rules.
- **Trusted calculations** — canonical totals are calculated from quantity and unit price instead of trusting source totals.
- **Explicit data quality** — invalid records and validation errors are surfaced rather than silently discarded.
- **Controlled duplicate handling** — order_id is used as the business key.
- **Persistent operational history** — processing runs are stored in SQLite.
- **Reusable API access** — the same pipeline can be triggered through FastAPI.
- **Multiple reporting formats** — CSV, JSON, TXT, and Excel outputs.
- **Isolated testing** — tests use temporary project roots and databases rather than relying on generated runtime artifacts.

---

## 17. ⚠️ Limitations

The current implementation is intentionally designed as a **self-contained local pipeline**.

Current limitations include:

- SQLite is intended for local/small-scale operation.
- Processing is synchronous rather than queue-based.
- No authentication layer is included for the local API.
- No external object storage is used.
- No distributed execution or background job system is included.
- No production-grade monitoring or alerting system is included.
- Input is currently CSV-oriented.

---

## 18. 🔮 Future Improvements

Potential production-oriented extensions include:

- ☁️ Object storage for raw and processed datasets
- 🔐 Authenticated API access
- ⚡ Background processing and job queues
- 🔁 Retry and dead-letter handling
- 📈 Metrics and alerting
- 🗃️ Managed relational database support
- 🧬 Schema versioning and stronger data lineage
- 📦 Larger-scale batch processing
- ⏱️ Scheduled pipeline execution
- 🔎 Expanded observability and operational dashboards

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

DataFlow Pro demonstrates practical **data engineering + business automation** capabilities through:

- Modular pipeline architecture
- Defensive data validation
- Deterministic transformations
- Data-quality analysis
- Business KPI generation
- Safe SQLite persistence
- REST API operations
- Multi-format reporting
- Automated testing

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.
