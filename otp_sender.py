import smtplib
from email.message import EmailMessage
import os

def send_otp(email, otp):
    sender_email = os.getenv("EMAIL_ID")
    app_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not app_password:
        print("Email credentials not set")
        return False

    try:
        msg = EmailMessage()
        msg.set_content(f"Your OTP is: {otp}")
        msg["Subject"] = "Your OTP Verification Code"
        msg["From"] = sender_email
        msg["To"] = email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print("✅ OTP sent successfully")
        return True

    except Exception as e:
        print("❌ Email sending failed:", e)
        return False
