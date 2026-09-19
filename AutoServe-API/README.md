# ⚙️ AutoServe API — Automation Backend Platform

> **A reusable FastAPI automation backend for deterministic job execution, lifecycle management, idempotency, controlled retries, auditability, metrics, and SQLite persistence.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.10.6-E92063?logo=pydantic&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)

AutoServe API is a local automation backend built with **FastAPI, Pydantic, Python, and SQLite**. It provides a structured lifecycle for automation jobs: validate a request, create an idempotent job, execute a registered local action, persist the result, record audit events, support controlled retries, and expose operational metrics.

The implementation is intentionally local and deterministic. The currently registered actions simulate business operations without sending real notifications, calling cloud APIs, or requiring credentials.

---

## 1. 📌 Project Title

**AutoServe API — Automation Backend Platform**

**Service category:** Automation Backend / Python API

---

## 2. 📝 One-Line Description

> A local FastAPI backend that manages deterministic automation jobs with validation, state transitions, idempotency, retries, audit logs, persistence, and metrics.

---

## 3. 🎯 Problem

A production-oriented automation backend needs more than a function that performs an action.

A reliable job-processing layer also needs to answer:

- Has this request already been submitted?
- What state is the job currently in?
- What happened during execution?
- Can a failed job be retried safely?
- How many attempts have occurred?
- What actions were executed?
- What results were produced?
- How can operators inspect aggregate execution metrics?

Without explicit lifecycle management, persistence, idempotency, retry controls, and auditability, automation workflows become harder to reason about and operate consistently.

---

## 4. 💡 Solution

AutoServe API packages these backend concerns into a modular local service.

### Core execution flow

```text
Client
  ↓
FastAPI
  ↓
Pydantic Validation
  ↓
Job Management
  ↓
State Machine
  ↓
Execution Engine
  ↓
Action Registry
  ↓
SQLite Persistence
  ├── Jobs
  ├── Runs
  ├── Results
  └── Audit Logs
```

The result is a reusable foundation for automation services where execution must be **controlled, traceable, repeatable, and locally testable**.

---

## 5. ✨ Key Features

- 🌐 **FastAPI REST API** with OpenAPI/Swagger documentation.
- 🧱 **Explicit job state machine** for controlled lifecycle transitions.
- ♻️ **Request-ID idempotency** to prevent duplicate job creation.
- ▶️ **Deterministic local execution** through a registered action system.
- 🧪 **Run tracking** with persisted action results.
- 🔁 **Controlled retries** with a configurable maximum retry count.
- 📝 **Audit logging** for important lifecycle and execution events.
- 📊 **Database-backed metrics** calculated from persisted records.
- 🗄️ **SQLite persistence** using parameterized SQL.
- 🔒 **Local-only execution** with no external side effects.
- 🧩 **Separation of API, service, core, repository, and data responsibilities**.
- 🧪 **Isolated testing support** for the application and database behavior.

---

## 6. ⚙️ How It Works

A typical automation request follows this lifecycle:

1. **Client submits** a job request.
2. **Pydantic validates** the request payload and required identifiers.
3. **Idempotency checks** determine whether the `request_id` already exists.
4. **Job creation** stores the request with a pending status.
5. **Execution** starts the requested automation.
6. **State validation** ensures the requested transition is allowed.
7. **Action resolution** selects the registered local action.
8. **Action execution** produces a deterministic result.
9. **Persistence** stores the result and run information.
10. **Completion or failure** updates the job/run lifecycle state.
11. **Audit logging** records important events.
12. **Metrics** can be queried from the persisted database state.

### Failure path

```text
Execution
   ↓
Failure
   ↓
Persist failure
   ↓
Audit event
   ↓
Retry request
   ↓
New run
   ↓
Successful completion OR recorded failure
```

---

## 7. 🏗️ Architecture / Workflow

```text
┌──────────────────────────────┐
│            Client            │
└──────────────┬───────────────┘
               │ HTTP
               ▼
┌──────────────────────────────┐
│        FastAPI Layer         │
│ Routes + Request Schemas     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Service Layer          │
│ Jobs / Runs / Audit / Metrics│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Core Layer          │
│ State / Actions / Retry /    │
│ Idempotency                  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Repository Layer       │
│ SQLite persistence + queries │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│            SQLite            │
│ Jobs / Runs / Results / Logs │
└──────────────────────────────┘
```

### Architectural responsibilities

| Layer | Responsibility |
|---|---|
| **API** | FastAPI routes, request handling, and API schemas |
| **Service** | Job execution, run management, audit handling, and metrics |
| **Core** | State transitions, action registry, idempotency, and retry rules |
| **Repository** | SQLite persistence and database queries |
| **Data** | Jobs, runs, action results, and audit records |

---

## 8. 🛠️ Technologies

| Technology | Version | Purpose |
|---|---:|---|
| **Python** | 3.x | Application language |
| **FastAPI** | 0.115.6 | REST API framework |
| **Uvicorn** | 0.32.1 | ASGI application server |
| **Pydantic** | 2.10.6 | Request/data validation |
| **SQLite** | Local | Persistent relational storage |
| **pytest** | 8.3.4 | Automated testing |
| **httpx** | 0.28.1 | API/test HTTP client support |

The runtime application is designed for local execution and does not require cloud services or external API credentials.

---

## 9. 📁 Project Structure

```text
AutoServe-API/
├── data/
│   └── autoserve.db              # Runtime SQLite database
├── docs/
│   ├── architecture/
│   └── setup/
├── src/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── config.py
│   └── main.py
├── tests/
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

The project separates HTTP/API concerns from business execution, persistence, models, and supporting services.

---

## 10. 🚀 Installation

### Prerequisites

- Python 3.x
- Git
- PowerShell, Command Prompt, or another terminal

### Clone the repository

```bash
git clone https://github.com/Hammad-Borz/Automation-Service-Projects.git
cd Automation-Service-Projects/AutoServe-API
```

### Create a virtual environment

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

AutoServe uses environment variables for optional local configuration.

| Variable | Default | Purpose |
|---|---|---|
| `AUTOSERVE_ENVIRONMENT` | `local` | Identifies the runtime environment |
| `AUTOSERVE_DB_PATH` | `data/autoserve.db` | Overrides the SQLite database path |

### Retry configuration

The current application configuration defines:

```text
MAX_RETRY_COUNT = 3
```

### Example PowerShell configuration

```powershell
$env:AUTOSERVE_ENVIRONMENT="local"
$env:AUTOSERVE_DB_PATH="data/autoserve.db"
```

No API keys, passwords, or third-party service credentials are required for the current implementation.

---

## 12. ▶️ Usage

### Start the API

From the `AutoServe-API/` directory:

```powershell
python -m src.main
```

The application runs locally at:

```text
http://127.0.0.1:8000
```

### API documentation

FastAPI exposes:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/openapi.json
```

### Run the test suite

```powershell
pytest
```

---

## 13. 🧪 Example

### Example automation lifecycle

A client can create an automation job, execute it, inspect the resulting run, and query metrics.

```text
POST /jobs
     │
     │ request_id = "request-001"
     ▼
┌─────────────────────┐
│ Job created         │
│ status: pending     │
└─────────┬───────────┘
          │
          ▼
POST /jobs/{job_id}/execute
          │
          ▼
┌─────────────────────┐
│ Action resolved     │
│ Action executed     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Run + result stored │
│ Job completed       │
└─────────┬───────────┘
          │
          ▼
GET /runs/{run_id}

GET /metrics/summary
```

### Supported local actions

| Action | Example purpose |
|---|---|
| `send_notification` | Simulate notification delivery |
| `create_task` | Produce a local task result |
| `update_customer_status` | Produce a customer-status update result |
| `generate_summary` | Generate a deterministic text summary |

These are **local simulations** and do not send real notifications or call external services.

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

AutoServe provides a structured backend foundation for local automation workflows:

- Centralizes automation job lifecycle management.
- Prevents duplicate job creation through request-ID idempotency.
- Makes execution states explicit and traceable.
- Preserves run and action-result history.
- Provides controlled retry behavior for failed jobs.
- Records important lifecycle events through audit logs.
- Exposes database-backed operational metrics.
- Keeps the current automation actions deterministic and side-effect free.
- Separates API, business logic, persistence, and data responsibilities.

### Operational visibility

The metrics service exposes:

- Total jobs
- Pending jobs
- Running jobs
- Completed jobs
- Failed jobs
- Total runs
- Successful runs
- Failed runs
- Success rate

---

## 17. ⚠️ Limitations

The current implementation has a deliberately local scope:

- Automation actions are deterministic local simulations.
- No real email, messaging, payment, CRM, or external API integration is included.
- SQLite is used for persistence rather than a production database server.
- Execution is local rather than queue-based or distributed.
- There is no background worker system in the current implementation.
- Observability is exposed through API metrics rather than a dedicated dashboard.
- Retry behavior is controlled by the configured maximum count; advanced backoff strategies are not currently described as implemented.
- Authentication and authorization are not part of the current API scope.
- The API is configured for local execution on `127.0.0.1:8000`.

---

## 18. 🔮 Future Improvements

Potential extensions include:

- Queue- or background-worker-based execution.
- Plugin-based automation types.
- Richer run and job filtering.
- Advanced retry and backoff policies.
- External service integrations.
- Authentication and authorization.
- Dedicated observability dashboards.
- More advanced operational monitoring.
- Production database support such as PostgreSQL.
- Expanded automation action libraries.

These are **future extensions**, not capabilities currently claimed as implemented.

---

## 19. 📄 License

No dedicated license file is currently included in the AutoServe API project directory.

Until a license is added, treat the project as **all rights reserved** rather than assuming an open-source license.

---

## 20. 👤 Author / Contact

**Hammad-Borz**

- GitHub: [Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

For project-related discussion, use the repository's GitHub Issues or project documentation.

---

## 💼 Portfolio Positioning

**Service:** Automation Backend / Python API  
**Project:** AutoServe API — Automation Backend Platform  
**Focus:** REST API design, automation lifecycle management, idempotency, retry control, auditability, persistence, metrics, and deterministic execution.

AutoServe API demonstrates how a repetitive automation requirement can be structured into a maintainable backend with explicit lifecycle controls and operational visibility.

---

## 🧪 Verification

The project includes tests covering areas such as:

- API health and behavior
- Request/data schemas
- State transitions
- Action registration
- Job creation and execution
- Idempotency
- Retry handling
- Repository behavior
- Audit logging
- Metrics
- Error handling

Run the verification suite with:

```powershell
pytest
```

---

> **Built as part of a professional automation-services portfolio.**
