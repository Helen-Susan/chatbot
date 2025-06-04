import mysql.connector
cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="root",
            database="pandeyji_eatery"
        )
def insert_order_item(food_item,quantity,order_id):
    try:
        cursor = cnx.cursor()
        cursor.callproc('insert_order_item',(food_item,quantity,order_id))
       
        cnx.commit()
        cursor.close()

        print("Order item inserted successfully!")

        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occurred: {e}")
        # Rollback changes if necessary
        cnx.rollback()

        return -1
    
def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Insert into order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Call stored procedure with correct tuple format
    cursor.callproc('get_deliverytime', (order_id,))

    cnx.commit()
    cursor.close()

def get_total_order_price(order_id):
    cursor=cnx.cursor()
    query=f"SELECT get_total_order_price({order_id})"   
    cursor.execute(query)
    result=cursor.fetchone()[0]
    cursor.close()
    return result
def get_order_status(order_id: int):
    try:
       
        cursor = cnx.cursor()
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()
        cursor.close()
        cnx.close()
        
        if result:
            return result[0]
        return None

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
def get_next_order_id():
    cursor=cnx.cursor()
    query="SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    cursor.close()
    if result is None:
        return 1
    else:
        return result +1
def get_delieverytime(order_id):
    if not cnx.is_connected():
        cnx.reconnect()
    
    cursor = cnx.cursor()
    try:
        # Use parameterized query to avoid SQL injection
        query = "SELECT get_delieverytimeslot(%s)"
        cursor.execute(query, (order_id,))
        
        result = cursor.fetchone()  # Fetch one row
        if result:
            return result[0]  # Return the delivery time value
        else:
            return None
    finally:
        cursor.close()



