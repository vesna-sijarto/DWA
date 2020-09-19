"""empty message

Revision ID: 26363f7c4cfc
Revises: 3a4f78721891
Create Date: 2020-08-15 02:46:48.013068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26363f7c4cfc'
down_revision = '3a4f78721891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')

    op.drop_table('user')
    # ### end Alembic commands ###