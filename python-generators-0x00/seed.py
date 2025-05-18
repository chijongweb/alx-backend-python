import mysql.connector
from mysql.connector import Error
import pandas as pd
import uuid

#  Database Connection 
def connect_db():
    """Connect to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="T!g3rfish"
        )
        if connection.is_connected():
            print(" Connected to MySQL server")
        return connection
    except Error as e:
        print(f" Error connecting to MySQL server: {e}")
        return None

#  Database Creation 
def create_database(connection):
    """Create the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print(" Database 'ALX_prodev' is ready.")
    except Error as e:
        print(f" Error creating database: {e}")

#  Connect to ALX_prodev 
def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="********",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print(" Connected to database 'ALX_prodev'")
        return connection
    except Error as e:
        print(f" Error connecting to database ALX_prodev: {e}")
        return None

#  Table Creation
def create_table(connection):
    """Create the user_data table if it does not exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        connection.commit()
        print(" Table 'user_data' is ready.")
    except Error as e:
        print(f" Error creating table: {e}")

#  Data Insertion 
def insert_data(connection, data):
    """Insert data into the user_data table if it does not already exist."""
    cursor = connection.cursor()
    for _, row in data.iterrows():
        user_id = str(uuid.uuid4())  # Generate a UUID for each user
        try:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, row['name'], row['email'], row['age']))
            connection.commit()
            print(f" Inserted: {row['name']}, {row['email']}, {row['age']}")
        except Error as e:
            print(f" Error inserting data: {e}")

#  Main Execution 
if __name__ == "__main__":
    # Connect to MySQL Server and create the database
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
    
    # Connect to the ALX_prodev database
    prodev_connection = connect_to_prodev()
    
    # Create the table if it doesn't exist
    if prodev_connection:
        create_table(prodev_connection)
    
        # Read data from CSV
        try:
            data = pd.read_csv('user_data.csv')
            insert_data(prodev_connection, data)
        except FileNotFoundError:
            print(" CSV file not found. Please place 'user_data.csv' in the same directory.")
        
        # Close the database connection
        prodev_connection.close()
        print(" Database connection closed.")
