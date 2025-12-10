import discord
from discord.ext import commands
from discord import app_commands
import requests

BASE_URL = "https://www.albion-online-data.com/api/v2/stats/prices"

class Profit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profit",
        description="Calcula la ganancia moviendo un item entre dos ciudades."
    )
    async def profit(self, interaction: discord.Interaction, item: str, ciudad1: str, ciudad2: str):
        
        await interaction.response.defer()

        url1 = f"{BASE_URL}/{item}.json?locations={ciudad1}"
        url2 = f"{BASE_URL}/{item}.json?locations={ciudad2}"

        r1 = requests.get(url1).json()
        r2 = requests.get(url2).json()

        if not r1 or not r2:
            await interaction.followup.send("❌ Item o ciudades no encontrados.")
            return

        sell1 = r1[0]["sell_price_min"]
        buy2  = r2[0]["buy_price_max"]

        profit = buy2 - sell1

        embed = discord.Embed(
            title=f"📈 Profit transporte {item}",
            color=discord.Color.green()
        )
        embed.add_field(name=ciudad1, value=f"Vender mínimo: {sell1}", inline=True)
        embed.add_field(name=ciudad2, value=f"Comprar máximo: {buy2}", inline=True)
        embed.add_field(name="Ganancia estimada", value=f"🔥 {profit} plata", inline=False)

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profit(bot))