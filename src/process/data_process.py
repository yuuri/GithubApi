import time
import math
import re
from src.conf.const import *
from src.httprequest.request import Request
from src.storage.impl_sqlalchemy import *
from multiprocessing import Pool

from src.common.log import LogAdapter
LOG = LogAdapter().set_log(__name__)


user_conn = UserConnect()
pull_conn = PullRequestConnect()
comment_conn = CommentConnect()
commit_conn = CommitConnect()
project_conn = ProjectConnect()
commit_file_conn = CommitFileConnect()
review_conn = ReviewConnect()
label_conn = LabelConnect()


def convert_time(date_str):
    time_convert = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%fZ')
    return time_convert


class DataProcess(object):
    def __init__(self, project):
        self.request = Request()
        self.project = project
    
    def get_project_info(self):
        try:
            print('==== Project is {} ===='.format(self.project))
            LOG.info('==== Project is {} ==== '.format(self.project))
            url = PROJECT_URL.format(self.project)
            content = self.request.requests(url)
            if not content:
                print('can not get project info')
                LOG.error('can not get project info')
                return
            project_id = content.get('id', 0)
            project_url = content.get('url', '')
            project_date = content.get('created_at')
            
            project_data = {
                'project_name': self.project,
                'project_id': project_id,
                'project_date': convert_time(project_date),
                'project_url': project_url
            }
            project_conn.add_project_info(project_data)
        except Exception as e:
            LOG.error('Get Project Info Failed, Cause {}'.format(e))
        
    def get_pull_by_page(self):
        try:
            # get total pull count
            total_count = self.get_total_count()
            total_page = math.ceil(total_count / PER_PAGE)
            print('Pull Request count is {}, total page is {}'.format(total_count, total_page))
            LOG.info('Pull Request count is {}, total page is {}'.format(total_count, total_page))
            
            # get pull request info
            pool = Pool(processes=20)
            # for i in range(total_page):
            pool.map_async(self.get_pull_info, range(total_page))
            pool.close()
            pool.join()
        except Exception as e:
            LOG.error('Get Pull Request by Page Failed , Cause {}'.format(e))

    def get_pull_info(self, page):
        # get pull request by page
        page = page+1
        try:
            url = BY_PAGE_URL.format(self.project, page, PER_PAGE)
            content = self.request.requests(url)
            if not content:
                print('can not get content page is {}'.format(page))
                LOG.warning('can not get content page is {}'.format(page))
                return
            print('Now Page is {}'.format(page))
    
            for item in content:
                # page_dict = {}
                title = item.get('title')
                pull_number = item.get('number')
                state = item.get('state')
                description = item.get('body')
                user_name = item.get('user').get('login')
                user_id = item.get('user').get('id')
                # user_url = item.get('user').get('url')
                # commit_url = item.get('commits_url')
                # comment_url = item.get('comments_url')
                # pull_url = item.get('url')
                created_at = item.get('created_at','')
                merge_status = item.get('merged_at')
                # get labels
                labels = item.get('labels')
                label_list = []
                for label in labels:
                    label_name = label.get('name', '')
                    color = label.get('color', '')
                    description = label.get('description', '')
                    if not label_name:
                        continue
                    label_list.append({
                        'label_name':label_name,
                        'color':color,
                        'description':description
                    })

                label_conn.add_label_info(label_list)

                merged = False
                if merge_status:
                    merged = True

                print('Get Pull Request Number is {}'.format(pull_number))
                
                mysql_data = {
                    'number': int(pull_number),
                    'title': title,
                    'description': description,
                    'user_login': user_name,
                    'user_id': user_id,
                    'state': state,
                    'request_date': convert_time(created_at),
                    'project': self.project,
                    'merged':merged
                }
                pull_conn.add_pull_info(mysql_data)
        except Exception as e:
            LOG.error('Get Pull Request Number Failed, Cause {},Page is {}'.format(e,page))
            
    def get_commit_info(self,pull_number):
        # get commit info by pull number
        try:
            commit_url = COMMIT_URL.format(self.project, pull_number)
            commits = self.request.requests(commit_url)
            # print(self.request.number)
            if not commits:
                print('commits not exist! Pull Request Number is {}'.format(pull_number))
                # LOG.warning('commits not exist! Pull Request Number is {}'.format(pull_number))
                return
            print('get commit info Pull Request Number is {}'.format(pull_number))
            commit_list = []
            for commit in commits:
                commit_dict = {}
                commit_sha = commit.get('sha')
                if not commit_sha:
                    continue
                commit_user = commit.get('commit').get('author').get('name')
                commit_email = commit.get('commit').get('author').get('email')
                commit_date = commit.get('commit').get('author').get('date')
                commit_msg = commit.get('commit').get('message')
                
                # insert to database
                commit_data = {
                    'pull_number': pull_number,
                    'commit_sha': commit_sha,
                    'commit_user': commit_user,
                    'user_email': commit_email,
                    'commit_date': convert_time(commit_date),
                    'commit_msg': commit_msg,
                    'project': self.project
                    
                }
                commit_conn.add_commit_info(commit_data)
        except Exception as e:
            LOG.error('Get Commit Info Failed Pull Request Number is {},Cause {}.'.format(pull_number,e))
            
    def get_comment_msg(self,pull_number):
        # get comment msg by pull number
        try:
            url = COMMENT_URL.format(self.project,pull_number)
            comments = self.request.requests(url)
            if not comments:
                print('comment is empty Pull Request Number is {}'.format(pull_number))
                # LOG.warning('comment is empty pull number is {}'.format(pull_number))
                return
            print('get comment info Pull Request Number is {} '.format(pull_number))
            for comment in comments:
                comment_user = comment.get('user').get('login')
                comment_id = comment.get('id')
                created_at = comment.get('created_at')
                comment_content = comment.get('body','')
                
                comment_data = {
                    'pull_number': pull_number,
                    'comment_user': comment_user,
                    'comment_content': comment_content,
                    'comment_date': convert_time(created_at),
                    'project': self.project
    
                }
                comment_conn.add_comment_info(comment_data)
        except Exception as e:
            LOG.error(f'Get Comment info Failed ,pull number is {pull_number},Cause {e}',exc_info=True)

    def get_review_info(self,pull_number):
        try:
            url = REVIEWER_URL.format(self.project, pull_number)
            reviews = self.request.requests(url)
            if not reviews:
                print('reviewer info is empty pull number is {}'.format(pull_number))
            print('get reviewer info pull number is {}'.format(pull_number))
            for review in reviews:
                try:
                    reviewer = review.get('user', '').get('login', '')
                    review_date = review.get('submitted_at')
                    review_content = review.get('body', '')
                    review_data = {
                        'pull_number': pull_number,
                        'reviewer': reviewer,
                        'review_description': review_content,
                        'review_date': convert_time(review_date),
                        'project': self.project
                    }
                    review_conn.add_review_info(review_data)
                except Exception as e:
                    LOG.error(f'Get review info Failed ,Cause {e} review info is {review}',exc_info=True)
        except Exception as e:
            LOG.error(f'Get Reviews info Failed ,pull number is {pull_number},Cause {e}', exc_info=True)

    def get_pull_file(self, pull_number):
        # get pull file by pull number
        try:
            url = FILE_CHANGE_URL.format(self.project,pull_number)
            file_changes = self.request.requests(url)
            if not file_changes:
                print('pull files is empty,Pull Request Number is {}'.format(pull_number))
                return
            print('get files info, Pull Request Number is {}'.format(pull_number))
            file_change_list = []
            for item in file_changes:
                change_dict = {}
                sha = item.get('sha')
                if not sha:
                    continue
                file_name = item.get('filename','')
                status = item.get('status','')
                additions = item.get('additions',0)
                deletions = item.get('deletions',0)
                change = item.get('changes','')
                # patch = item.get('patch','')
                
                file_data = {
                    'pull_number': pull_number,
                    'file_sha': sha,
                    'file_name': file_name,
                    'status': status,
                    'additions': additions,
                    'deletions': deletions,
                    'changes':change,
                    # 'patch':patch,
                    'project': self.project,
                    
                }
                commit_file_conn.add_commit_file_info(file_data)
        except Exception as e:
            LOG.error('Get File Info Failed , Cause {}'.format(e))
    
    def get_total_count(self):
        """
        this way is by get response header's link
        and use regex to get all count.
        all count number in link's mark as <'last'> url
        :return:
        """
        try:
            page = 1
            per_page = 1
            url = BY_PAGE_URL.format(self.project, page, per_page)
            # content = self.requests(url)
            header = self.request.response_header(url)
            print(header)
            if not header:
                return 0
            # use regex to get total pull count
            link = header.get('Link')
            link_text = re.findall('<.+?>', link)
            last_page_content = link_text[len(link_text) - 1]
            # page_text = re.findall('(?<=page=)(.+?)>', last_page_content)
            count = re.findall(r'&page=(\d+)', last_page_content)[0]
            # print('Total Pull Request is {}'.format(count))
        except Exception as e:
            LOG.error('Get total Pull Request Number Failed ,Cause {}'.format(e), exc_info=True)
            count = 0
        return int(count)
      
    def get_total_commit_count(self):
        page = 2
        per_page = 1
        url = COMMIT_BY_PAGE_URL.format(self.project, page, per_page)
        # content = self.requets(url)
        header = self.request.response_header(url)
        print(header)
        if not header:
            return 0
        # use regex to get total pull count
        link = header.get('Link')
        text = re.findall('<.+?>', link)
        last_page_content = text[1]
        # page_text = re.findall('(?<=page=)(.+?)>', last_page_content)
        count = re.findall(r'\?page=(\d+)', last_page_content) [0]
        print('Total commit is {}'.format(count))
        return int(count)
    
    def get_all_pull_number(self):
        try:
            number_list = []
            id_obj = pull_conn.select_all_pull_number(self.project)
            for id_tuple in id_obj:
                number_list.append(id_tuple[0])
            request_count = len(number_list)
            
            print('=== Pull Request Count is {} ==='.format(request_count))
            LOG.info('=== Pull Request Count is {} ==='.format(request_count))
        except Exception as e:
            number_list = []
            LOG.error('Get all Pull Request Number failed , cause {}'.format(e),exc_info=True)
        return number_list

    def get_label_info(self,pull_number):
        try:
            url = PULL_URL.format(self.project, pull_number)
            labels = self.request.requests(url).get('labels','')
            if not labels:
                print('label info is empty pull number is {}'.format(pull_number))
            print('get label info pull number is {}'.format(pull_number))
            try:
                label_list = []
                for label in labels:
                    label_name = label.get('name', '')
                    color = label.get('color', '')
                    description = label.get('description', '')
                    if not label_name:
                        continue
                    label_list.append({
                        'label_name':label_name,
                        'color':color,
                        'description':description,
                        'pull_number':pull_number,
                        'project':self.project
                    })

                label_conn.add_label_info(label_list)
            except Exception as e:
                LOG.error(f'Get review info Failed ,Cause {e} review info is {labels}',exc_info=True)
        except Exception as e:
            LOG.error(f'Get Reviews info Failed ,pull number is {pull_number},Cause {e}', exc_info=True)

    def commit_comment_file(self, pull_number):
        self.get_commit_info(pull_number)
        self.get_comment_msg(pull_number)
        self.get_pull_file(pull_number)
        self.get_review_info(pull_number)
        # self.get_label_info(pull_number)

    def select_user_info(self):
        user_list = []
        pull_users = pull_conn.select_pull_user(self.project)
        comment_users = comment_conn.select_comment_user(self.project)
        for pull_user in pull_users:
            user_list.append(pull_user[0])
        for comment_user in comment_users:
            user_list.append(comment_user[0])
        #  distinct comment user and pull request user
        distinct_list = list({}.fromkeys(user_list).keys())
        # if project user info in the user table,will not get info by http request
        old_user = user_conn.select_user_info()
        for user in old_user:
            if user in distinct_list:
                distinct_list.remove(user)
        user_count = len(distinct_list)
        print('=== User Count is {} ==='.format(user_count))
        LOG.info('=== User Count is {} ==='.format(user_count))
        
        pool = Pool(processes=20)
        pool.map_async(self.get_user_info, distinct_list)
        pool.close()
        pool.join()
    
    def get_user_info(self, login):
        try:
            url = USER_URL.format(login)
            message = self.request.requests(url)
            print('get user info user is {}'.format(login))
            user_login = message.get('login')
            name = message.get('name')
            user_id = message.get('id')
            user_url = message.get('url')
            user_date = message.get('created_at')
            
            data = {
                'user_login': user_login,
                'name': name,
                'user_id': user_id,
                'user_url': user_url,
                'user_date': convert_time(user_date)
            }
            user_conn.add_user_info(data)
        except Exception as e:
            LOG.error('Get User Info Failed , Cause {}'.format(e))


            
        
def main(project):
    start_time = time.time()
    run = DataProcess(project)
    pool = Pool(processes=20)
    # 0. if project is already in database
    # and project update option is True ,process will not run
    project_list = project_conn.select_project_name()
    if project in project_list:
        LOG.warning('Project already in databases, project name is {}'.format(project))
        print('This Project already in databases! project name is {}'.format(project))
        return
    # 1.get project info
    run.get_project_info()
    # 2.get pull request
    run.get_pull_by_page()
    pull_list = run.get_all_pull_number()
    # print(pull_list)
    # 3.get commit comment pull_file
    # for i in pull_list:
    pool.map_async(run.commit_comment_file, pull_list)
    pool.close()
    pool.join()
    # 4.get user info
    # run.select_user_info()
    
    end_time = time.time()
    spend_time = end_time - start_time
    print('Spend Time is {} s'.format(spend_time))
    LOG.info('spend time is {} s'.format(spend_time))


# if __name__ == '__main__':
#     main()
