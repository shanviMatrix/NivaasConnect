from psycopg.rows import dict_row


async def get_apartments(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT apartment_id, building_name, flat_number, floor_number
                FROM apartments
                ORDER BY apartment_id
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_apartment(pool, apartment_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT apartment_id, building_name, flat_number, floor_number
                FROM apartments
                WHERE apartment_id = %s
                """,
                (apartment_id,),
            )
            return await cursor.fetchone()


async def create_apartment(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO apartments (building_name, flat_number, floor_number)
                VALUES (%s, %s, %s)
                RETURNING apartment_id, building_name, flat_number, floor_number
                """,
                (
                    data["building_name"],
                    data["flat_number"],
                    data["floor_number"],
                ),
            )
            return await cursor.fetchone()


async def update_apartment(pool, apartment_id: int, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE apartments
                SET building_name = %s,
                    flat_number = %s,
                    floor_number = %s
                WHERE apartment_id = %s
                RETURNING apartment_id, building_name, flat_number, floor_number
                """,
                (
                    data["building_name"],
                    data["flat_number"],
                    data["floor_number"],
                    apartment_id,
                ),
            )
            return await cursor.fetchone()


async def delete_apartment(pool, apartment_id: int):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM apartments
                WHERE apartment_id = %s
                RETURNING apartment_id
                """,
                (apartment_id,),
            )
            return await cursor.fetchone()
