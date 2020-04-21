from src.httprequest.request import USER, TOKEN
from src.storage.impl_sqlalchemy import ProjectConnect
import subprocess
import re
import time
import json
auth_list = list(zip(USER, TOKEN))
url = 'https://api.github.com/repos/twbs/bootstrap'
cmd_temple = 'curl -s -u "{}:{}" -I {}'


def get_remain_token():
    for i in auth_list:

        cmd = cmd_temple.format(i[0], i[1], url)
        ret = subprocess.Popen(cmd,stdout=subprocess.PIPE)
        result = str(ret.stdout.read())
        re_value = re.findall(r'(?<=X-RateLimit-Remaining: ).*?(?=X-RateLimit-Reset)|(?<=X-RateLimit-Reset: ).*?(?=Cache-Control:)',result)
        re_value = [i.replace('\\r\\n', '') for i in re_value]
        reset_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(re_value[1])))
        print('{} {} {} '.format(i[0],re_value[0],reset_time))


def get_project_start_count():
    project_name = ProjectConnect().select_project_name()
    project_name.sort(key=str.lower)
    print(len(project_name))
    print(project_name)
    _api = 'https://api.github.com/repos/{}'
    _command = 'curl -s -X GET -H "Content-Type:application/json" -u ' \
               '"justtestazx:3f2daaea57b6915b8a7e7946a289d1b1620eab5b" {}'
    for project in project_name:
        project_api = _api.format(project)
        # print(project_api)
        com = _command.format(project_api)
        ret = subprocess.Popen(com, stdout=subprocess.PIPE)
        result = ret.stdout.read().decode()
        result_dict = json.loads(result)
        star = result_dict.get('stargazers_count')
        print(f'{project},{star}')






get_remain_token()
# get_project_start_count()
