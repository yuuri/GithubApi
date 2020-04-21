from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from src.conf.setting import STORAGE_URL
import datetime

# 1.create engine
engine = create_engine(STORAGE_URL)

# 2.create mapping object
base = declarative_base()


# 3.define table info
class Project(base):
    __tablename__ = "git_project"
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    project_name = Column(VARCHAR(100), nullable=True)
    project_id = Column(Integer, nullable=True)
    project_url = Column(VARCHAR(100), nullable=True)
    project_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow(), nullable=False)
    
    
class User(base):
    __tablename__ = "git_user"
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    user_login = Column(VARCHAR(100),nullable=True)
    user_id = Column(Integer, nullable=True)
    name = Column(VARCHAR(500), nullable=True)
    user_url = Column(VARCHAR(512), nullable=True)
    user_date = Column(TIMESTAMP, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class PullDetail(base):
    __tablename__ = "pull_request"
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    number = Column(Integer, nullable=True)
    title = Column(TEXT, nullable=True)
    description = Column(TEXT, nullable=True)
    user_login = Column(VARCHAR(100), nullable=True)
    user_id = Column(Integer, nullable=True)
    # user_email = Column(VARCHAR(100), nullable=True)
    state = Column(VARCHAR(20),nullable=True)
    request_date = Column(TIMESTAMP, nullable=False)
    # page = Column(Integer,nullable=True)
    project = Column(VARCHAR(100),nullable=True)
    merged = Column(BOOLEAN, default=False,nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=True)


class Commits(base):
    __tablename__ = 'commits'
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    pull_number = Column(Integer, nullable=True)
    commit_sha = Column(VARCHAR(100),nullable=True)
    commit_msg = Column(TEXT, nullable=True)
    commit_date = Column(TIMESTAMP, nullable=True)
    user_email = Column(VARCHAR(100), nullable=True)
    project = Column(VARCHAR(100),nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)


class Comments(base):
    __tablename__ = 'comments'
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pull_number = Column(Integer, nullable=True)
    comment_user = Column(VARCHAR(100), nullable=True)
    comment_content = Column(TEXT, nullable=True)
    comment_date = Column(TIMESTAMP, nullable=True)
    project = Column(VARCHAR(100), nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow(), nullable=False)


class Reviews(base):
    __tablename__="reviews"
    __table_args__ = (
        {
            'mysql_charset':'utf8mb4',
            'mysql_engine':'InnoDB'
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pull_number = Column(Integer, nullable=False)
    project = Column(VARCHAR(100))
    reviewer = Column(VARCHAR(100), nullable=False)
    review_description = Column(TEXT, nullable=True)
    review_date = Column(TIMESTAMP)
    create_at = Column(TIMESTAMP, default=datetime.datetime.utcnow(), nullable=True)


class CommitFile(base):
    __tablename__ = "request_file"
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    pull_number = Column(Integer, nullable=True)
    file_sha = Column(VARCHAR(512), nullable=True)
    file_name = Column(TEXT, nullable=True)
    status = Column(VARCHAR(10), nullable=True)
    project = Column(VARCHAR(100), nullable=True)
    additions = Column(BIGINT,nullable=True)
    deletions = Column(BIGINT,nullable=True)
    changes = Column(BIGINT,nullable=True)
    # patch = Column(TEXT, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow(), nullable=False)


class Labels(base):
    __tablename__ = "labels"
    __table_args__ = (
        {
            'mysql_charset': "utf8mb4",
            'mysql_engine': "InnoDB"
        }
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    label_name = Column(VARCHAR(256))
    pull_number = Column(Integer, nullable=False)
    project = Column(VARCHAR(100), nullable=True)
    color = Column(VARCHAR(100), nullable=True)
    description = Column(TEXT, nullable=True)

# 4.create table
# base.metadata.create_all(engine)
