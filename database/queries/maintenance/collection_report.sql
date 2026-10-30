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
