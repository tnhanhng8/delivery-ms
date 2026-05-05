-- Add a new customer
INSERT INTO customers (customer_id, customer_name, customer_phone_number)
VALUES ('CUST00999', 'Pacific Freight Co', '3105559021');
 
-- Place a new order for new customer
INSERT INTO orders (order_id, customer_id, order_date, order_status, origin_city, destination_city)
VALUES ('ORD00099901', 'CUST00999', '2025-03-15', 'Ordered', 'Phoenix', 'Kansas City');
 
-- Create a delivery for that order
INSERT INTO deliveries (delivery_id, order_id, truck_id, delivery_date)
VALUES ('DLV00099901', 'ORD00099901', 'TRK00064', NULL);
 
-- Log a fuel expense for that delivery
INSERT INTO expenses (expense_id, delivery_id, expense_type, expense_date, amount)
VALUES ('FUEL00099901', 'DLV00099901', 'Fuel', '2025-03-15', 420.50);
 
-- Log a toll expense on the same delivery
INSERT INTO expenses (expense_id, delivery_id, expense_type, expense_date, amount)
VALUES ('TOLL00099901', 'DLV00099901', 'Toll', '2025-03-16', 85.00);
 