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
