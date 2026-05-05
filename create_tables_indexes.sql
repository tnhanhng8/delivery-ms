CREATE database DeliveryServiceDB;
use DeliveryServiceDB;

CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone_number VARCHAR(10) NOT NULL
);

CREATE TABLE orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    order_status ENUM("Ordered", "Picked Up", "In Transit", "Completed") NOT NULL,
    origin_city VARCHAR(50) NOT NULL,
    destination_city VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    
CREATE TABLE trucks (
    truck_id VARCHAR(20) PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    vin VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE deliveries (
    delivery_id VARCHAR(20) PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    truck_id VARCHAR(20) NOT NULL,
    delivery_date DATE,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (truck_id) REFERENCES trucks(truck_id)
);

CREATE TABLE expenses (
    expense_id VARCHAR(20) PRIMARY KEY,
    delivery_id VARCHAR(20) NOT NULL,
    expense_type VARCHAR(50) NOT NULL,
    expense_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id)
);

-- Speed up order lookups by customer
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
 
-- Speed up filtering orders by status (e.g. finding all 'In Transit')
CREATE INDEX idx_orders_status ON orders(order_status);
 
-- Speed up delivery lookups by order and truck
CREATE INDEX idx_deliveries_order_id ON deliveries(order_id);
CREATE INDEX idx_deliveries_truck_id ON deliveries(truck_id);
 
-- Speed up expense lookups per delivery
CREATE INDEX idx_expenses_delivery_id ON expenses(delivery_id);




