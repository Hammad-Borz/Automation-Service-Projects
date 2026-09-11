# 🏗️ AutomationFlow — System Architecture

> **AutomationFlow** is a business lead-processing automation system demonstrating how **n8n, Make, Python, HTTP APIs, validation, routing, and structured responses** can be combined into a practical automation workflow.

---

## 🎯 Architecture Goal

The system receives a business lead through a webhook, validates the incoming data, processes the lead, determines its priority and type, and prepares the appropriate business automation action.

The architecture deliberately keeps the orchestration layer separate from the supporting Python service so the workflow can be implemented and compared across both **n8n** and **Make**.

---

## 🧩 High-Level Architecture

```text
                         BUSINESS LEAD
                              │
                              ▼
                    ┌───────────────────┐
                    │   Webhook Input   │
                    │  JSON Lead Data   │
                    └─────────┬─────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌────────────────┐
        │      n8n      │          │      Make      │
        │ Orchestration │          │  Orchestration │
        └───────┬───────┘          └───────┬────────┘
                │                           │
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌────────────────┐
        │ Python HTTP   │          │ Native Make    │
        │ Lead Processor│          │ Classification │
        └───────┬───────┘          └───────┬────────┘
                │                           │
                ▼                           ▼
        ┌───────────────┐          ┌────────────────┐
        │ Lead Analysis │          │ Lead Routing   │
        │ type/priority │          │ by category   │
        │ score/reason  │          │ and priority   │
        └───────┬───────┘          └───────┬────────┘
                │                           │
                └─────────────┬─────────────┘
                              ▼
                    ┌───────────────────┐
                    │ Structured JSON   │
                    │ Automation Result │
                    └───────────────────┘
```

---

## 🔵 n8n Architecture

The primary implementation is built as an n8n workflow:

```text
Webhook
   ↓
Edit Fields
   ↓
IF — Email Validation
   ├── Invalid → Respond to Webhook
   │
   └── Valid
        ↓
     HTTP Request
        ↓
     Python Lead Processor
        ↓
     IF — High Priority
        ↓
     Edit Fields
        ↓
     Respond to Webhook
```

### Responsibilities

| Component | Responsibility |
|---|---|
| Webhook | Receives lead JSON from an external client/system |
| Edit Fields | Normalizes incoming webhook fields |
| IF | Validates that an email is present |
| HTTP Request | Sends valid leads to the Python processing API |
| Python service | Classifies the lead and calculates score/priority |
| IF1 | Detects high-priority leads |
| Edit Fields1 | Builds the automation action payload |
| Respond to Webhook | Returns a structured result to the caller |

---

## 🟢 Make Architecture

Make provides a second implementation using native Make routing rather than calling the local Python service.

```text
Custom Webhook
      ↓
Classify Lead — Flow Control
      ├── Invalid Lead → Webhook Response
      ├── Sales Lead → Webhook Response
      ├── Support Lead → Webhook Response
      ├── Billing Lead → Webhook Response
      └── General Lead → Webhook Response
```

This distinction is intentional:

- **n8n:** orchestration + Python HTTP processing.
- **Make:** cloud-native routing and classification.

This demonstrates the ability to design the same business requirement using two automation platforms without incorrectly implying that a cloud Make scenario can directly access the local Docker/Python environment.

---

## 🐍 Python Supporting Service

The Python service is a lightweight FastAPI application.

```text
HTTP Request
     ↓
FastAPI /process-lead
     ↓
process_lead()
     ↓
Keyword Classification
     ↓
Lead Score
     ↓
Priority
     ↓
JSON Response
```

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Service health check |
| `POST` | `/process-lead` | Analyze and score a lead |
| `POST` | `/notify-sales` | Prepare a sales notification response |

---

## 🧠 Lead Analysis Logic

The processor evaluates message content against business keyword groups:

```text
Message
   │
   ├── Sales keywords
   ├── Support keywords
   └── Billing keywords
          ↓
      Lead Type
          ↓
      Base Score
          ↓
   Source / Urgency Adjustments
          ↓
      Final Score
          ↓
       Priority
```

The resulting analysis contains:

- `lead_type`
- `priority`
- `score`
- `reason`

---

## 🔐 Validation & Safety

AutomationFlow uses several simple but important safeguards:

- Email presence is checked before processing in the n8n workflow.
- Structured JSON is used between workflow components.
- The Python API returns explicit success/error responses.
- External actions are represented as prepared automation results rather than silently sending real-world notifications.
- The Make scenario is designed around explicit routing branches.

---

## 🔄 End-to-End Data Flow

```text
Client / Form / CRM
        ↓
Webhook JSON
        ↓
Validate Lead
        ↓
Classify Lead
        ↓
Calculate Score
        ↓
Determine Priority
        ↓
Prepare Automation Action
        ↓
Structured JSON Response
```

---

## 📁 Architecture Components

```text
AutomationFlow/
├── n8n/
│   └── workflows/
│       └── automationflow-lead-processing.json
├── make/
│   └── scenarios/
│       └── automationflow-make-lead-processing.json
├── python/
│   ├── app.py
│   ├── processor.py
│   └── requirements.txt
└── docs/
    ├── architecture/
    │   └── architecture.md
    └── setup/
        └── setup.md
```

---

## 💼 Design Principles

1. **Separation of concerns** — orchestration and business logic are separated.
2. **Reusable components** — the Python processor can be consumed through HTTP.
3. **Platform comparison** — n8n and Make implement the same business objective using their native strengths.
4. **Explicit routing** — lead classification and automation decisions are visible in the workflow.
5. **Safe-by-default actions** — the portfolio implementation prepares automation results without requiring real external side effects.
6. **Portfolio readiness** — exported workflows and documentation make the system reviewable and reproducible.
