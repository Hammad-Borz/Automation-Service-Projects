from unittest.mock import Mock

from api_client import APINetworkError
from integration_service import IntegrationService


def test_successful_workflow():
    client = Mock()
    client.get.return_value = [
        {"id": 1, "name": "Ada", "email": "ada@example.com"},
        {"id": 2, "name": "Grace", "email": "grace@example.com"},
    ]
    service = IntegrationService(client)

    summary = service.run("https://source.test", "https://destination.test")

    assert summary == {"total_fetched": 2, "valid_records": 2, "invalid_records": 0, "successfully_sent": 2, "failed_to_send": 0}
    assert client.post.call_count == 2


def test_partial_failures_do_not_stop_valid_records():
    client = Mock()
    client.get.return_value = [
        {"id": 1, "name": "Ada", "email": "ada@example.com"},
        {"id": 2, "name": "Invalid"},
        {"id": 3, "name": "Grace", "email": "grace@example.com"},
    ]
    client.post.side_effect = [None, APINetworkError("POST", "https://destination.test", ConnectionError("offline"))]
    service = IntegrationService(client)

    summary = service.run("https://source.test", "https://destination.test")

    assert summary == {"total_fetched": 3, "valid_records": 2, "invalid_records": 1, "successfully_sent": 1, "failed_to_send": 1}
    assert client.post.call_count == 2
