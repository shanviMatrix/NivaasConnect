CREATE TABLE IF NOT EXISTS visitor_logs (
    visitor_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resident_id INTEGER NOT NULL
        REFERENCES residents(resident_id),
    guard_id INTEGER NOT NULL
        REFERENCES security_guards(guard_id),
    visitor_name VARCHAR(100) NOT NULL,
    visitor_phone VARCHAR(15),
    purpose VARCHAR(200) NOT NULL,
    entry_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMPTZ,
    approval_status VARCHAR(15) NOT NULL DEFAULT 'Pending'
        CHECK (approval_status IN ('Pending', 'Approved', 'Denied')),
    CHECK (exit_time IS NULL OR exit_time >= entry_time)
);
