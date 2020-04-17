"""empty message

Revision ID: 63b206a18211
Revises: 0943c82ae270
Create Date: 2020-04-15 23:38:18.628710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63b206a18211'
down_revision = '0943c82ae270'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('photo_name', sa.String(length=500), nullable=False),
    sa.Column('photo_url', sa.String(length=500), nullable=False),
    sa.Column('good_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['good_id'], ['goods.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_photos_photo_name'), 'photos', ['photo_name'], unique=False)
    op.create_index(op.f('ix_photos_photo_url'), 'photos', ['photo_url'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_photos_photo_url'), table_name='photos')
    op.drop_index(op.f('ix_photos_photo_name'), table_name='photos')
    op.drop_table('photos')
    # ### end Alembic commands ###