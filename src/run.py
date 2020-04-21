from src.process import data_process
from src.common.log import LogAdapter
from src.conf.setting import PROJECT

LOG = LogAdapter().set_log(__name__)
start = '======== Process Start ========'
end = '======== Process Done ========'

if __name__ == '__main__':
    print(start)
    LOG.info(start)
    
    # main process
    projects = PROJECT.split(';')
    for project in projects:
        data_process.main(project)
    
    print(end)
    LOG.info(end)
