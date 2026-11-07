from psycopg.rows import dict_row


VISITOR_COLUMNS = """
    visitor_id, resident_id, guard_id, visitor_name, visitor_phone,
    purpose, entry_time, exit_time, approval_status
"""


async def get_visitors(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                f"""
                SELECT {VISITOR_COLUMNS}
                FROM visitor_logs
                ORDER BY entry_time DESC, visitor_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_visitor(pool, visitor_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                f"""
                SELECT {VISITOR_COLUMNS}
                FROM visitor_logs
                WHERE visitor_id = %s
                """,
                (visitor_id,),
            )
            return await cursor.fetchone()


async def create_visitor(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO visitor_logs
                    (resident_id, guard_id, visitor_name,
                     visitor_phone, purpose)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING visitor_id
                """,
                (
                    data["resident_id"],
                    data["guard_id"],
                    data["visitor_name"],
                    data["visitor_phone"],
                    data["purpose"],
                ),
            )
            visitor_id = (await cursor.fetchone())["visitor_id"]

    return await get_visitor(pool, visitor_id)


async def update_visitor_approval(pool, visitor_id: int, approval_status: str):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE visitor_logs
                SET approval_status = %s
                WHERE visitor_id = %s
                  AND exit_time IS NULL
                RETURNING visitor_id
                """,
                (approval_status, visitor_id),
            )
            result = await cursor.fetchone()

    if result is None:
        return None

    return await get_visitor(pool, visitor_id)


async def checkout_visitor(pool, visitor_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE visitor_logs
                SET exit_time = CURRENT_TIMESTAMP
                WHERE visitor_id = %s
                  AND approval_status = 'Approved'
                  AND exit_time IS NULL
                RETURNING visitor_id
                """,
                (visitor_id,),
            )
            result = await cursor.fetchone()

    if result is None:
        return None

    return await get_visitor(pool, visitor_id)
