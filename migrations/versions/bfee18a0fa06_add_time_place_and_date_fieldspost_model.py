"""Add time, place, and date fieldsPost model

Revision ID: bfee18a0fa06
Revises: 5dccbdab3c01
Create Date: 2023-10-26 14:03:05.576354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfee18a0fa06'
down_revision = '5dccbdab3c01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('place', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('date', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('date')
        batch_op.drop_column('place')
        batch_op.drop_column('time')

    # ### end Alembic commands ###
