"""add reddit-related tables

Revision ID: c8d06153172a
Revises: 15ff55751894
Create Date: 2022-11-30 00:29:48.861365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8d06153172a'
down_revision = '15ff55751894'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('redditpost',
    sa.Column('id', sa.String(length=256), nullable=False),
    sa.Column('location', sa.String(length=256), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('op_text', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_redditpost_id'), 'redditpost', ['id'], unique=False)
    op.create_table('redditcomment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.String(length=256), nullable=True),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.Column('top_comment', sa.String(length=1000), nullable=False),
    sa.Column('comment_tree', sa.String(length=1000), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['redditpost.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_redditcomment_id'), 'redditcomment', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_redditcomment_id'), table_name='redditcomment')
    op.drop_table('redditcomment')
    op.drop_index(op.f('ix_redditpost_id'), table_name='redditpost')
    op.drop_table('redditpost')
    # ### end Alembic commands ###