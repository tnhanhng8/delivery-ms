
CREATE USER IF NOT EXISTS 'delivery_manager'@'localhost' IDENTIFIED BY 'Mgr@Secure1!';
CREATE USER IF NOT EXISTS 'dispatcher'@'localhost'       IDENTIFIED BY 'Dsp@Secure1!';
CREATE USER IF NOT EXISTS 'accountant'@'localhost'       IDENTIFIED BY 'Acc@Secure1!';
 
-- Delivery Manager: full read access + can update order status
GRANT SELECT ON DeliveryServiceDB.*                   TO 'delivery_manager'@'localhost';
GRANT UPDATE (order_status) ON DeliveryServiceDB.orders TO 'delivery_manager'@'localhost';
GRANT INSERT, UPDATE ON DeliveryServiceDB.deliveries  TO 'delivery_manager'@'localhost';
 
-- Dispatcher: can manage trucks and deliveries, see orders (read-only)
GRANT SELECT ON DeliveryServiceDB.orders              TO 'dispatcher'@'localhost';
GRANT SELECT, INSERT, UPDATE ON DeliveryServiceDB.trucks      TO 'dispatcher'@'localhost';
GRANT SELECT, INSERT, UPDATE ON DeliveryServiceDB.deliveries  TO 'dispatcher'@'localhost';
 
-- Accountant: can only see and manage expenses and cost views
GRANT SELECT ON DeliveryServiceDB.expenses            TO 'accountant'@'localhost';
GRANT SELECT ON DeliveryServiceDB.cost_per_order      TO 'accountant'@'localhost';
GRANT INSERT, UPDATE ON DeliveryServiceDB.expenses    TO 'accountant'@'localhost';
 
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'accountant'@'localhost';
SHOW GRANTS FOR 'dispatcher'@'localhost';
SHOW GRANTS FOR 'delivery_manager'@'localhost';

