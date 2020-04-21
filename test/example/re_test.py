import re
# text = '<https://api.github.com/repositories/2126244/pulls?state=all&%EF%BC%86page=2&per_page=10&Authorization%3Atoken+d78bb04f628e94654b337959e00b5eb43557635d=&page=987>'
#
#
# url_2 = 'https://api.github.com/repositories/2126244/pulls?state=all&page=9861&per_page=1&Authorization%3Atoken+d78bb04f628e94654b337959e00b5eb43557635d='
#
# # str = re.findall('(?<=page=)(.+?)>', text)
# content = re.findall('&page=(.\d+)',url_2)
#
# print(content)
#
#
# commit_link = '<https://api.github.com/repositories/2126244/commits?page=18744&per_page=1>'
# count = re.findall(r'\?page=(.\d+)',commit_link)
# print(count)

# link = '<https://api.github.com/repositories/194458534/pulls?state=all&page=2&per_page=1>; rel="next", <https://api.github.com/repositories/194458534/pulls?state=all&page=7&per_page=1>; rel="last"'
# text = re.findall('<.+?>', link)
# print(text)
# print(len(text))
# if len(text) == 2:
#     last_page_content = text[len(text) - 1]
# else:
#     last_page_content = text[len(text) - 2]
# print(last_page_content)
# page_text = re.findall('(?<=page=)(.+?)>', last_page_content)


# <https://api.github.com/repositories/136505169/pulls?state=all&page=1&per_page=1>; rel="prev", <https://api.github.com/repositories/136505169/pulls?state=all&page=3&per_page=1>; rel="next", <https://api.github.com/repositories/136505169/pulls?state=all&page=327&per_page=1>; rel="last", <https://api.github.com/repositories/136505169/pulls?state=all&page=1&per_page=1>; rel="first"

last_page_content = 'https://api.github.com/repositories/194458534/pulls?state=all&page=7&per_page=1'
count = re.findall(r'&page=(\d+)', last_page_content)
print(count)
