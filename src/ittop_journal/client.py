"""Public client facade."""

from __future__ import annotations

from collections.abc import Mapping

import httpx

from .resources import (
    AttendanceResource,
    AuthResource,
    FeedbackResource,
    GradesResource,
    RatingsResource,
    RawResource,
    ScheduleResource,
    UserResource,
)
from .transport import JournalTransport


class JournalClient:
    """Async client for the confirmed IT TOP Journal API surface."""

    BASE_URL = "https://msapi.top-academy.ru/api/v2"

    def __init__(
        self,
        *,
        token: str | None = None,
        cookies: Mapping[str, str] | httpx.Cookies | None = None,
        base_url: str = BASE_URL,
        timeout: float | httpx.Timeout = 20.0,
        headers: Mapping[str, str] | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._transport = JournalTransport(
            base_url=base_url,
            token=token,
            cookies=cookies,
            timeout=timeout,
            headers=headers,
            client=http_client,
        )
        self.auth = AuthResource(self._transport)
        self.user = UserResource(self._transport)
        self.schedule = ScheduleResource(self._transport)
        self.grades = GradesResource(self._transport)
        self.progress = self.grades
        self.attendance = AttendanceResource(self._transport)
        self.feedback = FeedbackResource(self._transport)
        self.ratings = RatingsResource(self._transport)
        self.raw = RawResource(self._transport)

    @property
    def token(self) -> str | None:
        """Current in-memory bearer token, if supplied or obtained."""
        return self._transport.token

    async def __aenter__(self) -> JournalClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._transport.aclose()
