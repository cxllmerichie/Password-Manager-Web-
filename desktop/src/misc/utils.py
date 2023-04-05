from typing import Any
import aiohttp


async def request(url: str, method: str, headers: dict[str, Any], data: dict[str, Any]) -> dict[str, Any] | None:
    assert method.lower() in ('get', 'post', 'put', 'delete')
    async with aiohttp.ClientSession() as session:
        async with getattr(session, method.lower())(url=url, headers=headers, data=data) as response:
            return await response.json()
