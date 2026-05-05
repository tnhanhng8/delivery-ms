-- Auto-assign a truck to an order
CALL AssignDelivery('DLV00099902', 'ORD00099901');
 
-- Get expense summary for a delivery

-- Average delivery cost across the whole system
SELECT GetAverageDeliveryCost() AS avg_cost;
 
-- Delivery count per truck
SELECT
    truck_id,
    make,
    GetDeliveryCountByTruck(truck_id) AS total_deliveries
FROM trucks
ORDER BY total_deliveries DESC
LIMIT 10;

-- Move order through the lifecycle step by step
UPDATE orders SET order_status = 'Picked Up'  WHERE order_id = 'ORD00099901';
UPDATE orders SET order_status = 'In Transit' WHERE order_id = 'ORD00099901';
 
-- Mark as Completed → fires the trigger (sets delivery_date automatically)
UPDATE orders SET order_status = 'Completed'  WHERE order_id = 'ORD00099901';
 
-- Verify trigger fired: delivery_date should now show today's date
SELECT delivery_id, order_id, delivery_date
FROM deliveries
WHERE delivery_id = 'DLV00099901';
 
-- Update a customer phone number
UPDATE customers
SET customer_phone_number = '3105559999'
WHERE customer_id = 'CUST00999';

