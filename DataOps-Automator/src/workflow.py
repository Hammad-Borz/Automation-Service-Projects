"""End-to-end DataOps workflow."""

from pathlib import Path

from .analytics import Analytics
from .config import Settings
from .data_loader import DataLoader
from .data_processor import DataProcessor
from .data_repository import DataRepository
from .data_validator import DataValidator
from .database_manager import DatabaseManager
from .logger import configure_logging
from .models import WorkflowResult
from .report_exporter import ReportExporter


class DataOpsWorkflow:
    """Coordinate data ingestion, persistence, SQL analytics, and exports."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.from_project_root()
        self.settings.ensure_directories()
        self.logger = configure_logging(self.settings.logs_dir)
        self.database = DatabaseManager(self.settings.database_path)
        self.repository = DataRepository(self.database)

    def run(self, source: Path | None = None) -> WorkflowResult:
        source_path = Path(source) if source else self.settings.input_dir / "sales_data.csv"
        self.logger.info("Data loading started: %s", source_path)
        frame = DataLoader().load(source_path)
        DataValidator(self.settings.required_columns).validate(frame)
        self.logger.info("Data validation completed")
        processed = DataProcessor().process(frame)
        self.database.initialize_schema()
        self.logger.info("Database schema created")
        records_processed = self.repository.insert_sales_data(processed)
        database_records = self.repository.count_sales_records()
        self.logger.info("Records processed: %s; database records: %s", records_processed, database_records)
        analytics = Analytics(self.database).calculate()
        self.logger.info("Analytics completed")
        report_paths = ReportExporter().export(analytics, self.settings.output_dir)
        self.logger.info("Reports generated: %s", len(report_paths))
        return WorkflowResult(source_path, self.settings.database_path, records_processed, database_records, analytics, report_paths)
