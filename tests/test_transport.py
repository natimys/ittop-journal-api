import httpx
import pytest
import respx

from ittop_journal import AuthenticationError, JournalClient


@pytest.mark.asyncio
@respx.mock
async def test_transport_sends_bearer_and_decodes_json() -> None:
    route = respx.get("https://msapi.top-academy.ru/api/v2/settings/user-info").mock(
        return_value=httpx.Response(200, json={"id": 7, "group": "A"})
    )
    async with JournalClient(token="secret") as client:
        info = await client.user.get_info()
    assert route.called
    assert route.calls[0].request.headers["Authorization"] == "Bearer secret"
    assert info.id == 7
    assert info.group == "A"


@pytest.mark.asyncio
@respx.mock
async def test_401_is_mapped_without_echoing_token() -> None:
    respx.get("https://msapi.top-academy.ru/api/v2/settings/user-info").mock(
        return_value=httpx.Response(401, json={"error": "expired"})
    )
    async with JournalClient(token="do-not-echo") as client:
        with pytest.raises(AuthenticationError) as exc_info:
            await client.user.get_info()
    assert "do-not-echo" not in str(exc_info.value)
