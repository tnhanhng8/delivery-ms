DELIMITER $$
 
-- Trigger: When order status is updated to 'Completed',
-- automatically set the delivery_date to today on the linked delivery
CREATE TRIGGER trg_set_delivery_date
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_status = 'Completed' AND OLD.order_status != 'Completed' THEN
        UPDATE deliveries
        SET delivery_date = CURDATE()
        WHERE order_id = NEW.order_id
          AND delivery_date IS NULL;
    END IF;
END$$
 
DELIMITER ;
