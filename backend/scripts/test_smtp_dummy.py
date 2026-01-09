#!/usr/bin/env python3
import smtplib
print('patching smtplib.SMTP with DummySMTP')
class DummySMTP:
    def __init__(self, server, port, timeout=None):
        print('DummySMTP init', server, port)
    def starttls(self, context=None):
        print('starttls')
    def login(self, user, pw):
        print('login', user)
    def sendmail(self, from_addr, to_addrs, msg):
        print('sendmail called', from_addr, to_addrs)
        print('MSG:\n', msg[:200])
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False

smtplib.SMTP = DummySMTP
from backend.email_utils import send_email
print('calling send_email...')
send_email('recipient@example.com','Test Subject','Hello body')
print('done')
