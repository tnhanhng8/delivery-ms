DELIMITER $$
 
-- Procedure 1: Automate delivery assignment
-- Assigns the first available truck to a given order and creates a delivery record
CREATE PROCEDURE AssignDelivery(
    IN p_delivery_id VARCHAR(20),
    IN p_order_id    VARCHAR(20)
)
BEGIN
    DECLARE v_truck_id VARCHAR(20);
 
    -- Find an available truck (not currently on an active delivery)
    SELECT truck_id INTO v_truck_id
    FROM trucks
    WHERE truck_id NOT IN (
        SELECT d.truck_id
        FROM deliveries d
        JOIN orders o ON d.order_id = o.order_id
        WHERE o.order_status != 'Completed'
    )
    LIMIT 1;
 
    IF v_truck_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No trucks available for assignment.';
    ELSE
        INSERT INTO deliveries (delivery_id, order_id, truck_id, delivery_date)
        VALUES (p_delivery_id, p_order_id, v_truck_id, NULL);
 
        -- Update order status to Picked Up
        UPDATE orders
        SET order_status = 'Picked Up'
        WHERE order_id = p_order_id;
    END IF;
END$$
 
 
-- Procedure 2: Calculate total expenses for a specific delivery
CREATE PROCEDURE GetDeliveryExpenses(
    IN p_delivery_id VARCHAR(20)
)
BEGIN
    SELECT
        d.delivery_id,
        o.order_id,
        o.origin_city,
        o.destination_city,
        SUM(e.amount)       AS total_expenses,
        COUNT(e.expense_id) AS expense_count
    FROM deliveries d
    JOIN orders o ON d.order_id = o.order_id
    LEFT JOIN expenses e ON d.delivery_id = e.delivery_id
    WHERE d.delivery_id = p_delivery_id
    GROUP BY d.delivery_id, o.order_id, o.origin_city, o.destination_city;
END$$
 
DELIMITER ;

