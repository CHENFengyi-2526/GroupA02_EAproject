"""merge multiple heads

Revision ID: 457093f030d4
Revises: 21d4e918516e, cb723cc226d7
Create Date: 2026-04-28 04:29:03.386816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '457093f030d4'
down_revision = ('21d4e918516e', 'cb723cc226d7')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
