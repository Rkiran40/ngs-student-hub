#!/usr/bin/env python3
"""
Setup script to create admin user with SQLite fallback.
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

# Force SQLite fallback
os.environ['DEV_SQLITE_FALLBACK'] = '1'
os.environ['FLASK_ENV'] = 'development'
# Override the database URI to use the existing SQLite database
os.environ['DATABASE_URL'] = 'sqlite:///./backend/studenthub.db'

from backend.app import create_app
from backend.db import db
from backend.models import User, Profile
from backend.utils import hash_password

def main():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created.")

        # Check if admin user exists
        existing = User.query.filter_by(email='admin@nuhvin.com').first()
        if existing:
            print(f"Admin user already exists: {existing.email}")
            if existing.role != 'admin':
                existing.role = 'admin'
                print("Promoted to admin.")
            # Update password
            existing.password_hash = hash_password('123456')
            if existing.profile:
                existing.profile.username = 'admin'
                existing.profile.status = 'active'
            else:
                p = Profile(user_id=existing.id, username='admin', full_name='Admin', email='admin@nuhvin.com', status='active')
                db.session.add(p)
            db.session.commit()
            print("Admin user updated.")
        else:
            # Create new admin user
            u = User(email='admin@nuhvin.com', password_hash=hash_password('123456'), role='admin')
            db.session.add(u)
            db.session.commit()
            p = Profile(user_id=u.id, username='admin', full_name='Admin', email='admin@nuhvin.com', status='active')
            db.session.add(p)
            db.session.commit()
            print("Admin user created: admin@nuhvin.com / 123456")

if __name__ == '__main__':
    main()
