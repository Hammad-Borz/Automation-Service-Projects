# DataMiner — Web Data Extraction & Processing System

DataMiner is a reusable Python workflow for turning product-style HTML into clean, portable data. It fetches a page, extracts structured records using explicit CSS selectors, validates and normalizes each record, exports successful results, and creates a processing report.

## Business Problem

Teams often receive catalog information in HTML but need dependable CSV or JSON data for analysis, migrations, and operational workflows. DataMiner demonstrates a clear, testable path from controlled HTML to cleaned data without coupling the project to a third-party commercial website.

## Features

- Configurable HTTP fetching with timeout, User-Agent, and clear network/HTTP errors.
- BeautifulSoup extraction from documented `.product-card` selectors.
- Record-level validation and cleaning that lets valid data continue when individual records fail.
- Whitespace, price, category, and availability normalization.
- UTF-8 CSV and JSON exports, plus a human-readable processing report.
- File logging without duplicate handlers and a fully offline pytest suite.

## Architecture

```text
SOURCE_URL -> WebClient -> DataExtractor -> DataValidator -> DataCleaner -> DataExporter -> ReportGenerator
                              malformed cards   invalid records   cleaning failures
```

## Project Structure

```text
DataMiner/
├── demo/      # Local, reproducible sample catalog for the end-to-end demo
├── src/       # Fetching, extraction, validation, cleaning, export, reporting
├── tests/     # Offline unit tests with mocked HTTP
├── output/    # Generated CSV and JSON files (ignored by Git)
├── reports/   # Generated processing reports (ignored by Git)
└── logs/      # Generated application log (ignored by Git)
```

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

Set a source URL, then run the program from the project root:

```powershell
$env:SOURCE_URL = "https://example.com/catalog"
python src/main.py
```

## Local End-to-End Demo

The included `demo/sample_products.html` lets you run the whole workflow without
depending on an external website. It contains five complete product cards. Four
are exported after normalization; one uses `Price on request` to demonstrate how
an otherwise valid record is safely reported as a cleaning failure.

From the `DataMiner` directory, start Python's built-in web server in one
PowerShell window:

```powershell
cd demo
python -m http.server 8000
```

In a second PowerShell window, return to the `DataMiner` directory, activate the
environment if needed, and set the source URL before running the workflow:

```powershell
$env:SOURCE_URL = "http://localhost:8000/sample_products.html"
python src/main.py
```

Alternatively, copy `.env.example` to `.env` and run `python src/main.py`.
`main.py` loads `.env` automatically, while a value already set in the normal
environment takes precedence. The demo writes its CSV and JSON to `output/` and
its run summary to `reports/`.

For integration or demonstrations, use HTML with this controlled structure:

```html
<article class="product-card">
  <h2 class="product-name">Widget</h2>
  <span class="product-price">$12.50</span>
  <span class="product-category">Tools</span>
  <span class="product-availability">In Stock</span>
</article>
```

## Testing

```powershell
pytest
```

Tests cover successful and failed HTTP requests, HTML extraction, malformed cards, validation, cleaning and price conversion, CSV/JSON exports, and report generation. No internet access is required.

## Example Workflow

Given three product cards, DataMiner skips malformed HTML safely, reports invalid extracted data, cleans the usable records, writes `output/csv/products.csv` and `output/json/products.json`, and saves a summary in `reports/processing_report.txt`.

## Technology Stack

Python, requests, BeautifulSoup4, pytest, unittest.mock, csv, json, logging, and pathlib.

## Limitations and Future Improvements

This focused portfolio project processes one HTML response and a defined product-card structure. A production version may add pagination, retry/backoff behavior, rate limiting, configurable selectors, duplicate detection, provenance metadata, and scheduled execution.
