
from discord import app_commands
from utils.fetch_prices import fetch_prices
from utils.db import save_query
cities = ["Bridgewatch","Martlock","Lymhurst","FortSterling","Thetford","Caerleon"]

class Precio(app_commands.Group):
    pass

@Precio.command(name="item", description="Consulta precios de Albion Online (ej: T5_BAG)")
async def precio(interaction, item: str):
    await interaction.response.defer()
    data = await fetch_prices(item, cities)
    if not data:
        await interaction.followup.send("No encontré datos para ese item.")
        await save_query(item, "precio", "no_data")
        return
    text = f"Precios para **{item}**:\n"
    for d in data[:10]:
        text += f"🏙 **{d.get('city','?')}** - Buy: {d.get('buy_price_max')} / Sell: {d.get('sell_price_min')}\n"
    await interaction.followup.send(text)
    await save_query(item, "precio", "ok")
