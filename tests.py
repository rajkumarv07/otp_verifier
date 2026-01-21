from otp_verifier import hash_otp

otp = "123456"
hashed = hash_otp(otp)

assert hashed != otp
assert len(hashed) == 64

print("Hashing test passed.")
