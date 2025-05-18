import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="T!g3rfish",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
        cursor.execute(query)
        result = cursor.fetchall()
        
        return result

    except Error as e:
        print(f" Error fetching paginated data: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size):
   
    offset = 0

    while True:
        page_data = paginate_users(page_size, offset)
        if not page_data:
            break
        yield page_data
        offset += page_size


# Example usage:
if __name__ == "__main__":
    print(" Fetching paginated data lazily:")
    for page in lazy_paginate(page_size=5):
        print(f"--- Page ---")
        for user in page:
            print(f"{user['name']} | {user['email']} | {user['age']}")
