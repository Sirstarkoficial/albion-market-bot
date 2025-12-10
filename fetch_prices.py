
import aiohttp
import asyncio

ALBION_API = "https://www.albion-online-data.com/api/v2/stats/prices/"

async def fetch_prices(item, cities=None):
    try:
        params = ""
        if cities:
            params = "?locations=" + ",".join(cities)
        url = ALBION_API + item + params
        async with aiohttp.ClientSession() as s:
            async with s.get(url, timeout=10) as r:
                if r.status == 200:
                    return await r.json()
                return []
    except Exception:
        return []
