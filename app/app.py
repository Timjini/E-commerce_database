
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

        insert_fake_data(connection, "products", 1000)

        # try:
        #     insert_fake_data(connection, "products", 1000)
        #     insert_fake_data(connection, "shoppers", 1000)
        #     insert_fake_data(connection, "vendors", 1000)
        #     # insert_order_items(cursor, num_order_items=5, num_orders=1000, num_products=100, num_vendors=50)
        #     # insert_vendor_products(cursor, num_vendors=1000, num_products=1000)
        #     # connection.commit()
        #     print("Fake data inserted successfully")
        # except Exception as e:
        #     print(f"Error inserting data: {e}")
        #     connection.rollback()

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

