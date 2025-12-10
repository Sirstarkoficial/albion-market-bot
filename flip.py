
from discord import app_commands
from utils.fetch_prices import fetch_prices
from utils.db import save_query

cities = ["Bridgewatch","Martlock","Lymhurst","FortSterling","Thetford","Caerleon"]

@app_commands.command(name="flip", description="Busca mejor flip para un item")
async def flip(interaction, item: str):
    await interaction.response.defer()
    data = await fetch_prices(item, cities)
    if not data:
        await interaction.followup.send("No hay datos.")
        await save_query(item, "flip", "no_data")
        return
    # find cheapest sell and most expensive sell
    buy = min([d for d in data if d.get("sell_price_min")], key=lambda x: x["sell_price_min"])
    sell = max([d for d in data if d.get("sell_price_min")], key=lambda x: x["sell_price_min"])
    if buy["city"] == sell["city"]:
        await interaction.followup.send("No hay flip entre diferentes ciudades.")
        await save_query(item, "flip", "no_flip")
        return
    profit = sell["sell_price_min"] - buy["sell_price_min"]
    text = f"Compra en **{buy['city']}** a {buy['sell_price_min']} - Vende en **{sell['city']}** a {sell['sell_price_min']}\nGanancia: {profit}"
    await interaction.followup.send(text)
    await save_query(item, "flip", f"profit:{profit}")
