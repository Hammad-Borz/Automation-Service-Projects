from fastapi.testclient import TestClient

from src.main import app


def test_get_jobs_list(temp_db):
    client = TestClient(app)
    client.post(
        "/jobs",
        json={"automation_type": "create_task", "payload": {"title": "One", "priority": "high"}, "request_id": "REQ-GET-1"},
    )
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_job(temp_db):
    client = TestClient(app)
    created = client.post(
        "/jobs",
        json={"automation_type": "generate_summary", "payload": {"text": "summary"}, "request_id": "REQ-GET-2"},
    ).json()
    response = client.get(f"/jobs/{created['job_id']}")
    assert response.status_code == 200
    assert response.json()["automation_type"] == "generate_summary"


def test_get_automations(temp_db):
    client = TestClient(app)
    response = client.get("/automations")
    assert response.status_code == 200
    assert "create_task" in response.json()["automations"]
