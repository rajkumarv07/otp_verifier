from flask import Flask, render_template, request, redirect, session, flash
import time
import os

from otp_generator import generate_otp
from otp_sender import send_otp
from otp_verifier import hash_otp, verify_otp_gui
from config import OTP_EXPIRY_TIME, MAX_ATTEMPTS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")

        otp = generate_otp()
        session["otp_hash"] = hash_otp(otp)
        session["expiry"] = time.time() + OTP_EXPIRY_TIME
        session["attempts"] = MAX_ATTEMPTS

        try:
            send_otp(email, otp)
        except Exception as e:
            flash("Failed to send OTP. Please try again later.")
            print(f"Error sending OTP: {e}")

        return redirect("/verify")

    return render_template("index.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if "otp_hash" not in session:
        return redirect("/")

    message = ""

    if request.method == "POST":
        entered = request.form.get("otp")

        success, msg = verify_otp_gui(
            entered,
            session.get("otp_hash", ""),
            session.get("expiry", 0),
            session.get("attempts", 0),
        )

        if success:
            session.clear()
            return render_template("verify.html", success=True)

        else:
            session["attempts"] -= 1
            if session["attempts"] <= 0:
                session.clear()
                flash("Too many attempts. Please request a new OTP.")
                return redirect("/")

            message = msg

    return render_template("verify.html", message=message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
