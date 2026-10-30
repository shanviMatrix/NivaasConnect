CREATE TABLE IF NOT EXISTS maintenance_bills (
    bill_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    apartment_id INTEGER NOT NULL
        REFERENCES apartments(apartment_id),
    billing_month DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    due_date DATE NOT NULL,
    bill_status VARCHAR(20) NOT NULL DEFAULT 'Unpaid'
        CHECK (bill_status IN ('Unpaid', 'Partially Paid', 'Paid', 'Overdue')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (apartment_id, billing_month)
);
