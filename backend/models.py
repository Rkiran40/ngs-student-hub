from .db import db
from datetime import datetime, timezone
import uuid
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='student')
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete')
    uploads = db.relationship('DailyUpload', backref='user', cascade='all, delete')
    password_resets = db.relationship('PasswordResetOTP', back_populates='user', cascade='all, delete-orphan')



class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    username = db.Column(db.String(150), unique=True, nullable=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)
    college_name = db.Column(db.String(255), nullable=True)
    college_id = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    college_email = db.Column(db.String(255), nullable=True)
    course_name = db.Column(db.String(255), nullable=True)
    course_mode = db.Column(db.String(100), nullable=True)
    course_duration = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='pending')
    avatar_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class DailyUpload(db.Model):
    __tablename__ = 'daily_uploads'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    file_name = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(100), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    upload_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    description = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default='pending')
    admin_feedback = db.Column(db.String(1000), nullable=True)
    reviewed_by = db.Column(db.String(150), nullable=True)
    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    category = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(2000), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    attachments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='submitted')
    admin_response = db.Column(db.String(2000), nullable=True)
    responded_by = db.Column(db.String(150), nullable=True)
    responded_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class PasswordResetOTP(db.Model):
    __tablename__ = 'password_reset_otps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)  # nullable for signup OTP verification
    email = db.Column(db.String(255), nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    purpose = db.Column(db.String(50), nullable=False, default='password')  # 'password', 'username', or 'signup'
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='password_resets')
