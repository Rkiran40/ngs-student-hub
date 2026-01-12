import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import current_app
import smtplib, ssl
from email.mime.text import MIMEText

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = set([
    'pdf', 'doc', 'docx', 'zip', 'jpg', 'jpeg', 'png', 'gif', 'bmp',
    'webp', 'svg', 'tif', 'tiff', 'avif', 'ico', 'heic', 'jfif'
])


# ========================
# Password Utilities
# ========================
def hash_password(password: str) -> str:
    """Hash a plain-text password."""
    return generate_password_hash(password)


def verify_password(hash: str, password: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(hash, password)


# ========================
# File Upload Utilities
# ========================
def allowed_file(filename: str, mimetype: str = '') -> bool:
    """
    Return True if the file is allowed based on its extension or MIME type.

    Accepts if the filename extension matches ALLOWED_EXTENSIONS, 
    or if the uploaded file's MIME type indicates an image (e.g., image/jpeg, image/png).
    """
    if filename and '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    if mimetype and mimetype.startswith('image/'):
        return True
    return False


from .storage import get_storage, LocalStorage

def save_upload_file(file, user_id: str) -> str:
    """
    Save an uploaded file either to local disk or configured S3 storage.

    Returns:
        - If local storage: the relative path under the uploads root (e.g., "userid/123_file.png")
        - If S3 storage: the public URL returned by the storage backend (starts with http...)
    """
    uploads_root = current_app.config.get('UPLOAD_FOLDER')
    storage = get_storage(current_app.config)

    filename = secure_filename(file.filename)
    rel_path = os.path.join(user_id, f"{int(__import__('time').time())}_{filename}").replace('\\', '/')

    # If using LocalStorage, write to disk and return relative key
    if isinstance(storage, LocalStorage):
        storage.upload(file, rel_path)
        return rel_path

    # Otherwise (S3), upload to S3 with the key being the rel_path
    url = storage.upload(file, rel_path, content_type=(file.content_type or file.mimetype))
    return url


# ========================
# Email Utilities
# ========================
def send_username_email(to_email: str, username: str,full_name: str):
    """
    Sends the approved username to the user's registered email.
    Uses Flask current_app config for SMTP credentials.
    """
    subject = "Your StudentHub account has been Approved"
    body = f"Hello {full_name},\nYour account has been approved by the administrator\n\nYour username is: {username}\nYou can now sign in using your username \n\n\nRegards,\nStudentHub Team"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = to_email

    context = ssl.create_default_context()

    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        if current_app.config['MAIL_USE_TLS']:
            server.starttls(context=context)
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], [to_email], msg.as_string())

def send_suspension_email(to_email: str, full_name: str):
    """
    Sends suspension notification email to the student.
    """
    subject = "StudentHub Account Suspended"
    body = f"Hello {full_name},\n\nYour StudentHub account has been suspended by the administrator.\n\nIf you believe this is an error or would like to appeal, please contact support.\n\n\nRegards,\nStudentHub Team"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = to_email

    context = ssl.create_default_context()

    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        if current_app.config['MAIL_USE_TLS']:
            server.starttls(context=context)
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], [to_email], msg.as_string())

def send_registration_confirmation_email(to_email: str, full_name: str):
    """
    Sends registration confirmation email after account creation.
    """
    subject = "Welcome to StudentHub - Registration Confirmed"
    body = f"Hello {full_name},\n\nThank you for registering with StudentHub!\n\nYour account has been created successfully. Your account is currently pending approval by the administrator.\n\nOnce approved, you will receive your username via email and can start using the platform.\n\nIf you have any questions, please contact support.\n\n\nRegards,\nStudentHub Team"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = current_app.config['MAIL_USERNAME']
    msg['To'] = to_email

    context = ssl.create_default_context()

    with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
        if current_app.config['MAIL_USE_TLS']:
            server.starttls(context=context)
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.sendmail(msg['From'], [to_email], msg.as_string())
