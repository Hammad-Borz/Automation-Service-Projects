"""Command-line entry point for ConnectHub."""

from __future__ import annotations

import os

from dotenv import load_dotenv

from api_client import APIClient, APIClientError
from integration_service import IntegrationService
from logger import get_logger


def main() -> int:
    load_dotenv()
    source_url = os.getenv("SOURCE_API_URL")
    destination_url = os.getenv("DESTINATION_API_URL")
    if not source_url or not destination_url:
        print("Configuration error: set SOURCE_API_URL and DESTINATION_API_URL in your environment or .env file.")
        return 1

    logger = get_logger()
    service = IntegrationService(APIClient(), logger=logger)
    try:
        summary = service.run(source_url, destination_url)
    except APIClientError as exc:
        logger.error("Integration could not start: %s", exc)
        print(f"Integration failed while fetching source data: {exc}")
        return 1

    print("ConnectHub integration complete")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
