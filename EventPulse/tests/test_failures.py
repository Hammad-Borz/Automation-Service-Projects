from src.core import event_processor


def test_processing_failure_returns_generic_error_and_persists_failure(client, payload, monkeypatch):
    def fail(*args, **kwargs):
        raise RuntimeError("simulated rule failure")

    monkeypatch.setattr(event_processor, "evaluate_rules", fail)
    response = client.post("/webhooks/events", json=payload)
    assert response.status_code == 500
    assert response.json() == {"error": "internal_error", "detail": "Event processing failed"}
    stored = client.get(f"/events/{payload['event_id']}").json()
    assert stored["status"] == "failed"
    assert stored["error"] == "simulated rule failure"


def test_failed_event_does_not_expose_traceback(client, payload, monkeypatch):
    monkeypatch.setattr(event_processor, "evaluate_rules", lambda *args: 1 / 0)
    response = client.post("/webhooks/events", json=payload)
    assert "Traceback" not in response.text
    assert response.status_code == 500


def test_completed_event_status_is_persisted(client, payload):
    client.post("/webhooks/events", json=payload)
    stored = client.get(f"/events/{payload['event_id']}").json()
    assert stored["status"] == "completed"
    assert stored["processed_at"]


def test_analytics_completed_count(client, payload):
    client.post("/webhooks/events", json=payload)
    assert client.get("/analytics/overview").json()["completed_events"] == 1
