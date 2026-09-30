# Reverse-engineering report

Research date: 2026-09-24.

## Frontend

The site is an Angular application (`ng-version="7.2.16"`) with lazy-loaded bundles including
`main`, `dashboard`, `auth`, and `schedule`. The login HTML is served from
`journal.top-academy.ru/ru/auth/login/index`; post-login pages use client-side routes under
`/ru/main/.../page/index`.

## Hosts

- `journal.top-academy.ru` — web application and route shell.
- `msapi.top-academy.ru` — API origin used by the confirmed API catalog.
- `fs.top-academy.ru` — file service URLs embedded in rendered pages, including `/api/v1/files/{id}`.
- Roistat, Yandex, Google, and Amplitude — telemetry only, not Journal data APIs.

## Authentication

The login page contains a GET form action at `/ru/auth/login/index` with `username` and `password`.
After the user's normal browser login, the application redirects to the dashboard. The API login
contract independently observed in a public prior client is `POST /api/v2/auth/login` with JSON
`{username, password, application_key}` and a bearer-token response. The current session was used
only through the user's existing browser login; no credentials, cookies, or token values were read
or stored.

The current evidence does not prove refresh-token rotation, silent refresh, logout invalidation,
CSRF behavior, or token expiry. The SDK therefore does not claim automatic refresh.

## Pages investigated

Dashboard; schedule (month/day controls); grades/progress (filters, ledger, chart, control forms);
homework; library/materials; announcements; rewards; teacher feedback; payments; personal
cabinet/settings; FAQ; contacts; signals/requests; complaints; marketplace.

The schedule day view rendered lessons with time, subject, room, and teacher. The grades page
rendered the account's ledger, filters, chart, and control-form table. Account-specific values are
not stored in fixtures.

## Limitations and unresolved questions

The in-app browser exposed DOM and navigation state but not a raw Network/Fetch/XHR event stream or
bundle contents. Direct requests without the browser's bearer token returned `403 Forbidden` from
nginx. Consequently, request/response schemas for homework, library, news, rewards, payments,
settings updates, signal submission, complaints, and marketplace operations remain unconfirmed.
The same applies to WebSocket/SSE usage and refresh/logout mechanics.

The public prior client was used as a lead for route names and the auth payload; uncertain response
fields remain `extra="allow"` in Pydantic models and unconfirmed UI areas are explicitly marked
unresolved.
