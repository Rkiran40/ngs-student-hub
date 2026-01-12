import os
import smtplib
import ssl
import time
from email.message import EmailMessage

try:
    from flask import current_app
except Exception:
    # Allow using this module without Flask installed (for local tests)
    current_app = None


# -------------------------
# Helpers
# -------------------------

def _get_mail_output_dir():
    # Priority: app config -> env -> default ./mail_out
    return (
        (current_app.config.get("MAIL_OUTPUT_DIR") if current_app else None)
        or os.getenv("MAIL_OUTPUT_DIR")
        or os.path.join(os.getcwd(), "mail_out")
    )


def _build_message(from_addr: str, to: str, subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    return msg


# -------------------------
# Main mail sender
# -------------------------

def send_email(to: str, subject: str, body: str, max_retries: int = 2) -> bool:
    """
    Send an email using SMTP configured from Flask config or environment.

    Features:
    - Prefers Flask `current_app.config`
    - Supports STARTTLS (587) and SSL (465)
    - Retries on failure with backoff
    - Writes .eml to disk if SMTP fails
    - Returns True on success, False on failure
    """

    cfg = getattr(current_app, "config", {}) if current_app else os.environ

    mail_server = cfg.get("MAIL_SERVER") or os.getenv("MAIL_SERVER")
    mail_port = int(cfg.get("MAIL_PORT") or os.getenv("MAIL_PORT", 587))
    mail_user = cfg.get("MAIL_USERNAME") or os.getenv("MAIL_USERNAME")
    mail_pass = cfg.get("MAIL_PASSWORD") or os.getenv("MAIL_PASSWORD")

    mail_use_tls = str(
        cfg.get("MAIL_USE_TLS") or os.getenv("MAIL_USE_TLS", "True")
    ).lower() in ("true", "1", "yes")

    mail_use_ssl = str(
        cfg.get("MAIL_USE_SSL") or os.getenv("MAIL_USE_SSL", "False")
    ).lower() in ("true", "1", "yes")

    default_sender = (
        cfg.get("MAIL_DEFAULT_SENDER")
        or os.getenv("MAIL_DEFAULT_SENDER")
        or mail_user
        or "no-reply@studenthub.local"
    )

    msg = _build_message(default_sender, to, subject, body)

    # --------------------------------------------------
    # Fallback: SMTP not configured → save to file
    # --------------------------------------------------
    if not mail_server:
        try:
            out_dir = _get_mail_output_dir()
            os.makedirs(out_dir, exist_ok=True)
            filename = f"mail_{int(time.time() * 1000)}.eml"
            path = os.path.join(out_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(msg.as_string())

            if current_app:
                current_app.logger.warning(
                    f"SMTP not configured. Mail saved to {path}"
                )
            return True
        except Exception as e:
            if current_app:
                current_app.logger.exception(
                    f"Failed to write mail to file fallback: {e}"
                )
            return False

    # --------------------------------------------------
    # SMTP send with retry
    # --------------------------------------------------
    last_exc = None

    for attempt in range(1, max_retries + 1):
        try:
            # SSL (465)
            if mail_use_ssl or mail_port == 465:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(
                    mail_server,
                    mail_port,
                    context=context,
                    timeout=30,   # ⬅ increased timeout
                ) as server:
                    server.ehlo()
                    if mail_user and mail_pass:
                        server.login(mail_user, mail_pass)
                    server.send_message(msg)

            # STARTTLS (587)
            else:
                context = ssl.create_default_context()
                with smtplib.SMTP(
                    mail_server,
                    mail_port,
                    timeout=30,   # ⬅ increased timeout
                ) as server:
                    server.ehlo()
                    if mail_use_tls:
                        server.starttls(context=context)
                        server.ehlo()
                    if mail_user and mail_pass:
                        server.login(mail_user, mail_pass)
                    server.send_message(msg)

            if current_app:
                current_app.logger.info(
                    f"Email sent to {to} via {mail_server}:{mail_port}"
                )
            return True

        except Exception as exc:
            last_exc = exc
            if current_app:
                current_app.logger.exception(
                    f"Attempt {attempt} failed sending email to {to}: {exc}"
                )
            # Progressive backoff: 1s, 2s, 3s...
            time.sleep(attempt)

    # --------------------------------------------------
    # All retries failed → save .eml
    # --------------------------------------------------
    try:
        out_dir = _get_mail_output_dir()
        os.makedirs(out_dir, exist_ok=True)
        filename = f"mail_failed_{int(time.time() * 1000)}.eml"
        path = os.path.join(out_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(msg.as_string())

        if current_app:
            current_app.logger.error(
                f"All SMTP attempts failed; mail saved to {path}"
            )
    except Exception as e:
        if current_app:
            current_app.logger.exception(
                f"Failed to save failed mail to file: {e}"
            )

    return False
