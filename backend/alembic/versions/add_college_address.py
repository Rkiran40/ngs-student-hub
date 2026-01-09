"""Add college_address column to profiles table

Revision ID: add_college_address
Revises: ec93d8981a8e_initial_migration
Create Date: 2025-01-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_college_address'
down_revision = 'ec93d8981a8e_initial_migration'
branch_labels = None
depends_on = None


def upgrade():
    # Add college_address column to profiles table
    op.add_column('profiles', sa.Column('college_address', sa.String(500), nullable=True))


def downgrade():
    # Remove college_address column from profiles table
    op.drop_column('profiles', 'college_address')
