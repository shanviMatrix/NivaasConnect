CREATE TABLE IF NOT EXISTS facility_bookings (
    booking_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    facility_id INTEGER NOT NULL
        REFERENCES facilities(facility_id),
    resident_id INTEGER NOT NULL
        REFERENCES residents(resident_id),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    booking_status VARCHAR(20) NOT NULL DEFAULT 'Pending'
        CHECK (booking_status IN (
            'Pending', 'Approved', 'Rejected', 'Cancelled', 'Completed'
        )),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (end_time > start_time)
);
