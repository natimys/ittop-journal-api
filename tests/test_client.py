import httpx
import pytest
import respx

from ittop_journal import JournalClient


@pytest.mark.asyncio
@respx.mock
async def test_login_sets_in_memory_token() -> None:
    respx.post("https://msapi.top-academy.ru/api/v2/auth/login").mock(
        return_value=httpx.Response(200, json={"access_token": "abc", "token_type": "bearer"})
    )
    async with JournalClient() as client:
        token = await client.auth.login("user", "password", "application-key")
        assert token.access_token == "abc"
        assert client.token == "abc"


@pytest.mark.asyncio
@respx.mock
async def test_schedule_date_parameter() -> None:
    route = respx.get(
        "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date",
        params={"date_filter": "2026-09-24"},
    ).mock(return_value=httpx.Response(200, json=[{"subject": "Math"}]))
    async with JournalClient(token="t") as client:
        lessons = await client.schedule.get_by_date("2026-09-24")
    assert route.called
    assert lessons[0].subject == "Math"
