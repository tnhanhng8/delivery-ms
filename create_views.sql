USE DeliveryServiceDB;

-- View 1: Truck availability
-- Shows trucks that are not currently assigned to an active delivery
CREATE VIEW truck_availability AS
SELECT
    t.truck_id,
    t.make,
    t.vin,
    CASE
        WHEN d.truck_id IS NULL THEN 'Available'
        ELSE 'Unavailable'
    END AS availability_status
FROM trucks t
LEFT JOIN deliveries d
    ON t.truck_id = d.truck_id
    AND d.delivery_id IN (
        SELECT del.delivery_id
        FROM deliveries del
        JOIN orders o ON del.order_id = o.order_id
        WHERE o.order_status != 'Completed'
    );
 
 
-- View 2: Current delivery schedule
-- Shows all active deliveries with full order and truck details
CREATE VIEW current_delivery_schedule AS
SELECT
    d.delivery_id,
    o.order_id,
    c.customer_name,
    o.origin_city,
    o.destination_city,
    o.order_status,
    t.truck_id,
    t.make,
    d.delivery_date
FROM deliveries d
JOIN orders o ON d.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN trucks t ON d.truck_id = t.truck_id
WHERE o.order_status != 'Completed';
 
 
-- View 3: Cost per order
-- Shows total expenses grouped per order
CREATE VIEW cost_per_order AS
SELECT
    o.order_id,
    c.customer_name,
    o.origin_city,
    o.destination_city,
    o.order_status,
    COALESCE(SUM(e.amount), 0) AS total_cost
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN deliveries d ON o.order_id = d.order_id
LEFT JOIN expenses e ON d.delivery_id = e.delivery_id
GROUP BY o.order_id, c.customer_name, o.origin_city, o.destination_city, o.order_status;
