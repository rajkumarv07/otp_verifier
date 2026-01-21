import random
from config import OTP_LENGTH

def generate_otp():
    """Generate a random numeric OTP"""
    return ''.join(str(random.randint(0, 9)) for _ in range(OTP_LENGTH))
