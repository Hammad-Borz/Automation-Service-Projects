# EventPulse Setup

## Prerequisites

- Python 3.11 or newer
- PowerShell, Command Prompt, or another terminal

## Virtual Environment and Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuration

Defaults require no `.env` file. Optional environment variables are:

- `EVENTPULSE_DATABASE_PATH`: defaults to `data/eventpulse.sqlite3`
- `EVENTPULSE_ENVIRONMENT`: defaults to `development`
- `EVENTPULSE_LOGGING_LEVEL`: defaults to `INFO`

The database directory and schema are initialized on application startup.

## Start FastAPI

```powershell
uvicorn src.main:app --reload
```

Swagger is available at `http://127.0.0.1:8000/docs`; ReDoc is at `/redoc`.

## Send a Test Webhook

```powershell
$body = '{"event_id":"evt_demo","event_type":"lead.created","timestamp":"2026-09-11T10:30:00Z","source":"website","data":{"email":"demo@example.com","message":"Interested in pricing"}}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/webhooks/events -Method Post -ContentType 'application/json' -Body $body
```

Send the same request again to see the duplicate response. Then inspect `/events/evt_demo` and `/analytics/overview`.

## Run Tests

```powershell
pytest -q
```

## Troubleshooting

- If imports fail, run commands from the `EventPulse` directory or activate the virtual environment.
- If port 8000 is busy, use `uvicorn src.main:app --port 8001`.
- The test configuration uses an ignored project-local `pytest_temp` directory for Windows environments where the global temp directory is restricted.
- Runtime SQLite files are ignored by Git.

## Production Notes

Add webhook signature verification, HTTPS, secret management, authentication for operational endpoints, structured log shipping, monitoring, retry policy, and a queue when processing needs to become asynchronous.
