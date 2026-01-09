#!/usr/bin/env python
import sys
print('Starting...')
sys.stdout.flush()

from db import db
from app import create_app
import sqlalchemy as sa

print('Creating app...')
sys.stdout.flush()
app = create_app()

print('In app context...')
sys.stdout.flush()
with app.app_context():
    print('Inspecting database...')
    sys.stdout.flush()
    inspector = sa.inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('profiles')]
    print(f'Current columns: {columns}')
    sys.stdout.flush()
    
    if 'college_address' not in columns:
        print('Adding college_address column...')
        sys.stdout.flush()
        with db.engine.connect() as conn:
            conn.execute(sa.text('ALTER TABLE profiles ADD COLUMN college_address VARCHAR(500) NULL'))
            conn.commit()
        print('✅ Column added successfully')
        sys.stdout.flush()
    else:
        print('✅ Column already exists')
        sys.stdout.flush()
