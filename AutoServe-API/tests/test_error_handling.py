from fastapi.testclient import TestClient

from src.main import app


def test_404_for_missing_job(temp_db):
    client = TestClient(app)
    response = client.get("/jobs/NOT_REAL")
    assert response.status_code == 404


def test_404_for_missing_run(temp_db):
    client = TestClient(app)
    response = client.get("/runs/NOT_REAL")
    assert response.status_code == 404


def test_validation_error(temp_db):
    client = TestClient(app)
    response = client.post("/jobs", json={"automation_type": "", "payload": {"title": "bad"}, "request_id": "REQ-ERR"})
    assert response.status_code == 422


def test_unknown_automation_error(temp_db):
    client = TestClient(app)
    response = client.post("/jobs", json={"automation_type": "unknown_action", "payload": {"title": "x"}, "request_id": "REQ-ERR-2"})
    assert response.status_code == 201
    execute = client.post(f"/jobs/{response.json()['job_id']}/execute")
    assert execute.status_code == 400
