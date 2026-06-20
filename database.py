import sqlite3


def create_db():

    conn = sqlite3.connect("fedex.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shipments(

        shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,

        sender_name TEXT,
        sender_phone TEXT,
        sender_address TEXT,
        sender_zip TEXT,

        receiver_name TEXT,
        receiver_phone TEXT,
        receiver_address TEXT,
        receiver_zip TEXT,

        package_type TEXT,
        service_type TEXT,
        shipment_type TEXT,

        weight REAL,
        length REAL,
        width REAL,
        height REAL,

        billed_weight REAL,
        estimated_rate REAL
    )
    """)

    conn.commit()
    conn.close()


create_db()