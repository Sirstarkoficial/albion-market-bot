
KingdomLuxuriuos v3 - Discord Market Bot + FastAPI dashboard (FastAPI)

INSTRUCCIONES BÁSICAS
1) Copia .env.example -> .env y completa DISCORD_TOKEN y CLIENT_ID (y GUILD_ID opcional)
2) Instala dependencias: pip install -r requirements.txt
3) Ejecuta local: python bot.py
4) Para Railway, sube repo y en Environment variables añade DISCORD_TOKEN y CLIENT_ID. Railway ejecutará Procfile.

Estructura:
- bot.py         -> inicia bot de Discord y arranca servidor FastAPI en background
- api/           -> FastAPI app (app.py)
- db/            -> sqlite DB file (created at runtime)
- commands/      -> discord command handlers
- utils/         -> helpers: albion API fetcher, db helper
- requirements.txt
- Procfile
