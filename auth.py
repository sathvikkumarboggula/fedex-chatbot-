import bcrypt
import random

from db import conn, cursor
from email_utils import send_otp_email

# ==========================================
# GENERATE OTP
# ==========================================

def generate_otp():

    otp = str(random.randint(1000, 9999))

    return otp


# ==========================================
# CREATE USER
# ==========================================

def create_user(username, phone, password):

    # HASH PASSWORD

    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    )

    query = """

    INSERT INTO users
    (username, phone, password)

    VALUES (%s, %s, %s)

    """

    cursor.execute(
        query,
        (
            username,
            phone,
            hashed_password.decode('utf-8')
        )
    )

    conn.commit()


# ==========================================
# CHECK USER EXISTS
# ==========================================

def user_exists(phone):

    query = """

    SELECT * FROM users
    WHERE phone = %s

    """

    cursor.execute(query, (phone,))

    user = cursor.fetchone()

    return user


# ==========================================
# VERIFY LOGIN
# ==========================================

def verify_login(phone, password):

    query = """

    SELECT * FROM users
    WHERE phone = %s

    """

    cursor.execute(query, (phone,))

    user = cursor.fetchone()

    if user:

        stored_password = user["password"]

        if bcrypt.checkpw(
            password.encode('utf-8'),
            stored_password.encode('utf-8')
        ):

            return True

    return False


# ==========================================
# SEND OTP
# ==========================================

def send_signup_otp(email):

    otp = generate_otp()

    send_otp_email(email, otp)

    return otp