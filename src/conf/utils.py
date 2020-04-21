import configparser
from src.common.log import LogAdapter
LOG = LogAdapter().set_log(__name__)


def write_conf():
    cf = configparser.ConfigParser()
    cf.add_section('project')
    cf.set('project', 'project_owner', 'twbs')
    cf.set('project', 'project_name', 'bootstrap')
    with open('project.conf', 'w') as f:
        cf.write(f)


def read_conf():
    try:
        cf = configparser.ConfigParser()
        cf.read('project.conf')
        project_owner = cf.get('project', 'project_owner')
        project_name = cf.get('project', 'project_name')
        return project_owner, project_name
    except Exception as e:
        print('Read Conf Failed! Cause {}'.format(e))
        LOG.error('Read Conf Failed! Cause {}'.format(e), exc_info=True)
        


