from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from src.api.schemas import AnalyticsRunRequest
from src.config import Settings
from src.core.pipeline import AnalyticsPipeline
from src.database.repository import AnalyticsRepository


def build_router(settings: Settings, pipeline: AnalyticsPipeline, repository: AnalyticsRepository) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health(): return {"status": "ok"}

    @router.post("/analytics/run")
    def run(request: AnalyticsRunRequest):
        try: return pipeline.run(_safe_path(request.input_path, settings))
        except (FileNotFoundError, ValueError) as exc: raise HTTPException(400, str(exc)) from exc
        except Exception as exc: raise HTTPException(500, "Analytics execution failed") from exc

    @router.get("/analytics/overview")
    def overview(): return _latest_analytics(settings)
    @router.get("/analytics/trends")
    def trends(): return _latest_analytics(settings)["trends"]
    @router.get("/analytics/categories")
    def categories(): return _latest_analytics(settings)["categories"]
    @router.get("/analytics/products")
    def products(): return _latest_analytics(settings)["products"]
    @router.get("/analytics/regions")
    def regions(): return _latest_analytics(settings)["regions"]
    @router.get("/analytics/channels")
    def channels(): return _latest_analytics(settings)["channels"]
    @router.get("/analytics/customers")
    def customers(): return _latest_analytics(settings)["customers"]
    @router.get("/analytics/anomalies")
    def anomalies(): return _latest_analytics(settings)["anomalies"]
    @router.get("/insights")
    def insights(): return _latest_analytics(settings)["insights"]
    @router.get("/reports/latest")
    def reports(): return {"reports": _latest_run(repository).get("reports", [])}
    @router.get("/analytics/runs")
    def runs(): return {"items": repository.list_runs()}
    @router.get("/analytics/runs/{run_id}")
    def run_detail(run_id: str):
        result = repository.get_run(run_id)
        if not result: raise HTTPException(404, "Analytics run not found")
        return result
    @router.get("/data/quality")
    def quality(): return _latest_run(repository).get("quality", {})
    @router.get("/records")
    def records(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)): return {"items": repository.list_records(limit, offset), "limit": limit, "offset": offset}
    @router.get("/records/{order_id}")
    def record(order_id: str):
        result = repository.get_record(order_id)
        if not result: raise HTTPException(404, "Record not found")
        return result
    return router


def _safe_path(raw: str | None, settings: Settings) -> Path:
    path = settings.default_input_path if not raw else (settings.project_root / raw).resolve()
    data = settings.data_dir.resolve()
    if data not in path.parents and path != data: raise ValueError("input_path must remain inside the data directory")
    return path


def _latest_run(repository):
    runs = repository.list_runs()
    if not runs: raise HTTPException(404, "No analytics run available")
    return runs[0]


def _latest_analytics(settings):
    from src.services.analytics_service import run_analytics
    from src.core.data_loader import load_csv
    from src.core.normalizer import normalize_frame
    from src.core.validator import validate_frame
    frame = normalize_frame(load_csv(settings.default_input_path)); results = validate_frame(frame); valid = frame[[r.valid for r in results]].copy()
    return {**run_analytics(valid, settings.high_value_threshold, settings.anomaly_z_threshold), "insights": __import__('src.services.insight_service', fromlist=['generate_insights']).generate_insights(run_analytics(valid, settings.high_value_threshold, settings.anomaly_z_threshold))}
