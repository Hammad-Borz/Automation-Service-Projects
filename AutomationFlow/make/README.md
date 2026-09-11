# 🔵 AutomationFlow — Make Implementation

This directory contains the **native Make implementation** of AutomationFlow.

## Scenario

```text
Custom Webhook
      ↓
Classify Lead
      ├── Invalid Lead
      ├── Sales Lead
      ├── Support Lead
      ├── Billing Lead
      └── General Lead
      ↓
Webhook Response
```

## Routing Logic

- **Invalid:** email is empty.
- **Sales:** message contains sales-oriented terms such as `interested`, `automation`, `pricing`, or `quote`.
- **Support:** message contains terms such as `problem`, `issue`, `error`, or `support`.
- **Billing:** message contains terms such as `invoice`, `payment`, `billing`, or `refund`.
- **General:** catch-all route for other valid leads.

Each route returns a structured JSON response containing the lead classification and prepared automation action.

## Export

The scenario blueprint is stored at:

```text
scenarios/automationflow-make-lead-processing.json
```

## Important Implementation Detail

This Make version is a **native Make routing implementation**. It does not call the local Python service because a cloud-hosted Make scenario cannot directly reach a local `host.docker.internal` endpoint.

The n8n implementation uses the Python service for lead analysis, while the Make implementation demonstrates how the same business requirement can be implemented directly with Make's own routing and transformation capabilities.

## Scenario Status

The portfolio scenario is kept **inactive** by default. This prevents unintended production-style execution while preserving the complete workflow and blueprint for demonstration and deployment.
