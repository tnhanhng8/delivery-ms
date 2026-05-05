from db_connection import get_connection

#Maps expense types to their 4-letter ID prefix
EXPENSE_PREFIXES = {
    "Fuel":     "FUEL",
    "Toll":     "TOLL",
    "Handling": "HNDL"
}

def _next_id(prefix, table, id_column, digits):
    
    #Queries the table for the highest existing ID with the given prefix,
    #extracts the number, increments by 1, and returns the new formatted ID

    conn = get_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT MAX(CAST(SUBSTRING({id_column}, %s) AS UNSIGNED)) FROM {table} "
            f"WHERE {id_column} LIKE %s",
            (len(prefix) + 1, f"{prefix}%")
        )
        row = cursor.fetchone()
        current_max = row[0] if row[0] is not None else 0
        new_num = current_max + 1
        return f"{prefix}{str(new_num).zfill(digits)}"
    except Exception as e:
        print(f"  [ID GEN ERROR] {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def next_customer_id():
    return _next_id("CUST", "customers", "customer_id", 5)

def next_order_id():
    return _next_id("ORD", "orders", "order_id", 8)

def next_delivery_id():
    return _next_id("DLV", "deliveries", "delivery_id", 8)

def next_expense_id(expense_type):
    prefix = EXPENSE_PREFIXES.get(expense_type, expense_type[:4].upper())
    return _next_id(prefix, "expenses", "expense_id", 8)


def validate_exists(table, id_column, value):
    #Returns True if the value exists in the given table column
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT 1 FROM {table} WHERE {id_column} = %s LIMIT 1", (value,)
        )
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"  [VALIDATION ERROR] {e}")
        return False
    finally:
        cursor.close()
        conn.close()
