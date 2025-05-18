import mysql.connector
from mysql.connector import Error

def stream_users():
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="********",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:  
            yield row

    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage:
if __name__ == "__main__":
    for user in stream_users():
        print(user)
