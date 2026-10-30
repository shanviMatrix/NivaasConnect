from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.db.connection import get_connection

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "NivaasConnect API"}


@router.get("/health/db")
def database_health_check():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()

        return {"status": "connected", "database": "PostgreSQL"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "disconnected", "database": "PostgreSQL"}
        )
