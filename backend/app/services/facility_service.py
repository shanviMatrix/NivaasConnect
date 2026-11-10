from psycopg.rows import dict_row


FACILITY_COLUMNS = """
    facility_id, facility_name, location_description,
    capacity, booking_fee, is_active
"""


async def get_facilities(pool, limit: int, offset: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"""
                SELECT {FACILITY_COLUMNS}
                FROM facilities
                ORDER BY facility_name
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cur.fetchall()


async def get_facility(pool, facility_id: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"SELECT {FACILITY_COLUMNS} FROM facilities WHERE facility_id = %s",
                (facility_id,),
            )
            return await cur.fetchone()


async def create_facility(pool, data: dict):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                INSERT INTO facilities
                    (facility_name, location_description, capacity, booking_fee, is_active)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING facility_id
                """,
                (
                    data["facility_name"],
                    data["location_description"],
                    data["capacity"],
                    data["booking_fee"],
                    data["is_active"],
                ),
            )
            facility_id = (await cur.fetchone())["facility_id"]

    return await get_facility(pool, facility_id)


async def update_facility(pool, facility_id: int, data: dict):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE facilities
                SET facility_name = %s,
                    location_description = %s,
                    capacity = %s,
                    booking_fee = %s,
                    is_active = %s
                WHERE facility_id = %s
                RETURNING facility_id
                """,
                (
                    data["facility_name"],
                    data["location_description"],
                    data["capacity"],
                    data["booking_fee"],
                    data["is_active"],
                    facility_id,
                ),
            )
            result = await cur.fetchone()

    if result is None:
        return None

    return await get_facility(pool, facility_id)


async def delete_facility(pool, facility_id: int):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM facilities
                WHERE facility_id = %s
                RETURNING facility_id
                """,
                (facility_id,),
            )
            return await cur.fetchone()
