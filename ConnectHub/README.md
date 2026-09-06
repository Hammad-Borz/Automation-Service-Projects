# ConnectHub — Multi-API Integration & Automation System

ConnectHub is a portfolio-ready Python project that moves customer-style records between REST APIs reliably. It fetches source data, validates each record, converts it into a destination schema, and posts valid records individually so one failure does not halt the whole batch.

## Features

- Reusable `APIClient` with GET/POST support, configurable timeouts, and clear HTTP, network, and invalid-JSON errors.
- Per-record validation with actionable error messages for missing or malformed data.
- Explicit schema transformation from source records to destination payloads.
- Batch orchestration and a concise, machine-friendly result summary.
- File logging to `logs/connecthub.log` without duplicate handlers.
- Automated pytest coverage using mocked HTTP behavior.

## Architecture

```text
Source REST API -> APIClient.get -> DataValidator -> DataTransformer -> APIClient.post -> Destination REST API
                                      |                                      |
                                 invalid records                         failures counted
```

`IntegrationService` owns the workflow and returns:

```python
{
    "total_fetched": 3,
    "valid_records": 2,
    "invalid_records": 1,
    "successfully_sent": 1,
    "failed_to_send": 1,
}
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env`, then supply the two endpoint URLs. Do not commit `.env`; it is ignored by Git.

```env
SOURCE_API_URL=https://api.example.com/users
DESTINATION_API_URL=https://api.example.com/contacts
```

No API keys or secrets are stored in this repository. If an API needs authentication, inject its credentials through your deployment environment and extend `APIClient` with the appropriate headers.

## Usage

From the project root:

```bash
python src/main.py
```

The source response must be a JSON list of dictionaries containing `id`, `name`, and `email`. Each valid record is sent as:

```json
{
  "external_id": 123,
  "full_name": "Ada Lovelace",
  "contact_email": "ada@example.com"
}
```

The console displays the batch summary; operational events are recorded in `logs/connecthub.log`.

## Testing

```bash
pytest
```

The suite mocks HTTP transport and covers successful GET/POST requests, HTTP/network failures, invalid source data, schema transformation, complete workflows, and partial send failures.

## Example Workflow

Given three source records—two complete and one missing an email—ConnectHub validates all three, skips and logs the invalid record, transforms the two valid records, and posts each independently. If one post fails, the other remains successful and the summary reports both outcomes.

## Limitations and Next Steps

This focused example assumes JSON APIs and unauthenticated endpoints. Production deployments may add authentication headers, retry/backoff rules, rate limiting, pagination, idempotency keys, and a persistent dead-letter queue for failed records.
