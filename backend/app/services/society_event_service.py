from psycopg.rows import dict_row


EVENT_COLUMNS = """
    event_id, event_title, description, venue, start_time,
    end_time, created_by, event_status, created_at
"""


async def get_events(pool, limit: int, offset: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"""
                SELECT {EVENT_COLUMNS}
                FROM society_events
                ORDER BY start_time DESC, event_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cur.fetchall()


async def get_event(pool, event_id: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"SELECT {EVENT_COLUMNS} FROM society_events WHERE event_id = %s",
                (event_id,),
            )
            return await cur.fetchone()


async def create_event(pool, data: dict):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                INSERT INTO society_events
                    (event_title, description, venue, start_time, end_time, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING event_id
                """,
                (
                    data["event_title"],
                    data["description"],
                    data["venue"],
                    data["start_time"],
                    data["end_time"],
                    data["created_by"],
                ),
            )
            event_id = (await cur.fetchone())["event_id"]

    return await get_event(pool, event_id)


async def update_event(pool, event_id: int, data: dict):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE society_events
                SET event_title = %s,
                    description = %s,
                    venue = %s,
                    start_time = %s,
                    end_time = %s,
                    created_by = %s,
                    event_status = %s
                WHERE event_id = %s
                RETURNING event_id
                """,
                (
                    data["event_title"],
                    data["description"],
                    data["venue"],
                    data["start_time"],
                    data["end_time"],
                    data["created_by"],
                    data["event_status"],
                    event_id,
                ),
            )
            result = await cur.fetchone()

    if result is None:
        return None

    return await get_event(pool, event_id)


async def delete_event(pool, event_id: int):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM society_events
                WHERE event_id = %s
                RETURNING event_id
                """,
                (event_id,),
            )
            return await cur.fetchone()
