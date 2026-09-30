"""Shared async HTTP transport."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


class JournalTransport:
    """Reusable transport around :class:`httpx.AsyncClient`.

    Cookies are accepted for browser-session experiments but are never logged.
    """

    def __init__(
        self,
        *,
        base_url: str,
        token: str | None = None,
        cookies: Mapping[str, str] | httpx.Cookies | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float | httpx.Timeout = 20.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._owns_client = client is None
        default_headers = {
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "ittop-journal-api/0.1",
            "Origin": "https://journal.top-academy.ru",
            "Referer": "https://journal.top-academy.ru/",
        }
        if headers:
            default_headers.update(headers)
        self._client = client or httpx.AsyncClient(
            base_url=self.base_url,
            headers=default_headers,
            cookies=cookies,
            timeout=timeout,
            follow_redirects=True,
        )

    async def __aenter__(self) -> JournalTransport:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Send a request and return decoded JSON, or text for non-JSON replies."""
        headers = dict(kwargs.pop("headers", {}) or {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            response = await self._client.request(method, path, headers=headers, **kwargs)
        except httpx.HTTPError as exc:
            raise APIError("HTTP transport failed", method=method, url=path) from exc
        if response.status_code >= 400:
            raise self._map_error(response, method, path)
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    @staticmethod
    def _map_error(response: httpx.Response, method: str, path: str) -> APIError:
        try:
            payload: Any = response.json()
        except ValueError:
            payload = response.text[:1000]
        message = "Journal API request failed"
        if isinstance(payload, dict):
            message = str(payload.get("message") or payload.get("error") or message)
        elif isinstance(payload, str) and payload:
            message = payload
        error_type: type[APIError]
        if response.status_code in (401, 403):
            error_type = AuthenticationError if response.status_code == 401 else AuthorizationError
        elif response.status_code == 404:
            error_type = NotFoundError
        elif response.status_code == 422:
            error_type = ValidationError
        elif response.status_code == 429:
            error_type = RateLimitError
        else:
            error_type = APIError
        return error_type(
            message, status_code=response.status_code, method=method, url=path, response=payload
        )
