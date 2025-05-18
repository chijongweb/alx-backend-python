import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="T!g3rfish",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # Single loop to yield ages one by one
            yield age

    except Error as e:
        print(f" Error streaming user ages: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def compute_average_age():
   
    total_age = 0
    count = 0

    # Loop through the generator and aggregate the values
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    average_age = total_age / count
    print(f" Average age of users: {average_age:.2f}")


# Example usage:
if __name__ == "__main__":
    compute_average_age()
