import psycopg
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from psycopg_pool import PoolTimeout

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(request: Request):
    pool = request.app.state.db_pool

    try:
        async with pool.connection(timeout=3) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT 1")
                await cursor.fetchone()

        return {
            "status": "ok",
            "database": "connected",
        }

    except (psycopg.Error, PoolTimeout):
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "database": "unavailable",
            },
        )
