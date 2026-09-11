# DataFlow Pro Setup

## Prerequisites

- Python 3.11 or newer
- PowerShell on Windows, or an equivalent shell

## Install

From the `DataFlow-Pro` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run Tests

```powershell
pytest
```

The suite uses temporary databases and project directories. Runtime SQLite and generated output files are ignored by Git.

## Run the API

```powershell
python -m src.main
```

Open `http://127.0.0.1:8000/docs` for Swagger UI. The health endpoint is `GET /health`.

## Run the Pipeline Directly

```powershell
python -c "from src.config import Settings; from src.core.pipeline import Pipeline; print(Pipeline(Settings.for_project()).run())"
```

Outputs are generated under `data/output/`, and the local database is `data/dataflow.sqlite3`.

## Process Another CSV Safely

Place the file under the project `data` directory, then call the API with a project-relative path:

```powershell
$body = '{"input_path":"data/input/my_business_data.csv"}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/pipeline/run -Method Post -ContentType 'application/json' -Body $body
```

The API rejects paths outside `data/`. A CSV must include `order_id`, `customer_name`, `product`, `category`, `quantity`, `unit_price`, `order_date`, `status`, and `sales_region`. Optional fields include `record_id`, `customer_email`, `company`, `total_amount`, and `currency`.

## Troubleshooting

- Run commands from the `DataFlow-Pro` directory so `python -m src.main` resolves imports.
- If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` for the current shell.
- If port 8000 is occupied, start Uvicorn directly with `python -m uvicorn src.main:app --port 8001`.
- If a generated report is open in Excel, close it before running another pipeline on Windows.

## Configuration

Optional environment variables:

- `DATAFLOW_DATABASE_PATH`
- `DATAFLOW_HIGH_VALUE_THRESHOLD`
- `DATAFLOW_ENVIRONMENT`
- `DATAFLOW_LOGGING_LEVEL`

The defaults are suitable for local demonstration and require no `.env` file.
