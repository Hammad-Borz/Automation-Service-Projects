# 🏢 BusinessCore — End-to-End Business Automation System

> **A production-minded FastAPI workflow platform that turns a validated customer order into coordinated operations, persistence, tasks, notifications, audit events, analytics, and reports.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Tests](https://img.shields.io/badge/Tests-25-16A34A?logo=pytest)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 🎯 What It Solves

BusinessCore demonstrates how individual automation capabilities can be composed into one coordinated business workflow instead of remaining isolated utilities.

```text
Business Request
      ↓
Validation
      ↓
Customer Identify / Create
      ↓
Order Creation
      ↓
Business Rules
      ↓
Tasks + Notifications
      ↓
SQLite Persistence
      ↓
Audit Trail
      ↓
Analytics
      ↓
Business Reports
```

## ⚙️ Core Capabilities

- 🔄 End-to-end business workflow orchestration
- 🛡️ Pydantic request validation
- 👤 Customer identification and creation
- 🛒 Order processing and persistence
- 🧠 Deterministic business-rule evaluation
- 📋 Automatic operational task creation
- 🔔 Notification generation
- 📝 Audit-event recording
- 🗄️ SQLAlchemy + SQLite persistence
- ♻️ Request-ID-based idempotent workflow processing
- 📊 Business analytics and KPI summaries
- 📑 TXT, JSON, CSV, and Excel reporting
- 🌐 FastAPI REST endpoints
- 📚 OpenAPI / Swagger documentation
- 🧪 **25 automated tests**

## 🧠 Business Rules

| Condition | Automated behavior |
|---|---|
| Order amount ≥ 5,000 | High priority + manager approval task |
| Order amount ≥ 10,000 | Urgent priority + additional review workflow |
| Quantity ≥ 10 | Fulfillment task is created |
| Every valid order | Invoice task + customer notification |
| Blocked customer | Workflow is rejected |

The rules are deterministic and testable, making the workflow behavior predictable.

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │   REST API Layer     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   Validation Layer   │
                    │      Pydantic        │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Workflow Engine   │
                    └──────────┬───────────┘
                               ↓
             ┌─────────────────┼─────────────────┐
             ↓                 ↓                 ↓
       Business Rules      Services          Persistence
             │          ┌────────────┐       SQLAlchemy
             │          │ Customer   │           ↓
             │          │ Order      │         SQLite
             │          │ Task       │
             │          │ Notification│
             │          │ Audit      │
             │          └────────────┘
             ↓
       Analytics + Reporting
```

| Layer | Responsibility |
|---|---|
| **API** | HTTP interface, schemas, responses, and health endpoint |
| **Core** | Validation, business rules, and workflow orchestration |
| **Services** | Customer, order, task, notification, audit, analytics, and reporting |
| **Database** | SQLAlchemy sessions and repository operations |
| **Models** | Customer, order, task, notification, audit, and workflow state |

## 🌐 API Surface

| Area | Endpoints |
|---|---|
| Workflow | `POST /api/v1/workflows/process`, `GET /api/v1/workflows/{workflow_id}` |
| Customers | `POST /api/v1/customers`, `GET /api/v1/customers`, `GET /api/v1/customers/{customer_id}` |
| Orders | `POST /api/v1/orders`, `GET /api/v1/orders`, `GET /api/v1/orders/{order_id}` |
| Operations | `GET /api/v1/tasks`, `GET /api/v1/notifications`, `GET /api/v1/audit` |
| Analytics | `GET /api/v1/analytics/summary` |
| Reporting | `POST /api/v1/reports/generate` |
| Health | `GET /api/v1/health` |

Swagger/OpenAPI is available at `/docs`.

## 📁 Project Structure

```text
BusinessCore/
├── .env.example
├── .gitignore
├── README.md
├── pytest.ini
├── requirements.txt
├── sitecustomize.py
├── data/
│   └── input/
│       └── sample_orders.csv
├── docs/
├── src/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── config.py
│   └── main.py
└── tests/
```

## 🧪 Verification

The service-project verification recorded:

```powershell
pytest
python -m src.main
```

**Result: 25 passed**

The application runs with Uvicorn at:

```text
http://127.0.0.1:8000
```

The project uses a local **Python 3.12.x** environment on Windows.

## 🚀 Quick Start

From the **BusinessCore** directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Verify:

```powershell
pytest
python -m src.main
```

For custom configuration:

```text
Copy .env.example → .env
```

Default local outputs:

| Resource | Location |
|---|---|
| SQLite database | `data/businesscore.db` |
| Generated reports | `data/output/` |
| API | `http://127.0.0.1:8000` |
| Swagger UI | `http://127.0.0.1:8000/docs` |

Generated databases, reports, caches, logs, and the virtual environment are excluded from Git.

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| API | FastAPI, Uvicorn |
| Validation | Pydantic |
| ORM / Persistence | SQLAlchemy |
| Database | SQLite |
| Data / Analytics | pandas |
| Excel Reporting | openpyxl |
| Configuration | python-dotenv |
| Testing | pytest, httpx |
| Documentation | OpenAPI / Swagger |

## 💼 Business Value

BusinessCore demonstrates a reusable pattern for:

- Customer order intake
- Order routing and prioritization
- Approval workflows
- Fulfillment task generation
- Customer notifications
- Audit/compliance trails
- Operational analytics
- Automated business reporting

It can serve as a foundation for integrations with CRMs, email systems, payment platforms, ERP systems, task-management tools, and external automation platforms.

## 📌 Portfolio Position

**Project #15 — End-to-End Business Automation Systems**

BusinessCore brings together **API engineering, workflow orchestration, business rules, persistence, operational automation, analytics, reporting, and auditability** in one coordinated system.
