import random
import smtplib
import os

from email.mime.text import MIMEText
from dotenv import load_dotenv

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

# ==========================================
# GENERATE OTP
# ==========================================

def generate_otp():

    otp = str(random.randint(1000, 9999))

    return otp


# ==========================================
# SEND OTP EMAIL
# ==========================================

def send_otp_email(receiver_email, otp):

    # ======================================
    # GET EMAIL FROM .ENV
    # ======================================

    sender_email = os.getenv("EMAIL_USER")

    sender_password = os.getenv("EMAIL_PASS")

    # ======================================
    # EMAIL CONTENT
    # ======================================

    subject = "FedEx Shipment Verification OTP"

    body = f"""

Your FedEx verification OTP is:

{otp}

Do not share this OTP with anyone.

FedEx AI Assistant
"""

    # ======================================
    # CREATE EMAIL
    # ======================================

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # ======================================
    # SMTP SERVER
    # ======================================

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(sender_email, sender_password)

    server.sendmail(
        sender_email,
        receiver_email,
        msg.as_string()
    )

    server.quit()