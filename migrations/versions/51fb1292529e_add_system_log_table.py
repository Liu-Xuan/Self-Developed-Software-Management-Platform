"""Add system log table

Revision ID: 51fb1292529e
Revises: 32f40100e8ac
Create Date: 2025-02-10 23:55:29.678693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51fb1292529e'
down_revision = '32f40100e8ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('system_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('operator', sa.String(length=50), nullable=True),
    sa.Column('operation_time', sa.DateTime(), nullable=True),
    sa.Column('ip_address', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('system_log')
    # ### end Alembic commands ###
