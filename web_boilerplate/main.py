from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db_session, engine, Base
from .api import users  # Import the router
from .api import stats


app = FastAPI(title="Web Boilerplate")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(stats.router)


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


@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


