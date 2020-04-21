import requests
import random
from src.conf.const import *
from requests.adapters import HTTPAdapter
from src.conf.token import USER,TOKEN
from src.common.log import LogAdapter
LOG = LogAdapter().set_log(__name__)

MAX_REQUESTS = 4999


class Request(object):
    def __init__(self):
        self.number = 0
        self.auth = list(zip(USER, TOKEN))
        # add retries way
        self.requ = requests.session()
        self.requ.mount('http://', HTTPAdapter(max_retries=3))
        self.requ.mount('https://', HTTPAdapter(max_retries=3))
 
    def requests(self, url):
        auth = self.get_auth()
        try:
            response = self.requ.get(url, auth=auth, timeout=(20, 70))
            if response.status_code == 200:
                self.number += 1
                # print('Get Content Successful!')
                return response.json()
            else:
                header = response.headers
                status_code = response.status_code
                response = response.json()
                print(status_code, auth, response, header,)
                LOG.error('response failed cause {},\n auth is {} response is {} \n header is {} \n'
                          .format(status_code, auth, response, header),exc_info=True)
        except Exception as e:
            print('Request Error Cause {}'.format(e))
            LOG.error('Request Error Cause {}'.format(e), exc_info=True)
    
    def response_header(self, url):
        auth = self.get_auth()
        try:
            response = self.requ.get(url, auth=auth)
            # print(response.text)
            header = response.headers
            status_code = response.status_code
            if status_code == 200:
                self.number += 1
                print('Get Header Successful')
                return header
            else:
                print('error status code is {}'.format(status_code), header)
                LOG.warning('error status code is {}'.format(status_code), header)
        except Exception as e:
            LOG.error('request header failed cause {} , auth is {} '.format(e, auth))
    
    def get_auth(self):
        # ret = self.number // MAX_REQUESTS
        # # get auth list length
        # limit = len(self.auth)
        # # if ret more than limit, let ret reset
        # if ret >= limit:
        #     ret = (ret // limit) - 1
        ret = random.randint(0, len(self.auth)-1)
        auth = self.auth[ret]
        return auth

