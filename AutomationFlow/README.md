# ⚙️ AutomationFlow — n8n & Make Business Automation Workflows

> **Primary service demonstrated: n8n & Make Workflow Automation**

AutomationFlow is a practical business-automation project that demonstrates how the same lead-processing workflow can be designed and implemented with **n8n and Make**, supported by a lightweight Python service for deterministic lead analysis.

## 🎯 What This Project Demonstrates

- Webhook-based business workflow orchestration
- Lead intake and field normalization
- Input validation and routing
- Lead classification and priority scoring
- n8n workflow automation
- Native Make scenario routing
- HTTP integration with a Python supporting service
- Structured webhook responses
- Exportable workflow/scenario blueprints
- Architecture and setup documentation

## 🔄 End-to-End Architecture

```text
Lead Source
    ↓
Webhook
    ↓
Normalize Lead Fields
    ↓
Validate Email
    ├── Invalid → Error Response
    └── Valid
          ↓
   Lead Processing
      ├── n8n → Python HTTP Service
      └── Make → Native Make Routing
          ↓
   Classification / Priority
          ↓
   Automation Decision
          ↓
   Structured Response
```

## 🧩 Project Structure

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

## 🟣 n8n Implementation

The n8n implementation is the primary workflow demonstration.

```text
Webhook
  ↓
Edit Fields
  ↓
IF — Validate Email
  ├── Invalid → Response
  └── Valid
       ↓
HTTP Request → Python Lead Processor
       ↓
IF — High Priority
       ↓
Edit Fields
       ↓
Response
```

The exported workflow is available under `n8n/workflows/`.

## 🔵 Make Implementation

The Make implementation provides a native alternative to the n8n workflow.

```text
Custom Webhook
      ↓
Classify Lead
      ├── Invalid
      ├── Sales
      ├── Support
      ├── Billing
      └── General
      ↓
Webhook Response
```

The Make version uses native Make routing rather than calling the local Python service. Its exported blueprint is available under `make/scenarios/`.

## 🐍 Python Supporting Service

The Python service provides deterministic lead classification and scoring for the n8n implementation.

### Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Service health check |
| `POST /process-lead` | Classify and score a lead |
| `POST /notify-sales` | Prepare a sales notification result |

### Lead Analysis

The processor evaluates message content and source information to determine:

- Lead type: `sales`, `support`, `billing`, or `general`
- Priority: `high`, `medium`, or `low`
- Score: `0–100`
- Human-readable classification reason

## 🛡️ Safety & Configuration

The workflow is designed to be safe for portfolio demonstration:

- No real customer credentials are stored in the repository.
- External actions are represented through structured automation results.
- The Make scenario is documented as a separate native implementation.
- Local Python service configuration is kept outside the workflow export.

## 📚 Documentation

- [Architecture](docs/architecture/architecture.md)
- [Setup Guide](docs/setup/setup.md)
- [n8n Documentation](n8n/README.md)
- [Make Documentation](make/README.md)
- [Python Service](python/README.md)

## 💼 Portfolio Value

AutomationFlow demonstrates a practical freelancer-ready capability: **turning a business requirement into a documented, webhook-driven automation workflow and implementing it across two leading automation platforms.**

It also shows how a Python service can be integrated into an automation platform when deterministic business logic is more appropriate than embedding all logic directly in the workflow.
