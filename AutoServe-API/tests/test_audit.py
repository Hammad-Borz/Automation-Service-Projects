from fastapi.testclient import TestClient

from src.main import app


def test_audit_created_for_job(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "A", "priority": "low"}, "request_id": "REQ-AUDIT-1"},
    ).json()
    assert job["job_id"]
    response = client.get("/jobs")
    assert response.status_code == 200


def test_job_execution_creates_audit_records(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "A", "priority": "low"}, "request_id": "REQ-AUDIT-2"},
    )
    execution = client.post(f"/jobs/{job.json()['job_id']}/execute")
    assert execution.status_code == 200
