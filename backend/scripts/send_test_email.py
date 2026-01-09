#!/usr/bin/env python3
"""Send a test email using the app's send_email function.
Usage: python backend/scripts/send_test_email.py --to you@example.com --subject "sub" --body "body"
"""
import argparse
from backend.app import create_app

parser = argparse.ArgumentParser(description='Send a test email via StudentHub backend')
parser.add_argument('--to', required=True, help='Recipient email address')
parser.add_argument('--subject', default='Test email from StudentHub', help='Email subject')
parser.add_argument('--body', default='This is a test email from StudentHub', help='Email body')
args = parser.parse_args()

app = create_app()
with app.app_context():
    from backend.email_utils import send_email
    ok = send_email(args.to, args.subject, args.body)
    print('send_email returned:', ok)
