def test_pagination(client, payload):
    for index in range(3):
        item = {**payload, "event_id": f"evt-{index}"}
        client.post("/webhooks/events", json=item)
    response = client.get("/events?limit=2&offset=1")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 2


def test_event_types_appear_in_analytics(client):
    base = {"timestamp": "2026-09-11T10:30:00Z", "source": "system", "data": {}}
    for event_type, event_id in [("order.created", "order-1"), ("payment.received", "payment-1")]:
        client.post("/webhooks/events", json={**base, "event_type": event_type, "event_id": event_id})
    result = client.get("/analytics/overview").json()
    assert result["events_by_type"] == {"order.created": 1, "payment.received": 1}
