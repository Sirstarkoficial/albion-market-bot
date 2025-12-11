import aiosqlite
import os

DB_PATH = "db/data.db"

async def init_db():
    os.makedirs("db", exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT,
                precio INT,
                fecha TEXT
            )
        """)
        await db.commit()
