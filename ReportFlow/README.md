# 📊 ReportFlow

## 1. Project Title

**ReportFlow — Automated Business Reporting System**

A modular Python workflow that converts business order data into validated KPIs, analytical summaries, Excel reports, CSV exports, charts, and an executive text report.

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-12%20Passing-16A34A)
![Reporting](https://img.shields.io/badge/Focus-Business_Reporting-7C3AED)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 2. One-Line Description

> **ReportFlow automates the path from raw CSV/Excel business data to validated analytics and multi-format management reports through one repeatable workflow.**

---

## 3. Problem

Recurring business reporting often involves repetitive spreadsheet work:

- 📥 Loading and reconciling source data.
- 🔍 Checking required fields and basic data quality.
- 🧮 Recalculating revenue and KPIs.
- 📊 Building product, category, regional, and monthly summaries.
- 📗 Formatting Excel reporting packs.
- 📝 Preparing executive summaries.

Manual repetition can make reporting slower and less consistent.

---

## 4. Solution

ReportFlow provides an end-to-end local reporting pipeline:

1. 📥 Load CSV or Excel input.
2. 🛡️ Validate the required data contract.
3. 🧹 Normalize and clean the data.
4. 💰 Calculate row-level revenue.
5. 📈 Calculate business KPIs and aggregate views.
6. 📗 Generate a formatted Excel workbook with charts.
7. 📄 Export processed and analytical CSV files.
8. 📝 Generate an executive text report.

The workflow is orchestrated through a single `ReportingWorkflow` class.

---

## 5. Key Features

### 📥 Data Ingestion

- Supports `.csv` input.
- Supports `.xlsx` input.
- Rejects missing files.
- Rejects unsupported file extensions.
- Rejects empty input files.

### 🛡️ Validation

Required columns:

- `order_id`
- `order_date`
- `product`
- `category`
- `region`
- `quantity`
- `unit_price`

Validation also checks:

- Order IDs are present.
- Quantity values are numeric and non-negative.
- Unit prices are numeric and non-negative.
- Order dates are valid.

### 🧹 Data Processing

- Normalizes column names.
- Strips text fields.
- Handles missing text values as `Unknown`.
- Parses dates.
- Converts numeric fields.
- Calculates `revenue = quantity × unit_price`.
- Derives a monthly reporting dimension.

### 📊 Analytics

ReportFlow calculates:

- Total revenue.
- Total orders.
- Total units.
- Average order value.
- Revenue by product.
- Revenue by category.
- Revenue by region.
- Monthly performance.
- Top five products.

### 📗 Excel Reporting

The generated workbook contains:

- Executive Summary
- Products
- Categories
- Regions
- Monthly Trends

It also generates:

- 📊 Revenue-by-product bar chart.
- 📈 Monthly revenue trend line chart.
- Formatted headers.
- Frozen panes.
- Currency formatting where applicable.

### 📄 CSV Reporting

Generated CSV outputs include:

- Processed orders.
- Product summary.
- Regional summary.
- Monthly summary.

### 📝 Executive Report

The text report includes:

- Executive summary.
- KPI summary.
- Revenue by product.
- Revenue by category.
- Revenue by region.
- Monthly performance.
- Top performers.

### 🧪 Testing

The project documents **12 automated tests** covering configuration, loading, validation, processing, analytics, report generation, Excel output, and end-to-end workflow behavior.

---

## 6. How It Works

The complete processing flow is:

```text
📥 CSV / Excel Input
        │
        ▼
📂 DataLoader
        │
        ▼
🛡️ DataValidator
        │
        ▼
🧹 DataProcessor
        │
        ▼
📈 Analytics
        │
        ├───────────────┐
        ▼               ▼
📗 ExcelExporter   📝 ReportGenerator
        │               │
        ▼               ▼
   Excel Workbook    Text Report
        │
        └───────────────┐
                        ▼
                  📄 CSV Exports
```

The CLI entry point creates a `ReportingWorkflow`, runs the pipeline, and prints the resulting KPI and report paths.

---

## 7. Architecture / Workflow

### 🧩 Core Architecture

| Module | Responsibility |
|---|---|
| `data_loader.py` | CSV/Excel ingestion |
| `data_validator.py` | Required-column and business-rule validation |
| `data_processor.py` | Cleaning, normalization, revenue, and month derivation |
| `analytics.py` | KPI and aggregate calculations |
| `excel_exporter.py` | Multi-sheet Excel workbook and charts |
| `report_generator.py` | Executive text report |
| `workflow.py` | End-to-end orchestration |
| `config.py` | Project filesystem settings |
| `models.py` | Workflow and analytics result contracts |
| `logger.py` | Logging configuration |
| `exceptions.py` | Application-specific errors |
| `main.py` | CLI entry point |

### 🔄 Workflow Boundary

```text
Source File
   │
   ▼
┌─────────────────┐
│ Load            │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Validate        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Process         │
│ + Revenue       │
│ + Month         │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Analytics       │
└────────┬────────┘
         ▼
┌────────────────────────────┐
│ Reporting Outputs          │
├────────────────────────────┤
│ Excel + Charts             │
│ CSV Exports                │
│ Executive Text Report      │
└────────────────────────────┘
```

---

## 8. Technologies

| Category | Technology |
|---|---|
| 🐍 Language | Python 3.14+ |
| 📊 Data Processing | pandas |
| 📗 Excel Automation | openpyxl |
| 🧪 Testing | pytest |
| 📁 Filesystem | pathlib |
| 📝 Logging | Python `logging` |

### Dependencies

```text
pandas>=2.0
openpyxl>=3.1
pytest>=8.0
```

The current workflow is local and does not require a database, external API, or cloud service.

---

## 9. Project Structure

```text
ReportFlow/
│
├── 📂 data/
│   ├── 📂 input/
│   │   └── sales_data.csv
│   └── 📂 output/
│
├── 📂 logs/
│
├── 📂 src/
│   ├── analytics.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_processor.py
│   ├── data_validator.py
│   ├── excel_exporter.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── report_generator.py
│   └── workflow.py
│
├── 📂 tests/
├── README.md
├── requirements.txt
└── pytest.ini
```

Generated files are written to `data/output/`.

---

## 10. Installation

### 1️⃣ Clone the portfolio repository

```bash
git clone https://github.com/Hammad-Borz/Automation-Service-Projects.git
cd Automation-Service-Projects/ReportFlow
```

### 2️⃣ Create a virtual environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3️⃣ Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 11. Configuration

ReportFlow currently uses filesystem-based settings rather than an environment-variable configuration layer.

The default project settings resolve:

```text
data/input/
data/output/
logs/
```

The default input file is:

```text
data/input/sales_data.csv
```

The required input schema is:

```text
order_id
order_date
product
category
region
quantity
unit_price
```

The `Settings` class also creates the input, output, and log directories when initialized.

---

## 12. Usage

### ▶️ Run the included demo

```powershell
python -m src.main
```

The workflow reads the included `data/input/sales_data.csv`, validates it, processes it, calculates analytics, and writes all report outputs to `data/output/`.

### 🧪 Run the test suite

```powershell
pytest
```

Expected documented result:

```text
12 passed
```

---

## 13. Example

The included demo dataset contains **15 orders**.

A successful run produces:

```text
ReportFlow demo completed successfully

Revenue: $21,350.00
Orders: 15
Average order value: $1,423.33

Excel report:
reportflow_business_report.xlsx

Text report:
business_report.txt

CSV exports:
- processed_orders.csv
- product_summary.csv
- regional_summary.csv
- monthly_summary.csv
```

### 📊 KPI Calculation

The implementation calculates:

```text
Revenue = quantity × unit_price

Average Order Value =
total revenue ÷ unique order count
```

For the included dataset:

- 💰 Total revenue: **$21,350.00**
- 📦 Total orders: **15**
- 📊 Average order value: **$1,423.33**

---

## 14. Screenshots

> 🟡 **Reserved area — screenshots will be added later.**

Planned visual proof:

- 📥 Input dataset.
- 🛡️ Validation / processing flow.
- 📊 KPI output.
- 📗 Excel Executive Summary.
- 📈 Product revenue chart.
- 📈 Monthly revenue chart.
- 📄 Generated CSV reports.
- 📝 Executive text report.
- 🧪 Test execution.

---

## 15. Demo Video / GIF

> 🟡 **Reserved area — demo video/GIF will be added later.**

### Planned demonstration

```text
Open ReportFlow
      ↓
Load sales_data.csv
      ↓
Validate input
      ↓
Clean & enrich data
      ↓
Calculate KPIs
      ↓
Generate Excel workbook
      ↓
Generate CSV exports
      ↓
Generate executive report
      ↓
Open final outputs
```

The visual demo will focus on the complete transformation from source business data to finished reporting outputs.

---

## 16. Results / Benefits

### 🧪 Current Verification

- **12 automated tests** are documented.
- Included dataset contains **15 orders**.
- Demo produces **$21,350.00** total revenue.
- Demo produces **15 unique orders**.
- Demo calculates **$1,423.33** average order value.
- Excel output contains multiple analytical sheets.
- Excel output includes product and monthly charts.
- CSV exports provide processed and summarized data.
- Executive text reporting is generated automatically.
- The workflow runs locally without external services.

### 💼 Portfolio / Service Relevance

ReportFlow demonstrates practical capabilities in:

`Python` • `Business Automation` • `pandas` • `Excel Automation` • `openpyxl` • `KPI Analytics` • `Reporting Automation` • `pytest`

---

## 17. Limitations

The current implementation has deliberate boundaries:

- The reporting workflow is local and file-based.
- The current input/output flow does not use a database.
- There is no scheduled execution layer.
- There is no automated email delivery.
- There is no interactive dashboard.
- There is no authentication or role-based access control.
- The current analytics layer focuses on the implemented order, revenue, product, category, regional, and monthly metrics.
- Currency conversion and profitability metrics are not currently implemented.

These are extension boundaries rather than capabilities currently claimed by the project.

---

## 18. Future Improvements

Potential next iterations include:

- ⏰ Scheduled report generation.
- 📧 Automated email delivery.
- 💱 Currency conversion.
- 📅 Configurable fiscal calendars.
- 💹 Margin and profitability metrics.
- 👥 Customer and cohort analytics.
- 📊 Interactive dashboard integration.
- 🔐 Role-based access controls.
- 🔎 Expanded data-quality observability.

---

## 19. License

No license file is currently documented for ReportFlow.

Until a license is added to the repository, users should not assume that the project is released under an open-source license.

---

## 20. Author / Contact

**Hammad Borz**

> Python • AI Automation • API Integration • Data Automation • Automation Systems

ReportFlow is part of the **Automation-Service-Projects** portfolio and is positioned as a service-specific business reporting automation implementation.

---

### 🔗 Repository

[Automation-Service-Projects](../)

### 📌 Project

[ReportFlow](./)
