import os
import smtplib
import ssl
import time
from email.message import EmailMessage
from flask import current_app


def _get_mail_output_dir():
    # Priority:
    # 1. App config
    # 2. Environment variable
    # 3. Default ./mail_out
    return (
        current_app.config.get("MAIL_OUTPUT_DIR")
        or os.getenv("MAIL_OUTPUT_DIR")
        or os.path.join(os.getcwd(), "mail_out")
    )


def send_email(to, subject, body):
    """
    Sends email either via:
    - SMTP (if MAIL_SERVER env exists)
    - File output (for dev/test)
    """

    mail_server = os.getenv("MAIL_SERVER")

    # Build email
    msg = EmailMessage()
    from_addr = os.getenv("MAIL_USERNAME", "no-reply@studenthub.local")
    msg["From"] = from_addr
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    # -----------------------------
    # SMTP MODE
    # -----------------------------
    if mail_server:
        mail_port = int(os.getenv("MAIL_PORT", "587"))
        mail_user = os.getenv("MAIL_USERNAME")
        mail_pass = os.getenv("MAIL_PASSWORD")
        use_tls = os.getenv("MAIL_USE_TLS", "true").lower() == "true"

        context = ssl.create_default_context()

        with smtplib.SMTP(mail_server, mail_port, timeout=10) as server:
            if use_tls:
                server.starttls(context=context)

            if mail_user and mail_pass:
                server.login(mail_user, mail_pass)

            server.sendmail(from_addr, [to], msg.as_string())

        return True

    # -----------------------------
    # FILE MODE (DEV / TEST)
    # -----------------------------
    out_dir = _get_mail_output_dir()
    os.makedirs(out_dir, exist_ok=True)

    filename = f"mail_{int(time.time() * 1000)}.eml"
    path = os.path.join(out_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(msg.as_string())

    return True
