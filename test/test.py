from src.storage.models import User
from src.storage.impl_sqlalchemy import UserConnect
user_login = 'test1'
user_id = 9999
name = 'yuuri1'
user_url = 'http://localhost'
# create_at = '2019-07-10T08:22:20Z'
import datetime
create_at = datetime.datetime.now()
print(create_at, type(create_at))

data = {
    'user_login': user_login,
    'user_id': user_id,
    'user_url': user_url,
    'name': name,
    'create_at': create_at
}

user = UserConnect()
result = user.add_user_info(data)
print(result)
