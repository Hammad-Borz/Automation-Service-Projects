"""Command-line entry point for DocuMind."""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ai_processor import AIProcessor
from src.document_reader import DocumentReader
from src.logger import get_logger
from src.report_generator import ReportGenerator
from src.result_exporter import ResultExporter


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a PDF or DOCX document with DocuMind.")
    parser.add_argument("document", help="Path to a supported PDF or DOCX document")
    args = parser.parse_args()
    load_dotenv(PROJECT_ROOT / ".env")
    logger = get_logger(PROJECT_ROOT / "logs")
    source = Path(args.document)
    try:
        logger.info("Started processing %s", source.name)
        text = DocumentReader().extract_text(source)
        analysis = AIProcessor().analyze(text)
        result_path = ResultExporter(PROJECT_ROOT / "output" / "results").export(analysis, source.name)
        report_path = ReportGenerator(PROJECT_ROOT / "output" / "reports").generate(analysis, source.name)
        logger.info("Completed processing %s", source.name)
        print("Processing complete.")
        print(f"Analysis JSON: {result_path}")
        print(f"Report: {report_path}")
        return 0
    except Exception as exc:
        logger.error("Processing failed for %s: %s", source.name, exc)
        print(f"Processing failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
