"""Command-line workflow for DataMiner."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from data_cleaner import DataCleaner
from data_exporter import DataExporter
from data_extractor import DataExtractor
from data_validator import DataValidator
from logger import get_logger
from report_generator import ReportGenerator
from web_client import WebClient, WebClientError


def main() -> int:
    # Keep explicitly supplied environment variables authoritative over `.env`.
    load_dotenv()
    source_url = os.getenv("SOURCE_URL")
    if not source_url:
        print("Configuration error: set SOURCE_URL before running DataMiner.")
        return 1
    logger = get_logger()
    try:
        html = WebClient().fetch(source_url)
    except WebClientError as exc:
        logger.error("Fetch failed: %s", exc)
        print(f"Unable to fetch source URL: {exc}")
        return 1

    extracted = DataExtractor().extract(html)
    validation = DataValidator().validate_records(extracted)
    cleaning = DataCleaner().clean_records(validation.valid_records)
    export_paths = DataExporter().export(cleaning.cleaned_records)
    summary = {
        "total_extracted": len(extracted),
        "valid_records": len(validation.valid_records),
        "invalid_records": len(validation.invalid_records),
        "successfully_cleaned_records": len(cleaning.cleaned_records),
        "failed_cleaning_records": len(cleaning.failed_records),
    }
    report_path = ReportGenerator().generate(source_url, summary, export_paths.csv_path, export_paths.json_path)
    logger.info("Processing completed: %s", summary)
    print("DataMiner processing complete")
    print(f"  Clean records: {summary['successfully_cleaned_records']}")
    print(f"  CSV: {export_paths.csv_path}\n  JSON: {export_paths.json_path}\n  Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
