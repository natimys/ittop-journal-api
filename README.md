# ittop-journal-api

Async, typed Python client for the documented API surface behind `journal.top-academy.ru`.

## Status

The SDK targets `https://msapi.top-academy.ru/api/v2`, the backend origin identified during
frontend and public-client research. It deliberately does not invent endpoints for UI sections
whose exact network contract could not be captured safely.

## Install

```bash
uv add ittop-journal-api
```

For local development:

```bash
uv sync --extra dev
```

## Quick start

```python
from datetime import date
from ittop_journal import JournalClient

async with JournalClient(token="your-token") as journal:
    profile = await journal.user.get_info()
    lessons = await journal.schedule.get_by_date(date.today())
    visits = await journal.grades.student_visits()
```

The token is kept in memory only. The login flow is explicit:

```python
async with JournalClient() as journal:
    token = await journal.auth.login(
        username="...", password="...", application_key="..."
    )
```

Never commit credentials, tokens, cookies, or personal response fixtures.

## Resources and errors

Implemented resources are `auth`, `user`, `schedule`, `grades`/`progress`, `attendance`,
`feedback`, and `ratings`. HTTP failures map to typed exceptions such as `AuthenticationError`,
`AuthorizationError`, `NotFoundError`, `ValidationError`, and `RateLimitError`.

See [docs/api.md](docs/api.md) for the endpoint catalog and
[docs/reverse-engineering.md](docs/reverse-engineering.md) for evidence and limitations.
