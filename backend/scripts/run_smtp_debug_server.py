#!/usr/bin/env python3
"""Run a simple SMTP debugging server that prints received emails to stdout using aiosmtpd.

Usage:
  python backend/scripts/run_smtp_debug_server.py --host 127.0.0.1 --port 1025

This uses `aiosmtpd` (install in the venv: `pip install aiosmtpd`).
"""
import argparse
import time
from aiosmtpd.controller import Controller


class PrintHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            payload = envelope.content.decode('utf-8', errors='replace')
        except Exception:
            payload = str(envelope.content)
        print('--- SMTP DEBUG SERVER RECEIVED MESSAGE ---')
        print('Peer:', session.peer)
        print('From:', envelope.mail_from)
        print('To:', envelope.rcpt_tos)
        print('Message:')
        print(payload)
        print('--- END MESSAGE ---')
        return '250 Message accepted for delivery'


def main():
    parser = argparse.ArgumentParser(description='Run SMTP debug server')
    parser.add_argument('--host', default='127.0.0.1', help='Bind address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=1025, help='Port to listen on (default: 1025)')
    args = parser.parse_args()

    handler = PrintHandler()
    controller = Controller(handler, hostname=args.host, port=args.port)
    controller.start()
    print(f'SMTP debug server listening on {args.host}:{args.port} (Ctrl-C to stop)')
    try:
        # Keep the main thread alive while controller runs
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()
        print('\nSMTP debug server stopped')


if __name__ == '__main__':
    main()
