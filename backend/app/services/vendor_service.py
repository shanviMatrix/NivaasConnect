from psycopg.rows import dict_row


async def get_vendors(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT vendor_id, vendor_name, service_category,
                       phone, email, is_active, created_at
                FROM vendors
                ORDER BY vendor_id
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_vendor(pool, vendor_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT vendor_id, vendor_name, service_category,
                       phone, email, is_active, created_at
                FROM vendors
                WHERE vendor_id = %s
                """,
                (vendor_id,),
            )
            return await cursor.fetchone()


async def create_vendor(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO vendors
                    (vendor_name, service_category, phone, email, is_active)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING vendor_id, vendor_name, service_category,
                          phone, email, is_active, created_at
                """,
                (
                    data["vendor_name"],
                    data["service_category"],
                    data["phone"],
                    data["email"],
                    data["is_active"],
                ),
            )
            return await cursor.fetchone()


async def update_vendor(pool, vendor_id: int, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE vendors
                SET vendor_name = %s,
                    service_category = %s,
                    phone = %s,
                    email = %s,
                    is_active = %s
                WHERE vendor_id = %s
                RETURNING vendor_id, vendor_name, service_category,
                          phone, email, is_active, created_at
                """,
                (
                    data["vendor_name"],
                    data["service_category"],
                    data["phone"],
                    data["email"],
                    data["is_active"],
                    vendor_id,
                ),
            )
            return await cursor.fetchone()


async def delete_vendor(pool, vendor_id: int):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM vendors
                WHERE vendor_id = %s
                RETURNING vendor_id
                """,
                (vendor_id,),
            )
            return await cursor.fetchone()
