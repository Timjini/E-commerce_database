from faker import Faker
from faker_commerce import Provider as CommerceProvider
import random

fake = Faker()
fake.add_provider(CommerceProvider)

def insert_fake_data(cursor, connection, table_name, num_rows=1000):
    print(f"Inserting data into {table_name}...")
    
    try:
        # map to track vendor.email and shopper.email to avoid duplicates and vendor.tax_number
        used_emails = set()
        used_tax_numbers = set()

        # Fetch existing emails & tax numbers from the database once
        if table_name == "shoppers":
            cursor.execute("SELECT email FROM shoppers")
            used_emails.update(row[0] for row in cursor.fetchall())
        elif table_name == "vendors":
            cursor.execute("SELECT contact_email, tax_number FROM vendors")
            for email, tax_number in cursor.fetchall():
                used_emails.add(email)
                used_tax_numbers.add(tax_number)

        for _ in range(num_rows):
            if table_name == "products":
                name = fake.ecommerce_name()
                cost = round(random.uniform(0.01, 99.99), 2)
                description = f"{name}: {fake.sentence()}"
                cursor.execute(
                    "INSERT INTO products (name, cost, description) VALUES (%s, %s, %s)",
                    (name, cost, description)
                )
            elif table_name == "shoppers":
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                # Generate a unique email
                email = fake.email()
                while email in used_emails:
                    email = fake.email()
                used_emails.add(email)

                phone_number = fake.phone_number()[:20]
                address = fake.address()
                is_member = fake.boolean()
                cursor.execute(
                    "INSERT INTO shoppers (first_name, last_name, email, phone_number, address, is_member) VALUES (%s, %s, %s, %s, %s, %s)",
                    (first_name, last_name, email, phone_number, address, is_member)
                )
            elif table_name == "vendors":
                contact_name = fake.name()
                company_name = fake.company()
                
                # Generate a unique email
                contact_email = fake.email()
                while contact_email in used_emails:
                    contact_email = fake.email()
                used_emails.add(contact_email)

                contact_phone = fake.phone_number()[:20]
                address = fake.address()
                
                # Generate a unique tax number
                tax_number = fake.random_int(min=100000000, max=999999999)
                while tax_number in used_tax_numbers:
                    tax_number = fake.random_int(min=100000000, max=999999999)
                used_tax_numbers.add(tax_number)

                commission_rate = round(random.uniform(0.01, 100.00), 2)
                cursor.execute(
                    "INSERT INTO vendors (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (contact_name, company_name, contact_email, contact_phone, address, tax_number, commission_rate)
                )

        connection.commit()
        print(f"{num_rows} rows inserted into {table_name}")

    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error inserting data into {table_name}: {e}")


            
def insert_orders_for_shoppers(cursor, num_orders):
    # fetch all shopper IDs
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

        for vendor in vendors:
            vendor_id = vendor[0]
            commission_rate = vendor[1]

            for product in products:
                product_id = product[0]
                product_cost = product[1]

                # calculate vendor product based on commission
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
        connection.rollback()
        print(f"Error inserting vendor-products: {e}")
