CREATE TABLE IF NOT EXISTS society_events (
    event_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    event_title VARCHAR(150) NOT NULL,
    description TEXT,
    venue VARCHAR(150) NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    created_by INTEGER NOT NULL
        REFERENCES residents(resident_id),
    event_status VARCHAR(20) NOT NULL DEFAULT 'Planned'
        CHECK (event_status IN ('Planned', 'Ongoing', 'Completed', 'Cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_time > start_time)
);
