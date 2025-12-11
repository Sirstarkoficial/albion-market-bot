import os
import asyncio
import logging
from discord import Intents
from discord.ext import commands
from discord import app_commands
import uvicorn

# FastAPI: API para precios de Albion
from fastapi import FastAPI
from api.routes import router as market_router  # <-- ESTA RUTA ES LA CORRECTA

# Base de datos (si la usas)
from utils.db import init_db


# ----------------------------------
# CONFIGURACIÓN
# ----------------------------------
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN or not CLIENT_ID:
    print("Faltan variables: DISCORD_TOKEN o CLIENT_ID")
    raise SystemExit(1)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------
# FASTAPI (API pública de precios)
# ----------------------------------
app = FastAPI()
app.include_router(market_router)


# ----------------------------------
# BOT READY
# ----------------------------------
@bot.event
async def on_ready():
    print(f"✅ Bot online como: {bot.user}")
    await init_db()
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print("Error al sincronizar comandos:", e)


# ----------------------------------
# API SERVER (se ejecuta en paralelo)
# ----------------------------------
async def start_api():
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


# ----------------------------------
# MAIN (bot + API)
# ----------------------------------
async def main():
    api_task = asyncio.create_task(start_api())
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())