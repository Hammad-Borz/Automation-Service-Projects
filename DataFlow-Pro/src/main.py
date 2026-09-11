import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.routes import build_router
from src.config import Settings
from src.database.connection import initialize_database
from src.database.repository import DataRepository
from src.core.pipeline import Pipeline


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings.for_project()
    app_settings.ensure_directories()
    initialize_database(app_settings.database_path)
    logging.basicConfig(level=getattr(logging, app_settings.logging_level.upper(), logging.INFO))
    repository = DataRepository(app_settings.database_path)
    pipeline = Pipeline(app_settings, repository)
    app = FastAPI(title="DataFlow Pro", version="1.0.0")
    app.include_router(build_router(app_settings, pipeline, repository))

    @app.exception_handler(Exception)
    async def internal_error_handler(request, exc):
        return JSONResponse(status_code=500, content={"error": "internal_error", "detail": "Operation failed"})

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=False)
