import mysql.connector
from mysql.connector import Error

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
            if command:  # Ignore empty commands
                try:
                    cursor.execute(command)  # Execute each command
                    print(f"Executed: {command}")
                except mysql.connector.Error as err:
                    print(f"Error executing command: {err}")
        
        # Commit the transaction (in case of INSERTs or other changes)
        connection.commit()
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()
