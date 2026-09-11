from fastapi.testclient import TestClient

from src.main import app


def test_job_creation_success(temp_db):
    client = TestClient(app)
    response = client.post(
        "/jobs",
        json={
            "automation_type": "create_task",
            "payload": {"title": "Follow up with customer", "priority": "high"},
            "request_id": "REQ-001",
        },
    )
    assert response.status_code == 201
    assert response.json()["request_id"] == "REQ-001"


def test_duplicate_request_returns_existing_job(temp_db):
    client = TestClient(app)
    payload = {"automation_type": "create_task", "payload": {"title": "Task", "priority": "high"}, "request_id": "REQ-DUP"}
    first = client.post("/jobs", json=payload)
    second = client.post("/jobs", json=payload)
    assert first.status_code == 201
    assert second.status_code == 201
    assert second.json()["job_id"] == first.json()["job_id"]
