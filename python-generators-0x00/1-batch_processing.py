import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
   
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="******",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        offset = 0
        while True:
            query = f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            cursor.execute(query)
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

    except Error as e:
        print(f"Error fetching data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
   
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        # Do something with filtered_users; here we just print them
        for user in filtered_users:
            print(f"User: {user['name']}, Age: {user['age']}, Email: {user['email']}")


if __name__ == "__main__":
    batch_processing(batch_size=5)
