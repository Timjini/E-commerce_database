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
    """Retry connecting to the database up to 10 times with a 5-second interval."""
    for _ in range(10):
        connection = get_db_connection()
        if connection and connection.is_connected():
            return connection
        time.sleep(5)
    return None 

def check_tables_exist(connection, tables):
    """Check if the given tables exist in the database."""
    cursor = connection.cursor()
    for table in tables:
        cursor.execute(f"SHOW TABLES LIKE '{table}'")
        result = cursor.fetchone()
        if not result:
            print(f"Table {table} does not exist. Waiting for table to be created...")
            return False
    return True

def create_trigger():
    """Create the trigger to validate reviews before insert."""
    connection = get_db_connection()
    if connection is not None:
        cursor = connection.cursor()

        # Trigger creation SQL
        trigger_sql = """
        DELIMITER $$

        CREATE TRIGGER validate_review_before_insert
        BEFORE INSERT ON reviews
        FOR EACH ROW
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                WHERE oi.vendor_product_id = NEW.vendor_product_id
                AND o.shopper_id = NEW.shopper_id
            ) THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Cannot review a product that has not been purchased.';
            END IF;
        END$$

        DELIMITER ;
        """
        try:
            # Execute the trigger creation
            cursor.execute(trigger_sql)
            connection.commit()
            print("Trigger created successfully.")
        except mysql.connector.Error as err:
            print(f"Error creating trigger: {err}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to establish a database connection.")

# Calling the function to create the trigger when the script runs
create_trigger()
