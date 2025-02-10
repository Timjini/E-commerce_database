from faker import Faker
import random

fake = Faker()

def insert_reviews_data(cursor, connection, num_reviews=1000):
    try:
        cursor.execute("SELECT id FROM vendor_products")
        vendor_products = cursor.fetchall()

        cursor.execute("SELECT id FROM shoppers")
        shoppers = cursor.fetchall()

        if not vendor_products or not shoppers:
            print("No vendor products or shoppers found.")
            return

        for _ in range(num_reviews):
            vendor_product_id = random.choice(vendor_products)[0]
            shopper_id = random.choice(shoppers)[0]

            rating = random.randint(1, 5)

            comment = None if random.random() < 0.3 else fake.text(max_nb_chars=200)

            cursor.execute("""
                INSERT INTO reviews (vendor_product_id, shopper_id, rating, comment, created_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """, (vendor_product_id, shopper_id, rating, comment))

        connection.commit()
        print(f"{num_reviews} reviews inserted successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error inserting reviews: {e}")

from datetime import datetime, timedelta

def insert_time_spent_data(cursor, connection, num_records=1000):
    try:
        cursor.execute("SELECT id FROM shoppers")
        shoppers = cursor.fetchall()

        if not shoppers:
            print("No shoppers found.")
            return

        for _ in range(num_records):
            shopper_id = random.choice(shoppers)[0]
            
            duration_minutes = random.randint(1, 120)

            session_date = fake.date_this_year()

            cursor.execute("""
                INSERT INTO time_spent (shopper_id, duration_minutes, session_date)
                VALUES (%s, %s, %s)
            """, (shopper_id, duration_minutes, session_date))

        connection.commit()
        print(f"{num_records} time spent records inserted successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error inserting time spent data: {e}")

