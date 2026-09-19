# ⚡ EventPulse — Webhook & Event Automation System

> **A production-minded webhook and event-driven automation service built with FastAPI, Pydantic, SQLite, and deterministic business rules.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-34-16A34A?logo=pytest)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 🎯 What It Solves

Webhook integrations become difficult to maintain when HTTP handling, validation, routing, business rules, side effects, and persistence are tightly coupled.

**EventPulse separates those responsibilities** into a modular event-processing pipeline:

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

## 🏗️ Architecture

EventPulse uses a modular-monolith design with explicit boundaries between the API, processing logic, database layer, domain models, and services.

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
                    │    Action Executor   │
                    │    safe local work   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ SQLite Persistence   │
                    └──────────────────────┘
```

| Layer | Responsibility |
|---|---|
| `api/` | HTTP routes and Pydantic request/response schemas |
| `core/` | Event processing, routing, rules, and action execution |
| `database/` | SQLite connection and repository operations |
| `models/` | Normalized event/domain models |
| `services/` | Application-level event and automation services |
| `tests/` | API, integration, and unit verification |
| `docs/` | Architecture and setup documentation |

## ⚙️ Key Capabilities

- 🔗 FastAPI webhook ingestion
- 🛡️ Pydantic payload validation
- 🔄 Event normalization
- 🔀 Event-family routing
- 🧠 Deterministic business rules
- ♻️ `event_id`-based idempotency
- 🗄️ SQLite persistence with parameterized SQL
- 📊 Processing and analytics tracking
- 📝 Structured logging and errors
- 🔒 Safe local action simulation
- 🧪 **34 automated tests**

## 📡 Supported Automation

| Event | Example behavior |
|---|---|
| `lead.created` | Classify valid leads and prepare sales handling |
| `lead.updated` | Re-evaluate lead information and priority |
| `order.created` | Flag high-value orders at the configured threshold |
| `payment.received` | Prepare payment recording/confirmation actions |
| `support.ticket_created` | Route urgent or high-priority tickets |
| Unknown event | Complete safely with `no_action` |

Lead rules recognize terms such as `interested`, `pricing`, `quote`, `demo`, and `buy` when determining sales priority.

### Idempotency

Repeated delivery of the same `event_id` is detected through a SQLite uniqueness constraint. The existing processing result is reused instead of executing the automation again.

```text
First event
   ↓
Process → Store result → completed

Same event_id
   ↓
Detect duplicate → Reuse result → duplicate
```

## 🌐 API Surface

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/webhooks/events` | Receive and process an event |
| `GET` | `/events` | List persisted events |
| `GET` | `/events/{event_id}` | Retrieve an event |
| `GET` | `/events/{event_id}/result` | Retrieve its result |
| `GET` | `/automations/rules` | Inspect configured rules |
| `GET` | `/analytics/overview` | View processing analytics |

Swagger/OpenAPI is available at `/docs`.

## 🧪 Verification

**34 automated tests** cover:

- API behavior
- Webhook processing
- Event-family handling
- Normalization
- Rule evaluation
- Idempotency
- Validation
- Failure handling
- Processing behavior

```powershell
pytest
```

Tests use temporary SQLite databases and do not require network access, Docker, n8n, Make, paid APIs, or external services.

## 🚀 Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.main
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative:

```powershell
uvicorn src.main:app --reload
```

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

Example response:

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

## 📁 Project Structure

```text
EventPulse/
├── data/
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

## 🔐 Security & Production Considerations

The local implementation validates payloads, uses parameterized SQL, avoids exposing stack traces through API responses, and performs no real external side effects.

A production deployment should additionally consider:

- Signed webhook authentication
- HTTPS/TLS
- Secret management
- Rate limiting and access controls
- Retry and dead-letter policies
- Metrics and observability
- Durable queues
- Controlled external integrations

## 💼 Portfolio Value

EventPulse demonstrates **event-driven business automation** through:

- Clean API boundaries
- Normalized internal events
- Deterministic routing and rules
- Idempotent processing
- Persistent operational history
- Safe action execution
- Structured errors and logging
- Automated verification
- Architecture documentation

## 🛠️ Technology Stack

`Python 3.11+` • `FastAPI` • `Pydantic 2` • `Uvicorn` • `SQLite` • `pytest` • `SQL` • `REST/Webhooks`

## 👨‍💻 Author

**Hammad Borz**

> Python • AI Automation • Webhooks • Event-Driven Automation • FastAPI • API Integration • Business Automation
