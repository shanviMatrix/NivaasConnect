from psycopg_pool import AsyncConnectionPool

from app.core.config import settings


def create_db_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(
        conninfo=settings.database_conninfo,
        min_size=1,
        max_size=5,
        open=False,
    )
