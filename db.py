import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH", "data.db")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                command TEXT,
                result TEXT,
                ts DATETIME DEFAULT (datetime('now','localtime'))
            );
        """)
        await db.commit()

async def save_query(item, command, result):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO queries(item,command,result) VALUES (?, ?, ?)", (item, command, result))
        await db.commit()
