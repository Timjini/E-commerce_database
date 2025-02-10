
from models.db_connection import retry_connection, check_tables_exist
from models.db_create_tables import create_tables_from_sql
from services.data_insertion import insert_fake_data , insert_order_items, insert_vendor_products
from mysql.connector import Error
import time


try:
    connection = retry_connection()
    sql_data = 'app/sql/db.sql'
    create_tables_from_sql(connection, sql_data)
    if connection.is_connected():
        print("Successfully connected to the database")
        required_tables = ['products', 'shoppers', 'vendors', 'orders', 'vendor_products']

        while not check_tables_exist(connection, required_tables):
            time.sleep(5)  
            print("table not found")

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

