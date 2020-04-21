"""add_label_info

Revision ID: 75d5a839bc0d
Revises: f3a382076205
Create Date: 2020-01-17 11:20:29.113604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75d5a839bc0d'
down_revision = 'f3a382076205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('labels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('label_name', sa.VARCHAR(length=256), nullable=True),
    sa.Column('pull_number', sa.Integer(), nullable=False),
    sa.Column('project', sa.VARCHAR(length=100), nullable=True),
    sa.Column('color', sa.VARCHAR(length=100), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('labels')
    # ### end Alembic commands ###
