# BusinessCore

BusinessCore is a local FastAPI service for processing customer orders through a validated business workflow. It persists workflow state in SQLite, creates operational tasks and notifications, records audit events, and generates analytics reports.

## Requirements

- Windows
- Python 3.12.x

BusinessCore uses its own project-local `.venv`. Do not install these dependencies into a parent repository or global Python environment.

## Setup

From this directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Python 3.12 is used because the pinned FastAPI, Pydantic, SQLAlchemy, pandas, and reporting stack has compatible Windows wheels there. Python 3.14 is not used for this environment because the pinned Pydantic release requires a source build on Python 3.14, and pandas `2.2.3` does not provide a Python 3.14 wheel. The project does not depend on `sqlite-utils`; SQLite access is provided by Python's standard library and SQLAlchemy.

## Verify

```powershell
pytest
python -m src.main
```

The API starts at `http://127.0.0.1:8000`. The health endpoint is available at `/health`.

## Configuration

Copy `.env.example` to `.env` when custom settings are needed. The default database is `data/businesscore.db` and generated reports are written to `data/output/`. Database, cache, virtual-environment, and generated report files are ignored by Git.