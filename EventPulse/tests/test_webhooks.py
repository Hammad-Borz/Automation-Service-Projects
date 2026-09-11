def test_lead_webhook_processes(client, payload):
    response = client.post("/webhooks/events", json=payload)
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "completed"
    assert body["result"][0]["action"] == "notify_sales"


def test_unknown_event_is_safe(client):
    payload = {
        "event_id": "evt-unknown", "event_type": "invoice.unknown",
        "timestamp": "2026-09-11T10:30:00Z", "source": "billing", "data": {},
    }
    response = client.post("/webhooks/events", json=payload)
    assert response.status_code == 200
    assert response.json()["result"][0]["action"] == "no_action"


def test_event_can_be_listed_and_retrieved(client, payload):
    client.post("/webhooks/events", json=payload)
    listed = client.get("/events").json()
    retrieved = client.get(f"/events/{payload['event_id']}").json()
    assert listed["items"][0]["event_id"] == payload["event_id"]
    assert retrieved["payload"]["email"] == "john@example.com"


def test_event_result_endpoint(client, payload):
    client.post("/webhooks/events", json=payload)
    response = client.get(f"/events/{payload['event_id']}/result")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
