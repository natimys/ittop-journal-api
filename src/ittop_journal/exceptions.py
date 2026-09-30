"""Exception hierarchy and safe error context."""

from __future__ import annotations

from typing import Any


class JournalError(Exception):
    """Base class for all SDK errors."""


class APIError(JournalError):
    """An HTTP or decoding error returned by the Journal API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        method: str | None = None,
        url: str | None = None,
        response: Any = None,
    ) -> None:
        self.status_code = status_code
        self.method = method
        self.url = url
        self.response = response
        location = f" {method} {url}" if method and url else ""
        status = f" [{status_code}]" if status_code is not None else ""
        super().__init__(f"{message}{status}{location}")


class AuthenticationError(APIError):
    """Credentials or token were rejected."""


class AuthorizationError(APIError):
    """The session is authenticated but lacks permission."""


class NotFoundError(APIError):
    """The requested resource was not found."""


class ValidationError(APIError):
    """The server rejected request data or a response could not be decoded."""


class RateLimitError(APIError):
    """The server rate-limited the request."""
