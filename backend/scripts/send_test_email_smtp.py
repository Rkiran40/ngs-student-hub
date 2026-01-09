#!/usr/bin/env python3
r"""Send a test email using explicit SMTP env vars or the app's mailer.

This script is useful to verify SMTP connectivity to MailHog or a real SMTP provider
(eg: SendGrid, Mailgun, AWS SES) using the same env vars the app reads.

Usage examples:
  # Quick local MailHog test
  MAIL_SERVER=localhost MAIL_PORT=1025 MAIL_USE_TLS=False .venv\\Scripts\\python backend/scripts/send_test_email_smtp.py --to you@example.com

  # Test using the app's `send_email` helper (boots the app)
  .venv\\Scripts\\python backend/scripts/send_test_email_smtp.py --to you@example.com --use-app

Env vars used (either SMTP_* or MAIL_* are accepted by the app):
  SMTP_SERVER / MAIL_SERVER
  SMTP_PORT / MAIL_PORT
  SMTP_USER / MAIL_USERNAME
  SMTP_PASSWORD / MAIL_PASSWORD
  SMTP_USE_TLS / MAIL_USE_TLS
  SMTP_FROM / MAIL_FROM

Exit codes:
  0 - success (email accepted by SMTP server or app send_email completed)
  1 - failure (could not connect/auth/send)

"""
import argparse
import os
import smtplib
import ssl
import sys
import time


def send_via_smtp(to: str, subject: str, body: str) -> bool:
    server = os.environ.get('SMTP_SERVER') or os.environ.get('MAIL_SERVER')
    port = os.environ.get('SMTP_PORT') or os.environ.get('MAIL_PORT')
    user = os.environ.get('SMTP_USER') or os.environ.get('MAIL_USERNAME') or os.environ.get('MAIL_USER')
    password = os.environ.get('SMTP_PASSWORD') or os.environ.get('MAIL_PASSWORD')
    use_tls = (os.environ.get('SMTP_USE_TLS', '0').lower() in ('1', 'true', 'yes')) or (os.environ.get('MAIL_USE_TLS', '0').lower() in ('1', 'true', 'yes'))
    from_env = os.environ.get('SMTP_FROM') or os.environ.get('MAIL_FROM')

    if not server:
        print('No SMTP server configured in env (SMTP_SERVER or MAIL_SERVER required)')
        return False

    port_int = int(port) if port else (587 if use_tls else 25)
    try:
        if use_tls:
            context = ssl.create_default_context()
            with smtplib.SMTP(server, port_int, timeout=10) as smtp:
                smtp.starttls(context=context)
                if user and password:
                    smtp.login(user, password)
                from_addr = from_env or user or (f"noreply@{server}")
                msg = f"From: {from_addr}\nTo: {to}\nSubject: {subject}\n\n{body}\n"
                smtp.sendmail(from_addr, [to], msg)
        else:
            with smtplib.SMTP(server, port_int, timeout=10) as smtp:
                if user and password:
                    smtp.login(user, password)
                from_addr = from_env or user or (f"noreply@{server}")
                msg = f"From: {from_addr}\nTo: {to}\nSubject: {subject}\n\n{body}\n"
                smtp.sendmail(from_addr, [to], msg)
        print('SMTP send succeeded')
        return True
    except Exception as e:  # pragma: no cover - integration helper
        print('SMTP send failed:', str(e))
        return False


def main():
    parser = argparse.ArgumentParser(description='Send a test email using SMTP or the app helper')
    parser.add_argument('--to', required=True, help='Recipient email address')
    parser.add_argument('--subject', default='Test email from StudentHub', help='Email subject')
    parser.add_argument('--body', default='This is a test email from StudentHub', help='Email body')
    parser.add_argument('--use-app', action='store_true', help='Boot the Flask app and call send_email (uses app config/env vars)')

    args = parser.parse_args()

    if args.use_app:
        # Ensure repository root is on sys.path so `import backend` works reliably
        try:
            import pathlib
            repo_root = str(pathlib.Path(__file__).resolve().parents[2])
            if repo_root not in sys.path:
                sys.path.insert(0, repo_root)
        except Exception:
            pass

        # Import lazily so this script can be used without Flask if desired
        try:
            from backend.app import create_app
            app = create_app()
            with app.app_context():
                from backend.email_utils import send_email
                ok = send_email(args.to, args.subject, args.body)
                print('send_email returned:', ok)
                sys.exit(0 if ok else 1)
        except Exception as e:  # pragma: no cover - integration helper
            print('Error when calling app send_email:', e)
            sys.exit(1)

    ok = send_via_smtp(args.to, args.subject, args.body)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
