import asyncio

import httpx

from http_client import get_json


def test_get_json_success() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://example.test/health"
        return httpx.Response(200, json={"status": "ok"})

    async def run_test() -> dict[str, object]:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            return await get_json(
                client,
                "https://example.test/health",
            )

    assert asyncio.run(run_test()) == {"status": "ok"}


def test_get_json_raises_for_http_error() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"message": "unavailable"})

    async def run_test() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport) as client:
            await get_json(client, "https://example.test/health")

    try:
        asyncio.run(run_test())
    except httpx.HTTPStatusError as error:
        assert error.response.status_code == 503
    else:
        raise AssertionError("503 response should raise HTTPStatusError")
