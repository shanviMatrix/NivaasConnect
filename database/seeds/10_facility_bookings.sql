INSERT INTO facility_bookings
(facility_id, resident_id, start_time, end_time, booking_status)
SELECT f.facility_id, r.resident_id, d.start_time, d.end_time, d.status
FROM (VALUES
('Community Hall', 'aarav@example.com',
 TIMESTAMPTZ '2026-11-14 10:00:00+05:30',
 TIMESTAMPTZ '2026-11-14 13:00:00+05:30', 'Approved'),
('Indoor Badminton Court', 'kabir@example.com',
 TIMESTAMPTZ '2026-11-15 17:00:00+05:30',
 TIMESTAMPTZ '2026-11-15 18:00:00+05:30', 'Pending')
) AS d(facility_name, email, start_time, end_time, status)
JOIN facilities f ON f.facility_name = d.facility_name
JOIN residents r ON r.email = d.email;
