"""empty message

Revision ID: a8ef3c5b1cf0
Revises: 121adc6b6880
Create Date: 2020-04-12 17:01:49.359989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8ef3c5b1cf0'
down_revision = '121adc6b6880'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attributes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attribute_name', sa.String(length=32), nullable=False),
    sa.Column('attribute_sel', sa.Enum('only', 'many'), nullable=False),
    sa.Column('attribute_write', sa.Enum('manual', 'list'), nullable=False),
    sa.Column('attribute_values', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.Date(), nullable=True),
    sa.Column('updated_at', sa.Date(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attributes_attribute_name'), 'attributes', ['attribute_name'], unique=False)
    op.create_index(op.f('ix_attributes_attribute_values'), 'attributes', ['attribute_values'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_attributes_attribute_values'), table_name='attributes')
    op.drop_index(op.f('ix_attributes_attribute_name'), table_name='attributes')
    op.drop_table('attributes')
    # ### end Alembic commands ###