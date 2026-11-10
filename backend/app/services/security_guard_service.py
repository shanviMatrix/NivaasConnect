from psycopg.rows import dict_row


async def get_security_guards(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT guard_id, full_name, phone, shift_name,
                       is_active, created_at
                FROM security_guards
                ORDER BY guard_id
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_security_guard(pool, guard_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT guard_id, full_name, phone, shift_name,
                       is_active, created_at
                FROM security_guards
                WHERE guard_id = %s
                """,
                (guard_id,),
            )
            return await cursor.fetchone()


async def create_security_guard(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO security_guards
                    (full_name, phone, shift_name, is_active)
                VALUES (%s, %s, %s, %s)
                RETURNING guard_id, full_name, phone, shift_name,
                          is_active, created_at
                """,
                (
                    data["full_name"],
                    data["phone"],
                    data["shift_name"],
                    data["is_active"],
                ),
            )
            return await cursor.fetchone()


async def update_security_guard(pool, guard_id: int, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                UPDATE security_guards
                SET full_name = %s,
                    phone = %s,
                    shift_name = %s,
                    is_active = %s
                WHERE guard_id = %s
                RETURNING guard_id, full_name, phone, shift_name,
                          is_active, created_at
                """,
                (
                    data["full_name"],
                    data["phone"],
                    data["shift_name"],
                    data["is_active"],
                    guard_id,
                ),
            )
            return await cursor.fetchone()


async def delete_security_guard(pool, guard_id: int):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM security_guards
                WHERE guard_id = %s
                RETURNING guard_id
                """,
                (guard_id,),
            )
            return await cursor.fetchone()
