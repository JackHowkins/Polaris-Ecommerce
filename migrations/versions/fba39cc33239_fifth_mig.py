"""fifth mig

Revision ID: fba39cc33239
Revises: a64debb2b7ec
Create Date: 2020-12-20 02:11:52.973444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba39cc33239'
down_revision = 'a64debb2b7ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('soldhistory', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'soldhistory')
    # ### end Alembic commands ###
