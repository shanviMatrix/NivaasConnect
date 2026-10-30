INSERT INTO complaints
(resident_id, vendor_id, title, description, category, priority, complaint_status)
SELECT r.resident_id, v.vendor_id, d.title, d.description,
d.category, d.priority, d.status
FROM (VALUES
('aarav@example.com', 'Apex Plumbing Services',
 'Water leakage in bathroom', 'Water is leaking from the bathroom tap.',
 'Plumbing', 'High', 'Assigned'),
('diya@example.com', 'Bright Electrical Works',
 'Corridor light not working', 'The corridor light near the flat is not working.',
 'Electrical', 'Medium', 'In Progress'),
('kabir@example.com', NULL,
 'Parking area cleanliness', 'Parking area needs proper cleaning.',
 'Cleaning', 'Low', 'Open')
) AS d(email, vendor_name, title, description, category, priority, status)
JOIN residents r ON r.email = d.email
LEFT JOIN vendors v ON v.vendor_name = d.vendor_name;
