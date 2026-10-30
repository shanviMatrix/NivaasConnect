SELECT
    vl.visitor_id,
    vl.visitor_name,
    vl.purpose,
    r.full_name AS resident_name,
    a.building_name,
    a.flat_number,
    g.full_name AS guard_name,
    vl.entry_time,
    vl.exit_time,
    vl.approval_status
FROM visitor_logs AS vl
JOIN residents AS r
    ON vl.resident_id = r.resident_id
JOIN apartments AS a
    ON r.apartment_id = a.apartment_id
JOIN security_guards AS g
    ON vl.guard_id = g.guard_id
ORDER BY vl.entry_time DESC;
