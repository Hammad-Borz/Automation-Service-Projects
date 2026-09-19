# 🗄️ DataOps Automator — SQL & Database Automation

> **A repeatable Python + SQLite + SQL automation pipeline that validates sales CSV data, transforms it into database-ready records, performs safe UPSERT operations, calculates business analytics, and generates decision-ready reports.**

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-17-16A34A?logo=pytest)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 1. 🎯 Project Title

**DataOps Automator — SQL & Database Automation**

DataOps Automator is a local business-data automation system that moves sales data through validation, transformation, SQLite persistence, SQL analytics, and report generation.

---

## 2. 📝 One-Line Description

> **Validate sales data → transform it → UPSERT into SQLite → analyze with SQL → export business reports.**

---

## 3. 🔴 Problem

Manual spreadsheet-to-database workflows can create:

- Duplicate records
- Inconsistent calculations
- Weak input validation
- Fragile reporting processes
- Repetitive copy-and-paste work
- Limited repeatability

A reliable automation workflow needs a defined data contract, deterministic transformations, controlled database writes, and repeatable analytics.

---

## 4. 🟢 Solution

DataOps Automator provides an end-to-end Python + SQLite + SQL workflow:

~~~text
📥 Sales CSV
     ↓
🛡️ Validate Data
     ↓
🧹 Clean & Transform
     ↓
🗄️ Initialize SQLite Schema
     ↓
🔁 UPSERT Sales Records
     ↓
📊 SQL Analytics
     ↓
📤 CSV Reports + Executive Report
~~~

The workflow is implemented as reusable modules and can be executed locally without an external database, cloud service, or API.

---

## 5. ⚙️ Key Features

- 📥 CSV ingestion with missing-file and unsupported-format handling
- 🛡️ Required-column validation
- 🔢 Positive numeric validation for quantity and unit price
- 📅 Order-date validation
- 🧹 Non-mutating pandas transformation
- 💰 Automatic revenue calculation
- 📆 Reporting-month generation
- 🗄️ Automatic SQLite schema creation
- 🔁 Repeatable `order_id` UPSERT operations
- 🔒 Parameterized SQL persistence
- ↩️ Transaction rollback handling
- 📊 SQL-based KPI and grouped analytics
- 🌍 Regional revenue analysis
- 📦 Product and category revenue analysis
- 📅 Monthly revenue analysis
- 🏆 Top-product analysis
- 📤 Six CSV analytics exports
- 📝 Human-readable executive report
- 🧾 Structured application logging
- 🧪 **17 automated pytest tests**
- ⚙️ Fully automated end-to-end workflow

---

## 6. 🔄 How It Works

1. **Load** — Reads the configured sales CSV.
2. **Validate** — Checks required columns, non-empty order IDs, positive quantities/prices, and valid dates.
3. **Transform** — Creates a normalized copy, standardizes fields, calculates revenue, and derives the reporting month.
4. **Initialize** — Creates the SQLite sales table when required.
5. **Persist** — Inserts or updates records using `order_id` as the primary key.
6. **Analyze** — Executes SQL aggregation queries against the database.
7. **Export** — Writes six CSV analytics files plus a business report.
8. **Log** — Records workflow stages and results in the project logs.

---

## 7. 🏗️ Architecture / Workflow

~~~text
                 ┌──────────────────────┐
                 │     Sales CSV        │
                 └──────────┬───────────┘
                            ↓
                    ┌───────────────┐
                    │  DataLoader   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ DataValidator │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ DataProcessor │
                    └───────┬───────┘
                            ↓
                 ┌──────────────────────┐
                 │ SQLite + UPSERT      │
                 └──────────┬───────────┘
                            ↓
                    ┌───────────────┐
                    │   Analytics   │
                    └───────┬───────┘
                            ↓
                 ┌──────────────────────┐
                 │ ReportExporter       │
                 └──────────────────────┘
~~~

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `config.py` | Centralized project paths and required-column settings |
| `data_loader.py` | CSV ingestion and input-boundary errors |
| `data_validator.py` | Required-field and business-rule validation |
| `data_processor.py` | Normalization, revenue calculation, and month derivation |
| `database_manager.py` | SQLite connections, transactions, rollback, and schema lifecycle |
| `data_repository.py` | Parameterized persistence and UPSERT operations |
| `analytics.py` | SQL KPIs and grouped business analytics |
| `report_exporter.py` | CSV and executive-report generation |
| `workflow.py` | End-to-end orchestration |
| `main.py` | Command-line demo entry point |

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.14+** | Application and workflow implementation |
| **pandas** | CSV processing and data transformation |
| **SQLite / sqlite3** | Local relational persistence |
| **SQL** | KPI and grouped business analytics |
| **pytest** | Automated testing |
| **pathlib** | Filesystem management |
| **Python logging** | Operational logging |

Dependencies are defined in `requirements.txt`.

---

## 9. 📁 Project Structure

~~~text
DataOps-Automator/
├── data/
│   ├── input/
│   │   └── sales_data.csv
│   └── output/
├── database/
├── logs/
├── src/
│   ├── analytics.py
│   ├── config.py
│   ├── database_manager.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── data_repository.py
│   ├── data_validator.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── report_exporter.py
│   ├── schema.py
│   └── workflow.py
├── tests/
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
~~~

### Runtime Locations

~~~text
data/input/sales_data.csv
data/output/
database/dataops.db
logs/
~~~

Generated database, output, and log artifacts are excluded from Git.

---

## 10. 🚀 Installation

From the `DataOps-Automator` directory:

~~~powershell
python -m pip install -r requirements.txt
~~~

The current dependency set includes pandas and pytest.

---

## 11. 🔧 Configuration

Project settings are centralized in `src/config.py`.

The default project configuration creates:

| Setting | Default |
|---|---|
| Input directory | `data/input/` |
| Output directory | `data/output/` |
| Database directory | `database/` |
| Database | `database/dataops.db` |
| Logs directory | `logs/` |

Required input columns:

~~~text
order_id
order_date
customer
region
product
category
quantity
unit_price
~~~

The application creates required runtime directories automatically.

---

## 12. ▶️ Usage

### Run the Complete Workflow

~~~powershell
python -m src.main
~~~

The default workflow processes:

~~~text
data/input/sales_data.csv
~~~

and generates:

~~~text
data/output/
database/dataops.db
logs/
~~~

### Run the Test Suite

~~~powershell
pytest
~~~

The workflow does not require an external database, cloud service, or API.

---

## 13. 🧪 Example

### Sample Dataset Result

The included sample dataset contains **16 sales records**.

The documented demo output is:

~~~text
Records processed: 16
Database records: 16

Total Revenue: $27,720.00
Total Orders: 16
Average Order Value: $1,732.50
Total Quantity Sold: 38

Reports generated: 7

Automation completed successfully.
~~~

### SQL Analytics

The analytics layer calculates:

| Analysis | SQL Operation |
|---|---|
| Total revenue | `SUM(revenue)` |
| Total orders | `COUNT(DISTINCT order_id)` |
| Average order value | `AVG(revenue)` |
| Quantity sold | `SUM(quantity)` |
| Revenue by region | `GROUP BY region` |
| Revenue by product | `GROUP BY product` |
| Revenue by category | `GROUP BY category` |
| Monthly revenue | `GROUP BY month` |
| Top products | `ORDER BY revenue DESC LIMIT 5` |

### Generated Reports

~~~text
kpi_summary.csv
revenue_by_region.csv
revenue_by_product.csv
revenue_by_category.csv
monthly_revenue.csv
top_products.csv
business_report.txt
~~~

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- Terminal workflow execution
- Input sales CSV
- SQLite database/table
- UPSERT evidence
- SQL analytics output
- Generated CSV reports
- Executive business report
- Application logs

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

~~~text
Sales CSV
   ↓
Validation
   ↓
Transformation
   ↓
SQLite Schema
   ↓
UPSERT
   ↓
SQL Analytics
   ↓
6 CSV Reports
   ↓
Executive Report
   ↓
Completed Automation
~~~

The final demo should show the complete workflow from raw sales data through database persistence and business reporting.

---

## 16. 📊 Results / Benefits

DataOps Automator provides:

- **Repeatable database automation** instead of manual spreadsheet-to-database processing.
- **Validated inputs** before database persistence.
- **Deterministic revenue calculations** from quantity × unit price.
- **Duplicate-safe persistence** through `order_id` UPSERT behavior.
- **Transactional database operations** with rollback handling.
- **SQL-driven analytics** directly against persisted business data.
- **Automated reporting** in reusable CSV and text formats.
- **Local reproducibility** without external infrastructure.
- **Automated verification** through 17 pytest tests.

---

## 17. ⚠️ Limitations

The current implementation is intentionally a local batch automation system.

Current limitations include:

- CSV is the supported input format.
- SQLite is intended for local/small-scale workloads.
- Processing is synchronous.
- No external database deployment is included.
- No authentication/API layer is included.
- No scheduled execution is included.
- No interactive dashboard is included.
- No incremental ingestion audit table is currently implemented.
- No automated email delivery is currently implemented.

---

## 18. 🔮 Future Improvements

Potential extensions include:

- 📥 Configurable input-file selection
- 🖥️ Command-line options
- 🧾 Incremental ingestion audit tables
- 💵 Margin and profitability analytics
- 👥 Customer lifetime value analysis
- 🧩 Cohort analytics
- 📅 Scheduled execution
- 📧 Automated email delivery
- 🗃️ Database migrations
- 📊 Interactive dashboard layer

These are future extensions rather than current implementation claims.

---

## 19. 📜 License

No license file is currently included in the project.

> If this repository is later intended for open-source redistribution, add an appropriate `LICENSE` file and update this section accordingly.

---

## 20. 👤 Author / Contact

**Hammad-Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For project-specific questions, use the repository's GitHub issues or discussion mechanisms where appropriate.

---

## 💼 Portfolio Positioning

DataOps Automator demonstrates practical **SQL + database automation** capabilities through:

- Python data pipelines
- CSV ingestion
- Business-rule validation
- pandas transformation
- SQLite schema management
- Parameterized SQL
- UPSERT operations
- Transaction rollback
- SQL analytics
- Automated report generation
- Logging
- pytest verification

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.
