CREATE TABLE IF NOT EXISTS security_guards (
    guard_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    shift_name VARCHAR(20) NOT NULL
        CHECK (shift_name IN ('Morning', 'Evening', 'Night', 'Rotational')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
