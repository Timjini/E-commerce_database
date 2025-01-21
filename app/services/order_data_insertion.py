from faker import Faker

fake = Faker()

def insert_orders_data(cursor, connection, num_orders):
    num_orders = 1000
    try:
        cursor.execute("SELECT id FROM shoppers")
        shoppers = cursor.fetchall()

        if not shoppers:
            print("No shoppers found.")
            return

        statuses = ['complete', 'incomplete']

        # Insert random orders
        for _ in range(num_orders):
            shopper_id = random.choice(shoppers)[0]
            status = random.choice(statuses)

            try:
                # Insert the order with total_amount set to 0
                cursor.execute("""
                    INSERT INTO orders (shopper_id, status, total_amount)
                    VALUES (%s, %s, %s)
                """, (shopper_id, status, 0.00))
            except Exception as e:
                print(f"Error inserting order for shopper_id {shopper_id}: {e}")
                connection.rollback()

        # Commit the changes
        connection.commit()
        print(f"{num_orders} orders inserted successfully.")
    except Exception as e:
        # Rollback if any critical error occurs
        connection.rollback()
        print(f"Error inserting orders: {e}")

def inset_order_items_data(cursor, connection, max_items_per_order=5):
    try:
        # Fetch all orders
        cursor.execute("SELECT id, total_amount FROM orders")
        orders = cursor.fetchall()

        # Fetch vendor products with vendor commission rates
        cursor.execute("""
            SELECT 
                vendor_products.id AS vendor_product_id,
                vendor_products.price AS base_price,
                vendors.commission_rate
            FROM vendor_products
            JOIN vendors ON vendor_products.vendor_id = vendors.id
        """)
        vendor_products = cursor.fetchall()

        if not orders or not vendor_products:
            print("No orders or vendor products available.")
            return

        # Iterate through each order to create order items
        for order in orders:
            order_id, current_total = order
            total_amount = current_total or 0
            num_items = random.randint(1, max_items_per_order)
            # Add items to this order
            for _ in range(num_items):
                vendor_product = random.choice(vendor_products)
                vendor_product_id = vendor_product[0]
                base_price = vendor_product[1]
                commission_rate = vendor_product[2]

                # Calculate item price with commission
                item_price = round(base_price * (1 + commission_rate / 100), 2)
                quantity = random.randint(1, 5)  # Random quantity

                # Insert the order item
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, vendor_id, quantity, price)
                    SELECT %s, vendor_products.product_id, vendor_products.vendor_id, %s, %s
                    FROM vendor_products
                    WHERE vendor_products.id = %s
                """, (order_id, quantity, item_price, vendor_product_id))

                # Update the order's total amount
                total_amount += item_price * quantity

            # Update the total amount in the orders table
            cursor.execute("UPDATE orders SET total_amount = %s WHERE id = %s", (total_amount, order_id))

        # Commit all changes
        connection.commit()
        print(f"Order items created successfully and totals updated.")
    except Exception as e:
        print(f"Error creating order items: {e}")
