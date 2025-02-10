from faker import Faker
import random

fake = Faker()

def insert_orders_data(cursor, connection, num_orders=10000):
    try:
        cursor.execute("SELECT id FROM shoppers")
        shoppers = cursor.fetchall()

        if not shoppers:
            print("No shoppers found.")
            return

        statuses = ['complete', 'incomplete']

        for _ in range(num_orders):
            shopper_id = random.choice(shoppers)[0]
            status = random.choice(statuses)

            try:
                cursor.execute("""
                    INSERT INTO orders (shopper_id, status, total_amount)
                    VALUES (%s, %s, %s)
                """, (shopper_id, status, 0.00))
            except Exception as e:
                print(f"Error inserting order for shopper_id {shopper_id}: {e}")
                connection.rollback()

        connection.commit()
        print(f"{num_orders} orders inserted successfully.")
    except Exception as e:
        connection.rollback()
        print(f"Error inserting orders: {e}")

def insert_order_items_data(cursor, connection, max_items_per_order=3):
    try:
        cursor.execute("""
            SELECT 
                vendor_products.id AS vendor_product_id,
                vendor_products.price AS base_price,
                vendors.commission_rate
            FROM vendor_products
            JOIN vendors ON vendor_products.vendor_id = vendors.id
        """)
        vendor_products = cursor.fetchall()

        # Fetch all orders
        cursor.execute("SELECT id, total_amount FROM orders")
        orders = cursor.fetchall()

        if not orders or not vendor_products:
            print("No orders or vendor products available.")
            return

        for order in orders:
            order_id, current_total = order
            total_amount = current_total or 0
            num_items = random.randint(1, max_items_per_order)
            for _ in range(num_items):
                vendor_product = random.choice(vendor_products)
                vendor_product_id = vendor_product[0]
                base_price = vendor_product[1]
                commission_rate = vendor_product[2]

                item_price = round(base_price * (1 + commission_rate / 100), 2)
                quantity = random.randint(1, 5)

                cursor.execute("SELECT COUNT(*) FROM vendors WHERE id = %s", (vendor_product[2],))
                vendor_exists = cursor.fetchone()[0]
                if vendor_exists:
                    cursor.execute("""
                        INSERT INTO order_items (order_id, vendor_product_id, vendor_id, quantity, price)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (order_id, vendor_product_id, vendor_product[2], quantity, item_price))
                else:
                    print(f"Vendor ID {vendor_product[2]} does not exist.")

                total_amount += item_price * quantity

            cursor.execute("UPDATE orders SET total_amount = %s WHERE id = %s", (total_amount, order_id))

        connection.commit()
        print(f"Order items created successfully and totals updated.")
    except Exception as e:
        print(f"Error creating order items: {e}")

def insert_revenue_data(cursor, connection):
    try:
        cursor.execute("""
            SELECT 
                oi.order_id,
                oi.vendor_id,
                oi.price,
                v.commission_rate
            FROM order_items oi
            JOIN vendors v ON oi.vendor_id = v.id
        """)
        order_items = cursor.fetchall()

        if not order_items:
            print("No order items found.")
            return

        for item in order_items:
            order_id, vendor_id, item_price, commission_rate = item
            commission_amount = round(item_price * (commission_rate / 100), 2)

            try:
                cursor.execute("""
                    INSERT INTO revenue (order_id, vendor_id, commission_amount)
                    VALUES (%s, %s, %s)
                """, (order_id, vendor_id, commission_amount))
            except Exception as e:
                print(f"Error inserting revenue for order_id {order_id}, vendor_id {vendor_id}: {e}")
                connection.rollback()

        connection.commit()
        print("Revenue data inserted successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error inserting revenue data: {e}")

def insert_cost_data(cursor, connection):
    try:
        cursor.execute("""
            SELECT 
                oi.order_id,
                oi.vendor_id,
                oi.price,
                v.commission_rate
            FROM order_items oi
            JOIN vendors v ON oi.vendor_id = v.id
        """)
        order_items = cursor.fetchall()

        if not order_items:
            print("No order items found.")
            return

        cost_types = ['delivery_failure', 're_attempt', 'return_fraud']

        for item in order_items:
            order_id, vendor_id, item_price, commission_rate = item
            for cost_type in cost_types:
                # possible costs
                if cost_type == 'delivery_failure':
                    cost_amount = round(float(item_price) * 0.10, 2)  # 10%
                elif cost_type == 're_attempt':
                    cost_amount = round(float(item_price) * 0.05, 2)  # 5%
                elif cost_type == 'return_fraud':
                    cost_amount = round(float(item_price) * 0.15, 2)  # 15%

                cursor.execute("""
                    INSERT INTO costs (order_id, type, cost_amount)
                    VALUES (%s, %s, %s)
                """, (order_id, cost_type, cost_amount))

        connection.commit()
        print("Cost data inserted successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error inserting cost data: {e}")
