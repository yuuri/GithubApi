from sqlalchemy.orm import sessionmaker
from src.storage.models import *

from src.common.log import LogAdapter
LOG = LogAdapter().set_log(__name__)

engine = create_engine(STORAGE_URL)
session_class = sessionmaker(bind=engine)


class UserConnect(object):
    def __init__(self):
        self.session = session_class()
        
    def add_user_info(self, data):
        try:
            user = User()
            for k, v in data.items():
                setattr(user, k, v)
            result = self.session.merge(user)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add User Info Error ,Cause {}'.format(e))
            LOG.error('Add User Info Error ,Cause {}'.format(e))
        finally:
            self.session.close()
    
    def select_user_info(self):
        result = self.session.query(User.user_login).all()
        result_list = []
        for i in result:
            result_list.append(i[0])
        return result_list


class PullRequestConnect(object):
    def __init__(self):
        self.session = session_class()
        
    def add_pull_info(self, data):
        try:
            pull = PullDetail()
            for k, v in data.items():
                setattr(pull, k, v)
            result = self.session.add(pull)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Pull Info Error ,Cause {}'.format(e))
            LOG.error('Add Pull Info Error ,Cause {}'.format(e))
        finally:
            self.session.close()
    
    def select_all_pull_number(self,project):
        try:
            result = self.session.query(distinct(PullDetail.number)).\
                filter(PullDetail.project == project).all()
            self.session.close()
            return result
        except Exception as e:
            print('Select Pull Number Failed, Cause {}'.format(e))
            LOG.error('Select Pull Number Failed, Cause {}'.format(e),exc_info=True)
    
    def select_pull_user(self,project):
        try:
            # distinct 去重查询
            result = self.session.query(distinct(PullDetail.user_login)).\
                filter(PullDetail.project == project).all()
            self.session.commit()
            self.session.close()
            return result
        except Exception as e:
            print('Select Request User info Failed,Cause {}'.format(e))
            LOG.error('Select Request User Info Failed,Cause {}'.format(e), exc_info=True)


class CommentConnect(object):
    def __init__(self):
        self.session = session_class()
    
    def add_comment_info(self, data):
        try:
            comment = Comments()
            for k, v in data.items():
                setattr(comment, k, v)
            result = self.session.merge(comment)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Comment Error , Cause {}'.format(e))
            LOG.error('Add Comment Error , Cause {}'.format(e))
        finally:
            self.session.close()
    
    def select_comment_user(self,project):
        try:
            result = self.session.query(distinct(Comments.comment_user)).\
                filter(Comments.project == project).all()
            self.session.close()
            return result
        except Exception as e:
            print('Select Comment User Info Failed,Cause {}'.format(e))
            LOG.error('Select Comment User Info Failed,Cause {}'.format(e),exc_info=True)


class CommitConnect(object):
    def __init__(self):
        self.session = session_class()
    
    def add_commit_info(self, data):
        try:
            commit = Commits()
            for k, v in data.items():
                setattr(commit, k, v)
            result = self.session.merge(commit)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Commit Info Error ,Cause {}'.format(e))
            LOG.error('Add Commit Info Error ,Cause {}'.format(e))
        finally:
            self.session.close()


class CommitFileConnect(object):
    def __init__(self):
        self.session = session_class()
    
    def add_commit_file_info(self, data):
        try:
            commit_file = CommitFile()
            for k, v in data.items():
                setattr(commit_file, k, v)
            result = self.session.merge(commit_file)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Commit File Info Error, Cause {}'.format(e))
            LOG.error('Add Commit File Info Error, Cause {}'.format(e))
        finally:
            self.session.close()


class ProjectConnect(object):
    def __init__(self):
        self.session = session_class()
    
    def add_project_info(self, data):
        try:
            project = Project()
            for k, v in data.items():
                setattr(project, k, v)
            result = self.session.merge(project)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Project Info Error ,Cause {}'.format(e))
            LOG.error('Add Project Info Error ,Cause {}'.format(e))
        finally:
            self.session.close()

    def select_project_name(self):
        try:
            result_list = []
            result = self.session.query(Project.project_name).all()
            self.session.close()
            for i in result:
                project_name = i[0]
                result_list.append(project_name)
            return result_list
        except Exception as e:
            print('Select Project Name Failed,Cause {}'.format(e))
            LOG.error('Select Project Name Failed,Cause {}'.format(e),exc_info=True)


class ReviewConnect(object):
    def __init__(self):
        self.session = session_class()

    def add_review_info(self, data):
        try:
            review = Reviews()
            for k, v in data.items():
                setattr(review, k, v)
            result = self.session.merge(review)
            self.session.commit()
            self.session.close()
            # return result
        except Exception as e:
            print('Add Review Error , Cause {}'.format(e))
            LOG.error('Add Review Error , Cause {}'.format(e))
        finally:
            self.session.close()


class LabelConnect(object):
    def __init__(self):
        self.session = session_class()

    def add_label_info(self, data):
        try:
            data_object = []
            for i in data:
                label = Labels()
                for k, v in i.items():
                    setattr(label, k, v)
                data_object.append(label)
            self.session.bulk_save_objects(data_object)
            self.session.commit()
            self.session.close()
        except Exception as e:
            print('Add Label Info Failed Cause {}'.format(e))
            LOG.error('Add Label Info Failed Cause {}'.format(e))
        finally:
            self.session.close()
