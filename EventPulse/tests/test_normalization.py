from src.services.event_service import normalize_event


def test_normalization_separates_payload_from_http_shape():
    event = normalize_event("evt-1", "lead.created", "2026-09-11T10:30:00+00:00", "website", {"email": "x@y.test"})
    assert event.event_id == "evt-1"
    assert event.payload == {"email": "x@y.test"}
    assert event.received_at
