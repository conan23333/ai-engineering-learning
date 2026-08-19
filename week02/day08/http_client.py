import httpx


async def get_json(
    client: httpx.AsyncClient,
    url: str,
) -> dict[str, object]:
    response = await client.get(url)
    response.raise_for_status()
    return response.json()
