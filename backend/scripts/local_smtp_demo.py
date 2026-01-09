#!/usr/bin/env python3
"""Local SMTP demo: start an in-process SMTP debug server, send a test email using the app, and report results.

Usage:
  .venv\Scripts\python backend/scripts/local_smtp_demo.py --to you@example.com --port 2505

This avoids Docker and runs fully in Python for quick verification in CI or locally.
"""
import argparse
import time
import sys
import threading
from aiosmtpd.controller import Controller


class CapturingHandler:
    def __init__(self):
        self.messages = []

    async def handle_DATA(self, server, session, envelope):
        try:
            payload = envelope.content.decode('utf-8', errors='replace')
        except Exception:
            payload = str(envelope.content)
        record = {
            'peer': session.peer,
            'from': envelope.mail_from,
            'to': envelope.rcpt_tos,
            'payload': payload,
        }
        print('--- SMTP DEBUG SERVER RECEIVED MESSAGE ---')
        print('Peer:', record['peer'])
        print('From:', record['from'])
        print('To:', record['to'])
        print('Message:')
        print(record['payload'])
        print('--- END MESSAGE ---')
        self.messages.append(record)
        return '250 Message accepted for delivery'


def start_controller(handler, host, port):
    controller = Controller(handler, hostname=host, port=port)
    controller.start()
    return controller


def main():
    parser = argparse.ArgumentParser(description='Run local SMTP demo and send a test email via the app')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=2505)
    parser.add_argument('--to', required=True)
    parser.add_argument('--subject', default='Local SMTP demo')
    parser.add_argument('--body', default='Hello from local demo')
    args = parser.parse_args()

    handler = CapturingHandler()
    controller = start_controller(handler, args.host, args.port)
    # Give server a moment to start
    time.sleep(0.3)

    # Temporarily set env vars for the app to use the local debug server
    import os
    prev_server = os.environ.get('MAIL_SERVER')
    prev_port = os.environ.get('MAIL_PORT')
    prev_tls = os.environ.get('MAIL_USE_TLS')
    os.environ['MAIL_SERVER'] = args.host
    os.environ['MAIL_PORT'] = str(args.port)
    os.environ['MAIL_USE_TLS'] = 'False'

    # Boot the app and call send_email
    try:
        import pathlib
        repo_root = str(pathlib.Path(__file__).resolve().parents[2])
        if repo_root not in sys.path:
            sys.path.insert(0, repo_root)
    except Exception:
        pass

    try:
        from backend.app import create_app
        app = create_app()
        with app.app_context():
            from backend.email_utils import send_email
            ok = send_email(args.to, args.subject, args.body)
            print('send_email returned:', ok)
    except Exception as e:  # pragma: no cover - integration helper
        print('Error while sending via app:', e)
        ok = False

    # Give the server a moment to receive
    time.sleep(0.5)

    # Stop controller
    controller.stop()

    # Restore env
    if prev_server is None:
        os.environ.pop('MAIL_SERVER', None)
    else:
        os.environ['MAIL_SERVER'] = prev_server
    if prev_port is None:
        os.environ.pop('MAIL_PORT', None)
    else:
        os.environ['MAIL_PORT'] = prev_port
    if prev_tls is None:
        os.environ.pop('MAIL_USE_TLS', None)
    else:
        os.environ['MAIL_USE_TLS'] = prev_tls

    if ok and handler.messages:
        print('\nDemo succeeded: message was received by local SMTP server')
        sys.exit(0)
    elif ok:
        print('\nPartial success: send_email reported success but server received no messages')
        sys.exit(2)
    else:
        print('\nDemo failed: send_email reported failure')
        sys.exit(1)


if __name__ == '__main__':
    main()
