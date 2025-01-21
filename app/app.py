import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from faker import Faker
import random

load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT", 3307)
database = os.getenv("MYSQL_DATABASE")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

fake = Faker()

def insert_fake_data(cursor, table_name, num_rows=1000):
    for _ in range(num_rows):
        if table_name == "products":
            name = fake.word()
            cost = round(fake.random_number(digits=2), 2)
            description = fake.text(max_nb_chars=200)
            cursor.execute(f"INSERT INTO {table_name} (name, cost, description) VALUES (%s, %s, %s)",
                           (name, cost, description))
        elif table_name == "shoppers":
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            phone_number = fake.phone_number()[:20]
            address = fake.address()
            is_member = fake.boolean()
            cursor.execute(f"INSERT INTO {table_name} (first_name, last_name, email, phone_number, address, is_member) VALUES (%s, %s, %s, %s, %s, %s)",
                           (first_name, last_name, email, phone_number, address, is_member))
        elif table_name == "vendors":
            contact_name = fake.name()
            company_name = fake.company()
            contact_email = fake.email()
            contact_phone = fake.phone_number()[:20]
            address = fake.address()
            tax_number = fake.random_int(min=100000000, max=999999999)
            commission_rate = round(fake.random_number(digits=2), 2)
            cursor.execute(f"INSERT INTO {table_name} (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate))

def insert_orders_for_shoppers(cursor, num_orders):
    # Fetch all shopper IDs
    cursor.execute("SELECT id FROM shoppers")
    shoppers = cursor.fetchall()
    
    for shopper in shoppers:
        shopper_id = shopper[0]
        
        for _ in range(num_orders):
            created_at = fake.date_this_year()
            status = fake.random_element(elements=("complete", "incomplete"))
            total_amount = round(fake.random_number(digits=2), 2)
            
            cursor.execute(f"""
                INSERT INTO orders (shopper_id, created_at, status, total_amount)
                VALUES (%s, %s, %s, %s)
            """, (shopper_id, created_at, status, total_amount))


def insert_order_items(cursor, num_order_items, num_orders, num_products, num_vendors):
    cursor.execute("SELECT id FROM orders")
    orders = cursor.fetchall()
    
    for order in orders:
        order_id = order[0]
        
        for _ in range(num_order_items):
            product_id = fake.random_int(min=1, max=num_products)
            vendor_id = fake.random_int(min=1, max=num_vendors)
            quantity = fake.random_int(min=1, max=10)
            price = round(fake.random_number(digits=2), 2)
            
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, vendor_id, quantity, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, product_id, vendor_id, quantity, price))


def insert_vendor_products(cursor, num_vendors, num_products):
    try:
        cursor.execute("SELECT COUNT(*) FROM vendor_products")
        result = cursor.fetchone()
        
        if result[0] > 0:
            print("Vendor products already exist. Exiting method.")
            return
        
        cursor.execute("SELECT id FROM vendors")
        vendors = cursor.fetchall()
        # Fetch all product IDs
        cursor.execute("SELECT id FROM products")
        products = cursor.fetchall()
        for vendor in vendors:
            vendor_id = vendor[0]
            
            num_products_for_vendor = fake.random_int(min=1, max=num_products)
            
            for _ in range(num_products_for_vendor):
                product_id = random.choice(products)[0] 
                price = round(fake.random_number(digits=2), 2)
                
                cursor.execute("""
                    INSERT INTO vendor_products (vendor_id, product_id, price)
                    VALUES (%s, %s, %s)
                """, (vendor_id, product_id, price))
    except Error as e:
        print(f"Error: {e}")


try:
    connection = mysql.connector.connect(user=user, password=password,
                                         host=host, port=port,
                                         database=database)

    if connection.is_connected():
        print("Successfully connected to the database")

        cursor = connection.cursor()

        # # Insert data into tables
        print("Inserting data into products...")
        insert_fake_data(cursor, "products", 1000)

        print("Inserting data into shoppers...")
        insert_fake_data(cursor, "shoppers", 1000)

        print("Inserting data into vendors...")
        insert_fake_data(cursor, "vendors", 1000)

        # Insert orders for each shopper
        print("Inserting order items for orders...")
        insert_order_items(cursor, num_order_items=5, num_orders=1000, num_products=100, num_vendors=50)

        print("Inserting vendor products...")
        insert_vendor_products(cursor, num_vendors=1000, num_products=1000)

        connection.commit()
        print("Fake data inserted successfully")

        cursor.close()

except Error as e:
    print(f"Error: {e}")

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")
