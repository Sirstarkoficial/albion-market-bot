
from fastapi import FastAPI
from utils.db import last_queries, init_db
app = FastAPI(title="KingdomLuxuriuos API")

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/last_queries")
async def get_last(q: int = 20):
    rows = await last_queries(limit=q)
    return [{"id":r[0],"item":r[1],"command":r[2],"result":r[3],"ts":r[4]} for r in rows]
