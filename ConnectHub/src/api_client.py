"""Small, reusable HTTP client used by ConnectHub."""

from __future__ import annotations

from typing import Any, Mapping

import requests


class APIClientError(Exception):
    """Base exception for errors raised by :class:`APIClient`."""


class APIHTTPError(APIClientError):
    """An HTTP response returned an unsuccessful status code."""

    def __init__(self, method: str, url: str, status_code: int) -> None:
        self.method = method
        self.url = url
        self.status_code = status_code
        super().__init__(f"{method} {url} failed with HTTP status {status_code}.")


class APINetworkError(APIClientError):
    """A request could not reach the remote service."""

    def __init__(self, method: str, url: str, reason: Exception) -> None:
        self.method = method
        self.url = url
        self.reason = reason
        super().__init__(f"{method} {url} failed due to a network error: {reason}")


class APIResponseError(APIClientError):
    """A successful response did not contain valid JSON."""


class APIClient:
    """Issue JSON GET and POST requests with consistent error handling."""

    def __init__(self, timeout: float = 10.0, session: requests.Session | None = None) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.timeout = timeout
        self.session = session or requests.Session()

    def get(self, url: str) -> Any:
        """Fetch and decode JSON from *url*."""
        return self._request_json("GET", url)

    def post(self, url: str, payload: Mapping[str, Any]) -> Any:
        """Send *payload* as JSON to *url* and decode the JSON response."""
        return self._request_json("POST", url, json=dict(payload))

    def _request_json(self, method: str, url: str, **kwargs: Any) -> Any:
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        except requests.RequestException as exc:
            raise APINetworkError(method, url, exc) from exc

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise APIHTTPError(method, url, response.status_code) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise APIResponseError(f"{method} {url} returned invalid JSON.") from exc
