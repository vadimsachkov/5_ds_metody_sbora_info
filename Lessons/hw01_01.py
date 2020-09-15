# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import json
# pip install requests
import requests
import pprint

# имя пользователя
username='kubernetes'

git_link='https://api.github.com/users'
# получение перонального токена  https://github.com/settings/tokens
#с доступом только для чтения репозитариев : 1796be928bde072f660c07298ec9d51c7bd21a9

headers={'Accept': 'application/vnd.github.v3+json', 'Authorization' : 'token 1796be928bde072f660c07298ec9d51c7bd21a9e'}

# адрес всех репозитариев пользователя username (kubernetes) в виде
# https://api.github.com/users/kubernetes/repos
fulllink=git_link+'/'+username+'/repos'
# запрос на сайт
response = requests.get(fulllink, headers=headers)
#преобразовываем ответ в формат json
rjson=response.json()
# печатаем ответ в формате json
#pprint.pprint(rjson)
# сохраняем всю информацию в файле json.
with open(username + '_repos.json', 'w') as outfile:
    json.dump(rjson, outfile)

# вывод всех репозитариев пользоватeля username
for repo in rjson:
    if not repo['private']:
        print(repo['html_url'])