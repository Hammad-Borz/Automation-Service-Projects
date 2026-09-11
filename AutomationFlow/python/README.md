# 🐍 AutomationFlow — Python Supporting Service

This directory contains the lightweight FastAPI service used as the deterministic processing layer for the n8n implementation.

## Responsibilities

- Accept structured lead data.
- Classify leads using deterministic keyword-based business rules.
- Calculate a bounded lead score.
- Assign `high`, `medium`, or `low` priority.
- Return structured JSON suitable for downstream workflow nodes.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/process-lead` | Analyze a lead |
| `POST` | `/notify-sales` | Prepare a sales notification result |

## Files

| File | Responsibility |
|---|---|
| `app.py` | FastAPI application and HTTP endpoints |
| `processor.py` | Lead classification and scoring logic |
| `requirements.txt` | Python dependencies |

## Local Run

From this directory:

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

The n8n Docker container reaches the local service through:

```text
http://host.docker.internal:8000
```

## Design Note

The processing logic is intentionally deterministic for this portfolio project. This keeps the workflow reproducible and makes the automation behavior easy to inspect, test, and explain.
