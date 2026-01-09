import os
import tempfile
from backend.utils import hash_password
from backend.models import User, Profile


def test_resend_approval_writes_mailfile(client, db, app, monkeypatch):
    tmp = tempfile.mkdtemp(prefix='mail_out_')
    monkeypatch.setenv('MAIL_OUTPUT_DIR', tmp)

    # create active profile with username
    student = User(email='resend1@example.com', password_hash=hash_password('pass1'))
    db.session.add(student)
    db.session.commit()
    p = Profile(user_id=student.id, full_name='Resend One', email='resend1@example.com', username='resend1name', status='active')
    db.session.add(p)

    # admin
    admin = User(email='admin3@example.com', password_hash=hash_password('adminpw'), role='admin')
    db.session.add(admin)
    db.session.commit()
    admin_profile = Profile(user_id=admin.id, username='admin', full_name='Admin', email='admin3@example.com', status='active')
    db.session.add(admin_profile)
    db.session.commit()

    # login
    login = client.post('/auth/login', json={'email': 'admin3@example.com', 'password': 'adminpw'})
    token = login.json.get('access_token')
    headers = {'Authorization': f'Bearer {token}'}

    # call resend
    resp = client.post(f'/admin/students/{p.id}/resend-approval', headers=headers)
    assert resp.status_code == 200
    assert resp.json.get('success') is True

    files = sorted(os.listdir(tmp))
    assert len(files) >= 1
    path = os.path.join(tmp, files[-1])
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'Your username is: resend1name' in content
