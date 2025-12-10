
import os
import asyncio
import logging
from discord import Intents
from discord.ext import commands
from discord import app_commands
from api import app as fastapi_app
import uvicorn
from utils.db import init_db

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")  # optional, for quick command registration
CLIENT_ID = os.getenv("CLIENT_ID")

if not TOKEN or not CLIENT_ID:
    print("Please set DISCORD_TOKEN and CLIENT_ID in environment.")
    raise SystemExit(1)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands
@bot.event
async def on_ready():
    print(f"Bot ready: {bot.user} (id: {bot.user.id})")
    try:
        await init_db()
    except Exception as e:
        print("DB init error", e)

async def start_api():
    config = uvicorn.Config(fastapi_app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)), log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # start API server in background
    api_task = asyncio.create_task(start_api())
    # register command tree from commands folder
    # dynamic import
    import importlib.util, pathlib
    cmd_dir = pathlib.Path('commands')
    for p in cmd_dir.glob('*.py'):
        spec = importlib.util.spec_from_file_location(p.stem, str(p))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # register app commands found in module
        for obj in mod.__dict__.values():
            if hasattr(obj, '__call__') and getattr(obj, '__name__','').lower() in ('precio','flip'):
                try:
                    bot.tree.add_command(obj, guild=None if not GUILD_ID else app_commands.Object(id=int(GUILD_ID), type=1))
                except Exception:
                    # fallback: add as app command directly
                    try:
                        bot.tree.add_command(obj)
                    except Exception as e:
                        print("add_command error", e)
    await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
