import os
from backend.email_utils import send_email


def test_send_email_uses_mail_env(monkeypatch):
    called = {}

    class DummySMTP:
        def __init__(self, server, port, timeout=None):
            called['server'] = server
            called['port'] = port

        def starttls(self, context=None):
            called['starttls'] = True

        def login(self, user, pw):
            called['login'] = (user, pw)

        def sendmail(self, from_addr, to_addrs, msg):
            called['sendmail'] = (from_addr, to_addrs, msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    # Set MAIL_* env vars (our new fallback)
    monkeypatch.setenv('MAIL_SERVER', 'smtp.mail.example')
    monkeypatch.setenv('MAIL_PORT', '2525')
    monkeypatch.setenv('MAIL_USERNAME', 'user@example.com')
    monkeypatch.setenv('MAIL_PASSWORD', 'pw')
    monkeypatch.setenv('MAIL_USE_TLS', 'True')

    # Replace smtplib.SMTP with our dummy
    monkeypatch.setattr('smtplib.SMTP', DummySMTP)

    res = send_email('to@example.com', 'subject', 'body')
    assert res is True
    # Confirm SMTP was invoked and sendmail called
    assert 'sendmail' in called
    assert called['server'] == 'smtp.mail.example'
    assert called['port'] == 2525 or called['port'] == '2525'
    # Ensure message includes a From header and the sender is the configured username
    from_addr, to_addrs, msg = called['sendmail']
    assert from_addr == 'user@example.com'
    assert msg.startswith('From:')


def test_fallback_file_contains_from_header(monkeypatch, tmp_path):
    # Set MAIL_OUTPUT_DIR so send_email writes to disk (no SMTP configured)
    maildir = tmp_path / 'mails'
    monkeypatch.setenv('MAIL_OUTPUT_DIR', str(maildir))
    # Ensure no SMTP configuration is present so send_email falls back to writing files
    monkeypatch.delenv('MAIL_SERVER', raising=False)
    monkeypatch.delenv('SMTP_SERVER', raising=False)
    monkeypatch.delenv('SMTP_USER', raising=False)
    monkeypatch.delenv('MAIL_USERNAME', raising=False)

    res = send_email('to@example.com', 'sub', 'body')
    assert res is True

    files = list(maildir.iterdir())
    assert len(files) >= 1
    # Read latest file and assert it contains a From header
    files = sorted(files)
    path = files[-1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.startswith('From:')
    assert 'To: to@example.com' in content


def test_mail_from_used_in_fallback(monkeypatch, tmp_path):
    maildir = tmp_path / 'mails'
    monkeypatch.setenv('MAIL_OUTPUT_DIR', str(maildir))
    # Ensure no SMTP configuration
    monkeypatch.delenv('MAIL_SERVER', raising=False)
    monkeypatch.delenv('SMTP_SERVER', raising=False)
    monkeypatch.setenv('MAIL_FROM', 'sender@example.com')

    res = send_email('to@example.com', 'sub', 'body')
    assert res is True

    files = sorted(list(maildir.iterdir()))
    path = files[-1]
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'From: sender@example.com' in content


def test_mail_from_used_for_smtp(monkeypatch):
    called = {}

    class DummySMTP:
        def __init__(self, server, port, timeout=None):
            called['server'] = server
            called['port'] = port

        def starttls(self, context=None):
            called['starttls'] = True

        def login(self, user, pw):
            called['login'] = (user, pw)

        def sendmail(self, from_addr, to_addrs, msg):
            called['sendmail'] = (from_addr, to_addrs, msg)

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setenv('MAIL_SERVER', 'smtp.mail.example')
    monkeypatch.setenv('MAIL_PORT', '2525')
    monkeypatch.setenv('MAIL_USERNAME', 'user@example.com')
    monkeypatch.setenv('MAIL_PASSWORD', 'pw')
    monkeypatch.setenv('MAIL_USE_TLS', 'True')
    monkeypatch.setenv('MAIL_FROM', 'sender@example.com')

    monkeypatch.setattr('smtplib.SMTP', DummySMTP)

    res = send_email('to@example.com', 'subject', 'body')
    assert res is True
    assert 'sendmail' in called
    from_addr, to_addrs, msg = called['sendmail']
    assert from_addr == 'sender@example.com'
    assert 'From:' in msg


