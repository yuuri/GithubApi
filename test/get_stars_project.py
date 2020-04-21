import json
with open('1.json','rb') as f:
    content = f.read().decode('utf-8')

content = json.loads(content)
project_full_name = []
item = content['items']
for i in item:
    full_name = i['full_name']
    project_full_name.append(full_name)

for i in project_full_name:
    print(i)
