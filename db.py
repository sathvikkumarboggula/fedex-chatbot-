import mysql.connector

# ==========================================
# MYSQL CONNECTION
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fedex_chatbot"
)

cursor = conn.cursor(dictionary=True)

# ==========================================
# GET TRACKING DETAILS
# ==========================================

def get_tracking_details(tracking_number):

    query = """

    SELECT * FROM shipments
    WHERE tracking_number = %s

    """

    cursor.execute(query, (tracking_number,))

    result = cursor.fetchone()

    return result