from src.models.events import NormalizedEvent, utc_now


def normalize_event(event_id: str, event_type: str, timestamp: str, source: str, data: dict) -> NormalizedEvent:
    return NormalizedEvent(
        event_id=event_id,
        event_type=event_type,
        source=source,
        timestamp=timestamp,
        payload=data,
        received_at=utc_now(),
    )
