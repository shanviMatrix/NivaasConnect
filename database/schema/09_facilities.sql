CREATE TABLE IF NOT EXISTS facilities (
    facility_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    facility_name VARCHAR(100) NOT NULL UNIQUE,
    location_description VARCHAR(150),
    capacity INTEGER CHECK (capacity > 0),
    booking_fee NUMERIC(10, 2) NOT NULL DEFAULT 0
        CHECK (booking_fee >= 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
