
-- 1. INNER JOIN: show each resident with their apartment
SELECT
    r.resident_id,
    r.full_name,
    r.email,
    a.building_name,
    a.flat_number,
    a.floor_number
FROM residents AS r
INNER JOIN apartments AS a
    ON r.apartment_id = a.apartment_id
ORDER BY a.building_name, a.flat_number, r.full_name;


-- 2. LEFT JOIN: show every apartment, even if it has no residents
SELECT
    a.apartment_id,
    a.building_name,
    a.flat_number,
    COUNT(r.resident_id) AS resident_count
FROM apartments AS a
LEFT JOIN residents AS r
    ON a.apartment_id = r.apartment_id
GROUP BY
    a.apartment_id,
    a.building_name,
    a.flat_number
ORDER BY a.building_name, a.flat_number;


-- 3. Aggregate functions: overall resident statistics
SELECT
    COUNT(*) AS total_residents,
    COUNT(DISTINCT apartment_id) AS occupied_apartments,
    COUNT(DISTINCT email) AS unique_emails
FROM residents;


-- 4. GROUP BY: count residents in each apartment
SELECT
    a.building_name,
    a.flat_number,
    COUNT(r.resident_id) AS resident_count
FROM apartments AS a
LEFT JOIN residents AS r
    ON a.apartment_id = r.apartment_id
GROUP BY a.building_name, a.flat_number
ORDER BY resident_count DESC, a.building_name;


-- 5. HAVING: find apartments with more than one resident
SELECT
    a.building_name,
    a.flat_number,
    COUNT(r.resident_id) AS resident_count
FROM apartments AS a
JOIN residents AS r
    ON a.apartment_id = r.apartment_id
GROUP BY a.building_name, a.flat_number
HAVING COUNT(r.resident_id) > 1;


-- 6. Integrity check: identify any orphaned resident records
SELECT r.resident_id, r.full_name, r.apartment_id
FROM residents AS r
LEFT JOIN apartments AS a
    ON r.apartment_id = a.apartment_id
WHERE a.apartment_id IS NULL;
