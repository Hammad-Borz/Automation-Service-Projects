# ⚡ EventPulse — Webhook & Event Automation System

> **A modular event-driven automation service that receives webhooks, validates and normalizes events, applies deterministic business rules, prevents duplicate processing, persists results in SQLite, and exposes operational APIs.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-34-16A34A?logo=pytest)
![Status](https://img.shields.io/badge/Status-Complete-16A34A)

---

## 1. 🎯 Project Title

**EventPulse — Webhook & Event Automation System**

EventPulse is a service-specific business automation project focused on webhook ingestion, event-driven processing, deterministic rules, idempotency, safe action preparation, and persistent operational history.

---

## 2. 📝 One-Line Description

> **Webhook → validate → normalize → idempotency check → route → evaluate rules → prepare actions → persist result.**

---

## 3. 🔴 Problem

Webhook-driven business integrations can become difficult to maintain when transport handling, validation, normalization, routing, business rules, side effects, and persistence are tightly coupled.

A robust automation service needs to answer questions such as:

- Is the incoming payload valid?
- What internal event does it represent?
- Has this event already been processed?
- Which business workflow should handle it?
- Which deterministic rules apply?
- What action should be prepared?
- What happened to the event after processing?
- Can the result be inspected later?

---

## 4. 🟢 Solution

EventPulse separates those responsibilities into explicit application boundaries.

```text
🌐 External System
       ↓
📡 FastAPI Webhook
       ↓
🛡️ Pydantic Validation
       ↓
🔄 Event Normalization
       ↓
♻️ Idempotency Check
       ↓
🗄️ Persist Event
       ↓
🔀 Event Routing
       ↓
🧠 Deterministic Rules
       ↓
⚙️ Safe Action Preparation
       ↓
🗄️ Persist Result
       ↓
📤 Structured API Response
```

The project uses a modular-monolith architecture: FastAPI handles transport and validation, services normalize external payloads, the event processor coordinates execution, core modules own routing/rules/action preparation, and the repository owns SQLite persistence.

---

## 5. ⚙️ Key Features

- 📡 FastAPI webhook ingestion
- 🛡️ Pydantic request validation with extra fields rejected
- 🔄 Normalization into an internal `NormalizedEvent`
- 🔀 Event-family routing
- 🧠 Deterministic business-rule evaluation
- ♻️ `event_id`-based idempotency
- 🗄️ SQLite persistence
- 🔐 Parameterized SQL
- ⚙️ Safe local action preparation with no external side effects
- 📊 Processing analytics
- 🔎 Event and result lookup endpoints
- 📋 Configured-rule inspection endpoint
- 📝 Structured error responses and server-side logging
- 🧪 **34 automated tests**
- 📚 Architecture and setup documentation

---

## 6. 🔄 How It Works

1. **Receive** — FastAPI accepts a webhook at `POST /webhooks/events`.
2. **Validate** — Pydantic validates the event envelope.
3. **Normalize** — The external payload is converted into a `NormalizedEvent`.
4. **Check idempotency** — The `event_id` primary key prevents the same event from being processed twice.
5. **Persist** — A new event is stored with `processing` status.
6. **Route** — The event type is mapped to a workflow.
7. **Evaluate rules** — Deterministic rules inspect the normalized event.
8. **Prepare actions** — The action executor creates safe local action records.
9. **Persist result** — The event is updated with its final status and result.
10. **Respond** — The API returns a structured response.
11. **Observe** — Events, results, duplicate deliveries, and analytics remain queryable.

---

## 7. 🏗️ Architecture / Workflow

```text
┌─────────────────────────┐
│      FastAPI API        │
│ routes + Pydantic       │
│ validation              │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│   Event Normalization   │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│    Event Processor      │
└────────────┬────────────┘
             ↓
      ┌──────┴──────┐
      │             │
      ↓             ↓
┌───────────┐  ┌──────────────┐
│Idempotency│  │ SQLite       │
│event_id   │  │ Repository   │
└─────┬─────┘  └──────────────┘
      ↓
┌─────────────────────────┐
│     Event Router        │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│      Rule Engine        │
└────────────┬────────────┘
             ↓
┌─────────────────────────┐
│     Action Executor     │
│    safe local work      │
└────────────┬────────────┘
             ↓
      Persist Result
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `api/` | HTTP routes and Pydantic request/response schemas |
| `services/` | Normalize inbound webhook data |
| `core/event_processor.py` | Coordinate persistence, routing, rules, actions, and final status |
| `core/event_router.py` | Map event types to workflows |
| `core/rule_engine.py` | Evaluate deterministic business rules |
| `core/action_executor.py` | Convert rule results into safe local action records |
| `database/` | SQLite connection, schema initialization, and repository operations |
| `models/` | Internal normalized event model |
| `tests/` | API, integration, and unit verification |
| `docs/` | Architecture and setup documentation |

### Event Lifecycle

```text
New Event
   ↓
processing
   ↓
completed
   │
   └── or failed

Repeated event_id
   ↓
duplicate
```

Unknown event types are handled safely with a `no_action` result rather than an external side effect.

---

## 8. 🛠️ Technologies

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application implementation |
| **FastAPI** | REST API and webhook ingestion |
| **Pydantic 2** | Request and response validation |
| **Uvicorn** | ASGI application server |
| **SQLite** | Local event persistence |
| **SQL** | Parameterized persistence queries |
| **pytest** | Automated testing |
| **httpx** | HTTP/API testing support |

Dependencies are declared in `requirements.txt`.

---

## 9. 📁 Project Structure

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

### Main Runtime Data

```text
data/eventpulse.sqlite3
```

The database schema contains `events` and `duplicate_events`. The `events` table stores event IDs, types, sources, payloads, timestamps, status, results, and errors.

---

## 10. 🚀 Installation

From the `EventPulse` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Start the API

```powershell
uvicorn src.main:app --reload
```

The service starts locally on `http://127.0.0.1:8000`.

---

## 11. 🔧 Configuration

EventPulse works with defaults and does **not require a `.env` file** for the standard local setup.

Optional environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `EVENTPULSE_DATABASE_PATH` | `data/eventpulse.sqlite3` | SQLite database location |
| `EVENTPULSE_ENVIRONMENT` | `development` | Application environment |
| `EVENTPULSE_LOGGING_LEVEL` | `INFO` | Logging level |

The database directory and schema are initialized when the application starts.

---

## 12. ▶️ Usage

### Start with Uvicorn

```powershell
uvicorn src.main:app --reload
```

### Swagger / OpenAPI

Open `http://127.0.0.1:8000/docs`.

ReDoc is available at `http://127.0.0.1:8000/redoc`.

### Send a Webhook

```powershell
$body = '{"event_id":"evt_demo","event_type":"lead.created","timestamp":"2026-09-11T10:30:00Z","source":"website","data":{"email":"demo@example.com","message":"Interested in pricing"}}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/webhooks/events -Method Post -ContentType 'application/json' -Body $body
```

### Run Tests

```powershell
pytest -q
```

---

## 13. 🧪 Example

### Example Webhook

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

Because the event comes from the website and contains an email plus a sales term, the deterministic rule engine prepares a sales notification.

### Example Response

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

### Duplicate Delivery

Sending the same `event_id` again is detected through the SQLite primary key.

```text
First request
    ↓
Process → Persist result → completed

Same event_id
    ↓
Duplicate detected → duplicate
```

The original event is not reprocessed.

### Supported Event Automation

| Event Type | Rule / Behavior |
|---|---|
| `lead.created` | Website + email → sales notification; sales terms produce high priority |
| `lead.updated` | Re-evaluate lead information using the lead automation rules |
| `order.created` | Total ≥ 1000 → flag high-value order |
| `payment.received` | Prepare local payment-recording and confirmation actions |
| `support.ticket_created` | Urgent/high priority → prepare support routing |
| Unknown event type | Safe `no_action` |

---

## 14. 📸 Screenshots

> **Reserved area — screenshots will be added later.**

Planned portfolio evidence:

- 🌐 Swagger/OpenAPI interface
- 📡 Webhook request
- 📤 Structured API response
- ♻️ Duplicate-event response
- 🗄️ SQLite event records
- 📊 Analytics overview
- 📋 Configured automation rules
- 🧪 Test results

---

## 15. 🎥 Demo Video / GIF

> **Reserved area — demo video/GIF will be added later.**

Planned demonstration:

```text
Start EventPulse
      ↓
Open Swagger
      ↓
POST webhook event
      ↓
Validate + normalize
      ↓
Check event_id
      ↓
Route event
      ↓
Evaluate business rules
      ↓
Prepare safe action
      ↓
Persist result in SQLite
      ↓
Show API response
      ↓
Send same event again
      ↓
Show duplicate protection
      ↓
Open analytics
```

The demonstration should show the system's local behavior without implying that real external emails, SMS messages, payments, or third-party actions are being executed.

---

## 16. 📊 Results / Benefits

EventPulse demonstrates:

- **Webhook-driven automation** through a FastAPI REST interface.
- **Clear separation of concerns** between transport, normalization, processing, rules, actions, and persistence.
- **Deterministic business automation** with explicit, inspectable rules.
- **Idempotent event processing** using `event_id` as the event primary key.
- **Persistent operational history** through SQLite.
- **Safe action preparation** without real external side effects.
- **Structured API errors** that avoid exposing implementation details.
- **Operational analytics** for totals, completed/failed events, duplicates, event types, and prepared actions.
- **Automated verification** with 34 documented tests.
- **Local reproducibility** without Docker, n8n, Make, paid APIs, or external services for the test suite.

---

## 17. ⚠️ Limitations

- Action execution is simulated/prepared locally; it does not send real external notifications or perform third-party side effects.
- SQLite is used for persistence rather than a production distributed database.
- There is no durable message queue.
- There is no asynchronous worker architecture.
- Webhook signature verification is not currently implemented.
- Production HTTPS/TLS is not provided by the local application itself.
- Rate limiting and production authentication are not implemented.
- Retry/dead-letter policies are not implemented.
- Observability is limited to application logging and stored analytics.
- The rule engine is deterministic and code-defined rather than externally configurable.

---

## 18. 🔮 Future Improvements

- 🔐 Webhook signature verification
- 🔑 Secret management
- 🌐 HTTPS/TLS deployment
- 🚦 Rate limiting and authentication
- 🔁 Retry and dead-letter policies
- 📨 Durable message queues
- ⚡ Asynchronous workers
- 📊 Advanced metrics and observability
- 🔌 Controlled external integrations
- 🧩 Externalized rule configuration
- 🗄️ Production database support

These are future extensions, not current implementation claims.

---

## 19. 📜 License

No dedicated `LICENSE` file is currently documented for EventPulse.

> If the project is later distributed as open-source software, add the appropriate license file and update this section.

---

## 20. 👤 Author / Contact

**Hammad Borz**

- GitHub: [@Hammad-Borz](https://github.com/Hammad-Borz)
- Repository: [Automation-Service-Projects](https://github.com/Hammad-Borz/Automation-Service-Projects)

---

## 💼 Portfolio Positioning

**EventPulse** is a service-specific **Webhook & Event Automation** project demonstrating:

- Python backend development
- FastAPI REST APIs
- Webhook ingestion
- Pydantic validation
- Event normalization
- Event-driven architecture
- Deterministic business rules
- Idempotent processing
- SQLite persistence
- Safe action preparation
- Structured API errors
- Operational analytics
- Automated testing
- Modular architecture

> **Portfolio note:** Points **14 (Screenshots)** and **15 (Demo Video/GIF)** are intentionally reserved for the later Visual Presentation and Demo Video phases.