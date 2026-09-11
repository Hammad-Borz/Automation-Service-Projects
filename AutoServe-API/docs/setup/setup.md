# Setup Guide

## Python requirement

This project requires Python 3.11 or newer.

## Create a virtual environment

```powershell
cd AutoServe-API
python -m venv .venv
.venv\Scripts\activate
```

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Run tests

```powershell
pytest
```

## Run the application

```powershell
python -m src.main
```

Then open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Database location

The SQLite database is created under:

```text
data/autoserve.db
```

The database is created automatically on startup and during tests when the environment variable `AUTOSERVE_DB_PATH` is set.

## Troubleshooting

### Import errors

Make sure you are running from the AutoServe-API project root, and that the virtual environment is active.

### Database not created

Check that the `data` directory exists and that the app or tests have initialized the database.

### Port already in use

If port 8000 is already occupied, stop the process using it and restart the app.

### Test database pollution

Tests use a temporary SQLite database and must not touch the real `data/autoserve.db` file.
