def test_blank_event_id_rejected(client, payload):
    payload["event_id"] = ""
    assert client.post("/webhooks/events", json=payload).status_code == 422


def test_extra_fields_rejected(client, payload):
    payload["unexpected"] = "value"
    assert client.post("/webhooks/events", json=payload).status_code == 422


def test_pagination_bounds_rejected(client):
    assert client.get("/events?limit=0").status_code == 422
