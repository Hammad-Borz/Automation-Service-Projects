def test_duplicate_event_is_not_processed_twice(client, payload):
    first = client.post("/webhooks/events", json=payload).json()
    second = client.post("/webhooks/events", json=payload).json()
    assert first["status"] == "completed"
    assert second["status"] == "duplicate"
    assert second["duplicate"] is True
    stored = client.get(f"/events/{payload['event_id']}").json()
    assert len(stored["result"]) == 1


def test_analytics_counts_duplicate(client, payload):
    client.post("/webhooks/events", json=payload)
    client.post("/webhooks/events", json=payload)
    analytics = client.get("/analytics/overview").json()
    assert analytics["total_events"] == 1
    assert analytics["duplicate_events"] == 1
    assert analytics["actions_prepared"] == 1
