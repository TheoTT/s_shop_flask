"""empty message

Revision ID: 3e2aba961298
Revises: 94a0a113a438
Create Date: 2020-03-28 14:06:58.696883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e2aba961298'
down_revision = '94a0a113a438'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PDMAN_DB_VERSION')
    op.drop_index('ix_submenus_auth_name', table_name='submenus')
    op.drop_table('submenus')
    op.add_column('menus', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.drop_index('ix_menus_created_at', table_name='menus')
    op.drop_index('ix_menus_updated_at', table_name='menus')
    op.create_foreign_key(None, 'menus', 'menus', ['parent_id'], ['id'])
    op.drop_column('menus', 'created_at')
    op.drop_column('menus', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('updated_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    op.add_column('menus', sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    op.drop_constraint(None, 'menus', type_='foreignkey')
    op.create_index('ix_menus_updated_at', 'menus', ['updated_at'], unique=False)
    op.create_index('ix_menus_created_at', 'menus', ['created_at'], unique=False)
    op.drop_column('menus', 'parent_id')
    op.create_table('submenus',
    sa.Column('auth_name', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32), nullable=False),
    sa.Column('path', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=256), nullable=False),
    sa.Column('level', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parent_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['menus.id'], name='submenus_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_submenus_auth_name', 'submenus', ['auth_name'], unique=False)
    op.create_table('PDMAN_DB_VERSION',
    sa.Column('DB_VERSION', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=256), nullable=True),
    sa.Column('VERSION_DESC', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=1024), nullable=True),
    sa.Column('CREATED_TIME', mysql.VARCHAR(collation='utf8mb4_unicode_ci', length=32), nullable=True),
    mysql_collate='utf8mb4_unicode_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###