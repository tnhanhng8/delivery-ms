DELIMITER $$
 
-- UDF 1: Compute average delivery cost across all deliveries
CREATE FUNCTION GetAverageDeliveryCost()
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE avg_cost DECIMAL(10,2);
 
    SELECT AVG(total)
    INTO avg_cost
    FROM (
        SELECT SUM(amount) AS total
        FROM expenses
        GROUP BY delivery_id
    ) AS delivery_totals;
 
    RETURN COALESCE(avg_cost, 0.00);
END$$
 
 
-- UDF 2: Count number of deliveries for a specific truck
CREATE FUNCTION GetDeliveryCountByTruck(
    p_truck_id VARCHAR(20)
)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE delivery_count INT;
 
    SELECT COUNT(*) INTO delivery_count
    FROM deliveries
    WHERE truck_id = p_truck_id;
 
    RETURN delivery_count;
END$$
 
DELIMITER ;