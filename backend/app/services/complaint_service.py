from psycopg.rows import dict_row


COMPLAINT_COLUMNS = """
    complaint_id, resident_id, vendor_id, title, description,
    category, priority, complaint_status, created_at, resolved_at
"""



async def get_complaints(pool, limit: int, offset: int, resident_id: int | None = None):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            query = f"SELECT {COMPLAINT_COLUMNS} FROM complaints"
            params = []
            if resident_id is not None:
                query += " WHERE resident_id = %s"
                params.append(resident_id)
            query += " ORDER BY created_at DESC, complaint_id DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            await cursor.execute(query, params)
            return await cursor.fetchall()

async def get_complaint(pool, complaint_id: int, resident_id: int | None = None):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            query = f"SELECT {COMPLAINT_COLUMNS} FROM complaints WHERE complaint_id = %s"
            params = [complaint_id]
            if resident_id is not None:
                query += " AND resident_id = %s"
                params.append(resident_id)
            await cursor.execute(query, params)
            return await cursor.fetchone()
async def create_complaint(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO complaints
                    (resident_id, vendor_id, title, description,
                     category, priority)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING complaint_id
                """,
                (
                    data["resident_id"],
                    data["vendor_id"],
                    data["title"],
                    data["description"],
                    data["category"],
                    data["priority"],
                ),
            )
            complaint_id = (await cursor.fetchone())["complaint_id"]

    return await get_complaint(pool, complaint_id)



async def update_complaint(
    pool, complaint_id: int, data: dict, resident_id: int | None = None
):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            query = """
                UPDATE complaints
                SET vendor_id = %s,
                    title = %s,
                    description = %s,
                    category = %s,
                    priority = %s,
                    complaint_status = %s,
                    resolved_at = CASE
                        WHEN %s IN ('Resolved', 'Closed')
                            THEN COALESCE(resolved_at, CURRENT_TIMESTAMP)
                        ELSE NULL
                    END
                WHERE complaint_id = %s
            """
            params = [
                data["vendor_id"], data["title"], data["description"],
                data["category"], data["priority"], data["complaint_status"],
                data["complaint_status"], complaint_id,
            ]
            if resident_id is not None:
                query += " AND resident_id = %s"
                params.append(resident_id)
            query += " RETURNING complaint_id"
            await cursor.execute(query, params)
            result = await cursor.fetchone()

    if result is None:
        return None
    return await get_complaint(pool, complaint_id, resident_id)

async def delete_complaint(pool, complaint_id: int, resident_id: int | None = None):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            query = "DELETE FROM complaints WHERE complaint_id = %s"
            params = [complaint_id]
            if resident_id is not None:
                query += " AND resident_id = %s"
                params.append(resident_id)
            query += " RETURNING complaint_id"
            await cursor.execute(query, params)
            return await cursor.fetchone()
