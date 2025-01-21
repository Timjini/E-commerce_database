from faker import Faker
import random

fake = Faker()

def insert_fake_data(cursor, connection, table_name, num_rows=1000):
    print(f"Inserting data into {table_name}...")
    try:
        for _ in range(num_rows):
            if table_name == "products":
                name = fake.word()
                cost = round(fake.random_number(digits=2), 2)
                description = fake.text(max_nb_chars=200)
                cursor.execute(
                    f"INSERT INTO {table_name} (name, cost, description) VALUES (%s, %s, %s)",
                    (name, cost, description)
                )
            elif table_name == "shoppers":
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                phone_number = fake.phone_number()[:20]
                address = fake.address()
                is_member = fake.boolean()
                cursor.execute(
                    f"INSERT INTO {table_name} (first_name, last_name, email, phone_number, address, is_member) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, phone_number, address, is_member)
                )
            elif table_name == "vendors":
                contact_name = fake.name()
                company_name = fake.company()
                contact_email = fake.email()
                contact_phone = fake.phone_number()[:20]
                address = fake.address()
                tax_number = fake.random_int(min=100000000, max=999999999)
                commission_rate = round(fake.random_number(digits=2), 2)
                cursor.execute(
                    f"INSERT INTO {table_name} (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate)
                )
        # Commit the transaction
        connection.commit()
        print(f"{num_rows} rows inserted into {table_name}")
    except Exception as e:
        # Rollback in case of any error
        connection.rollback()
        print(f"Error inserting data into {table_name}: {e}")

            
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

def insert_order_items(cursor, connection, num_order_items, num_orders, num_products, num_vendors):
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

def insert_vendor_products(cursor, connection):
    try:
        # get vendors
        cursor.execute("SELECT id, commission_rate FROM vendors")
        vendors = cursor.fetchall()

        if not vendors:
            print("No vendors found.")
            return

        # get products
        cursor.execute("SELECT id, cost FROM products")
        products = cursor.fetchall()

        if not products:
            print("No products found.")
            return

        # vendor-product associations
        for vendor in vendors:
            vendor_id = vendor[0]
            commission_rate = vendor[1]

            for product in products:
                product_id = product[0]
                product_cost = product[1]

                # calcualte vendor product based on commission
                price = round(product_cost * (1 + commission_rate / 100), 2)

                try:
                    cursor.execute("""
                        INSERT INTO vendor_products (vendor_id, product_id, price)
                        VALUES (%s, %s, %s)
                    """, (vendor_id, product_id, price))
                except Exception as e:
                    print(f"Error inserting vendor product for vendor_id {vendor_id}, product_id {product_id}: {e}")
                    connection.rollback()

        connection.commit()
        print("Vendor-product associations inserted successfully.")
    except Exception as e:
        # rollback when issue
        connection.rollback()
        print(f"Error inserting vendor-products: {e}")
