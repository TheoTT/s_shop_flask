"""empty message

Revision ID: 85f90e9c2bbc
Revises: 400d51820ea2
Create Date: 2020-03-30 10:42:05.546122

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '85f90e9c2bbc'
down_revision = '400d51820ea2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('association',
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], )
    )
    op.drop_constraint('menus_ibfk_2', 'menus', type_='foreignkey')
    op.drop_column('menus', 'role_id')
    op.alter_column('roles', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('roles', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_index('ix_roles_created_at', table_name='roles')
    op.drop_index('ix_roles_updated_at', table_name='roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_roles_updated_at', 'roles', ['updated_at'], unique=False)
    op.create_index('ix_roles_created_at', 'roles', ['created_at'], unique=False)
    op.alter_column('roles', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('roles', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.add_column('menus', sa.Column('role_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('menus_ibfk_2', 'menus', 'roles', ['role_id'], ['id'])
    op.drop_table('association')
    # ### end Alembic commands ###
