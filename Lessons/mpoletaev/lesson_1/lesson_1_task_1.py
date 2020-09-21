import requests
import json


headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.83 Safari/537.36',
    'Authorization': 'token 55bee1f6ce36e4f8a18b44255ba1b02e8c5a6df2'
}

print('\n======= Домашняя работа 1 - задание 1 =======')
print('=============================================\n')

user_type = ''
while not user_type:
    user_type = input('Выберите тип пользователя ("u" - частное лицо / "o" - организация): ').lower()
    if user_type == 'u':
        user_type = 'users'
    elif user_type == 'o':
        user_type = 'orgs'
    else:
        user_type = ''

owner_name = ''
while not owner_name:
    owner_name = input('Введите название профиля на github.com: ')

response = requests.get(f'https://api.github.com/{user_type}/{owner_name}/repos', headers=headers)

if response.ok:
    json_data = json.loads(response.text)

    json_data_len = len(json_data)
    if json_data_len:
        print('\nКол-во публичных репозиториев: ', json_data_len)

        print('Список публичных репозиториев: ')
        for i in range(len(json_data)):
            print(f'\t\t\t\t\t\t\t\t{i+1}.', json_data[i]['name'])

        file_name = f'task_1_{user_type}_{owner_name}.json'
        with open(file_name, 'w') as f:
            f.write(response.text)
        print(f'\n\tПодробная информация записана в файл "{file_name}"')
    else:
        print('\nУ данного пользователя нет публичных репозиториев!')
else:
    print(f'\n\tОшибка выполнения запроса! ({response.status_code})')
