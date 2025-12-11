import os, asyncio, logging, importlib.util, pathlib
from discord import Intents, app_commands
from discord.ext import commands

import uvicorn
from api import app as fastapi_app
from utils.db import init_db

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
GUILD_ID = os.getenv("GUILD_ID")

if not TOKEN or not CLIENT_ID:
    raise SystemExit("Faltan variables DISCORD_TOKEN o CLIENT_ID")

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot listo", bot.user)
    await init_db()
    if GUILD_ID:
        await bot.tree.sync(guild=app_commands.Object(id=int(GUILD_ID)))
    else:
        await bot.tree.sync()
    print("Comandos sincronizados")

async def start_api():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=int(os.getenv("PORT",8000)), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def load_commands():
    cmd_dir = pathlib.Path("commands")
    for p in cmd_dir.glob("*.py"):
        spec = importlib.util.spec_from_file_location(p.stem, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for obj in mod.__dict__.values():
            if isinstance(obj, app_commands.Command):
                bot.tree.add_command(obj)

async def main():
    await load_commands()
    asyncio.create_task(start_api())
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
