from unittest.mock import Mock

import pytest
import requests

from web_client import HTTPResponseError, NetworkError, WebClient


def test_fetch_returns_html_with_user_agent_and_timeout():
    session = Mock()
    response = Mock(text="<html></html>")
    response.raise_for_status.return_value = None
    session.get.return_value = response

    assert WebClient(timeout=4, session=session).fetch("https://example.test") == "<html></html>"
    session.get.assert_called_once_with("https://example.test", timeout=4, headers={"User-Agent": WebClient.USER_AGENT})


def test_fetch_raises_network_error():
    session = Mock()
    session.get.side_effect = requests.ConnectionError("offline")
    with pytest.raises(NetworkError, match="offline"):
        WebClient(session=session).fetch("https://example.test")


def test_fetch_raises_http_error():
    session = Mock()
    response = Mock(status_code=500)
    response.raise_for_status.side_effect = requests.HTTPError("server error")
    session.get.return_value = response
    with pytest.raises(HTTPResponseError, match="500"):
        WebClient(session=session).fetch("https://example.test")
