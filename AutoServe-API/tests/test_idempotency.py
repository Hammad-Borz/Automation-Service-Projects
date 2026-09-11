from fastapi.testclient import TestClient

from src.main import app


def test_duplicate_request_is_idempotent(temp_db):
    client = TestClient(app)
    body = {"automation_type": "create_task", "payload": {"title": "Repeated", "priority": "low"}, "request_id": "REQ-IDEMPOTENT"}
    first = client.post("/jobs", json=body)
    second = client.post("/jobs", json=body)
    assert first.json()["job_id"] == second.json()["job_id"]
    assert first.json()["job_id"] == second.json()["job_id"]


def test_same_request_returns_same_job_instance(temp_db):
    client = TestClient(app)
    body = {"automation_type": "send_notification", "payload": {"recipient": "a@example.com", "message": "hi"}, "request_id": "REQ-UNIQUE-1"}
    first = client.post("/jobs", json=body)
    second = client.post("/jobs", json=body)
    assert first.status_code == 201 and second.status_code == 201
    assert first.json()["job_id"] == second.json()["job_id"]
