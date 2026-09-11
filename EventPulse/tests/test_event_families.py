import pytest


@pytest.mark.parametrize(
    ("event_type", "data", "expected_action"),
    [
        ("lead.updated", {"email": "lead@example.com", "source": "website"}, "notify_sales"),
        ("order.created", {"total": 1000}, "flag_high_value_order"),
        ("payment.received", {"amount": 250}, "record_payment"),
        ("support.ticket_created", {"priority": "high"}, "route_support"),
    ],
)
def test_supported_event_families(client, event_type, data, expected_action):
    response = client.post("/webhooks/events", json={
        "event_id": f"evt-{event_type}", "event_type": event_type,
        "timestamp": "2026-09-11T10:30:00Z", "source": "test", "data": data,
    })
    assert response.status_code == 200
    assert response.json()["result"][0]["action"] == expected_action


def test_support_standard_priority_is_noop(client):
    response = client.post("/webhooks/events", json={
        "event_id": "support-standard", "event_type": "support.ticket_created",
        "timestamp": "2026-09-11T10:30:00Z", "source": "support", "data": {"priority": "normal"},
    })
    assert response.json()["result"][0]["action"] == "no_action"


def test_lead_without_email_is_noop(client):
    response = client.post("/webhooks/events", json={
        "event_id": "lead-no-email", "event_type": "lead.created",
        "timestamp": "2026-09-11T10:30:00Z", "source": "website", "data": {"message": "pricing"},
    })
    assert response.json()["result"][0]["action"] == "no_action"


def test_invalid_timestamp_is_rejected(client, payload):
    payload["timestamp"] = "not-a-timestamp"
    assert client.post("/webhooks/events", json=payload).status_code == 422


def test_result_not_found(client):
    assert client.get("/events/missing/result").status_code == 404


def test_offset_beyond_events_is_empty(client):
    assert client.get("/events?offset=10").json()["items"] == []
