"""empty message

Revision ID: a8e8753c9f48
Revises: 3219d735a84f
Create Date: 2020-03-23 15:21:58.407312

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a8e8753c9f48'
down_revision = '3219d735a84f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('submenus',
    sa.Column('auth_name', sa.String(length=32), nullable=False),
    sa.Column('path', sa.String(length=256), nullable=False),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submenus_auth_name'), 'submenus', ['auth_name'], unique=False)
    op.drop_constraint('menus_ibfk_1', 'menus', type_='foreignkey')
    op.drop_column('menus', 'parent_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('parent_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('menus_ibfk_1', 'menus', 'menus', ['parent_id'], ['id'])
    op.drop_index(op.f('ix_submenus_auth_name'), table_name='submenus')
    op.drop_table('submenus')
    # ### end Alembic commands ###