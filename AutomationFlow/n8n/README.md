# 🟣 AutomationFlow — n8n Implementation

This directory contains the **primary n8n implementation** of AutomationFlow.

## Workflow

```text
Webhook
   ↓
Edit Fields
   ↓
IF — Email Validation
   ├── Invalid → Respond to Webhook
   └── Valid
         ↓
HTTP Request → Python Lead Processor
         ↓
IF — High Priority
         ↓
Edit Fields
         ↓
Respond to Webhook
```

## Workflow Responsibilities

1. Receive a lead through a POST webhook.
2. Normalize the incoming lead fields.
3. Validate that an email address is present.
4. Send valid leads to the Python processing service.
5. Inspect the returned priority.
6. Prepare the automation action for high-priority leads.
7. Return a structured JSON response to the caller.

## Export

The portable n8n workflow is stored at:

```text
workflows/automationflow-lead-processing.json
```

The export can be imported into another n8n environment and reconfigured for its target infrastructure.

## Local Integration

The workflow's HTTP Request node targets the local Python service through Docker's host gateway:

```text
http://host.docker.internal:8000/process-lead
```

This is a local development configuration and should be changed for another deployment environment.

## Portfolio Evidence

The n8n workflow demonstrates webhook handling, conditional routing, HTTP integration, data mapping, and structured responses without relying on an external email credential for the portfolio implementation.
