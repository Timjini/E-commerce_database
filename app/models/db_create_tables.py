import mysql.connector
from mysql.connector import Error
from services.data_insertion import insert_fake_data , insert_order_items, insert_vendor_products
from services.order_data_insertion import insert_orders_data, inset_order_items_data


def create_tables_from_sql(connection, sql_file_path):
    print("connection while creating table", connection)
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        with open(sql_file_path, 'r') as file:
            sql_commands = file.read()
        
        cursor = connection.cursor()
        
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print(f"Executed: {command}")
                except mysql.connector.Error as err:
                    print(f"Error executing command: {err}")
        
        insert_fake_data(cursor, connection, "products", 1000)
        insert_fake_data(cursor, connection, "shoppers", 1000)
        insert_fake_data(cursor, connection, "vendors", 1000)
        insert_vendor_products(cursor, connection)
        insert_orders_data(cursor, connection)
        inset_order_items_data(cursor, connection, max_items_per_order=5)
        # insert_reviews_data(cursor, connection)
        # insert_time_spent_data(cursor, connection)
        # insert_costs_data(cursor, connection)
        # insert_revenue_data(cursor, connection)
        connection.commit()
        print("All tables created successfully.")
        return True
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
