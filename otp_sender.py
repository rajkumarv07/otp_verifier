import os
import requests

def send_otp(email, otp):
    api_key = os.getenv("SENDGRID_API_KEY")
    from_email = os.getenv("FROM_EMAIL")

    if not api_key or not from_email:
        print("SendGrid environment variables missing")
        return False

    data = {
        "personalizations": [
            {
                "to": [{"email": email}],
                "subject": "Your OTP Verification Code"
            }
        ],
        "from": {"email": from_email},
        "content": [
            {"type": "text/plain", "value": f"Your OTP is: {otp}"}
        ]
    }

    r = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=data
    )

    return r.status_code == 202
