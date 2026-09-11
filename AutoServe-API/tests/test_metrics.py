from fastapi.testclient import TestClient

from src.main import app


def test_metrics_summary(temp_db):
    client = TestClient(app)
    client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "A", "priority": "low"}, "request_id": "REQ-METRICS-1"},
    )
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    assert response.json()["total_jobs"] >= 1
