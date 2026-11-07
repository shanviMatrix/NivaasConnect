from psycopg.rows import dict_row


BOOKING_COLUMNS = """
    booking_id, facility_id, resident_id, start_time,
    end_time, booking_status, created_at
"""


async def get_bookings(pool, limit: int, offset: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"""
                SELECT {BOOKING_COLUMNS}
                FROM facility_bookings
                ORDER BY start_time DESC, booking_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cur.fetchall()


async def get_booking(pool, booking_id: int):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"SELECT {BOOKING_COLUMNS} FROM facility_bookings WHERE booking_id = %s",
                (booking_id,),
            )
            return await cur.fetchone()


async def create_booking(pool, data: dict):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Lock the facility row so simultaneous booking requests
            # cannot both pass the overlap check.
            await cur.execute(
                """
                SELECT facility_id, is_active
                FROM facilities
                WHERE facility_id = %s
                FOR UPDATE
                """,
                (data["facility_id"],),
            )
            facility = await cur.fetchone()

            if facility is None:
                return {"error": "facility_not_found"}

            if not facility["is_active"]:
                return {"error": "facility_inactive"}

            await cur.execute(
                """
                SELECT booking_id
                FROM facility_bookings
                WHERE facility_id = %s
                  AND booking_status IN ('Pending', 'Approved')
                  AND start_time < %s
                  AND end_time > %s
                LIMIT 1
                """,
                (
                    data["facility_id"],
                    data["end_time"],
                    data["start_time"],
                ),
            )

            if await cur.fetchone():
                return {"error": "booking_conflict"}

            await cur.execute(
                """
                INSERT INTO facility_bookings
                    (facility_id, resident_id, start_time, end_time)
                VALUES (%s, %s, %s, %s)
                RETURNING booking_id
                """,
                (
                    data["facility_id"],
                    data["resident_id"],
                    data["start_time"],
                    data["end_time"],
                ),
            )
            booking_id = (await cur.fetchone())["booking_id"]

    return await get_booking(pool, booking_id)


async def update_booking_status(pool, booking_id: int, booking_status: str):
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                UPDATE facility_bookings
                SET booking_status = %s
                WHERE booking_id = %s
                RETURNING booking_id
                """,
                (booking_status, booking_id),
            )
            result = await cur.fetchone()

    if result is None:
        return None

    return await get_booking(pool, booking_id)
