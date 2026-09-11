from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from src.api.routes import router
from src.database.connection import initialize_database

app = FastAPI(
    title="AutoServe API",
    description="Automation backend platform for deterministic local automation jobs, retries, idempotency, auditing, and metrics.",
    version="0.1.0",
)

app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    initialize_database()


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=False)
