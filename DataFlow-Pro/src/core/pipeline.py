import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.config import Settings
from src.core.analytics import calculate_analytics
from src.database.repository import DataRepository
from src.services.ingestion_service import load_csv
from src.services.processing_service import process_frame
from src.services.quality_service import quality_report
from src.services.reporting_service import generate_reports

logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, settings: Settings, repository: DataRepository | None = None) -> None:
        self.settings = settings
        self.repository = repository or DataRepository(settings.database_path)

    def run(self, input_path: Path | None = None) -> dict:
        run_id = str(uuid4())
        started_at = datetime.now(timezone.utc).isoformat()
        path = input_path or self.settings.default_input_path
        base = {"run_id": run_id, "started_at": started_at, "input_records": 0, "valid_records": 0, "invalid_records": 0, "duplicate_records": 0, "status": "failed"}
        try:
            logger.info("Pipeline started: %s", run_id)
            frame = load_csv(path)
            base["input_records"] = len(frame)
            processed = process_frame(frame, path.name, self.settings.high_value_threshold)
            quality = quality_report(processed)
            analytics = calculate_analytics(processed["valid"])
            base.update({"valid_records": quality["valid_records"], "invalid_records": quality["invalid_records"], "duplicate_records": quality["duplicate_records"]})
            self.repository.upsert_records(processed["valid"])
            reports = generate_reports(processed["valid"], quality, analytics, self.settings.output_dir)
            base.update({"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat(), "reports_generated": reports, "quality": quality, "analytics": analytics})
            self.repository.save_run(base)
            logger.info("Pipeline completed: %s", run_id)
            return base
        except Exception as exc:
            logger.exception("Pipeline failed: %s", run_id)
            base.update({"completed_at": datetime.now(timezone.utc).isoformat(), "error": str(exc)})
            self.repository.save_run(base)
            raise
