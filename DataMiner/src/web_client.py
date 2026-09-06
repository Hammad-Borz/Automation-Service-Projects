"""HTTP access for DataMiner."""

from __future__ import annotations

import requests


class WebClientError(Exception):
    """Base class for web client failures."""


class NetworkError(WebClientError):
    """The requested site could not be reached."""


class HTTPResponseError(WebClientError):
    """The server returned an unsuccessful HTTP status."""

    def __init__(self, url: str, status_code: int) -> None:
        self.url = url
        self.status_code = status_code
        super().__init__(f"GET {url} failed with HTTP status {status_code}.")


class WebClient:
    """Fetch HTML with a predictable timeout and User-Agent."""

    USER_AGENT = "DataMiner/1.0 (+https://example.com/dataminer)"

    def __init__(self, timeout: float = 10.0, session: requests.Session | None = None) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.timeout = timeout
        self.session = session or requests.Session()

    def fetch(self, url: str) -> str:
        try:
            response = self.session.get(url, timeout=self.timeout, headers={"User-Agent": self.USER_AGENT})
        except requests.RequestException as exc:
            raise NetworkError(f"Could not fetch {url}: {exc}") from exc
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise HTTPResponseError(url, response.status_code) from exc
        return response.text
