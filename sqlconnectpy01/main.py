from datetime import date
from orders import (
    add_customer, list_customers,
    create_order, update_order_status, list_orders, track_order,
    VALID_STATUSES
)
from deliveries import (
    list_truck_availability,
    assign_delivery, view_delivery_schedule,
    add_expense, get_delivery_expenses, generate_invoice,
    VALID_EXPENSE_TYPES
)
from reports import (
    report_delivery_performance,
    report_delivery_history,
    report_cost_breakdown,
    report_truck_utilisation
)

def prompt(label, required=True):
    while True:
        val = input(f"  {label}: ").strip()
        if val or not required:
            return val
        print("  This field is required.")

def pause():
    input("\n  Press Enter to continue...")

def header(title):
    print("\n" + "=" * 55)
    print(f"  {title}")
    print("=" * 55)

def menu_customers():
    while True:
        header("CUSTOMER MANAGEMENT")
        print("  1. Add new customer")
        print("  2. List all customers")
        print("  0. Back")
        choice = prompt("Select")
        if choice == "1":
            name  = prompt("Full name")
            phone = prompt("Phone number (10 digits)")
            add_customer(name, phone)
            pause()
        elif choice == "2":
            list_customers()
            pause()
        elif choice == "0":
            break

def menu_orders():
    while True:
        header("ORDER MANAGEMENT")
        print("  1. Create new order")
        print("  2. List all orders")
        print("  3. Filter orders by status")
        print("  4. Update order status")
        print("  5. Track an order")
        print("  0. Back")
        choice = prompt("Select")

        if choice == "1":
            cid   = prompt("Customer ID")
            odate = prompt("Order date (YYYY-MM-DD) [Enter for today]", required=False) or str(date.today())
            ori   = prompt("Origin city")
            dest  = prompt("Destination city")
            create_order(cid, odate, ori, dest)
            pause()
        elif choice == "2":
            list_orders()
            pause()
        elif choice == "3":
            print(f"  Statuses: {' / '.join(VALID_STATUSES)}")
            status = prompt("Filter by status")
            list_orders(status_filter=status)
            pause()
        elif choice == "4":
            oid = prompt("Order ID")
            print(f"  Statuses: {' / '.join(VALID_STATUSES)}")
            new_status = prompt("New status")
            update_order_status(oid, new_status)
            pause()
        elif choice == "5":
            oid = prompt("Order ID")
            track_order(oid)
            pause()
        elif choice == "0":
            break

def menu_trucks():
    while True:
        header("TRUCK MANAGEMENT")
        print("  1. View truck availability")
        print("  0. Back")
        choice = prompt("Select")
        if choice == "1":
            list_truck_availability()
            pause()
        elif choice == "0":
            break

def menu_deliveries():
    while True:
        header("DELIVERY MANAGEMENT")
        print("  1. Assign delivery to order  (auto-selects truck)")
        print("  2. View current delivery schedule")
        print("  3. Add expense to a delivery")
        print("  4. View expense summary for a delivery")
        print("  5. Generate invoice for an order")
        print("  0. Back")
        choice = prompt("Select")

        if choice == "1":
            oid = prompt("Order ID")
            assign_delivery(oid)
            pause()
        elif choice == "2":
            view_delivery_schedule()
            pause()
        elif choice == "3":
            did   = prompt("Delivery ID")
            print(f"  Types: {' / '.join(VALID_EXPENSE_TYPES)}")
            etype = prompt("Expense type")
            edate = prompt("Date (YYYY-MM-DD) [Enter for today]", required=False) or str(date.today())
            amt   = prompt("Amount (e.g. 420.50)")
            try:
                add_expense(did, etype, edate, float(amt))
            except ValueError:
                print("  Invalid amount — please enter a number.")
            pause()
        elif choice == "4":
            did = prompt("Delivery ID")
            get_delivery_expenses(did)
            pause()
        elif choice == "5":
            oid = prompt("Order ID")
            generate_invoice(oid)
            pause()
        elif choice == "0":
            break

def menu_reports():
    while True:
        header("REPORTS")
        print("  1. Delivery performance summary")
        print("  2. Delivery history (all)")
        print("  3. Delivery history (by customer)")
        print("  4. Cost breakdown per order")
        print("  5. Truck utilisation")
        print("  0. Back")
        choice = prompt("Select")

        if choice == "1":
            report_delivery_performance()
            pause()
        elif choice == "2":
            report_delivery_history()
            pause()
        elif choice == "3":
            cid = prompt("Customer ID")
            report_delivery_history(customer_id=cid)
            pause()
        elif choice == "4":
            report_cost_breakdown()
            pause()
        elif choice == "5":
            report_truck_utilisation()
            pause()
        elif choice == "0":
            break

def main():
    while True:
        header("DELIVERY SERVICE MANAGEMENT SYSTEM")
        print("  1. Customer Management")
        print("  2. Order Management")
        print("  3. Truck Management")
        print("  4. Delivery Management")
        print("  5. Reports")
        print("  0. Exit")
        choice = prompt("Select")

        if   choice == "1": menu_customers()
        elif choice == "2": menu_orders()
        elif choice == "3": menu_trucks()
        elif choice == "4": menu_deliveries()
        elif choice == "5": menu_reports()
        elif choice == "0":
            print("\n  Goodbye.\n")
            break
        else:
            print("  Invalid option.")

if __name__ == "__main__":
    main()
