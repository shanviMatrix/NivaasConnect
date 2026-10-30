CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bill_id INTEGER NOT NULL
        REFERENCES maintenance_bills(bill_id),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    payment_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(20) NOT NULL
        CHECK (payment_method IN ('Cash', 'UPI', 'Card', 'Bank Transfer')),
    transaction_reference VARCHAR(100) UNIQUE,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Completed'
        CHECK (payment_status IN ('Pending', 'Completed', 'Failed', 'Refunded'))
);
