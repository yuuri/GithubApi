
GITHUB_API_HOST = 'https://api.github.com/'

PER_PAGE = 100

# GIT_URL = 'https://github.com/twbs/bootstrap'
# REPO_URL = 'https://api.github.com/repos/twbs/bootstrap'
# PULL_URL = 'https://api.github.com/repos/twbs/bootstrap/pulls'
# ALL_PULL_URL = 'https://api.github.com/repos/twbs/bootstrap/pulls?state=all'
# COMMIT_DETAIL_URL = 'https://api.github.com/repos/twbs/bootstrap/commits/{}'
# STARTED_REPO = 'https://api.github.com/search/repositories?q=language:{}&sort=stars'

USER_URL = 'https://api.github.com/users/{}'
CLOSE_PULL_URL = 'https://api.github.com/repos/{}/pulls?state=closed'
BY_PAGE_URL = 'https://api.github.com/repos/{}/pulls?state=closed&page={}&per_page={}'
COMMIT_BY_PAGE_URL = 'https://api.github.com/repos/{}/commits?page={}&per_page={}'
FILE_CHANGE_URL = 'https://api.github.com/repos/{}/pulls/{}/files'
COMMIT_URL = 'https://api.github.com/repos/{}/pulls/{}/commits'
COMMENT_URL = 'https://api.github.com/repos/{}/issues/{}/comments'
PROJECT_URL = 'https://api.github.com/repos/{}'
STAR_URL = 'https://api.github.com/search/repositories?q=stars:>1000&per_page=20'
REVIEWER_URL = 'https://api.github.com/repos/{}/pulls/{}/reviews'
PULL_URL = 'https://api.github.com/repos/{}/pulls/{}'
# 获取token剩余次数 curl 命令
# curl -u "name:token" -I 'https://api.github.com/repos/twbs/bootstrap'
# example：
# curl -u "nnlp:d9986d8ee6e886a3bd35a70fbacda71e404a8fb3" -I 'https://api.github.com/repos/twbs/bootstrap'
