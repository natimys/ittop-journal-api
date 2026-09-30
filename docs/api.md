# Implemented API catalog

Base URL:

```text
https://msapi.top-academy.ru/api/v2
```

All data routes below require the authenticated bearer token unless the server changes that policy.
The request body and response envelope are intentionally not guessed where raw XHR responses could
not be exposed by the browser tooling.

| Method | Path | SDK |
|---|---|---|
| POST | `/auth/login` | `client.auth.login()` |
| GET | `/schedule/operations/get-by-date?date_filter=YYYY-MM-DD` | `client.schedule.get_by_date()` |
| GET | `/settings/user-info` | `client.user.get_info()` |
| GET | `/progress/operations/student-visits` | `client.grades.student_visits()` |
| GET | `/dashboard/chart/average-progress` | `client.grades.average_progress()` |
| GET | `/dashboard/chart/attendance` | `client.attendance.chart()` |
| GET | `/reviews/index/list` | `client.feedback.list()` |
| GET | `/feedback/students/evaluate-lesson-list` | `client.feedback.evaluation_lessons()` |
| POST | `/feedback/students/evaluate-lesson` | `client.feedback.evaluate_lesson()` |
| GET | `/dashboard/progress/leader-group` | `client.ratings.group()` |
| GET | `/dashboard/progress/leader-stream` | `client.ratings.stream()` |

## Authentication

The login page contains `username` and `password` fields. The separate API flow observed in the
frontend ecosystem uses JSON `{username, password, application_key}` at `/auth/login`, returning an
`access_token` and `token_type`. The SDK supports that flow but does not hard-code an application
key.

## Not yet confirmed

The UI exposes homework, library/materials, announcements, rewards, payments, profile documents,
signals, complaints, and marketplace pages. Their exact API paths, payloads, and schemas were not
safely recoverable from the available browser network surface, so they are not represented by fake
routes.
