"""End-to-end reporting workflow."""

from pathlib import Path

from .analytics import Analytics
from .config import Settings
from .data_loader import DataLoader
from .data_processor import DataProcessor
from .data_validator import DataValidator
from .excel_exporter import ExcelExporter
from .logger import configure_logging
from .models import WorkflowResult
from .report_generator import ReportGenerator


class ReportingWorkflow:
    """Coordinate ingestion, analysis, and all report outputs."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_project_root()
        self.logger = configure_logging(self.settings.logs_dir)

    def run(self, source: Path | None = None) -> WorkflowResult:
        input_path = Path(source) if source else self.settings.input_dir / "sales_data.csv"
        self.logger.info("Loading business data from %s", input_path)
        raw = DataLoader().load(input_path)
        DataValidator(self.settings.required_columns).validate(raw)
        processed = DataProcessor().process(raw)
        analytics = Analytics().calculate(processed)
        excel_path = ExcelExporter().export(analytics, self.settings.output_dir / "reportflow_business_report.xlsx")
        text_path = ReportGenerator().generate(analytics, self.settings.output_dir / "business_report.txt")
        csv_paths = []
        for name, frame in (("processed_orders", processed), ("product_summary", analytics.by_product), ("regional_summary", analytics.by_region), ("monthly_summary", analytics.monthly)):
            path = self.settings.output_dir / f"{name}.csv"
            frame.to_csv(path, index=False)
            csv_paths.append(path)
        self.logger.info("Report generated successfully: %s", excel_path)
        return WorkflowResult(input_path, excel_path, text_path, tuple(csv_paths), analytics)
