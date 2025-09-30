from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .db import get_db_session


app = FastAPI(title="Web Boilerplate")


@app.get("/")
async def read_root():
    return {"status": "ok"}

@app.get("/health/db")
async def db_health(session: AsyncSession = Depends(get_db_session)):
    try:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()
        return {"database": "ok", "result": value}
    except Exception as exc:
        return {"database": "error", "detail": str(exc)}



