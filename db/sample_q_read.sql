-- All customers
SELECT customer_id, customer_name, customer_phone_number
FROM customers
ORDER BY customer_name;
 
-- All orders with customer names
SELECT
    o.order_id,
    c.customer_name,
    o.order_date,
    o.order_status,
    o.origin_city,
    o.destination_city
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;
 
-- Look up one specific order
SELECT
    o.order_id,
    c.customer_name,
    o.order_status,
    o.origin_city,
    o.destination_city
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_id = 'ORD00099901';
 
-- All expenses for the new delivery
SELECT expense_id, expense_type, expense_date, amount
FROM expenses
WHERE delivery_id = 'DLV00099901';
