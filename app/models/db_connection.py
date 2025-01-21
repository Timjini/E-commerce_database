import mysql.connector
from app.config import DATABASE_CONFIG

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
