# Make Implementation

AutomationFlow includes a Make.com implementation to demonstrate the same business automation concept using Make-native modules and routing.

## Scenario

**Scenario name:** `AutomationFlow — Make Lead Processing`

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

## Modules

### Custom Webhook

Receives:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "company": "Acme Corporation",
  "message": "I am interested in your automation services.",
  "source": "Website Contact Form"
}
```

The webhook data structure is learned from an incoming sample request.

### Classify Lead

The Make scenario uses an If-else router to branch based on the incoming lead data.

The routes cover:

- **Invalid Lead:** email is empty
- **Sales Lead:** sales/automation intent keywords are present
- **Support Lead:** support/problem keywords are present
- **Billing Lead:** invoice/payment/billing keywords are present
- **General Lead:** fallback route

### Webhook Response

Each route returns a structured JSON response containing the lead fields and the resulting business classification/action.

## Why This Implementation Is Separate

The n8n version uses the reusable Python/FastAPI processor for lead scoring and classification. The Make version demonstrates that the same business workflow can also be implemented with Make-native branching without requiring a paid AI provider.

This gives the portfolio project two useful demonstrations:

1. **n8n + Python API orchestration**
2. **Make-native no-code orchestration**

## Scenario Storage

The live scenario remains in the connected Make workspace. A scenario blueprint/export can be stored under:

```text
make/scenarios/
```

Do not commit API keys, webhook secrets, or private connection credentials.

## Production Adaptation

For a real client deployment, the response modules can be replaced or extended with modules for:

- CRM record creation
- Slack/Teams notifications
- Email notifications
- Google Sheets logging
- Lead enrichment
- Sales-assignment workflows
- Database persistence
- Error handling and retry paths

Production scenarios should also use appropriate authentication, credential management, logging, and failure handling.
