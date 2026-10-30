-- 1. Vendors: maintenance and society service providers
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    vendor_name VARCHAR(120) NOT NULL,
    service_category VARCHAR(80) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(150) UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2. Security guards
CREATE TABLE IF NOT EXISTS security_guards (
    guard_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL UNIQUE,
    shift_name VARCHAR(20) NOT NULL
        CHECK (shift_name IN ('Morning', 'Evening', 'Night', 'Rotational')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Maintenance bills: charges belong to an apartment
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

-- 4. Payments: one bill can have multiple payment records
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

-- 5. Complaints raised by residents
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

-- 6. Visitor logs: record entry and exit
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

-- 7. Shared society facilities
CREATE TABLE IF NOT EXISTS facilities (
    facility_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL UNIQUE,
    location_description VARCHAR(150),
    capacity INTEGER CHECK (capacity > 0),
    booking_fee NUMERIC(10, 2) NOT NULL DEFAULT 0
        CHECK (booking_fee >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- 8. Facility bookings
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

-- 9. Society events
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

CREATE INDEX IF NOT EXISTS idx_bills_apartment
    ON maintenance_bills(apartment_id);

CREATE INDEX IF NOT EXISTS idx_payments_bill
    ON payments(bill_id);

CREATE INDEX IF NOT EXISTS idx_complaints_resident_status
    ON complaints(resident_id, complaint_status);

CREATE INDEX IF NOT EXISTS idx_complaints_vendor
    ON complaints(vendor_id);

CREATE INDEX IF NOT EXISTS idx_visitors_resident_entry
    ON visitor_logs(resident_id, entry_time DESC);

CREATE INDEX IF NOT EXISTS idx_visitors_guard
    ON visitor_logs(guard_id);

CREATE INDEX IF NOT EXISTS idx_bookings_facility_time
    ON facility_bookings(facility_id, start_time, end_time);

CREATE INDEX IF NOT EXISTS idx_bookings_resident
    ON facility_bookings(resident_id);

CREATE INDEX IF NOT EXISTS idx_events_start_time
    ON society_events(start_time);

