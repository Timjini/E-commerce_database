import mysql.connector
from config.db_connection import DATABASE_CONFIG
import time


def get_db_connection():
    """Establish and return a MySQL database connection using the configuration."""
    try:
        connection = mysql.connector.connect(
            user=DATABASE_CONFIG["user"],
            password=DATABASE_CONFIG["password"],
            host=DATABASE_CONFIG["host"],
            port=DATABASE_CONFIG["port"],
            database=DATABASE_CONFIG["database"]
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def retry_connection():
    for _ in range(10):
        connection = get_db_connection()
        if connection and connection.is_connected():
            return connection
        time.sleep(5)
    return None 

def check_tables_exist(connection, tables):
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        result = cursor.fetchone()
        if not result:
            print(f"Table {table} does not exist. Waiting for table to be created...")
            return False
    return True

