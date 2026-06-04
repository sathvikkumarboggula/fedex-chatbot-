from db import get_tracking_details
from email_utils import generate_otp, send_otp_email

# ==========================================
# TRACK SHIPMENT
# ==========================================

def track_shipment(tracking_number):

    # Remove extra spaces and convert to uppercase
    tracking_number = tracking_number.strip().upper()

    # Fetch shipment details from database
    shipment = get_tracking_details(tracking_number)

    # ======================================
    # VALID TRACKING NUMBER
    # ======================================

    if shipment:

        response = f"""
📦 Shipment Found

━━━━━━━━━━━━━━━━━━

🔖 Tracking Number:
{shipment['tracking_number']}

👤 Sender:
{shipment['sender_name']}

📞 Sender Phone:
{shipment['sender_phone']}

📧 Sender Email:
{shipment['sender_email']}

🏠 Sender Address:
{shipment['sender_address']}

━━━━━━━━━━━━━━━━━━

👤 Receiver:
{shipment['receiver_name']}

📞 Receiver Phone:
{shipment['receiver_phone']}

🏠 Receiver Address:
{shipment['receiver_address']}

━━━━━━━━━━━━━━━━━━

📍 Current Location:
{shipment['current_location']}

🚚 Delivery Status:
{shipment['delivery_status']}
"""

        return response

    # ======================================
    # INVALID TRACKING NUMBER
    # ======================================

    else:
        
        otp = generate_otp()
        
        send_otp_email(
            "sathvikkumarboggula@gmail.com",
            otp
        )
            
            
        return {
            "status": "invalid",
            "otp": otp,
            "message": """
    ❌ Invalid Tracking Number

    📧 OTP has been sent to your email.

    Please enter the OTP below.
    """
       }
    