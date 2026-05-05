from db_connection import get_connection

def report_delivery_performance():
    
    #Summary report: total orders by status, average cost, total revenue
    
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        #Order count by status
        cursor.execute(
            "SELECT order_status, COUNT(*) AS count "
            "FROM orders GROUP BY order_status"
        )
        status_counts = cursor.fetchall()

        #Total orders and deliveries
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM deliveries")
        total_deliveries = cursor.fetchone()[0]

        #Average delivery cost via UDF
        cursor.execute("SELECT GetAverageDeliveryCost()")
        avg_cost = cursor.fetchone()[0]

        #Total expenses overall
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
        total_expenses = cursor.fetchone()[0]

        print("\n  ── Delivery Performance Report ──────────────────")
        print(f"  Total Orders     : {total_orders}")
        print(f"  Total Deliveries : {total_deliveries}")
        print(f"  Total Expenses   : ${float(total_expenses):.2f}")
        print(f"  Avg Cost/Delivery: ${float(avg_cost):.2f}")
        print(f"\n  Orders by Status:")
        for row in status_counts:
            bar = "█" * row[1]
            print(f"    {row[0]:<14} {row[1]:>3}  {bar}")

    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def report_delivery_history(customer_id=None):
    
    #All completed deliveries, can be filtered by customer
    
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        if customer_id:
            cursor.execute(
                "SELECT o.order_id, c.customer_name, o.origin_city, o.destination_city, "
                "o.order_date, d.delivery_date, t.make "
                "FROM orders o "
                "JOIN customers c ON o.customer_id = c.customer_id "
                "LEFT JOIN deliveries d ON o.order_id = d.order_id "
                "LEFT JOIN trucks t ON d.truck_id = t.truck_id "
                "WHERE o.order_status = 'Completed' AND o.customer_id = %s "
                "ORDER BY d.delivery_date DESC",
                (customer_id,)
            )
        else:
            cursor.execute(
                "SELECT o.order_id, c.customer_name, o.origin_city, o.destination_city, "
                "o.order_date, d.delivery_date, t.make "
                "FROM orders o "
                "JOIN customers c ON o.customer_id = c.customer_id "
                "LEFT JOIN deliveries d ON o.order_id = d.order_id "
                "LEFT JOIN trucks t ON d.truck_id = t.truck_id "
                "WHERE o.order_status = 'Completed' "
                "ORDER BY d.delivery_date DESC"
            )
        rows = cursor.fetchall()
        if not rows:
            print("  No completed deliveries found.")
            return
        print(f"\n  ── Delivery History {'(Customer: ' + customer_id + ')' if customer_id else '(All)'} ──")
        print(f"  {'Order ID':<12} {'Customer':<18} {'Route':<28} {'Ordered':<12} {'Delivered':<12} {'Truck'}")
        print("  " + "-" * 95)
        for r in rows:
            route = f"{r[2]} → {r[3]}"
            print(f"  {r[0]:<12} {r[1]:<18} {route:<28} {str(r[4]):<12} {str(r[5]):<12} {r[6] or 'N/A'}")

    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def report_cost_breakdown():
    
    #Cost per order from the cost_per_order view, sorted by total cost descending
    
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT order_id, customer_name, origin_city, destination_city, "
            "order_status, total_cost "
            "FROM cost_per_order ORDER BY total_cost DESC"
        )
        rows = cursor.fetchall()
        if not rows:
            print("  No cost data found.")
            return
        print(f"\n  ── Cost Breakdown per Order ─────────────────────")
        print(f"  {'Order ID':<12} {'Customer':<18} {'Route':<28} {'Status':<12} {'Total Cost':>12}")
        print("  " + "-" * 85)
        for r in rows:
            route = f"{r[2]} → {r[3]}"
            print(f"  {r[0]:<12} {r[1]:<18} {route:<28} {r[4]:<12} ${float(r[5]):>11.2f}")

    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()


def report_truck_utilisation():
    
    #Deliveries per truck using the GetDeliveryCountByTruck UDF
    
    conn = get_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT truck_id, make FROM trucks")
        trucks = cursor.fetchall()
        if not trucks:
            print("  No trucks found.")
            return

        print(f"\n  ── Truck Utilisation Report ─────────────────────")
        print(f"  {'Truck ID':<12} {'Make':<20} {'Deliveries':>12}")
        print("  " + "-" * 46)
        for truck in trucks:
            cursor.execute("SELECT GetDeliveryCountByTruck(%s)", (truck[0],))
            count = cursor.fetchone()[0]
            bar = "▪" * count
            print(f"  {truck[0]:<12} {truck[1]:<20} {count:>10}  {bar}")

    except Exception as e:
        print(f"  [ERROR] {e}")
    finally:
        cursor.close()
        conn.close()
