import random

test_list1 = ['a', 'b', 'c', 'd', 'e']
test_list2 = [1, 2, 3, 4, 5]
test_list = list(zip(test_list1, test_list2))
count_dict = {}


def set_auth_dict():
    for i in test_list:
        count_dict.update({i: 0})


def count_auth():
    if len(test_list) == 0:
        print('no available token!')
        return
    ret = random.randint(0, len(test_list)-1)
    s = test_list[ret]
    num = count_dict.get(s)
    count_dict.update({s: num+1})

    if num == 4999:
        print('-'*3, '删除token前', '-'*3, test_list)
        del(test_list[ret])
        print('-'*3, '删除token后', '-'*3, test_list)
    return s


set_auth_dict()
print(count_dict)

for i in range(9896):
    s = count_auth()
    if not s:
        print(i)
        break
print(count_dict)

for i in range(23000):
    s = count_auth()
    if not s:
        print(i)
        break
print(count_dict)

