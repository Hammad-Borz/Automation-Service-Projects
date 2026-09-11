# ⚡ EventPulse — Webhook & Event Automation System

> **A production-minded webhook and event-driven automation service built with FastAPI, Pydantic, SQLite, and deterministic business rules.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-34-16A34A)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 🎯 What EventPulse Does

EventPulse receives business webhook events, validates and normalizes them, applies deterministic automation rules, prepares safe local actions, and persists the complete processing lifecycle in SQLite.

It is designed around a common business problem: **webhook integrations become difficult to maintain when HTTP handling, validation, routing, business rules, side effects, and persistence are tightly coupled.** EventPulse separates these responsibilities into clear modules so new event types and rules can be added without rewriting the API layer.

### Business Flow

```text
External System
      ↓
Webhook Request
      ↓
Validate & Normalize
      ↓
Idempotency Check
      ↓
Persist Event
      ↓
Route Event
      ↓
Evaluate Rules
      ↓
Prepare Safe Actions
      ↓
Persist Result
      ↓
Structured Response
```

---

## 🏗️ Architecture

EventPulse follows a modular-monolith architecture with clear boundaries between the API, event-processing logic, database layer, domain models, and services.

```text
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    │ routes + schemas     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Event Normalization  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Event Processor     │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Event Router      │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    Rule Engine       │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Action Executor      │
                    │   safe local actions │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ SQLite Persistence   │
                    └──────────────────────┘
```

### Layer Responsibilities

| Layer | Responsibility |
|---|---|
| `api/` | HTTP routes and Pydantic request/response schemas |
| `core/` | Event processing, routing, business rules, and action execution |
| `database/` | SQLite connection and repository operations |
| `models/` | Normalized event/domain models |
| `services/` | Application-level event and automation services |
| `tests/` | Deterministic API, integration, and unit verification |
| `docs/` | Architecture and setup documentation |

---

## ⚙️ Key Capabilities

- 🔗 Webhook ingestion through FastAPI
- 🛡️ Pydantic validation with flexible event payloads
- 🔄 Event normalization into an internal representation
- 🔀 Event routing based on event family/type
- 🧠 Deterministic business-rule evaluation
- 🗄️ SQLite persistence using parameterized SQL
- ♻️ Idempotency protection using `event_id`
- 📊 Processing status and analytics tracking
- 📝 Structured Python logging
- 🚦 Structured error responses
- 🧪 34 automated tests
- 🔒 Safe local action simulation with no external side effects

---

## 📡 Supported Event Automation

| Event Type | Example Automation |
|---|---|
| `lead.created` | Classify valid leads and prepare sales handling |
| `lead.updated` | Re-evaluate lead information and priority |
| `order.created` | Flag high-value orders at or above the configured threshold |
| `payment.received` | Prepare payment recording and confirmation actions |
| `support.ticket_created` | Route urgent/high-priority support tickets |
| Unknown event | Complete safely with `no_action` |

### Lead Priority Rules

Sales-related terms such as `interested`, `pricing`, `quote`, `demo`, or `buy` can raise a lead's priority. Valid lead data with an email is classified for appropriate sales handling.

### Idempotency

`event_id` is unique in SQLite. If the same webhook is received again, EventPulse records it as a duplicate and returns the original processing result without executing the actions again.

```text
First request
    ↓
Process → Store result → completed

Same event_id again
    ↓
Detect duplicate → Reuse original result → duplicate
```

---

## 🌐 API Surface

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/webhooks/events` | Receive and process an event |
| `GET` | `/events` | List persisted events |
| `GET` | `/events/{event_id}` | Retrieve a specific event |
| `GET` | `/events/{event_id}/result` | Retrieve processing result |
| `GET` | `/automations/rules` | Inspect configured automation rules |
| `GET` | `/analytics/overview` | View processing/automation analytics |

Swagger/OpenAPI is available at `/docs` when the service is running locally.

---

## 🧪 Verification

EventPulse includes **34 automated tests** covering:

- API behavior
- Webhook processing
- Event-family handling
- Event normalization
- Rule evaluation
- Idempotency
- Validation
- Failure handling
- Processing behavior

Run the complete suite with:

```powershell
pytest
```

The tests use temporary SQLite databases and do not require network access, Docker, n8n, Make, paid APIs, or external services.

---

## 🚀 Quick Start

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Start the API

```powershell
python -m src.main
```

The service runs locally and exposes the FastAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

### Alternative Uvicorn command

```powershell
uvicorn src.main:app --reload
```

---

## 📦 Example Webhook

```json
{
  "event_id": "evt_1001",
  "event_type": "lead.created",
  "timestamp": "2026-09-11T10:30:00Z",
  "source": "website",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Corp",
    "message": "Interested in a demo"
  }
}
```

Example processing response:

```json
{
  "event_id": "evt_1001",
  "status": "completed",
  "duplicate": false,
  "result": [
    {
      "action": "notify_sales",
      "status": "prepared",
      "message": "Sales notification prepared"
    }
  ]
}
```

---

## 📁 Project Structure

```text
EventPulse/
├── data/
│   └── .gitkeep
├── docs/
│   ├── architecture/
│   │   └── architecture.md
│   └── setup/
│       └── setup.md
├── src/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── core/
│   │   ├── action_executor.py
│   │   ├── event_processor.py
│   │   ├── event_router.py
│   │   └── rule_engine.py
│   ├── database/
│   │   ├── connection.py
│   │   └── repository.py
│   ├── models/
│   │   └── events.py
│   ├── services/
│   │   ├── automation_service.py
│   │   └── event_service.py
│   ├── config.py
│   └── main.py
├── tests/
│   ├── test_api.py
│   ├── test_event_families.py
│   ├── test_event_processing.py
│   ├── test_failures.py
│   ├── test_idempotency.py
│   ├── test_normalization.py
│   ├── test_rules.py
│   ├── test_validation.py
│   └── test_webhooks.py
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🔐 Security & Production Considerations

The demonstration implementation validates incoming payloads, uses parameterized SQL, avoids exposing stack traces through API responses, and performs no real external side effects.

A production deployment should additionally consider:

- Signed webhook authentication
- HTTPS/TLS
- Secret management
- Rate limiting and access controls
- Retry and dead-letter policies
- Metrics and observability
- Durable queues for asynchronous workloads
- Real action integrations behind controlled interfaces

These concerns are intentionally documented separately from the local demonstration so the core event-processing architecture remains deterministic and easy to test.

---

## 💼 Portfolio Value

EventPulse demonstrates the engineering patterns required for **event-driven business automation** rather than a simple webhook endpoint:

- Clean API boundaries
- Normalized internal events
- Deterministic routing and rules
- Idempotent processing
- Persistent operational history
- Safe action execution
- Structured errors and logging
- Automated verification
- Clear architecture and setup documentation

It can serve as a foundation for integrations such as CRM events, e-commerce events, payment notifications, support workflows, and other webhook-driven business processes.

---

## 🛠️ Technology Stack

`Python 3.11+` • `FastAPI` • `Pydantic 2` • `Uvicorn` • `SQLite` • `pytest` • `SQL` • `REST/Webhooks`

---

## 👨‍💻 Author

**Hammad Borz**

> Python • AI Automation • Webhooks • Event-Driven Automation • FastAPI • API Integration • Business Automation
