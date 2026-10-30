INSERT INTO visitor_logs
(resident_id, guard_id, visitor_name, visitor_phone, purpose,
 entry_time, exit_time, approval_status)
SELECT r.resident_id, g.guard_id, d.visitor_name, d.visitor_phone,
d.purpose, CURRENT_TIMESTAMP - d.entry_offset,
CASE WHEN d.approval_status = 'Approved'
THEN CURRENT_TIMESTAMP - INTERVAL '30 minutes' ELSE NULL END,
d.approval_status
FROM (VALUES
('aarav@example.com', '9876522001', 'Rohan Mehta', '9876533001',
 'Personal Visit', INTERVAL '2 hours', 'Approved'),
('diya@example.com', '9876522002', 'Priya Sharma', '9876533002',
 'Food Delivery', INTERVAL '10 minutes', 'Pending')
) AS d(email, guard_phone, visitor_name, visitor_phone,
purpose, entry_offset, approval_status)
JOIN residents r ON r.email = d.email
JOIN security_guards g ON g.phone = d.guard_phone;
