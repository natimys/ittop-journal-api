"""Logical resource groups for the Journal API."""

from __future__ import annotations

from datetime import date
from typing import Any

from .models import (
    AuthToken,
    EvaluationLesson,
    Feedback,
    MetricPoint,
    RatingEntry,
    ScheduleLesson,
    UserInfo,
    VisitRecord,
    parse_many,
    parse_one,
)
from .transport import JournalTransport


class Resource:
    def __init__(self, transport: JournalTransport) -> None:
        self._transport = transport


class AuthResource(Resource):
    async def login(self, username: str, password: str, application_key: str) -> AuthToken:
        """Exchange credentials and the frontend application key for a bearer token."""
        payload = await self._transport.request(
            "POST",
            "/auth/login",
            json={"username": username, "password": password, "application_key": application_key},
        )
        token = parse_one(AuthToken, payload)
        self._transport.token = token.access_token
        return token  # type: ignore[return-value]


class UserResource(Resource):
    async def get_info(self) -> UserInfo:
        """Return the authenticated student's profile/group information."""
        return parse_one(
            UserInfo,
            await self._transport.request("GET", "/settings/user-info"),
        )  # type: ignore[return-value]


class ScheduleResource(Resource):
    async def get_by_date(self, date_filter: date | str) -> list[ScheduleLesson]:
        """Return lessons for one calendar date."""
        value = date_filter.isoformat() if isinstance(date_filter, date) else date_filter
        return parse_many(
            ScheduleLesson,
            await self._transport.request(
                "GET", "/schedule/operations/get-by-date", params={"date_filter": value}
            ),
        )  # type: ignore[return-value]


class GradesResource(Resource):
    async def student_visits(self) -> list[VisitRecord]:
        """Return the attendance/grade ledger shown by the grades page."""
        return parse_many(
            VisitRecord,
            await self._transport.request("GET", "/progress/operations/student-visits"),
        )  # type: ignore[return-value]

    async def average_progress(self) -> list[MetricPoint]:
        """Return monthly average-grade chart data."""
        return parse_many(
            MetricPoint,
            await self._transport.request("GET", "/dashboard/chart/average-progress"),
        )  # type: ignore[return-value]


class AttendanceResource(Resource):
    async def chart(self) -> list[MetricPoint]:
        """Return attendance chart data."""
        return parse_many(
            MetricPoint,
            await self._transport.request("GET", "/dashboard/chart/attendance"),
        )  # type: ignore[return-value]


class FeedbackResource(Resource):
    async def list(self) -> list[Feedback]:
        """Return teacher feedback/reviews shown on the feedback page."""
        return parse_many(
            Feedback,
            await self._transport.request("GET", "/reviews/index/list"),
        )  # type: ignore[return-value]

    async def evaluation_lessons(self) -> list[EvaluationLesson]:
        """Return lessons that can be evaluated by the student."""
        return parse_many(
            EvaluationLesson,
            await self._transport.request("GET", "/feedback/students/evaluate-lesson-list"),
        )  # type: ignore[return-value]

    async def evaluate_lesson(self, payload: dict[str, Any]) -> Any:
        """Submit a lesson evaluation; this mutates server state."""
        return await self._transport.request(
            "POST", "/feedback/students/evaluate-lesson", json=payload
        )


class RatingsResource(Resource):
    async def group(self) -> list[RatingEntry]:
        """Return the group leaderboard."""
        return parse_many(
            RatingEntry,
            await self._transport.request("GET", "/dashboard/progress/leader-group"),
        )  # type: ignore[return-value]

    async def stream(self) -> list[RatingEntry]:
        """Return the stream leaderboard."""
        return parse_many(
            RatingEntry,
            await self._transport.request("GET", "/dashboard/progress/leader-stream"),
        )  # type: ignore[return-value]


class RawResource(Resource):
    async def get(self, path: str, **kwargs: Any) -> Any:
        """Call a manually verified path while its schema is still documented."""
        return await self._transport.request("GET", path, **kwargs)
