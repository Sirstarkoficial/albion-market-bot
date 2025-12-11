from discord import app_commands, Interaction
from utils.fetch import fetch_prices
from utils.db import save_query

@app_commands.command(name="flip", description="Busca flip entre ciudades")
async def flip(interaction: Interaction, item: str):
    await interaction.response.defer()
    cities = ["Bridgewatch","Martlock","Lymhurst","FortSterling"]
    data = await fetch_prices(item, cities)
    if not data:
        await interaction.followup.send("No hay datos.")
        await save_query(item,"flip","no_data")
        return
    buy = min(data, key=lambda x: x.get("sell_price_min", 99999999))
    sell = max(data, key=lambda x: x.get("sell_price_min", 0))
    profit = (sell.get("sell_price_min") or 0) - (buy.get("sell_price_min") or 0)
    txt = f"Compra en {buy['city']} a {buy.get('sell_price_min')} | Vende en {sell['city']} a {sell.get('sell_price_min')} | Ganancia {profit}"
    await interaction.followup.send(txt)
    await save_query(item,"flip",txt)
