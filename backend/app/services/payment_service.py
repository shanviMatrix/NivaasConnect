from psycopg.rows import dict_row



async def get_payments(pool, limit: int, offset: int, resident_id: int | None = None):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            query = """
                SELECT p.payment_id, p.bill_id, p.amount, p.payment_date,
                       p.payment_method, p.transaction_reference, p.payment_status
                FROM payments p
                JOIN maintenance_bills b ON b.bill_id = p.bill_id
            """
            params = []
            if resident_id is not None:
                query += """
                    WHERE b.apartment_id = (
                        SELECT apartment_id FROM residents
                        WHERE resident_id = %s
                    )
                """
                params.append(resident_id)
            query += """
                ORDER BY p.payment_date DESC, p.payment_id DESC
                LIMIT %s OFFSET %s
            """
            params.extend([limit, offset])
            await cursor.execute(query, params)
            return await cursor.fetchall()

async def get_payment(pool, payment_id: int, resident_id: int | None = None):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            query = """
                SELECT p.payment_id, p.bill_id, p.amount, p.payment_date,
                       p.payment_method, p.transaction_reference, p.payment_status
                FROM payments p
                JOIN maintenance_bills b ON b.bill_id = p.bill_id
                WHERE p.payment_id = %s
            """
            params = [payment_id]
            if resident_id is not None:
                query += """
                    AND b.apartment_id = (
                        SELECT apartment_id FROM residents
                        WHERE resident_id = %s
                    )
                """
                params.append(resident_id)
            await cursor.execute(query, params)
            return await cursor.fetchone()
async def create_payment(pool, data: dict):
    async with pool.connection() as connection:
        async with connection.cursor(row_factory=dict_row) as cursor:
            # Lock the bill to prevent concurrent overpayments.
            await cursor.execute(
                """
                SELECT bill_id, amount
                FROM maintenance_bills
                WHERE bill_id = %s
                FOR UPDATE
                """,
                (data["bill_id"],),
            )
            bill = await cursor.fetchone()

            if bill is None:
                raise LookupError("Maintenance bill not found.")

            await cursor.execute(
                """
                SELECT COALESCE(SUM(amount), 0) AS paid
                FROM payments
                WHERE bill_id = %s AND payment_status = 'Completed'
                """,
                (data["bill_id"],),
            )
            paid = (await cursor.fetchone())["paid"]

            if data["payment_status"] == "Completed":
                if paid + data["amount"] > bill["amount"]:
                    raise ValueError(
                        "Payment exceeds the outstanding bill amount."
                    )

            await cursor.execute(
                """
                INSERT INTO payments
                    (bill_id, amount, payment_method,
                     transaction_reference, payment_status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING payment_id, bill_id, amount, payment_date,
                          payment_method, transaction_reference, payment_status
                """,
                (
                    data["bill_id"],
                    data["amount"],
                    data["payment_method"],
                    data["transaction_reference"],
                    data["payment_status"],
                ),
            )
            payment = await cursor.fetchone()

            if data["payment_status"] == "Completed":
                new_paid = paid + data["amount"]

                await cursor.execute(
                    """
                    UPDATE maintenance_bills
                    SET bill_status = CASE
                        WHEN %s >= amount THEN 'Paid'
                        WHEN %s > 0 THEN 'Partially Paid'
                        WHEN due_date < CURRENT_DATE THEN 'Overdue'
                        ELSE 'Unpaid'
                    END
                    WHERE bill_id = %s
                    """,
                    (new_paid, new_paid, data["bill_id"]),
                )

            return payment
