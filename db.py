
import aiosqlite
DB_PATH = "db/data.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            command TEXT,
            result TEXT,
            ts DATETIME DEFAULT (datetime('now','localtime'))
        )
        ''')
        await db.commit()

async def save_query(item, command, result):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('INSERT INTO queries (item,command,result) VALUES (?,?,?)', (item,command,result))
        await db.commit()

async def last_queries(limit=20):
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute('SELECT id,item,command,result,ts FROM queries ORDER BY id DESC LIMIT ?', (limit,))
        rows = await cur.fetchall()
        return rows
