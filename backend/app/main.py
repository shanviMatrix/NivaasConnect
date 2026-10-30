from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.pool import create_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = create_db_pool()
    await pool.open()
    app.state.db_pool = pool

    try:
        yield
    finally:
        await pool.close()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {
        "application": settings.app_name,
        "status": "running",
        "version": "0.1.0",
    }
