CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resident_id INTEGER NOT NULL
        REFERENCES residents(resident_id),
    vendor_id INTEGER
        REFERENCES vendors(vendor_id),
    title VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL
        CHECK (category IN (
            'Plumbing', 'Electrical', 'Cleaning', 'Lift',
            'Parking', 'Security', 'Common Area', 'Other'
        )),
    priority VARCHAR(15) NOT NULL DEFAULT 'Medium'
        CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    complaint_status VARCHAR(20) NOT NULL DEFAULT 'Open'
        CHECK (complaint_status IN (
            'Open', 'Assigned', 'In Progress', 'Resolved', 'Closed'
        )),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMPTZ,
    CHECK (resolved_at IS NULL OR resolved_at >= created_at)
);
