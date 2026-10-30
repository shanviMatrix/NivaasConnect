SELECT
    fb.booking_id,
    f.facility_name,
    r.full_name AS resident_name,
    a.building_name,
    a.flat_number,
    fb.start_time,
    fb.end_time,
    f.booking_fee,
    fb.booking_status
FROM facility_bookings AS fb
JOIN facilities AS f
    ON fb.facility_id = f.facility_id
JOIN residents AS r
    ON fb.resident_id = r.resident_id
JOIN apartments AS a
    ON r.apartment_id = a.apartment_id
ORDER BY fb.start_time;
