import telegraph as _telegraph
import aiohttp as _aiohttp
import io


__telegraph: _telegraph.Telegraph = _telegraph.Telegraph()


async def upload(files: io.BytesIO | str | list[io.BytesIO | str]) -> None | str | list[str]:
    """
    Upload media to telegra.ph
    :param files:
    :return:
    """
    sources: list = await __telegraph.upload_file(f=files)
    urls = [f"https://telegra.ph{source.get('src')}" for source in sources]
    if len(urls) == 1:
        return urls[0]
    if len(urls) > 1:
        return urls
    return None


async def download(url: str) -> bytes | None:
    """
    Download media from any source
    :param url:
    :return:
    """
    async with _aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
    return None
