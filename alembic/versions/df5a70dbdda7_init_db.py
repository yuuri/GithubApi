"""'init_db'

Revision ID: df5a70dbdda7
Revises: 
Create Date: 2019-08-02 09:35:15.356040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df5a70dbdda7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pull_number', sa.Integer(), nullable=True),
    sa.Column('comment_user', sa.VARCHAR(length=100), nullable=True),
    sa.Column('comment_content', sa.TEXT(), nullable=True),
    sa.Column('comment_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('project', sa.VARCHAR(length=100), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('commits',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pull_number', sa.Integer(), nullable=True),
    sa.Column('commit_sha', sa.VARCHAR(length=100), nullable=True),
    sa.Column('commit_msg', sa.TEXT(), nullable=True),
    sa.Column('commit_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('user_email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('project', sa.VARCHAR(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('git_project',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('project_url', sa.VARCHAR(length=100), nullable=True),
    sa.Column('project_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('git_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_login', sa.VARCHAR(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=500), nullable=True),
    sa.Column('user_url', sa.VARCHAR(length=512), nullable=True),
    sa.Column('user_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('pull_request',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('number', sa.Integer(), nullable=True),
    sa.Column('title', sa.TEXT(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('user_login', sa.VARCHAR(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.VARCHAR(length=20), nullable=True),
    sa.Column('request_date', sa.TIMESTAMP(), nullable=False),
    sa.Column('project', sa.VARCHAR(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('request_file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pull_number', sa.Integer(), nullable=True),
    sa.Column('file_sha', sa.VARCHAR(length=512), nullable=True),
    sa.Column('file_name', sa.TEXT(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=10), nullable=True),
    sa.Column('project', sa.VARCHAR(length=100), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_file')
    op.drop_table('pull_request')
    op.drop_table('git_user')
    op.drop_table('git_project')
    op.drop_table('commits')
    op.drop_table('comments')
    # ### end Alembic commands ###
