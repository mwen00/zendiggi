"""add location table

Revision ID: 15ff55751894
Revises: 
Create Date: 2022-11-29 21:45:10.281686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15ff55751894'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=256), nullable=False),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('update_date', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_location_id'), 'location', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_location_id'), table_name='location')
    op.drop_table('location')
    # ### end Alembic commands ###