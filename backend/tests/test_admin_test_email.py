import os
import tempfile
from backend.utils import hash_password
from backend.models import User, Profile


def test_send_test_email_writes_maildir(client, db, app, monkeypatch):
    tmp = tempfile.mkdtemp(prefix='mail_out_')
    monkeypatch.setenv('MAIL_OUTPUT_DIR', tmp)

    # Create an admin user
    admin = User(email='admin@nuhvin.com', password_hash=hash_password('123456'), role='admin')
    db.session.add(admin)
    db.session.commit()
    admin_profile = Profile(user_id=admin.id, username='admin@nuhvin.com', full_name='Admin', email='admin@nuhvin.com', status='active')
    db.session.add(admin_profile)
    db.session.commit()

    login = client.post('/auth/login', json={'email': 'admin@nuhvin.com', 'password': '123456'})
    assert login.status_code == 200
    token = login.json.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    resp = client.post('/admin/test-email', json={'to': 'to@example.com', 'subject': 'sub', 'body': 'body'}, headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success') is True

    files = os.listdir(tmp)
    assert len(files) >= 1
    files = sorted(files)
    path = os.path.join(tmp, files[-1])
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'To: to@example.com' in content
    assert 'sub' in content
    assert 'body' in content


def test_send_test_email_uses_smtp_when_mail_env_set(client, db, app, monkeypatch):
    # Set MAIL_* env vars so email_utils uses SMTP
    monkeypatch.setenv('MAIL_SERVER', 'smtp.test.local')
    monkeypatch.setenv('MAIL_PORT', '2525')
    monkeypatch.setenv('MAIL_USERNAME', 'sender@test.local')
    monkeypatch.setenv('MAIL_PASSWORD', 'pw')
    monkeypatch.setenv('MAIL_USE_TLS', 'True')

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

    monkeypatch.setattr('smtplib.SMTP', DummySMTP)

    # Create an admin user
    admin = User(email='admin_smtp@example.com', password_hash=hash_password('adminpw'), role='admin')
    db.session.add(admin)
    db.session.commit()
    admin_profile = Profile(user_id=admin.id, username='admin', full_name='Admin', email='admin_smtp@example.com', status='active')
    db.session.add(admin_profile)
    db.session.commit()

    login = client.post('/auth/login', json={'email': 'admin_smtp@example.com', 'password': 'adminpw'})
    assert login.status_code == 200
    token = login.json.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # Do not provide 'to' so endpoint defaults to admin email
    resp = client.post('/admin/test-email', json={'subject': 's', 'body': 'b'}, headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success') is True
    assert 'sendmail' in called
    _, to_addrs, msg = called['sendmail']
    assert 's' in msg
    assert 'b' in msg
