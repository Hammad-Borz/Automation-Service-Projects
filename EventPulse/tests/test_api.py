def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_webhook(client):
    response = client.post("/webhooks/events", json={"event_id": "missing-fields"})
    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_missing_event(client):
    response = client.get("/events/no-such-event")
    assert response.status_code == 404


def test_rules_endpoint(client):
    response = client.get("/automations/rules")
    assert response.status_code == 200
    assert len(response.json()["rules"]) >= 4
