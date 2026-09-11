import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.schemas import ErrorResponse, EventResponse, RulesResponse, WebhookEvent
from src.config import Settings
from src.core.event_processor import EventProcessor
from src.core.rule_engine import supported_rules
from src.database.connection import initialize_database
from src.database.repository import EventRepository
from src.models.events import utc_now
from src.services.event_service import normalize_event


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings.from_environment()
    app_settings.ensure_database_directory()
    initialize_database(app_settings.database_path)
    repository = EventRepository(app_settings.database_path)
    processor = EventProcessor(repository)
    logging.basicConfig(level=getattr(logging, app_settings.logging_level.upper(), logging.INFO))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        initialize_database(app_settings.database_path)
        yield

    app = FastAPI(title="EventPulse", version="1.0.0", lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422, content={"error": "validation_error", "detail": "Invalid webhook payload"})

    @app.exception_handler(Exception)
    async def internal_error_handler(request: Request, exc: Exception):
        return JSONResponse(status_code=500, content={"error": "internal_error", "detail": "Event processing failed"})

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/webhooks/events", response_model=EventResponse)
    def receive_event(payload: WebhookEvent):
        event = normalize_event(payload.event_id, payload.event_type, payload.timestamp.isoformat(), payload.source, payload.data)
        return processor.process(event)

    @app.get("/events")
    def list_events(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)):
        return {"items": repository.list_events(limit, offset), "limit": limit, "offset": offset}

    @app.get("/events/{event_id}")
    def get_event(event_id: str):
        event = repository.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    @app.get("/events/{event_id}/result")
    def get_result(event_id: str):
        event = repository.get_event(event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"event_id": event_id, "status": event["status"], "result": event["result"], "error": event["error"]}

    @app.get("/automations/rules", response_model=RulesResponse)
    def rules():
        return {"rules": supported_rules()}

    @app.get("/analytics/overview")
    def analytics():
        return repository.analytics()

    return app


app = create_app()
