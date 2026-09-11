from fastapi.testclient import TestClient

from src.main import app


def test_retry_failed_job(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={
            "automation_type": "create_task",
            "payload": {"title": "Retry demo", "priority": "medium"},
            "request_id": "REQ-RETRY-1",
        },
    ).json()
    client.post(f"/jobs/{job['job_id']}/execute")
    response = client.post(f"/jobs/{job['job_id']}/retry")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_retry_limit_error(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={
            "automation_type": "create_task",
            "payload": {"title": "Limit", "priority": "low"},
            "request_id": "REQ-RETRY-2",
        },
    ).json()
    response = client.post(f"/jobs/{job['job_id']}/retry")
    assert response.status_code == 400
    assert "retry_failed" in response.json()["detail"]["error"]
