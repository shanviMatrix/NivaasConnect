INSERT INTO payments
(bill_id, amount, payment_method, transaction_reference, payment_status)
SELECT mb.bill_id,
CASE WHEN a.flat_number = '101' THEN 1500 ELSE 500 END,
CASE WHEN a.flat_number = '101' THEN 'UPI' ELSE 'Cash' END,
CASE WHEN a.flat_number = '101' THEN 'NC-TXN-1001' ELSE 'NC-TXN-1002' END,
'Completed'
FROM maintenance_bills mb
JOIN apartments a ON a.apartment_id = mb.apartment_id
WHERE mb.billing_month = DATE '2026-10-01'
AND a.building_name = 'A Block'
AND a.flat_number IN ('101','102');
