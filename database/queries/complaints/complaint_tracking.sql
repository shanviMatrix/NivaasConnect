SELECT
    c.complaint_id,
    r.full_name AS resident_name,
    a.building_name,
    a.flat_number,
    c.title,
    c.category,
    c.priority,
    c.complaint_status,
    v.vendor_name,
    c.created_at
FROM complaints AS c
JOIN residents AS r
    ON c.resident_id = r.resident_id
JOIN apartments AS a
    ON r.apartment_id = a.apartment_id
LEFT JOIN vendors AS v
    ON c.vendor_id = v.vendor_id
ORDER BY
    CASE c.priority
        WHEN 'Urgent' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END,
    c.created_at DESC;
