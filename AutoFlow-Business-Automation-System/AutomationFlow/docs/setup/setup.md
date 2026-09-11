# AutomationFlow Setup Guide

## 1. Prerequisites

- Windows, macOS, or Linux
- Python 3
- Docker Desktop for the local n8n deployment
- n8n Community Edition or an appropriate n8n deployment
- Make account for the Make implementation

## 2. Python Service

From the `AutomationFlow/python` directory:

```bash
python -m venv .venv
```

Activate the environment.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The API documentation is available at:

```text
http://localhost:8000/docs
```

## 3. Local n8n with Docker

Create persistent n8n storage:

```bash
docker volume create n8n_data
```

Start n8n:

```bash
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

Open:

```text
http://localhost:5678
```

Create the local n8n owner account during first-time setup.

## 4. Import the n8n Workflow

Use the n8n editor's workflow import function and select:

```text
n8n/workflows/automationflow-lead-processing.json
```

The workflow expects the Python processor to be available at:

```text
http://host.docker.internal:8000/process-lead
```

This address is appropriate for the demonstrated Docker-on-Windows local setup. For other deployment architectures, replace it with the reachable internal API address.

## 5. Make Setup

Open Make and create/open the scenario:

```text
AutomationFlow — Make Lead Processing
```

The scenario uses a Custom Webhook. The webhook data structure should contain:

```text
name
email
company
message
source
```

The current demonstration keeps the scenario inactive until the owner intentionally enables it.

## 6. Example Request

A client or website can submit JSON similar to:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "company": "Acme Corporation",
  "message": "I am interested in your automation services.",
  "source": "Website Contact Form"
}
```

For local n8n testing, the test webhook URL is displayed directly by the n8n Webhook node while the test listener is active.

For Make, use the Custom Webhook URL shown by the Make scenario.

## 7. Production Configuration

Before using this architecture with real client data:

1. Deploy n8n/Make according to the client's environment.
2. Replace local host URLs with production service URLs.
3. Add webhook authentication/signatures.
4. Store credentials in the platform credential manager.
5. Enable HTTPS for externally reachable endpoints.
6. Configure logging, monitoring, retries, and alerting.
7. Replace simulated response actions with the client's approved CRM, email, messaging, or ticketing integrations.

## 8. Secrets

Never place the following in Git:

```text
.env
API keys
passwords
SMTP credentials
OAuth tokens
private webhook secrets
client credentials
```

Use environment variables and platform-managed credentials instead.

## 9. Troubleshooting

### n8n cannot reach FastAPI

Confirm FastAPI is running on port `8000` and that the n8n HTTP Request node uses:

```text
http://host.docker.internal:8000
```

### FastAPI import error

Run Uvicorn from the `python` directory:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Make webhook has no fields

Send a sample JSON request to the Make Custom Webhook URL so Make can learn the data structure.

## 10. Client Handover

A production handover should include:

- Workflow export/blueprint
- Setup instructions
- Required credentials/integrations
- Environment variables
- API endpoints
- Business rules
- Error-handling behavior
- Maintenance notes
- Ownership and access information
