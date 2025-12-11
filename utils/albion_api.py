import aiohttp

API_URL = "https://www.albion-online-data.com/api/v2/stats/prices/{}"

async def obtener_precios_item(item_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL.format(item_id)) as resp:
            return await resp.json()
