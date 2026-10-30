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
