from fastapi.testclient import TestClient

from src.main import app


def test_get_runs_list(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "A", "priority": "low"}, "request_id": "REQ-RUNS-1"},
    ).json()
    client.post(f"/jobs/{job['job_id']}/execute")
    response = client.get("/runs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_run_by_id(temp_db):
    client = TestClient(app)
    job = client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "A", "priority": "low"}, "request_id": "REQ-RUNS-2"},
    ).json()
    execution = client.post(f"/jobs/{job['job_id']}/execute").json()
    response = client.get(f"/runs/{execution['run_id']}")
    assert response.status_code == 200
    assert response.json()["job_id"] == job["job_id"]
