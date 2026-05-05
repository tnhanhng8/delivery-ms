from db_connection import get_connection
from utils import next_customer_id, next_order_id, validate_exists

# ── CUSTOMERS ─────────────────────────────────────────────────────────────────

def add_customer(name, phone):
    conn = get_connection()
    if not conn:
        return
    try:
        customer_id = next_customer_id()
        if not customer_id:
            print("  [ERROR] Could not generate customer ID.")
            return
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (customer_id, customer_name, customer_phone_number) "
            "VALUES (%s, %s, %s)",
            (customer_id, name, phone)
        )
        conn.commit()
        print(f"  ✓ Customer added. ID: {customer_id}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def list_customers():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, customer_name, customer_phone_number FROM customers")
        rows = cursor.fetchall()
        if not rows:
            print("  No customers found.")
            return
        print(f"\n  {'ID':<12} {'Name':<25} {'Phone':<15}")
        print("  " + "-" * 52)
        for row in rows:
            print(f"  {row[0]:<12} {row[1]:<25} {row[2]:<15}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


# ── ORDERS ────────────────────────────────────────────────────────────────────

VALID_STATUSES = ['Ordered', 'Picked Up', 'In Transit', 'Completed']

def create_order(customer_id, order_date, origin, destination):
    if not validate_exists("customers", "customer_id", customer_id):
        print(f"  [ERROR] Customer '{customer_id}' does not exist.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        order_id = next_order_id()
        if not order_id:
            print("  [ERROR] Could not generate order ID.")
            return
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO orders (order_id, customer_id, order_date, order_status, "
            "origin_city, destination_city) VALUES (%s, %s, %s, 'Ordered', %s, %s)",
            (order_id, customer_id, order_date, origin, destination)
        )
        conn.commit()
        print(f"  ✓ Order created. ID: {order_id} | {origin} → {destination}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def update_order_status(order_id, new_status):
    if not validate_exists("orders", "order_id", order_id):
        print(f"  [ERROR] Order '{order_id}' does not exist.")
        return
    if new_status not in VALID_STATUSES:
        print(f"  [ERROR] Invalid status. Choose from: {', '.join(VALID_STATUSES)}")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET order_status = %s WHERE order_id = %s",
            (new_status, order_id)
        )
        conn.commit()
        print(f"  ✓ Order '{order_id}' status updated to '{new_status}'.")
        if new_status == "Completed":
            print("    (Trigger fired: delivery date set automatically.)")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def list_orders(status_filter=None):
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        if status_filter:
            if status_filter not in VALID_STATUSES:
                print(f"  [ERROR] Invalid status. Choose from: {', '.join(VALID_STATUSES)}")
                return
            cursor.execute(
                "SELECT o.order_id, c.customer_name, o.order_date, o.order_status, "
                "o.origin_city, o.destination_city "
                "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
                "WHERE o.order_status = %s",
                (status_filter,)
            )
        else:
            cursor.execute(
                "SELECT o.order_id, c.customer_name, o.order_date, o.order_status, "
                "o.origin_city, o.destination_city "
                "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
                "ORDER BY o.order_date DESC"
            )
        rows = cursor.fetchall()
        if not rows:
            print("  No orders found.")
            return
        print(f"\n  {'Order ID':<14} {'Customer':<20} {'Date':<12} {'Status':<12} {'Route'}")
        print("  " + "-" * 80)
        for r in rows:
            route = f"{r[4]} → {r[5]}"
            print(f"  {r[0]:<14} {r[1]:<20} {str(r[2]):<12} {r[3]:<12} {route}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def track_order(order_id):
    if not validate_exists("orders", "order_id", order_id):
        print(f"  [ERROR] Order '{order_id}' does not exist.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT o.order_id, c.customer_name, c.customer_phone_number, "
            "o.order_date, o.order_status, o.origin_city, o.destination_city, "
            "d.delivery_id, t.truck_id, t.make, d.delivery_date "
            "FROM orders o "
            "JOIN customers c ON o.customer_id = c.customer_id "
            "LEFT JOIN deliveries d ON o.order_id = d.order_id "
            "LEFT JOIN trucks t ON d.truck_id = t.truck_id "
            "WHERE o.order_id = %s",
            (order_id,)
        )
        row = cursor.fetchone()
        if not row:
            print(f"  Order '{order_id}' not found.")
            return
        print(f"\n  ── Order Tracking: {order_id} ──────────────────")
        print(f"  Customer    : {row['customer_name']} ({row['customer_phone_number']})")
        print(f"  Route       : {row['origin_city']} → {row['destination_city']}")
        print(f"  Order Date  : {row['order_date']}")
        print(f"  Status      : {row['order_status']}")
        if row['delivery_id']:
            print(f"  Delivery ID : {row['delivery_id']}")
            print(f"  Truck       : {row['truck_id']} ({row['make']})")
            print(f"  Delivered   : {row['delivery_date'] or 'Not yet'}")
        else:
            print(f"  Delivery    : Not yet assigned")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()
