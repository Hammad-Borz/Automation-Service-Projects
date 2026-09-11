# ⚙️ AutomationFlow — Setup Guide

> Complete setup instructions for the **n8n + Make + Python** AutomationFlow portfolio project.

---

## 🎯 Setup Overview

AutomationFlow contains three practical layers:

1. **n8n** — primary workflow orchestration.
2. **Make** — secondary native automation implementation.
3. **Python/FastAPI** — supporting lead-processing service used by the n8n implementation.

The project is designed for local development and portfolio demonstration. External side effects such as real sales notifications are intentionally represented as prepared automation results.

---

## 📋 Prerequisites

### Required

- Python 3.10+
- Git
- VS Code or another code editor
- Docker Desktop with Docker Engine running
- n8n Community Edition running locally
- A Make account for the Make implementation

### Recommended

- PowerShell on Windows
- Basic REST API and JSON knowledge
- Access to a browser for n8n and Make configuration

---

## 📁 Project Structure

```text
AutomationFlow/
├── README.md
├── docs/
│   ├── README.md
│   ├── architecture/
│   │   └── architecture.md
│   └── setup/
│       └── setup.md
├── make/
│   ├── README.md
│   └── scenarios/
│       └── automationflow-make-lead-processing.json
├── n8n/
│   ├── README.md
│   └── workflows/
│       └── automationflow-lead-processing.json
└── python/
    ├── README.md
    ├── app.py
    ├── processor.py
    └── requirements.txt
```

---

# 🐍 1. Python Service Setup

Open a terminal in the Python directory:

```powershell
cd AutomationFlow\python
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the FastAPI service:

```powershell
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The service listens on:

```text
http://localhost:8000
```

Swagger documentation is available at:

```text
http://localhost:8000/docs
```

---

# 🐳 2. Local n8n Setup with Docker

Create the persistent n8n volume:

```powershell
docker volume create n8n_data
```

Start n8n:

```powershell
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

Open:

```text
http://localhost:5678
```

Complete the local n8n owner/onboarding setup when prompted.

### Container → Host Python networking

The n8n container reaches the Windows-hosted Python service through:

```text
http://host.docker.internal:8000/process-lead
```

This is why the n8n HTTP Request node uses `host.docker.internal` instead of `localhost`.

---

# 🔵 3. Import the n8n Workflow

The exported workflow is located at:

```text
n8n/workflows/automationflow-lead-processing.json
```

In n8n:

1. Open the workflow editor.
2. Use the workflow menu.
3. Choose the import option.
4. Select `automationflow-lead-processing.json`.
5. Review the nodes and connections.
6. Save the workflow.

### n8n workflow

```text
Webhook
   ↓
Edit Fields
   ↓
IF — Email Validation
   ├── false → Respond to Webhook
   └── true → HTTP Request
                    ↓
                 IF1 — Priority
                    ↓
                 Edit Fields1
                    ↓
                 Respond to Webhook
```

The webhook path is:

```text
POST /webhook-test/automationflow/leads
```

when using n8n's test webhook mode.

---

# 🟢 4. Make Setup

The Make implementation is stored as a portable blueprint:

```text
make/scenarios/automationflow-make-lead-processing.json
```

The scenario is named:

```text
AutomationFlow — Make Lead Processing
```

The implementation uses:

```text
Custom Webhook
      ↓
Flow Control — Lead Classification
      ├── Invalid Lead
      ├── Sales Lead
      ├── Support Lead
      ├── Billing Lead
      └── General Lead
```

### Important architecture note

The Make scenario **does not call the local Python service**. Make runs in the cloud and therefore cannot directly access the local Docker/Windows `host.docker.internal` address.

Instead, the Make version implements the classification/routing logic natively inside Make.

---

# 📦 5. Lead Payload

The workflow expects JSON containing:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "company": "Example Corp",
  "message": "We are interested in automation services and would like pricing.",
  "source": "website"
}
```

### Core fields

| Field | Purpose |
|---|---|
| `name` | Lead/contact name |
| `email` | Required contact email |
| `company` | Business/company name |
| `message` | Lead request or inquiry |
| `source` | Lead acquisition source |

---

# 🔄 6. Running the Complete Local Stack

Use two terminals.

### Terminal 1 — Python

```powershell
cd AutomationFlow\python
.\.venv\Scripts\Activate.ps1
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Terminal 2 — n8n

If the container is not running:

```powershell
docker start n8n
```

Then open:

```text
http://localhost:5678
```

Open the imported AutomationFlow workflow and use its test webhook when working locally.

---

# 🛡️ 7. Configuration & Security

AutomationFlow does not require secrets for its local Python service.

For production/client deployments:

- Keep credentials out of workflow exports and source control.
- Use environment variables or platform-managed credentials.
- Do not commit API keys, passwords, SMTP credentials, or webhook secrets.
- Use HTTPS for externally exposed webhooks.
- Apply authentication to production webhook endpoints where appropriate.
- Restrict real-world side effects behind explicit authorization and validation.

---

# 🧹 8. Repository Hygiene

Do not commit generated local Python files such as:

```text
__pycache__/
*.pyc
.venv/
```

Do not commit private credentials or local runtime configuration.

---

# 🧪 9. Operational Verification

The project was built with separate validation of its components:

- Python FastAPI service exposes health and processing endpoints.
- n8n workflow uses webhook input, validation, HTTP processing, priority routing, and structured responses.
- Make workflow uses native webhook and classification branches.
- Exported n8n and Make workflow files provide reproducible portfolio artifacts.

For normal portfolio use, avoid enabling real external side effects unless the required credentials and business authorization are intentionally configured.

---

# 🚀 10. Production Considerations

For a real client deployment, consider:

- Authentication and authorization
- HTTPS and secure webhook endpoints
- Persistent logging and monitoring
- Retry and timeout policies
- Rate limiting
- Secret management
- Structured observability
- Error notification and dead-letter handling
- Client-owned credentials and infrastructure
- Backup and versioning of automation workflows

---

## 📚 Related Documentation

- [`../architecture/architecture.md`](../architecture/architecture.md) — system architecture and data flow
- [`../../n8n/README.md`](../../n8n/README.md) — n8n implementation
- [`../../make/README.md`](../../make/README.md) — Make implementation
- [`../../python/README.md`](../../python/README.md) — Python supporting service
