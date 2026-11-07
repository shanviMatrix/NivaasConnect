from psycopg.rows import dict_row


BILL_SELECT = """
    SELECT
        b.bill_id,
        b.apartment_id,
        b.billing_month,
        b.amount,
        b.due_date,
        b.bill_status,
        b.created_at,
        COALESCE(SUM(p.amount) FILTER (
            WHERE p.payment_status = 'Completed'
        ), 0) AS paid_amount,
        GREATEST(
            b.amount - COALESCE(SUM(p.amount) FILTER (
                WHERE p.payment_status = 'Completed'
            ), 0),
            0
        ) AS outstanding_amount
    FROM maintenance_bills b
    LEFT JOIN payments p ON p.bill_id = b.bill_id
"""


async def get_bills(pool, limit: int, offset: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                BILL_SELECT + """
                GROUP BY b.bill_id
                ORDER BY b.billing_month DESC, b.bill_id
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            return await cursor.fetchall()


async def get_bill(pool, bill_id: int):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                BILL_SELECT + """
                WHERE b.bill_id = %s
                GROUP BY b.bill_id
                """,
                (bill_id,),
            )
            return await cursor.fetchone()


async def create_bill(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                INSERT INTO maintenance_bills
                    (apartment_id, billing_month, amount, due_date)
                VALUES (%s, %s, %s, %s)
                RETURNING bill_id
                """,
                (
                    data["apartment_id"],
                    data["billing_month"],
                    data["amount"],
                    data["due_date"],
                ),
            )
            bill_id = (await cursor.fetchone())["bill_id"]

            await cursor.execute(
                """
                UPDATE maintenance_bills
                SET bill_status = CASE
                    WHEN due_date < CURRENT_DATE THEN 'Overdue'
                    ELSE 'Unpaid'
                END
                WHERE bill_id = %s
                """,
                (bill_id,),
            )

    return await get_bill(pool, bill_id)


async def update_bill(pool, bill_id: int, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                """
                SELECT amount
                FROM maintenance_bills
                WHERE bill_id = %s
                FOR UPDATE
                """,
                (bill_id,),
            )
            existing = await cursor.fetchone()
            if existing is None:
                return None

            await cursor.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS paid
                FROM payments
                WHERE bill_id = %s AND payment_status = 'Completed'
                """,
                (bill_id,),
            )
            paid = (await cursor.fetchone())["paid"]

            if data["amount"] < paid:
                raise ValueError(
                    "Bill amount cannot be less than the completed payments."
                )

            await cursor.execute(
                """
                UPDATE maintenance_bills
                SET apartment_id = %s,
                    billing_month = %s,
                    amount = %s,
                    due_date = %s,
                    bill_status = CASE
                        WHEN %s >= %s THEN 'Paid'
                        WHEN %s > 0 THEN 'Partially Paid'
                        WHEN %s < CURRENT_DATE THEN 'Overdue'
                        ELSE 'Unpaid'
                    END
                WHERE bill_id = %s
                RETURNING bill_id
                """,
                (
                    data["apartment_id"],
                    data["billing_month"],
                    data["amount"],
                    data["due_date"],
                    paid,
                    data["amount"],
                    paid,
                    data["due_date"],
                    bill_id,
                ),
            )

    return await get_bill(pool, bill_id)


async def delete_bill(pool, bill_id: int):
    async with pool.connection() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                DELETE FROM maintenance_bills
                WHERE bill_id = %s
                RETURNING bill_id
                """,
                (bill_id,),
            )
            return await cursor.fetchone()
