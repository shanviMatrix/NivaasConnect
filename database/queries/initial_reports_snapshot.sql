-- 1. MAINTENANCE COLLECTION REPORT
-- Total bill amount, amount collected and balance per flat

SELECT
    a.building_name,
    a.flat_number,
    mb.billing_month,
    mb.amount AS bill_amount,
    COALESCE(SUM(p.amount), 0) AS amount_collected,
    mb.amount - COALESCE(SUM(p.amount), 0) AS balance_amount
FROM maintenance_bills AS mb
JOIN apartments AS a
    ON mb.apartment_id = a.apartment_id
LEFT JOIN payments AS p
    ON mb.bill_id = p.bill_id
   AND p.payment_status = 'Completed'
GROUP BY
    a.building_name,
    a.flat_number,
    mb.billing_month,
    mb.amount
ORDER BY a.building_name, a.flat_number;


-- 2. OUTSTANDING MAINTENANCE DUES
-- Only apartments with a positive remaining balance

SELECT
    a.building_name,
    a.flat_number,
    mb.bill_id,
    mb.amount AS total_bill,
    COALESCE(SUM(p.amount), 0) AS paid_amount,
    mb.amount - COALESCE(SUM(p.amount), 0) AS outstanding_amount,
    mb.due_date
FROM maintenance_bills AS mb
JOIN apartments AS a
    ON mb.apartment_id = a.apartment_id
LEFT JOIN payments AS p
    ON mb.bill_id = p.bill_id
   AND p.payment_status = 'Completed'
GROUP BY
    a.building_name,
    a.flat_number,
    mb.bill_id,
    mb.amount,
    mb.due_date
HAVING mb.amount - COALESCE(SUM(p.amount), 0) > 0
ORDER BY outstanding_amount DESC;


-- 3. COMPLAINT TRACKING REPORT
-- Resident, flat, assigned vendor and complaint status

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


-- 4. VISITOR ACTIVITY REPORT
-- Visitor entries, resident, guard and approval status

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


-- 5. FACILITY BOOKING REPORT
-- Booking details with resident and facility information

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


