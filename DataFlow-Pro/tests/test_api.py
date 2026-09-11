def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_pipeline_run_endpoint(client):
    response = client.post("/pipeline/run", json={})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_runs_endpoint(client):
    client.post("/pipeline/run", json={})
    assert len(client.get("/pipeline/runs").json()["items"]) == 1


def test_analytics_endpoint(client):
    client.post("/pipeline/run", json={})
    response = client.get("/analytics/overview")
    assert response.status_code == 200
    assert response.json()["total_orders"] == 1


def test_records_and_quality_endpoints(client):
    client.post("/pipeline/run", json={})
    assert client.get("/records").status_code == 200
    assert client.get("/records/ORD-1").status_code == 200
    assert client.get("/quality/latest").status_code == 200


def test_invalid_input_path_is_rejected(client):
    response = client.post("/pipeline/run", json={"input_path": "..\\outside.csv"})
    assert response.status_code == 400


def test_missing_run_returns_404(client):
    assert client.get("/pipeline/runs/nope").status_code == 404
