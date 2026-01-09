import os
import tempfile
import types
from backend.email_utils import send_email


class FailingOnceSMTP:
    def __init__(self, server, port, timeout=None):
        self.server = server
        self.port = port
        self._called = False

    def starttls(self, context=None):
        pass

    def login(self, user, pw):
        pass

    def sendmail(self, from_addr, to_addrs, msg):
        if not getattr(self, '_fail_once_done', False):
            self._fail_once_done = True
            raise Exception('simulated transient smtp error')
        # succeed on second call
        self._sent = (from_addr, to_addrs, msg)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class AlwaysFailSMTP:
    def __init__(self, server, port, timeout=None):
        pass

    def starttls(self, context=None):
        pass

    def login(self, user, pw):
        pass

    def sendmail(self, from_addr, to_addrs, msg):
        raise Exception('permanent failure')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_send_email_retries_and_succeeds(monkeypatch):
    # Replace SMTP with the failing-once implementation
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test')
    monkeypatch.setenv('MAIL_PORT', '25')
    monkeypatch.setenv('MAIL_USERNAME', 'u')
    monkeypatch.setenv('MAIL_PASSWORD', 'p')
    monkeypatch.setenv('MAIL_USE_TLS', 'False')
    monkeypatch.setenv('SMTP_MAX_RETRIES', '2')

    monkeypatch.setattr('smtplib.SMTP', FailingOnceSMTP)

    res = send_email('to@example.com', 'sub', 'body')
    assert res is True


def test_send_email_failure_triggers_sentry_and_writes_file(monkeypatch, tmp_path):
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test')
    monkeypatch.setenv('MAIL_PORT', '25')
    monkeypatch.setenv('MAIL_USERNAME', 'u')
    monkeypatch.setenv('MAIL_PASSWORD', 'p')
    monkeypatch.setenv('MAIL_USE_TLS', 'False')
    monkeypatch.setenv('SMTP_MAX_RETRIES', '0')

    # Make SMTP always fail
    monkeypatch.setattr('smtplib.SMTP', AlwaysFailSMTP)

    called = {}

    def fake_capture_exception(e):
        called['sentry'] = str(e)

    # monkeypatch sentry capture
    import builtins
    try:
        import sentry_sdk
        monkeypatch.setattr('sentry_sdk.capture_exception', fake_capture_exception)
    except Exception:
        # If sentry not installed, emulate it by inserting into sys.modules
        sentry = types.SimpleNamespace(capture_exception=fake_capture_exception)
        monkeypatch.setitem(__import__('sys').modules, 'sentry_sdk', sentry)

    maildir = tmp_path / 'mails'
    monkeypatch.setenv('MAIL_OUTPUT_DIR', str(maildir))

    res = send_email('to2@example.com', 'sub2', 'body2')
    assert res is True

    files = list(maildir.iterdir())
    assert len(files) >= 1
    assert 'sentry' in called
