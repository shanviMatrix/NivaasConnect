INSERT INTO maintenance_bills
(apartment_id, billing_month, amount, due_date, bill_status)
SELECT apartment_id, DATE '2026-10-01',
CASE WHEN flat_number = '201' THEN 1800 ELSE 1500 END,
DATE '2026-10-10',
CASE WHEN flat_number = '101' THEN 'Paid'
     WHEN flat_number = '102' THEN 'Partially Paid'
     ELSE 'Overdue' END
FROM apartments
WHERE (building_name = 'A Block' AND flat_number IN ('101','102'))
   OR (building_name = 'B Block' AND flat_number = '201');
