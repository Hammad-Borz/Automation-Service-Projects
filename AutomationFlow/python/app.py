from typing import Any

from fastapi import FastAPI, HTTPException

from processor import process_lead


app = FastAPI(
    title="AutomationFlow Lead Processor",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process-lead")
def process_lead_endpoint(lead: dict[str, Any]) -> dict[str, Any]:
    try:
        result = process_lead(lead)

        return {
            "success": True,
            "lead": lead,
            "analysis": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Lead processing failed: {exc}",
        ) from exc


@app.post("/notify-sales")
def notify_sales(lead_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": True,
        "action": "notify_sales",
        "message": (
            "High-priority sales lead notification prepared "
            f"for {lead_data.get('email')}"
        ),
    }