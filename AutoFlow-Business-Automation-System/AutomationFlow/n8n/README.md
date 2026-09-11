# n8n Implementation

AutomationFlow's primary workflow-orchestration implementation is built in **n8n Community Edition**.

## Workflow

```text
Webhook
   ↓
Edit Fields
   ↓
IF — email is not empty?
   ├── FALSE → Respond to Webhook1
   │
   └── TRUE → HTTP Request
                  ↓
              IF1 — priority = high?
                  ↓
              Edit Fields1
                  ↓
              Respond to Webhook
```

## Nodes

### 1. Webhook

- Method: `POST`
- Path: `automationflow/leads`
- Authentication: `None` for local demonstration
- Response mode: `Using 'Respond to Webhook' Node`

Expected payload:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "company": "Acme Corporation",
  "message": "I am interested in your automation services.",
  "source": "Website Contact Form"
}
```

### 2. Edit Fields

Maps the nested webhook body into a flat lead object:

- `name` → `{{$json.body.name}}`
- `email` → `{{$json.body.email}}`
- `company` → `{{$json.body.company}}`
- `message` → `{{$json.body.message}}`
- `source` → `{{$json.body.source}}`

### 3. IF — Email Validation

Checks:

```text
Value 1: {{$json.email}}
Operator: String → is not empty
```

The false branch returns an invalid-lead response.

### 4. HTTP Request — Python Processor

- Method: `POST`
- URL: `http://host.docker.internal:8000/process-lead`
- Body type: JSON

```json
{
  "name": "{{$json.name}}",
  "email": "{{$json.email}}",
  "company": "{{$json.company}}",
  "message": "{{$json.message}}",
  "source": "{{$json.source}}"
}
```

`host.docker.internal` allows the Dockerized n8n container to reach the FastAPI service running on the Windows host.

### 5. IF1 — High Priority Routing

Checks:

```text
Value 1: {{$json.analysis.priority}}
Operator: String → is equal to
Value 2: high
```

### 6. Edit Fields1

Builds the downstream sales action payload:

```json
{
  "action": "notify_sales",
  "priority": "{{$json.analysis.priority}}",
  "lead_type": "{{$json.analysis.lead_type}}",
  "score": "{{$json.analysis.score}}",
  "email": "{{$json.lead.email}}"
}
```

### 7. Respond to Webhook

Returns a structured success response containing the original lead and analysis/action metadata.

## Python Service

Start the service from the `python/` directory:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The service must be reachable by the n8n container at:

```text
http://host.docker.internal:8000
```

## Local n8n Runtime

The demonstrated local runtime uses Docker:

```bash
docker volume create n8n_data
docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n n8nio/n8n
```

Open n8n at `http://localhost:5678`.

## Workflow Export

The n8n workflow should be exported from the n8n editor as JSON and stored in:

```text
n8n/workflows/automationflow-lead-processing.json
```

Do not commit credentials or environment-specific secrets in the workflow export.
