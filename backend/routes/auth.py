# from flask import Blueprint, request, jsonify, current_app
# from ..db import db
# from ..models import User, Profile, PasswordResetOTP
# from ..utils import hash_password, verify_password
# from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
# from sqlalchemy.exc import IntegrityError, OperationalError
# from datetime import datetime, timezone, timedelta
# import os
# import random

# auth_bp = Blueprint('auth', __name__)

# # ----------------------- SEND EMAIL OTP FOR SIGNUP -----------------------
# @auth_bp.route('/send-signup-otp', methods=['POST'])
# def send_signup_otp():
#     """Send OTP to email for signup verification"""
#     data = request.get_json() or {}
#     email = data.get('email')
#     if not email:
#         return jsonify({'success': True, 'message': 'If the email is available, an OTP will be sent.'})

#     # Check if email already exists
#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return jsonify({'success': True, 'message': 'If the email is available, an OTP will be sent.'})

#     try:
#         # Generate OTP
#         otp = f"{random.randint(000000, 999999):06d}"
#         expires = datetime.now(timezone.utc) + timedelta(minutes=15)
        
#         pr = PasswordResetOTP(
#             user_id=None,  # Not linked to user yet
#             email=email,
#             otp=otp,
#             purpose='signup',
#             expires_at=expires
#         )
#         db.session.add(pr)
#         db.session.commit()

#         # Send OTP email
#         try:
#             from ..email_utils import send_email
#             subject = 'StudentHub Email Verification Code'
#             body = f"Hello,\n\nYour email verification code for StudentHub signup is: {otp}\nThis code will expire in 15 minutes.\n\nIf you did not request this, please ignore this email.\n\n— StudentHub Team"
#             sent = send_email(email, subject, body)
#             if sent:
#                 current_app.logger.info(f'Signup OTP sent to {email}')
#             else:
#                 current_app.logger.warning(f'Signup OTP created for {email} but email sending failed (mail saved to mail_out or SMTP failed)')
#         except Exception as e:
#             current_app.logger.exception(f'Failed to send signup OTP email to {email}: {str(e)}')
#             # Don't fail the request if email fails, OTP was still created

#         return jsonify({'success': True, 'message': 'Verification code sent to your email.'})
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.exception(f'Failed to generate signup OTP: {str(e)}')
#         return jsonify({'success': False, 'message': f'Failed to send OTP: {str(e)}'}), 500

# # ----------------------- VERIFY EMAIL OTP FOR SIGNUP -----------------------
# @auth_bp.route('/verify-signup-otp', methods=['POST'])
# def verify_signup_otp():
    
#     data = request.get_json() or {}
#     email = data.get('email')
#     otp = data.get('otp')
    
#     if not email or not otp:
#         return jsonify({'success': False, 'message': 'email and otp required'}), 400

#     pr = PasswordResetOTP.query.filter_by(email=email, otp=otp, purpose='signup').order_by(PasswordResetOTP.created_at.desc()).first()
#     if not pr or pr.expires_at < datetime.now(timezone.utc):
#         return jsonify({'success': False, 'message': 'Invalid or expired verification code'}), 400

#     try:
#         db.session.delete(pr)
#         db.session.commit()
#     except Exception:
#         db.session.rollback()

#     return jsonify({'success': True, 'message': 'Email verified successfully'})

# # ----------------------- SIGNUP -----------------------
# @auth_bp.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json() or {}
#     email = data.get('email')
#     email_otp = data.get('emailOtp') or data.get('email_otp')
#     password = data.get('password')
#     full_name = data.get('full_name')
#     contact_number = data.get('contact_number')
#     college_name = data.get('college_name')
#     college_id = data.get('college_id')
#     city = data.get('city')
#     pincode = data.get('pincode')
#     college_email = data.get('college_email')
#     course_name = data.get('course_name')
#     course_mode = data.get('course_mode')
#     course_duration = data.get('course_duration')

#     if not email or not password or not full_name:
#         return jsonify({'success': False, 'message': 'email, password, and full_name are required'}), 400

#     # Verify email OTP
#     if email_otp:
#         pr = PasswordResetOTP.query.filter_by(email=email, otp=email_otp, purpose='signup').order_by(PasswordResetOTP.created_at.desc()).first()
#         if not pr or pr.expires_at < datetime.now(timezone.utc):
#             return jsonify({'success': False, 'message': 'Invalid or expired verification code'}), 400

#     try:
#         user = User(email=email, password_hash=hash_password(password))
#         db.session.add(user)
#         db.session.flush()  # Get user.id without committing

#         profile = Profile(
#             user_id=user.id, 
#             username=None, 
#             full_name=full_name, 
#             email=email, 
#             contact_number=contact_number, 
#             college_name=college_name, 
#             college_id=college_id,
#             city=city,
#             pincode=pincode,
#             college_email=college_email,
#             course_name=course_name,
#             course_mode=course_mode,
#             course_duration=course_duration
#         )
#         db.session.add(profile)
#         db.session.commit()

#         # Delete OTP after successful signup
#         if email_otp:
#             try:
#                 db.session.delete(pr)
#                 db.session.commit()
#             except Exception:
#                 db.session.rollback()

#         # Send registration confirmation email
#         try:
#             from ..utils import send_registration_confirmation_email
#             send_registration_confirmation_email(email, full_name)
#         except Exception:
#             import traceback
#             current_app.logger.exception('Failed to send registration confirmation email: %s', traceback.format_exc())

#         return jsonify({'success': True, 'message': 'Signup successful', 'user': {'id': user.id, 'email': user.email}})
#     except IntegrityError as e:
#         db.session.rollback()
#         if 'email' in str(e.orig).lower() or 'unique' in str(e.orig).lower():
#             return jsonify({'success': False, 'message': 'Email already exists'}), 409
#         return jsonify({'success': False, 'message': 'Database error occurred'}), 500
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'message': f'Signup failed: {str(e)}'}), 500

# # ----------------------- LOGIN -----------------------
# @auth_bp.route('/login', methods=['POST'])
# def login():
#     try:
#         data = request.get_json() or {}
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         if not (username or email) or not password:
#             return jsonify({'success': False, 'message': 'username (or email) and password required'}), 400

#         user = None
#         profile = None
#         if email:
#             user = User.query.filter_by(email=email).first()
#             profile = user.profile if user else None
#         else:
#             profile = Profile.query.filter_by(username=username).first()
#             user = db.session.get(User, profile.user_id) if profile else None

#         if not user or not verify_password(user.password_hash, password):
#             return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

#         if user.role != 'admin' and not current_app.config.get('TESTING', False):
#             if not profile or profile.status != 'active':
#                 if profile and profile.status == 'pending':
#                     return jsonify({'success': False, 'message': 'Your account is pending approval. Please wait for admin verification.'}), 403
#                 elif profile and profile.status == 'suspended':
#                     return jsonify({'success': False, 'message': 'Your account has been suspended. Please contact support.'}), 403

#         access = create_access_token(identity=user.id)
#         refresh = create_refresh_token(identity=user.id)

#         return jsonify({
#             'success': True,
#             'access_token': access,
#             'refresh_token': refresh,
#             'user': {
#                 'id': user.id,
#                 'email': user.email,
#                 'username': profile.username if profile else None,
#                 'role': user.role or 'student'
#             }
#         })
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({'success': False, 'message': f'Login error: {str(e)}'}), 500

# # ----------------------- CURRENT USER -----------------------
# @auth_bp.route('/me', methods=['GET'])
# @jwt_required()
# def me():
#     user_id = get_jwt_identity()
#     user = db.session.get(User, user_id)
#     if not user:
#         return jsonify({'success': False, 'message': 'User not found'}), 404
#     profile = user.profile
#     return jsonify({'success': True, 'user': {
#         'id': user.id,
#         'email': user.email,
#         'role': user.role,
#         'profile': {
#             'id': profile.id if profile else None,
#             'username': profile.username if profile else None,
#             'full_name': profile.full_name if profile else None,
#             'email': profile.email if profile else None,
#             'contact_number': profile.contact_number if profile else None,
#             'college_name': profile.college_name if profile else None,
#             'college_id': profile.college_id if profile else None,
#             'city': profile.city if profile else None,
#             'pincode': profile.pincode if profile else None,
#             'college_email': profile.college_email if profile else None,
#             'course_name': profile.course_name if profile else None,
#             'course_mode': profile.course_mode if profile else None,
#             'course_duration': profile.course_duration if profile else None,
#             'avatar_url': profile.avatar_url if profile else None,
#             'status': profile.status if profile else 'pending',
#             'created_at': profile.created_at.isoformat() if profile and profile.created_at else None,
#             'updated_at': profile.updated_at.isoformat() if profile and profile.updated_at else None,
#         }
#     }})

# # ----------------------- REFRESH TOKEN -----------------------
# @auth_bp.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     user_id = get_jwt_identity()
#     access = create_access_token(identity=user_id)
#     return jsonify({'success': True, 'access_token': access})

# # ----------------------- FORGOT USERNAME -----------------------
# @auth_bp.route('/forgot-username', methods=['POST'])
# def forgot_username():
#     data = request.get_json() or {}
#     email = data.get('email')
#     if not email:
#         return jsonify({'success': True, 'message': 'If an account exists, a verification code will be sent to your email.'})

#     profile = Profile.query.filter_by(email=email).first()
#     if profile:
#         otp = f"{random.randint(0, 999999):06d}"
#         expires = datetime.now(timezone.utc) + timedelta(minutes=15)
#         pr = PasswordResetOTP(
#             user_id=profile.user_id,
#             email=email,
#             otp=otp,
#             purpose='username',
#             expires_at=expires
#         )
#         db.session.add(pr)
#         db.session.commit()

#         from ..email_utils import send_email
#         subject = 'StudentHub username recovery code'
#         body = f"Hello {profile.full_name or ''},\n\nYour verification code for username recovery is: {otp}\nThis code will expire in 15 minutes.\n\n— StudentHub Team"
#         send_email(email, subject, body)

#     return jsonify({'success': True, 'message': 'If an account exists, a verification code will be sent to your email.'})

# # ----------------------- RECOVER USERNAME -----------------------
# @auth_bp.route('/recover-username', methods=['POST'])
# def recover_username():
#     data = request.get_json() or {}
#     email = data.get('email')
#     otp = data.get('otp')
#     if not email or not otp:
#         return jsonify({'success': False, 'message': 'email and otp required'}), 400

#     pr = PasswordResetOTP.query.filter_by(email=email, otp=otp, purpose='username').order_by(PasswordResetOTP.created_at.desc()).first()
#     if not pr or pr.expires_at < datetime.now(timezone.utc):
#         return jsonify({'success': False, 'message': 'Invalid or expired code'}), 400

#     profile = Profile.query.filter_by(email=email).first()
#     if not profile or not profile.username:
#         return jsonify({'success': False, 'message': 'Username not found'}), 404

#     try:
#         db.session.delete(pr)
#         db.session.commit()
#     except Exception:
#         db.session.rollback()

#     return jsonify({'success': True, 'username': profile.username})

# # ----------------------- FORGOT PASSWORD -----------------------
# @auth_bp.route('/forgot-password', methods=['POST'])
# def forgot_password():
#     data = request.get_json() or {}
#     email = data.get('email')
#     if not email:
#         return jsonify({'success': True, 'message': 'If an account exists, a password reset code will be sent to your email.'})

#     user = User.query.filter_by(email=email).first()
#     if user:
#         otp = f"{random.randint(0, 999999):06d}"
#         expires = datetime.now(timezone.utc) + timedelta(minutes=15)
#         pr = PasswordResetOTP(
#             user_id=user.id,
#             email=email,
#             otp=otp,
#             purpose='password',
#             expires_at=expires
#         )
#         db.session.add(pr)
#         db.session.commit()

#         from ..email_utils import send_email
#         frontend = current_app.config.get('FRONTEND_URL') or os.environ.get('FRONTEND_URL') or 'http://localhost:5173'
#         subject = 'StudentHub password reset code'
#         body = f"Hello,\n\nYour password reset code is: {otp}\nThis code will expire in 15 minutes.\nReset here: {frontend}/auth/forgot-password\n\n— StudentHub Team"
#         send_email(email, subject, body)

#     return jsonify({'success': True, 'message': 'If an account exists, a password reset code will be sent to your email.'})

# # ----------------------- VERIFY PASSWORD OTP -----------------------
# @auth_bp.route('/verify-password-otp', methods=['POST'])
# def verify_password_otp():
#     """Verify OTP for password reset before allowing password change"""
#     data = request.get_json() or {}
#     email = data.get('email')
#     otp = data.get('otp')
    
#     if not email or not otp:
#         return jsonify({'success': False, 'message': 'email and otp required'}), 400

#     current_app.logger.info(f'Verifying password OTP for email: {email}, OTP: {otp}')
    
#     pr = PasswordResetOTP.query.filter_by(email=email, otp=otp, purpose='password').order_by(PasswordResetOTP.created_at.desc()).first()
    
#     if not pr:
#         current_app.logger.warning(f'No OTP found for email: {email}')
#         return jsonify({'success': False, 'message': 'Invalid or expired password reset code'}), 400
    
#     if pr.expires_at < datetime.now(timezone.utc):
#         current_app.logger.warning(f'OTP expired for email: {email}')
#         return jsonify({'success': False, 'message': 'Invalid or expired password reset code'}), 400

#     current_app.logger.info(f'Password OTP verified successfully for email: {email}')
#     return jsonify({'success': True, 'message': 'OTP verified successfully'})

# # ----------------------- RESET PASSWORD -----------------------
# @auth_bp.route('/reset-password', methods=['POST'])
# def reset_password():
#     data = request.get_json() or {}
#     email = data.get('email')
#     otp = data.get('otp')
#     new_password = data.get('newPassword') or data.get('new_password') or data.get('password')

#     if not email or not otp or not new_password:
#         return jsonify({'success': False, 'message': 'email, otp and new password are required'}), 400

#     pr = PasswordResetOTP.query.filter_by(email=email, otp=otp, purpose='password').order_by(PasswordResetOTP.created_at.desc()).first()
#     if not pr or pr.expires_at < datetime.now(timezone.utc):
#         return jsonify({'success': False, 'message': 'Invalid or expired code'}), 400

#     user = User.query.filter_by(email=email).first()
#     if not user:
#         return jsonify({'success': False, 'message': 'User not found'}), 404

#     try:
#         db.session.delete(pr)
#         db.session.commit()
#     except Exception:
#         db.session.rollback()

#     user.password_hash = hash_password(new_password)
#     db.session.commit()
#     return jsonify({'success': True, 'message': 'Password reset successful.'})

# # ----------------------- CHANGE PASSWORD -----------------------
# @auth_bp.route('/change-password', methods=['POST'])
# @jwt_required()
# def change_password():
#     data = request.get_json() or {}
#     new_password = data.get('newPassword') or data.get('new_password') or data.get('password')
#     if not new_password:
#         return jsonify({'success': False, 'message': 'new password is required'}), 400

#     user_id = get_jwt_identity()
#     user = db.session.get(User, user_id)
#     if not user:
#         return jsonify({'success': False, 'message': 'User not found'}), 404

#     user.password_hash = hash_password(new_password)
#     db.session.commit()
#     return jsonify({'success': True, 'message': 'Password changed successfully.'})


from flask import Blueprint, request, jsonify, current_app
from ..db import db
from ..models import User, Profile, PasswordResetOTP
from ..utils import hash_password, verify_password
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime, timezone, timedelta
import os
import random

auth_bp = Blueprint('auth', __name__)

# ---------------------------------------------------------
# Helper: normalize datetime to UTC-aware before comparing
# ---------------------------------------------------------
def is_expired(expires_at):
    if not expires_at:
        return True
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at < datetime.now(timezone.utc)

# ----------------------- SEND EMAIL OTP FOR SIGNUP -----------------------
@auth_bp.route('/send-signup-otp', methods=['POST'])
def send_signup_otp():
    data = request.get_json() or {}
    email = data.get('email')
    if not email:
        return jsonify({'success': True, 'message': 'If the email is available, an OTP will be sent.'})

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'success': True, 'message': 'If the email is available, an OTP will be sent.'})

    try:
        otp = f"{random.randint(0, 999999):06d}"
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

        pr = PasswordResetOTP(
            user_id=None,
            email=email,
            otp=otp,
            purpose='signup',
            expires_at=expires
        )
        db.session.add(pr)
        db.session.commit()

        try:
            from ..email_utils import send_email
            subject = 'StudentHub Email Verification Code'
            body = (
                f"Hello,\n\n"
                f"Your email verification code for StudentHub signup is: {otp}\n"
                f"This code will expire in 15 minutes.\n\n"
                f"If you did not request this, please ignore this email.\n\n"
                f"— StudentHub Team"
            )
            send_email(email, subject, body)
        except Exception:
            current_app.logger.exception(f'Failed sending signup OTP to {email}')

        return jsonify({'success': True, 'message': 'Verification code sent to your email.'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception('Failed to generate signup OTP')
        return jsonify({'success': False, 'message': 'Failed to send OTP'}), 500

# ----------------------- VERIFY EMAIL OTP FOR SIGNUP -----------------------
@auth_bp.route('/verify-signup-otp', methods=['POST'])
def verify_signup_otp():
    data = request.get_json() or {}
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({'success': False, 'message': 'email and otp required'}), 400

    pr = PasswordResetOTP.query.filter_by(
        email=email, otp=otp, purpose='signup'
    ).order_by(PasswordResetOTP.created_at.desc()).first()

    if not pr or is_expired(pr.expires_at):
        return jsonify({'success': False, 'message': 'Invalid or expired verification code'}), 400

    db.session.delete(pr)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Email verified successfully'})

# ----------------------- SIGNUP -----------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    email = data.get('email')
    email_otp = data.get('emailOtp') or data.get('email_otp')
    password = data.get('password')
    full_name = data.get('full_name')

    contact_number = data.get('contact_number')
    college_name = data.get('college_name')
    college_id = data.get('college_id')
    city = data.get('city')
    pincode = data.get('pincode')
    college_email = data.get('college_email')
    course_name = data.get('course_name')
    course_mode = data.get('course_mode')
    course_duration = data.get('course_duration')

    if not email or not password or not full_name:
        return jsonify({'success': False, 'message': 'email, password, and full_name are required'}), 400

    # if email_otp:
    #     pr = PasswordResetOTP.query.filter_by(
    #         email=email, otp=email_otp, purpose='signup'
    #     ).order_by(PasswordResetOTP.created_at.desc()).first()

    #     if not pr or is_expired(pr.expires_at):
    #         return jsonify({'success': False, 'message': 'Invalid or expired verification code'}), 400

    try:
        user = User(email=email, password_hash=hash_password(password))
        db.session.add(user)
        db.session.flush()

        profile = Profile(
            user_id=user.id,
            full_name=full_name,
            email=email,
            contact_number=contact_number,
            college_name=college_name,
            college_id=college_id,
            city=city,
            pincode=pincode,
            college_email=college_email,
            course_name=course_name,
            course_mode=course_mode,
            course_duration=course_duration
        )
        db.session.add(profile)
        db.session.commit()

        # if email_otp:
        #     db.session.delete(pr)
        #     db.session.commit()

        try:
            from ..utils import send_registration_confirmation_email
            send_registration_confirmation_email(email, full_name)
        except Exception:
            current_app.logger.exception('Failed to send registration confirmation email')

        return jsonify({'success': True, 'message': 'Signup successful'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Email already exists'}), 409
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Signup failed'}), 500

# ----------------------- LOGIN -----------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (username or email) or not password:
        return jsonify({'success': False, 'message': 'username/email and password required'}), 400

    user = None
    profile = None

    if email:
        user = User.query.filter_by(email=email).first()
        profile = user.profile if user else None
    else:
        profile = Profile.query.filter_by(username=username).first()
        user = db.session.get(User, profile.user_id) if profile else None

    if not user or not verify_password(user.password_hash, password):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    access = create_access_token(identity=user.id)
    refresh = create_refresh_token(identity=user.id)

    return jsonify({
        'success': True,
        'access_token': access,
        'refresh_token': refresh,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role or 'student'
        }
    })

# ----------------------- ME -----------------------
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = db.session.get(User, get_jwt_identity())
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    profile = user.profile
    return jsonify({'success': True, 'user': {
        'id': user.id,
        'email': user.email,
        'role': user.role,
        'profile': {
            'full_name': profile.full_name if profile else None,
            'email': profile.email if profile else None,
            'status': profile.status if profile else 'pending'
        }
    }})

# ----------------------- FORGOT PASSWORD -----------------------
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')

    if not email:
        return jsonify({'success': True})

    user = User.query.filter_by(email=email).first()
    if user:
        otp = f"{random.randint(0, 999999):06d}"
        expires = datetime.now(timezone.utc) + timedelta(minutes=15)

        pr = PasswordResetOTP(
            user_id=user.id,
            email=email,
            otp=otp,
            purpose='password',
            expires_at=expires
        )
        db.session.add(pr)
        db.session.commit()

        from ..email_utils import send_email
        send_email(email, 'Password Reset Code', f'Your reset code is: {otp}')

    return jsonify({'success': True})

# ----------------------- RESET PASSWORD -----------------------
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json() or {}
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('newPassword') or data.get('password')

    if not email or not otp or not new_password:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    pr = PasswordResetOTP.query.filter_by(
        email=email, otp=otp, purpose='password'
    ).order_by(PasswordResetOTP.created_at.desc()).first()

    if not pr or is_expired(pr.expires_at):
        return jsonify({'success': False, 'message': 'Invalid or expired code'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    user.password_hash = hash_password(new_password)
    db.session.delete(pr)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password reset successful'})
