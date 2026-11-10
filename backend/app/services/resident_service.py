from psycopg.rows import dict_row


async def get_residents(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT
                    r.resident_id,
                    r.full_name,
                    r.email,
                    r.phone,
                    r.apartment_id,
                    a.building_name,
                    a.flat_number
                FROM residents AS r
                JOIN apartments AS a
                    ON r.apartment_id = a.apartment_id
                ORDER BY r.resident_id
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_resident(pool, resident_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT
                    r.resident_id,
                    r.full_name,
                    r.email,
                    r.phone,
                    r.apartment_id,
                    a.building_name,
                    a.flat_number
                FROM residents AS r
                JOIN apartments AS a
                    ON r.apartment_id = a.apartment_id
                WHERE r.resident_id = %s
                """,
                (resident_id,),
            )
            return await cursor.fetchone()


async def create_resident(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO residents (full_name, email, phone, apartment_id)
                VALUES (%s, %s, %s, %s)
                RETURNING resident_id, full_name, email, phone, apartment_id
                """,
                (
                    data["full_name"],
                    data["email"],
                    data["phone"],
                    data["apartment_id"],
                ),
            )
            return await cursor.fetchone()


async def update_resident(pool, resident_id: int, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE residents
                SET full_name = %s,
                    email = %s,
                    phone = %s,
                    apartment_id = %s
                WHERE resident_id = %s
                RETURNING resident_id, full_name, email, phone, apartment_id
                """,
                (
                    data["full_name"],
                    data["email"],
                    data["phone"],
                    data["apartment_id"],
                    resident_id,
                ),
            )
            return await cursor.fetchone()


async def delete_resident(pool, resident_id: int):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM residents
                WHERE resident_id = %s
                RETURNING resident_id
                """,
                (resident_id,),
            )
            return await cursor.fetchone()
