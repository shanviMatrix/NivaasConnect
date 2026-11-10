CREATE TABLE IF NOT EXISTS user_accounts (
    account_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    role VARCHAR(20) NOT NULL
        CHECK (role IN ('Admin', 'Resident', 'Security')),

    resident_id INTEGER UNIQUE
        REFERENCES residents(resident_id),

    guard_id INTEGER UNIQUE
        REFERENCES security_guards(guard_id),

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT user_accounts_role_link_check CHECK (
        (role = 'Admin' AND resident_id IS NULL AND guard_id IS NULL)
        OR
        (role = 'Resident' AND resident_id IS NOT NULL AND guard_id IS NULL)
        OR
        (role = 'Security' AND resident_id IS NULL AND guard_id IS NOT NULL)
    )
);
