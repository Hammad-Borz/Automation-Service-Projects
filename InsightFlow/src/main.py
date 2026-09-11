import logging
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.api.routes import build_router
from src.config import Settings
from src.core.pipeline import AnalyticsPipeline
from src.database.connection import initialize_database
from src.database.repository import AnalyticsRepository


def create_app(settings: Settings | None = None) -> FastAPI:
    current = settings or Settings.for_project(); current.ensure_directories(); initialize_database(current.database_path); logging.basicConfig(level=getattr(logging, current.logging_level.upper(), logging.INFO))
    repository = AnalyticsRepository(current.database_path); app = FastAPI(title="InsightFlow", version="1.0.0"); app.include_router(build_router(current, AnalyticsPipeline(current, repository), repository))
    @app.exception_handler(Exception)
    async def internal_error(request, exc): return JSONResponse(500, {"error": "internal_error", "detail": "Analytics operation failed"})
    return app


app = create_app()

if __name__ == "__main__": uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=False)
