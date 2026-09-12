# 🏢 BusinessCore — End-to-End Business Automation System

> **A production-minded FastAPI workflow platform that turns a validated customer order into coordinated business operations, persistence, tasks, notifications, audit events, analytics, and reports.**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-25-16A34A)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 🎯 Project Overview

**BusinessCore** is an end-to-end business automation backend rather than a simple CRUD API. It orchestrates a complete order-processing workflow from request validation through operational execution and reporting.

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

The system is designed to demonstrate how individual automation capabilities can be composed into one reusable business workflow platform.

---

## ✨ Core Capabilities

- 🔄 End-to-end business workflow orchestration
- 🛡️ Pydantic request validation
- 👤 Customer identification and creation
- 🛒 Order processing and persistence
- 🧠 Deterministic business-rule evaluation
- 📋 Automatic operational task creation
- 🔔 Notification generation
- 📝 Audit-event recording
- 🗄️ SQLAlchemy + SQLite persistence
- ♻️ Request-id based idempotent workflow processing
- 📊 Business analytics and KPI summaries
- 📑 TXT/JSON/CSV/Excel reporting support
- 🌐 FastAPI REST endpoints
- 📚 OpenAPI / Swagger documentation
- 🧪 Automated pytest verification

---

## 🧠 Business Rules

BusinessCore applies deterministic rules to each valid order so that business decisions are represented as executable automation logic.

| Condition | Automated behavior |
|---|---|
| Order amount ≥ 5,000 | High priority + manager approval task |
| Order amount ≥ 10,000 | Urgent priority + additional review workflow |
| Quantity ≥ 10 | Fulfillment task is created |
| Every valid order | Invoice task + customer notification |
| Blocked customer | Workflow is rejected |

These rules are intentionally deterministic and testable, making the workflow predictable and suitable for automation backends.

---

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

### Layer responsibilities

- **API:** HTTP interface, request schemas, response handling, health endpoint
- **Core:** validation, business rules, workflow orchestration
- **Services:** customer, order, task, notification, audit, analytics, and reporting operations
- **Database:** SQLAlchemy session management and repository operations
- **Models:** customer, order, task, notification, audit, and workflow state

---

## 📡 API Surface

### Workflow
- `POST /api/v1/workflows/process`
- `GET /api/v1/workflows/{workflow_id}`

### Customers
- `POST /api/v1/customers`
- `GET /api/v1/customers`
- `GET /api/v1/customers/{customer_id}`

### Orders
- `POST /api/v1/orders`
- `GET /api/v1/orders`
- `GET /api/v1/orders/{order_id}`

### Operations
- `GET /api/v1/tasks`
- `GET /api/v1/notifications`
- `GET /api/v1/audit`

### Analytics & Reporting
- `GET /api/v1/analytics/summary`
- `POST /api/v1/reports/generate`

### Health
- `GET /api/v1/health`

Swagger/OpenAPI is available when the application is running at `/docs`.

---

## 🗂️ Project Structure

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
│   └── setup/
│       └── README.md
├── src/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── business_rules.py
│   │   ├── validation.py
│   │   └── workflow_engine.py
│   ├── database/
│   │   ├── connection.py
│   │   └── repository.py
│   ├── models/
│   │   ├── audit.py
│   │   ├── customer.py
│   │   ├── notification.py
│   │   ├── order.py
│   │   ├── task.py
│   │   └── workflow.py
│   ├── services/
│   │   ├── analytics_service.py
│   │   ├── audit_service.py
│   │   ├── customer_service.py
│   │   ├── notification_service.py
│   │   ├── order_service.py
│   │   ├── reporting_service.py
│   │   └── task_service.py
│   ├── config.py
│   └── main.py
└── tests/
    ├── test_api.py
    ├── test_business_rules.py
    ├── test_validation.py
    └── test_workflow.py
```

---

## 🧪 Verification

The project was verified with the standard service-project checks:

```powershell
pytest
python -m src.main
```

**Result:** `25 passed`

The application starts successfully with Uvicorn at:

```text
http://127.0.0.1:8000
```

The project uses its own local `.venv` and is configured for **Python 3.12.x** on Windows.

> ⚠️ The current dependency pins are intentionally used with Python 3.12 because the selected FastAPI/Pydantic/SQLAlchemy/pandas/reporting stack provides the required Windows-compatible wheels there.

---

## ⚙️ Setup

From the **BusinessCore** directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Then verify:

```powershell
pytest
python -m src.main
```

For custom configuration, copy `.env.example` to `.env`.

Default configuration uses:

- SQLite database: `data/businesscore.db`
- Generated reports: `data/output/`
- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

Generated databases, reports, caches, logs, and the virtual environment are excluded from Git.

---

## 🧰 Technology Stack

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

---

## 💼 Business Value

BusinessCore demonstrates a reusable pattern for automating operational business processes such as:

- customer order intake
- order routing and prioritization
- approval workflows
- fulfillment task generation
- customer notifications
- audit/compliance trails
- operational analytics
- automated business reporting

It can serve as a foundation for larger integrations with CRMs, email systems, payment platforms, ERP systems, task-management tools, and external automation platforms.

---

## 📌 Portfolio Position

**Project #15 — End-to-End Business Automation Systems**

BusinessCore extends the portfolio from individual automation capabilities into a coordinated business-process platform that combines **API engineering, workflow orchestration, business rules, persistence, operational automation, analytics, reporting, and auditability** in one system.
