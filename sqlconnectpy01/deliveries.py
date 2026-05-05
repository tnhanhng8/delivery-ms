from db_connection import get_connection
from utils import next_delivery_id, next_expense_id, validate_exists, EXPENSE_PREFIXES

# ── TRUCKS ────────────────────────────────────────────────────────────────────

def list_truck_availability():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT truck_id, make, vin, availability_status FROM truck_availability")
        rows = cursor.fetchall()
        if not rows:
            print("  No trucks found.")
            return
        print(f"\n  {'Truck ID':<12} {'Make':<20} {'VIN':<22} {'Status'}")
        print("  " + "-" * 65)
        for r in rows:
            status_display = f"[{'✓' if r[3] == 'Available' else '✗'}] {r[3]}"
            print(f"  {r[0]:<12} {r[1]:<20} {r[2]:<22} {status_display}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


# ── DELIVERIES ────────────────────────────────────────────────────────────────

def assign_delivery(order_id):
    if not validate_exists("orders", "order_id", order_id):
        print(f"  [ERROR] Order '{order_id}' does not exist.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        delivery_id = next_delivery_id()
        if not delivery_id:
            print("  [ERROR] Could not generate delivery ID.")
            return
        cursor = conn.cursor()
        cursor.callproc("AssignDelivery", [delivery_id, order_id])
        conn.commit()
        print(f"  ✓ Delivery assigned. ID: {delivery_id}")
        print(f"    A truck was auto-selected. Order status set to 'Picked Up'.")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def view_delivery_schedule():
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT delivery_id, order_id, customer_name, origin_city, "
            "destination_city, order_status, truck_id, make "
            "FROM current_delivery_schedule"
        )
        rows = cursor.fetchall()
        if not rows:
            print("  No active deliveries.")
            return
        print(f"\n  {'Del. ID':<14} {'Order ID':<14} {'Customer':<18} {'Route':<28} {'Status':<12} {'Truck'}")
        print("  " + "-" * 100)
        for r in rows:
            route = f"{r[3]} → {r[4]}"
            print(f"  {r[0]:<14} {r[1]:<14} {r[2]:<18} {route:<28} {r[5]:<12} {r[6]} ({r[7]})")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


# ── EXPENSES ──────────────────────────────────────────────────────────────────

VALID_EXPENSE_TYPES = list(EXPENSE_PREFIXES.keys())

def add_expense(delivery_id, expense_type, expense_date, amount):
    if not validate_exists("deliveries", "delivery_id", delivery_id):
        print(f"  [ERROR] Delivery '{delivery_id}' does not exist.")
        return
    if expense_type not in VALID_EXPENSE_TYPES:
        print(f"  [ERROR] Invalid expense type. Choose from: {', '.join(VALID_EXPENSE_TYPES)}")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        expense_id = next_expense_id(expense_type)
        if not expense_id:
            print("  [ERROR] Could not generate expense ID.")
            return
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (expense_id, delivery_id, expense_type, expense_date, amount) "
            "VALUES (%s, %s, %s, %s, %s)",
            (expense_id, delivery_id, expense_type, expense_date, amount)
        )
        conn.commit()
        print(f"  ✓ Expense recorded. ID: {expense_id} | {expense_type} — ${amount:.2f}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def get_delivery_expenses(delivery_id):
    if not validate_exists("deliveries", "delivery_id", delivery_id):
        print(f"  [ERROR] Delivery '{delivery_id}' does not exist.")
        return

    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.callproc("GetDeliveryExpenses", [delivery_id])
        for result in cursor.stored_results():
            row = result.fetchone()
            if not row:
                print(f"  No expense data for delivery '{delivery_id}'.")
                return
            print(f"\n  ── Expense Summary: {delivery_id} ──────────────────")
            print(f"  Order ID      : {row[1]}")
            print(f"  Route         : {row[2]} → {row[3]}")
            print(f"  Total Expenses: ${float(row[4]):.2f}")
            print(f"  Expense Count : {row[5]}")
    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


# ── INVOICE ───────────────────────────────────────────────────────────────────

def generate_invoice(order_id):
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
            "o.order_date, o.order_status, o.origin_city, o.destination_city "
            "FROM orders o JOIN customers c ON o.customer_id = c.customer_id "
            "WHERE o.order_id = %s", (order_id,)
        )
        order = cursor.fetchone()
        if not order:
            print(f"  Order '{order_id}' not found.")
            return

        cursor.execute(
            "SELECT d.delivery_id, t.truck_id, t.make, d.delivery_date "
            "FROM deliveries d JOIN trucks t ON d.truck_id = t.truck_id "
            "WHERE d.order_id = %s", (order_id,)
        )
        delivery = cursor.fetchone()

        expenses = []
        total = 0.0
        if delivery:
            cursor.execute(
                "SELECT expense_type, expense_date, amount FROM expenses "
                "WHERE delivery_id = %s ORDER BY expense_date",
                (delivery["delivery_id"],)
            )
            expenses = cursor.fetchall()
            total = sum(float(e["amount"]) for e in expenses)

        width = 52
        print("\n  " + "=" * width)
        print(f"  {'DELIVERY SERVICE INVOICE':^{width}}")
        print("  " + "=" * width)
        print(f"  Order ID    : {order['order_id']}")
        print(f"  Customer    : {order['customer_name']}")
        print(f"  Phone       : {order['customer_phone_number']}")
        print(f"  Order Date  : {order['order_date']}")
        print(f"  Status      : {order['order_status']}")
        print(f"  Route       : {order['origin_city']} → {order['destination_city']}")
        if delivery:
            print(f"  Truck       : {delivery['truck_id']} — {delivery['make']}")
            print(f"  Delivered   : {delivery['delivery_date'] or 'Pending'}")
        print("  " + "-" * width)
        print(f"  {'EXPENSE BREAKDOWN':^{width}}")
        print("  " + "-" * width)
        if expenses:
            print(f"  {'Type':<22} {'Date':<14} {'Amount':>10}")
            for e in expenses:
                print(f"  {e['expense_type']:<22} {str(e['expense_date']):<14} ${float(e['amount']):>9.2f}")
        else:
            print("  No expenses recorded.")
        print("  " + "-" * width)
        print(f"  {'TOTAL':<36} ${total:>9.2f}")
        print("  " + "=" * width)

    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()
