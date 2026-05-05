import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "pass",
    "database": "DeliveryServiceDB"
}

def get_connection():
    """Return a live MySQL connection, or None on failure."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"  [DB ERROR] Could not connect: {e}")
        return None
