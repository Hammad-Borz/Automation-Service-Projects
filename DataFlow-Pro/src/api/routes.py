from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from src.api.schemas import AnalyticsOverview, PipelineRunRequest, PipelineRunResponse
from src.config import Settings
from src.core.analytics import calculate_analytics
from src.core.pipeline import Pipeline
from src.database.repository import DataRepository
from src.services.ingestion_service import IngestionError


def build_router(settings: Settings, pipeline: Pipeline, repository: DataRepository) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/pipeline/run", response_model=PipelineRunResponse)
    def run_pipeline(request: PipelineRunRequest):
        try:
            path = _safe_input_path(request.input_path, settings)
            return pipeline.run(path)
        except (FileNotFoundError, IngestionError, ValueError) as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Pipeline execution failed") from exc

    @router.get("/pipeline/runs")
    def list_runs():
        return {"items": repository.list_runs()}

    @router.get("/pipeline/runs/{run_id}")
    def get_run(run_id: str):
        run = repository.get_run(run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Pipeline run not found")
        return run

    @router.get("/analytics/overview", response_model=AnalyticsOverview)
    def analytics():
        records = repository.list_records(limit=100000)
        import pandas as pd
        return calculate_analytics(pd.DataFrame(records))

    @router.get("/records")
    def records(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
        return {"items": repository.list_records(limit, offset), "limit": limit, "offset": offset}

    @router.get("/records/{order_id}")
    def record(order_id: str):
        item = repository.get_record(order_id)
        if not item:
            raise HTTPException(status_code=404, detail="Record not found")
        return item

    @router.get("/quality/latest")
    def quality_latest():
        item = repository.latest_quality()
        if not item:
            raise HTTPException(status_code=404, detail="No pipeline quality report available")
        return item

    return router


def _safe_input_path(raw_path: str | None, settings: Settings) -> Path:
    path = (settings.default_input_path if not raw_path else (settings.project_dir / raw_path).resolve())
    data_root = (settings.project_dir / "data").resolve()
    if data_root not in path.parents and path != data_root:
        raise ValueError("input_path must remain inside the project data directory")
    return path
