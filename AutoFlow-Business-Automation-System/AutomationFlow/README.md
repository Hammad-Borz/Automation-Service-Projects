# AutomationFlow — n8n & Make Business Automation Workflows

> **Service:** n8n & Make Workflow Automation  
> **Project type:** Business lead-processing automation  
> **Status:** Portfolio-ready implementation

AutomationFlow demonstrates how a business lead can enter through a webhook, be validated and classified, and receive a structured automation response using both **n8n** and **Make**. A lightweight **Python/FastAPI supporting service** is also included for reusable lead analysis in the n8n implementation.

## 🎯 Business Problem

Businesses often receive leads from website forms, landing pages, campaigns, and other sources. Processing those leads manually creates repetitive work and delays follow-up.

AutomationFlow demonstrates an automated pipeline that can:

- Receive lead submissions through a webhook
- Extract and normalize incoming fields
- Validate required information
- Classify leads by business intent
- Calculate a lead priority/score
- Route high-priority sales leads
- Return a structured response for downstream systems
- Implement the workflow in both n8n and Make

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │   Website / Client   │
                    │    Lead Submission   │
                    └──────────┬───────────┘
                               │ POST
                               ▼
                    ┌──────────────────────┐
                    │       Webhook        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Validate / Normalize │
                    │    Lead Payload      │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          ┌───────────────┐        ┌────────────────┐
          │      n8n      │        │      Make      │
          │ Orchestration │        │  Orchestration │
          └───────┬───────┘        └───────┬────────┘
                  │                         │
                  ▼                         ▼
          ┌───────────────┐        ┌────────────────┐
          │ Python/FastAPI│        │ Native routing │
          │ Lead Analysis │        │ & classification│
          └───────┬───────┘        └───────┬────────┘
                  │                         │
                  └────────────┬────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Structured Automation│
                    │       Response       │
                    └──────────────────────┘
```

See [`docs/architecture/architecture.md`](docs/architecture/architecture.md) for the detailed design.

## 🔄 n8n Workflow

```text
Webhook
   ↓
Edit Fields
   ↓
IF — email validation
   ├── FALSE → Respond to Webhook
   │
   └── TRUE → HTTP Request → Python /process-lead
                         ↓
                    IF1 — priority = high
                         ↓
                    Edit Fields1
                         ↓
                    Respond to Webhook
```

The n8n implementation uses the local FastAPI service to perform reusable lead classification and scoring.

### n8n processing

- `name`, `email`, `company`, `message`, and `source` are extracted from the webhook body.
- An email validation branch rejects missing email addresses.
- Valid leads are sent to the Python `/process-lead` endpoint.
- The Python service returns `lead_type`, `priority`, `score`, and `reason`.
- High-priority results are routed to the sales-action payload.
- The workflow returns a structured JSON response.

The exported workflow file is stored under `n8n/workflows/` in the local project copy.

## 🔁 Make Workflow

The Make implementation is a native Make scenario built around a **Custom Webhook**, **If-else routing**, and **Webhook Response** modules.

```text
Custom Webhook
      ↓
Classify Lead
      ├── Invalid Lead → Webhook Response
      ├── Sales Lead   → Webhook Response
      ├── Support Lead → Webhook Response
      ├── Billing Lead → Webhook Response
      └── General Lead → Webhook Response
```

The Make scenario demonstrates the same business objective with Make-native routing rather than depending on a paid AI service.

## 🐍 Python Supporting Service

The supporting service lives in `python/` and exposes:

| Endpoint | Purpose |
|---|---|
| `GET /health` | Service health check |
| `POST /process-lead` | Classifies and scores a lead |
| `POST /notify-sales` | Prepares a high-priority sales notification action |

The service uses FastAPI and deterministic keyword-based business rules, making the demo reproducible and avoiding external AI/API costs.

## 📁 Project Structure

```text
AutomationFlow/
├── n8n/
│   ├── workflows/
│   │   └── automationflow-lead-processing.json
│   └── README.md
├── make/
│   ├── scenarios/
│   └── README.md
├── python/
│   ├── app.py
│   ├── processor.py
│   └── requirements.txt
├── docs/
│   ├── architecture/
│   │   └── architecture.md
│   └── setup/
│       └── setup.md
└── README.md
```

## ⚙️ Setup

See [`docs/setup/setup.md`](docs/setup/setup.md) for the complete setup guide.

At a high level:

1. Install Docker Desktop and run the self-hosted n8n instance.
2. Start the Python FastAPI supporting service.
3. Import the exported n8n workflow.
4. Configure the Python service URL for the n8n HTTP Request node.
5. Configure the Make Custom Webhook and routing modules.
6. Keep credentials and environment-specific values outside Git.

## 🔐 Security Notes

- Do not commit API keys, passwords, SMTP credentials, webhook secrets, or `.env` files.
- The demo webhook is unauthenticated for local development; production deployments should add appropriate authentication and access controls.
- The default notification behavior is simulated/prepared rather than sending real business email.
- Client credentials should be stored in the automation platform's credential manager or another approved secret store.

## 💼 Client Use Cases

AutomationFlow can be adapted for:

- Website lead routing
- Sales qualification
- Contact-form automation
- CRM intake pipelines
- Support-ticket triage
- Billing request routing
- Notification workflows
- Lead enrichment pipelines
- Multi-platform workflow migration between n8n and Make

## 🛠️ Technology Stack

- **n8n** — workflow orchestration
- **Make** — no-code workflow orchestration
- **Python 3** — supporting business logic
- **FastAPI** — lightweight internal API
- **Docker** — local n8n runtime
- **JSON** — workflow/data interchange

## 📌 Portfolio Value

This project demonstrates practical automation engineering rather than a single isolated script. It combines webhook ingestion, branching logic, API integration, reusable Python business logic, structured responses, and equivalent workflow implementation across two major automation platforms.
