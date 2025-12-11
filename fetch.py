import aiohttp

ALBION_API = "https://www.albion-online-data.com/api/v2/stats/prices/"

async def fetch_prices(item: str, cities: list | None = None):
    params = ""
    if cities:
        params = "?locations=" + ",".join(cities)
    url = ALBION_API + item + params
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as r:
                if r.status == 200:
                    return await r.json()
                return []
    except Exception:
        return []
