# AutomationFlow Architecture

## 1. Purpose

AutomationFlow is a webhook-driven business automation pattern for processing incoming leads and routing them according to business intent and priority.

The project demonstrates the architecture in two automation platforms:

- **n8n** for visual orchestration with a reusable Python/FastAPI processing service
- **Make** for Make-native webhook, branching, and response automation

## 2. High-Level Architecture

```text
                External Lead Source
             (website / form / API)
                       │
                       ▼
                ┌──────────────┐
                │    Webhook   │
                └──────┬───────┘
                       │
                       ▼
             Validate + Normalize
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        ┌───────────┐     ┌───────────┐
        │    n8n    │     │    Make   │
        │ workflow  │     │ scenario  │
        └─────┬─────┘     └─────┬─────┘
              │                  │
              ▼                  ▼
       Python/FastAPI       Make-native
       lead processor        classification
              │                  │
              └────────┬─────────┘
                       ▼
               Structured Result
                       │
                       ▼
                Downstream Action
```

## 3. n8n Data Flow

```text
Webhook
  ↓
Edit Fields
  ↓
Email Validation
  ├── invalid → error response
  └── valid
       ↓
Python /process-lead
       ↓
Priority Check
       ↓
Sales Action Payload
       ↓
Final Webhook Response
```

### Responsibilities

| Component | Responsibility |
|---|---|
| Webhook | Accepts external lead submissions |
| Edit Fields | Converts nested webhook data into a predictable lead object |
| IF | Validates required email data |
| FastAPI | Provides reusable lead-processing logic |
| Python processor | Determines lead type, score, and priority |
| IF1 | Routes high-priority leads |
| Edit Fields1 | Creates a downstream action payload |
| Respond to Webhook | Returns structured JSON to the caller |

## 4. Python Processing Logic

The processor is deterministic and local. It does not require an external AI provider.

The classification considers three primary intent groups:

- Sales
- Support
- Billing

If no matching business intent is found, the lead is classified as general.

The score is then adjusted according to classification, source, and urgency indicators. The final score is capped at 100 and converted into a priority level.

## 5. Make Data Flow

```text
Custom Webhook
      ↓
If-else classification
      ├── Invalid
      ├── Sales
      ├── Support
      ├── Billing
      └── General
             ↓
       Webhook Response
```

The Make implementation intentionally uses Make-native routing so the project demonstrates a no-code alternative without requiring an external AI/API subscription.

## 6. Integration Boundary

The Python service is an internal HTTP API:

```text
n8n container
      │
      │ HTTP POST
      ▼
http://host.docker.internal:8000/process-lead
      │
      ▼
FastAPI application
```

`host.docker.internal` is used because n8n is running inside Docker on the Windows host while FastAPI runs on the host machine.

## 7. Production Extension Points

The current architecture is deliberately small but can be extended without replacing the core workflow.

Potential production integrations include:

- CRM systems
- Email providers
- Slack or Microsoft Teams
- Google Sheets
- Databases
- Lead enrichment APIs
- Customer support systems
- Authentication and signed webhooks
- Retry/error queues
- Observability and audit logging

## 8. Security Boundary

Production deployments should treat the webhook as an external trust boundary. Recommended controls include:

- Authentication or signed webhook requests
- HTTPS
- Secret management through platform credentials
- Input validation
- Rate limiting where appropriate
- Restricted internal API access
- Structured logs without sensitive payload leakage
- No secrets committed to Git

## 9. Design Principles

- **Modular:** orchestration and business logic are separated.
- **Deterministic:** the demo produces reproducible results without paid AI services.
- **Portable:** the business workflow is represented in both n8n and Make.
- **Extensible:** downstream business systems can replace the response stage.
- **Portfolio-oriented:** the repository preserves workflow exports and implementation documentation alongside supporting code.
