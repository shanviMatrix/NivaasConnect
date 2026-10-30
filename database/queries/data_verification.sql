
SELECT 'vendors' AS table_name, COUNT(*) AS total_rows FROM vendors
UNION ALL
SELECT 'security_guards', COUNT(*) FROM security_guards
UNION ALL
SELECT 'maintenance_bills', COUNT(*) FROM maintenance_bills
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'complaints', COUNT(*) FROM complaints
UNION ALL
SELECT 'visitor_logs', COUNT(*) FROM visitor_logs
UNION ALL
SELECT 'facilities', COUNT(*) FROM facilities
UNION ALL
SELECT 'facility_bookings', COUNT(*) FROM facility_bookings
UNION ALL
SELECT 'society_events', COUNT(*) FROM society_events
ORDER BY table_name;
