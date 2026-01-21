import time
import hashlib

def hash_otp(otp):
    """Hash OTP using SHA-256"""
    return hashlib.sha256(otp.encode()).hexdigest()

def verify_otp_gui(entered_otp, hashed_otp, expiry_time, attempts_left):
    if time.time() > expiry_time:
        return False, "OTP expired"

    if hash_otp(entered_otp) == hashed_otp:
        return True, "OTP verified successfully"

    return False, f"Incorrect OTP. Attempts left: {attempts_left - 1}"
