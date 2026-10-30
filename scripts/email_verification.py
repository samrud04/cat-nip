


CATNIP_EMAIL="aadisayamsatmanan@gmail.com"
CATNIP_APP_PASSWORD="thisisforcatnip"



import os
import secrets
import smtplib
import ssl
import time
from email.message import EmailMessage


OTP_EXPIRY_SECONDS = 5 * 60
RESEND_COOLDOWN_SECONDS = 60

# email -> {"code": str, "expires": float, "sent_at": float}
_pending_otps = {}


def send_otp(recipient_email):
    """Send a six-digit OTP. Returns (success: bool, message: str)."""
    sender_email = os.getenv("CATNIP_EMAIL", "").strip()
    app_password = os.getenv("CATNIP_APP_PASSWORD", "").replace(" ", "")

    if not sender_email or not app_password:
        return (
            False,
            "Email sender is not configured. Set CATNIP_EMAIL and "
            "CATNIP_APP_PASSWORD before starting Cat Nip."
        )

    recipient_email = recipient_email.strip().lower()
    if not recipient_email:
        return False, "Please enter an email address."

    now = time.time()
    previous = _pending_otps.get(recipient_email)

    if previous and now - previous["sent_at"] < RESEND_COOLDOWN_SECONDS:
        remaining = int(RESEND_COOLDOWN_SECONDS - (now - previous["sent_at"]))
        return False, f"Please wait {remaining} seconds before requesting another OTP."

    code = f"{secrets.randbelow(1_000_000):06d}"

    message = EmailMessage()
    message["Subject"] = "Your Cat Nip verification code"
    message["From"] = sender_email
    message["To"] = recipient_email
    message.set_content(
        "Hello!\n\n"
        f"Your Cat Nip email verification code is: {code}\n\n"
        "This code expires in 5 minutes and can only be used once.\n"
        "If you did not request this code, you can ignore this email.\n\n"
        "— Cat Nip"
    )

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, context=context, timeout=20
        ) as server:
            server.login(sender_email, app_password)
            server.send_message(message)

        _pending_otps[recipient_email] = {
            "code": code,
            "expires": now + OTP_EXPIRY_SECONDS,
            "sent_at": now,
        }
        return True, "OTP sent successfully. Please check your inbox."
    except smtplib.SMTPAuthenticationError:
        return (
            False,
            "Gmail authentication failed. Check the sender email and "
            "Google App Password."
        )
    except (smtplib.SMTPException, OSError) as exc:
        return False, f"Could not send the OTP email: {exc}"


def verify_otp(recipient_email, entered_otp):
    """Return True only for the correct, unexpired OTP; successful codes are consumed."""
    recipient_email = recipient_email.strip().lower()
    entered_otp = entered_otp.strip()

    record = _pending_otps.get(recipient_email)
    if not record:
        return False, "Please request an OTP first."

    if time.time() > record["expires"]:
        _pending_otps.pop(recipient_email, None)
        return False, "OTP expired. Please request a new one."

    if not (entered_otp.isdigit() and len(entered_otp) == 6):
        return False, "Enter the six-digit OTP."

    if not secrets.compare_digest(record["code"], entered_otp):
        return False, "Incorrect OTP. Please try again."

    _pending_otps.pop(recipient_email, None)
    return True, "Email verified successfully."


def clear_otp(recipient_email):
    """Clear a pending OTP, for example if the email field is changed."""
    _pending_otps.pop(recipient_email.strip().lower(), None)
