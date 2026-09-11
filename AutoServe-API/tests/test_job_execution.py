from fastapi.testclient import TestClient

from src.main import app


def test_execution_success(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={
            "automation_type": "create_task",
            "payload": {"title": "Follow up with customer", "priority": "high"},
            "request_id": "REQ-EXEC-1",
        },
    ).json()
    result = client.post(f"/jobs/{job['job_id']}/execute")
    assert result.status_code == 200
    assert result.json()["status"] == "completed"


def test_execution_unknown_action_fails_gracefully(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={
            "automation_type": "unknown_action",
            "payload": {"title": "Nope"},
            "request_id": "REQ-EXEC-2",
        },
    ).json()
    result = client.post(f"/jobs/{job['job_id']}/execute")
    assert result.status_code == 400
    assert "unknown_automation" in result.json()["detail"]["error"]


def test_execution_of_nonexistent_job(temp_db):
    client = TestClient(app)
    response = client.post("/jobs/NOT_REAL/execute")
    assert response.status_code == 404
