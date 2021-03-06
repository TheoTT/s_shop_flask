"""empty message

Revision ID: 0943c82ae270
Revises: 4b713bab619c
Create Date: 2020-04-14 14:59:27.100482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0943c82ae270'
down_revision = '4b713bab619c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goods', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('goods', sa.Column('good_desc', sa.String(length=200), nullable=True))
    op.add_column('goods', sa.Column('good_weight', sa.Float(), nullable=False))
    op.add_column('goods', sa.Column('hot_number', sa.Integer(), nullable=False))
    op.add_column('goods', sa.Column('is_promote', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'goods', 'categories', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'goods', type_='foreignkey')
    op.drop_column('goods', 'is_promote')
    op.drop_column('goods', 'hot_number')
    op.drop_column('goods', 'good_weight')
    op.drop_column('goods', 'good_desc')
    op.drop_column('goods', 'category_id')
    # ### end Alembic commands ###
