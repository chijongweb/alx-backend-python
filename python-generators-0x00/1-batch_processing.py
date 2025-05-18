import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="T!g3rfish",
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
        print(f"❌ Error fetching data: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
  
    all_filtered_users = []

    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        all_filtered_users.extend(filtered_users)  # Collect all filtered users
    
    return all_filtered_users



if __name__ == "__main__":
    users = batch_processing(batch_size=5)
    print("✅ Filtered Users Over 25:")
    for user in users:
        print(f"User: {user['name']}, Age: {user['age']}, Email: {user['email']}")
