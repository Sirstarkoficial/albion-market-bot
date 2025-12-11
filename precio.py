from discord import app_commands, Interaction
from utils.fetch import fetch_prices
from utils.db import save_query

@app_commands.command(name="precio", description="Busca precio de un item")
async def precio(interaction: Interaction, item: str):
    await interaction.response.defer()
    data = await fetch_prices(item, cities=["Bridgewatch","Martlock","Lymhurst"])
    if not data:
        await interaction.followup.send("No hay datos.")
        await save_query(item,"precio","no_data")
        return
    d = data[0]
    txt = f"Item: {item}\nSell min: {d.get('sell_price_min')} | Buy min: {d.get('buy_price_min')}"
    await interaction.followup.send(txt)
    await save_query(item,"precio",txt)
