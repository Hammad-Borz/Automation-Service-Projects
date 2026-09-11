import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
import pandas as pd
from src.config import Settings
from src.core.data_loader import load_csv
from src.core.normalizer import normalize_frame
from src.core.report_engine import generate_reports
from src.core.validator import validate_frame
from src.database.repository import AnalyticsRepository
from src.services.insight_service import generate_insights
from src.services.analytics_service import run_analytics

logger = logging.getLogger(__name__)


class AnalyticsPipeline:
    def __init__(self, settings: Settings, repository: AnalyticsRepository | None = None):
        self.settings = settings; self.repository = repository or AnalyticsRepository(settings.database_path)

    def run(self, input_path: Path | None = None) -> dict:
        run_id = str(uuid4()); started = datetime.now(timezone.utc).isoformat(); path = input_path or self.settings.default_input_path
        base = {"run_id": run_id, "started_at": started, "status": "failed", "input_records": 0, "valid_records": 0, "invalid_records": 0, "duplicate_records": 0}
        try:
            logger.info("Analytics run started: %s", run_id)
            raw = load_csv(path); base["input_records"] = len(raw)
            normalized = normalize_frame(raw)
            validation = validate_frame(normalized)
            valid_ids = {item.record_id for item in validation if item.valid}
            valid = normalized[normalized.record_id.isin(valid_ids)].copy()
            duplicate_mask = valid.duplicated("order_id", keep="first")
            canonical = valid.loc[~duplicate_mask].copy()
            base.update({"valid_records": len(canonical), "invalid_records": len(raw) - len(valid_ids), "duplicate_records": int(duplicate_mask.sum())})
            analytics = run_analytics(canonical, self.settings.high_value_threshold, self.settings.anomaly_z_threshold)
            quality = _quality(raw, validation, base["duplicate_records"])
            insights = generate_insights(analytics)
            self.repository.upsert_records(canonical)
            reports = generate_reports(canonical, analytics, insights, quality, self.settings.output_dir)
            base.update({"status": "completed", "completed_at": datetime.now(timezone.utc).isoformat(), "quality": quality, "analytics": analytics, "insights": insights, "reports": reports})
            self.repository.save_run(base, analytics)
            logger.info("Analytics run completed: %s", run_id)
            return base
        except Exception as exc:
            logger.exception("Analytics run failed: %s", run_id)
            base.update({"completed_at": datetime.now(timezone.utc).isoformat(), "error": str(exc)})
            self.repository.save_run(base, {})
            raise


def _quality(raw, validation, duplicates):
    from collections import Counter
    counts = Counter(error for item in validation for error in item.errors); valid = sum(item.valid for item in validation)
    return {"input_records": len(raw), "valid_records": valid, "invalid_records": len(raw) - valid, "duplicate_records": duplicates, "normalized_records": len(raw), "missing_values": sum(v for k, v in counts.items() if "required" in k), "invalid_dates": sum(v for k, v in counts.items() if "date" in k), "invalid_quantities": sum(v for k, v in counts.items() if "quantity" in k), "invalid_prices": sum(v for k, v in counts.items() if "price" in k or "amount" in k), "invalid_statuses": sum(v for k, v in counts.items() if "status" in k), "invalid_channels": sum(v for k, v in counts.items() if "channel" in k), "validation_error_counts": dict(counts), "quality_score": round(valid / len(raw) * 100, 2) if len(raw) else 100.0}
