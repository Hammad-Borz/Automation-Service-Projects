from unittest.mock import Mock

import pytest
import requests

from api_client import APIClient, APIHTTPError, APINetworkError


def response_with_json(data):
    response = Mock()
    response.json.return_value = data
    response.raise_for_status.return_value = None
    return response


def test_get_returns_json_and_uses_timeout():
    session = Mock()
    session.request.return_value = response_with_json([{"id": 1}])
    client = APIClient(timeout=4, session=session)

    assert client.get("https://source.test/users") == [{"id": 1}]
    session.request.assert_called_once_with("GET", "https://source.test/users", timeout=4)


def test_post_sends_json_payload():
    session = Mock()
    session.request.return_value = response_with_json({"created": True})
    client = APIClient(session=session)

    assert client.post("https://destination.test/contacts", {"external_id": 1}) == {"created": True}
    session.request.assert_called_once_with("POST", "https://destination.test/contacts", timeout=10.0, json={"external_id": 1})


def test_http_failure_has_clear_custom_error():
    session = Mock()
    response = response_with_json({})
    response.status_code = 503
    response.raise_for_status.side_effect = requests.HTTPError("unavailable")
    session.request.return_value = response

    with pytest.raises(APIHTTPError, match="503"):
        APIClient(session=session).get("https://source.test/users")


def test_network_failure_has_clear_custom_error():
    session = Mock()
    session.request.side_effect = requests.ConnectionError("offline")

    with pytest.raises(APINetworkError, match="network error"):
        APIClient(session=session).get("https://source.test/users")
