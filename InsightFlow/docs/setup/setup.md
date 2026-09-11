# InsightFlow Setup

## Prerequisites

Python 3.11+ and PowerShell or an equivalent terminal.

## Install

From the `InsightFlow` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run Tests

```powershell
pytest
```

Tests use temporary directories and SQLite databases, not the project runtime database.

## Start the API

```powershell
python -m src.main
```

Swagger: `http://127.0.0.1:8000/docs`.

## Run Analytics

Use Swagger or PowerShell:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/analytics/run -Method Post -ContentType 'application/json' -Body '{}'
```

The default dataset is `data/input/sample_sales_data.csv`. Generated reports are written to `data/output/`, and historical data is stored in `data/insightflow.sqlite3`.

## Process Another Dataset

Put a CSV beneath `data/`, then provide a project-relative path:

```powershell
$body = '{"input_path":"data/input/my_sales_data.csv"}'
Invoke-RestMethod -Uri http://127.0.0.1:8000/analytics/run -Method Post -ContentType 'application/json' -Body $body
```

Paths outside `data/` are rejected. Required columns are `order_id`, `customer_id`, `customer_name`, `customer_email`, `product`, `category`, `quantity`, `unit_price`, `total_amount`, `order_date`, `status`, `region`, and `sales_channel`. Statuses must be completed, pending, cancelled, or refunded; channels must be online, retail, or marketplace.

## Configuration

Optional environment variables:

- `INSIGHTFLOW_ANOMALY_Z`: anomaly z-score threshold, default `2.0`
- `INSIGHTFLOW_HIGH_VALUE`: high-value threshold, default `1000`
- `INSIGHTFLOW_LOG_LEVEL`: Python logging level, default `INFO`

## Troubleshooting

- Run commands from `InsightFlow` so `python -m src.main` resolves imports.
- If port 8000 is occupied, use `python -m uvicorn src.main:app --port 8001`.
- Close the Excel workbook before regenerating reports on Windows.
