# 📈 InsightFlow — Automated Reporting & Analytics System

> **A deterministic analytics pipeline that converts e-commerce transaction data into validated KPIs, trends, comparisons, customer segments, explainable anomalies, rule-based insights, historical runs, and business-ready reports.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-58-16A34A?logo=pytest)

---

## 1. 🎯 Project Title

**InsightFlow — Automated Reporting & Analytics System**

InsightFlow is a service-specific analytics automation project that transforms transaction data into reproducible business metrics, explainable findings, historical analytics records, and executive-ready reports.

---

## 2. 📝 One-Line Description

> **CSV transactions → validate → normalize → calculate analytics → detect anomalies → generate insights → persist history → export reports → expose API.**

---

## 3. 🔴 Problem

Businesses often have transaction data but still need a repeatable way to turn that data into trustworthy metrics and actionable reporting.

Static reporting alone does not provide enough operational structure for questions such as:

- What are the current KPIs?
- How is revenue changing over time?
- Which categories, products, regions, or channels contribute the most?
- How can customers be segmented consistently?
- Which daily metrics are statistically unusual?
- What insights can be generated from those measurements?
- Can previous analytics runs be inspected later?
- Can the same calculations be accessed through an API?

---

## 4. 🟢 Solution

InsightFlow implements a deterministic analytics pipeline with explicit business definitions and reusable processing stages.

```text
📄 Raw CSV
    ↓
🔍 Load + Validate
    ↓
🧹 Normalize + Calculate
    ↓
📊 Analytics Engine
 ┌──┼──┬──┬──┐
 ↓  ↓  ↓  ↓  ↓
KPIs Trends Comparisons Segments Anomalies
    ↓
🧠 Rule-Based Insights
    ↓
🗄️ SQLite History
    ↓
📑 Reports
    ↓
🌐 FastAPI API
```

The analytics engine operates on normalized, valid, de-duplicated data. Insights are generated from the calculated analytics object rather than from an independent text-generation system.

---

## 5. ⚙️ Key Features

- 📥 CSV transaction ingestion
- 🛡️ Row-level validation
- 🧹 Data normalization and authoritative calculated totals
- 📊 Revenue, order, customer, unit, and rate KPIs
- 📈 Daily, weekly, and monthly trends
- 🔄 Latest-versus-previous-period comparisons
- 🏷️ Category, product, region, and channel analysis
- 👥 Deterministic customer segmentation using revenue percentiles
- 🚨 Explainable daily revenue/order anomaly detection
- 🧠 Rule-based business insights and recommendations
- 🗄️ SQLite persistence and historical analytics runs
- 📸 KPI/trend/comparison snapshots
- 📑 CSV, JSON, TXT, and Excel report generation
- 🌐 FastAPI operational API
- 🔐 Data-path restrictions and parameterized SQL
- 🧪 **58 deterministic automated tests**
- 🚫 No AI API or external service required

---

## 6. 🔄 How It Works

1. **Load** — Read the selected CSV from the project data directory.
2. **Validate** — Check required fields and row-level data quality.
3. **Normalize** — Standardize values, parse dates/numbers, and calculate authoritative transaction totals.
4. **De-duplicate** — Retain the first valid occurrence of each `order_id`.
5. **Calculate KPIs** — Compute revenue, orders, AOV, units, customer metrics, rates, and high-value order counts.
6. **Analyze trends** — Produce daily, weekly, and monthly metrics plus latest-period growth.
7. **Compare periods** — Compare the latest available month with the immediately preceding available month.
8. **Segment customers** — Apply the 25th and 75th revenue percentiles.
9. **Detect anomalies** — Evaluate daily revenue and order z-scores when sufficient history exists.
10. **Generate insights** — Apply deterministic rules to analytics results.
11. **Persist** — Store normalized records, run history, and analytics snapshots in SQLite.
12. **Report** — Generate machine-readable and human-readable reports.
13. **Expose** — Provide analytics, history, quality, record, and report endpoints through FastAPI.

---

## 7. 🏗️ Architecture / Workflow

```text
┌─────────────────────────┐
│      CSV Input          │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Data Loader             │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Validation              │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Normalization           │
│ calculated totals       │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Analytics Engine        │
├─────────────────────────┤
│ KPIs                    │
│ Trends                  │
│ Comparisons             │
│ Breakdowns              │
│ Segmentation            │
│ Anomalies               │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│ Rule-Based Insights     │
└────────────┬────────────┘
             ↓
      ┌──────┴──────┐
      ↓             ↓
┌────────────┐ ┌───────────────┐
│ SQLite     │ │ Report Engine │
│ History    │ │ CSV/JSON/TXT/ │
│ + Snapshots│ │ Excel         │
└──────┬─────┘ └───────┬───────┘
       ↓               ↓
       └───────┬───────┘
               ↓
        ┌──────────────┐
        │   FastAPI    │
        └──────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `core/data_loader.py` | Load CSV input and enforce basic file/column requirements |
| `core/validator.py` | Validate required values, numbers, dates, statuses, regions, channels, and email data |
| `core/normalizer.py` | Normalize fields and calculate authoritative transaction totals |
| `analytics/kpis.py` | Calculate KPI definitions |
| `analytics/trends.py` | Produce daily/weekly/monthly trends and growth |
| `analytics/comparisons.py` | Compare latest and previous available periods |
| `core/analytics_engine.py` | Calculate category, product, region, and channel breakdowns |
| `analytics/segmentation.py` | Create deterministic customer segments |
| `analytics/anomalies.py` | Detect daily revenue/order anomalies using z-scores |
| `services/insight_service.py` | Produce deterministic descriptions and recommendations |
| `core/report_engine.py` | Generate CSV, JSON, text, and Excel reports |
| `database/repository.py` | Persist records, runs, and analytics snapshots |
| `api/routes.py` | Expose analytics and operational endpoints |

### Data Integrity Flow

```text
Raw Record
   ↓
Validation
   ↓
Normalization
   ↓
Valid Records
   ↓
First valid order_id retained
   ↓
Canonical Analytics Dataset
```

---

## 8. 📐 Business Rules & KPI Definitions

| Metric / Rule | Definition |
|---|---|
| **Revenue** | `quantity × unit_price` using the calculated total |
| **Completed revenue** | Revenue from transactions with `status == completed` |
| **AOV** | Completed revenue ÷ completed orders |
| **Status rates** | Completion, cancellation, and refund rates use total order count as denominator |
| **Growth** | Latest available month compared with previous available month; zero when no comparable period exists |
| **Duplicates** | First valid `order_id` occurrence is retained |
| **Customer segments** | 25th and 75th revenue percentiles define low, regular, and high-value groups |
| **Anomalies** | Daily revenue/order z-scores; at least four observations required |
| **Quality score** | `valid records / input records × 100` |

---

## 9. 📊 Analytics Capabilities

- Total and completed revenue
- Total orders and completed/cancelled/refunded/pending orders
- Total units sold
- Average order value
- Average units per order
- Unique customers
- Revenue per customer
- High-value order count
- Completion, cancellation, and refund rates
- Daily, weekly, and monthly trends
- Category, product, region, and channel rankings/shares
- Customer revenue segmentation
- Period comparisons
- Explainable anomaly detection
- Rule-based insights and recommendations
- Historical analytics runs and metric snapshots

---

## 10. 📑 Generated Reports

| Output | Purpose |
|---|---|
| `executive_summary.txt` | Reporting period, KPIs, leaders, growth, quality, and insights |
| `analytics_report.json` | Complete analytics, insights, and quality payload |
| `kpis.json` | KPI-only JSON |
| `clean_sales_data.csv` | Normalized canonical data |
| `insightflow_report.xlsx` | Executive, KPI, comparison, trend, category, product, region, channel, segment, anomaly, quality, and clean-data sheets |

All generated outputs are written under `data/output/`.

---

## 11. 🌐 API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/analytics/run` | Process a CSV analytics run |
| `GET` | `/analytics/overview` | Latest analytics |
| `GET` | `/analytics/trends` | Trend metrics |
| `GET` | `/analytics/categories` | Category analysis |
| `GET` | `/analytics/products` | Product analysis |
| `GET` | `/analytics/regions` | Regional analysis |
| `GET` | `/analytics/channels` | Channel analysis |
| `GET` | `/analytics/customers` | Customer segmentation |
| `GET` | `/analytics/anomalies` | Detected anomalies |
| `GET` | `/insights` | Generated insights |
| `GET` | `/reports/latest` | Latest report paths |
| `GET` | `/analytics/runs` | Historical runs |
| `GET` | `/analytics/runs/{run_id}` | Retrieve one analytics run |
| `GET` | `/data/quality` | Latest data-quality report |
| `GET` | `/records` | Normalized records |
| `GET` | `/records/{order_id}` | Retrieve one order |

Swagger/OpenAPI is available at `/docs`.

---

## 12. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application and analytics implementation |
| **pandas** | Data processing and analytics |
| **Pydantic 2** | Structured validation |
| **FastAPI** | Operational REST API |
| **Uvicorn** | ASGI server |
| **SQLite** | Historical persistence |
| **pytest** | Automated verification |
| **httpx** | API testing |
| **openpyxl** | Excel report generation |

**No AI API or external service is required.**

---

## 13. 🚀 Installation & Quick Start

From the `InsightFlow` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Start the API

```powershell
python -m src.main
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

### Run Tests

```powershell
pytest
```

### Run the Sample Analytics Workflow

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/analytics/run -Method Post -ContentType 'application/json' -Body '{}'
```

The sample dataset contains **44 transactions** spanning nine months, four categories, five products, three regions, and three channels.

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- 🌐 Swagger/OpenAPI interface
- 📊 Analytics overview
- 📈 Trend and comparison output
- 👥 Customer segmentation
- 🚨 Anomaly results
- 🧠 Generated insights
- 📑 Excel report
- 🗄️ SQLite historical run evidence
- 🧪 Test results

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

```text
Start InsightFlow
      ↓
Open Swagger
      ↓
Run sample CSV
      ↓
Validate + normalize
      ↓
Calculate KPIs
      ↓
Analyze trends/comparisons
      ↓
Segment customers
      ↓
Detect anomalies
      ↓
Generate rule-based insights
      ↓
Persist analytics run
      ↓
Generate reports
      ↓
Inspect API + historical results
```

The demonstration will use the local deterministic workflow and will not imply AI-generated analysis or external-service dependencies.

---

## 16. 📊 Results / Benefits

InsightFlow demonstrates:

- **Reproducible analytics** through explicit calculation rules.
- **Validated business data** before analytics execution.
- **Authoritative revenue calculation** from quantity and unit price.
- **Explainable anomaly detection** using measurable z-score deviations.
- **Deterministic customer segmentation** using recorded percentile thresholds.
- **Rule-based insights** generated directly from calculated metrics.
- **Historical run tracking** through SQLite.
- **Business-ready report generation** across text, JSON, CSV, and Excel formats.
- **Operational API access** to analytics, insights, quality, records, reports, and run history.
- **Safe input handling** by restricting analytics input paths to the project data directory.
- **Automated verification** with 58 deterministic tests.

---

## 17. ⚠️ Limitations

- The current implementation is a local modular monolith.
- Input is CSV-based.
- SQLite is used for historical persistence.
- There is no distributed processing or asynchronous job queue.
- There is no built-in dashboard UI.
- Authentication and role-based access are not implemented.
- Scheduled ingestion is not currently included.
- Raw-file object storage is not currently included.
- The rule-based insight service is deterministic and not an AI/LLM service.
- Anomaly detection requires at least four daily observations and depends on the configured z-score threshold.

---

## 18. 🔮 Future Improvements

- 📅 Scheduled analytics jobs
- ☁️ Object storage for raw datasets
- 🗄️ PostgreSQL or warehouse-backed persistence
- 🔐 Authentication and role-based access
- 📊 Interactive dashboards
- 📨 Queues and asynchronous processing
- 📡 Monitoring and alerting
- 🔄 Incremental ingestion
- 🧬 Schema evolution and stronger data contracts
- 🗑️ Data retention policies

These are future extensions, not current implementation claims.

---

## 19. 📜 License

No dedicated `LICENSE` file is currently documented for InsightFlow.

> If the project is later distributed as open-source software, add the appropriate license file and update this section.

---

## 20. 👤 Author / Contact

**Hammad Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

---

## 💼 Portfolio Positioning

**InsightFlow** is a service-specific **Analytics & Automated Reporting** project demonstrating:

- Python analytics engineering
- pandas data processing
- Business KPI design
- Data validation and normalization
- Trend and period comparison analysis
- Customer segmentation
- Explainable anomaly detection
- Rule-based business insights
- SQLite historical persistence
- Excel/report automation
- FastAPI API development
- Automated testing
- Deterministic, reproducible workflows

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.