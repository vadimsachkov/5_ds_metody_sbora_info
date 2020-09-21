import requests
import json


print('\n======= Домашняя работа 1 - задание 2 =======')
print('=============================================\n')

user_id = 0
while not user_id:
    try:
        user_id = int(input('Введите id пользователя: '))
    except ValueError:
        print('\t\t\tОшибка: введите натуральное число!')
    else:
        if user_id < 1:
            print('\t\t\tОшибка: введите целое положительное число!')
            user_id = 0

response = requests.get('https://api.vk.com/method/groups.get?'
                        f'user_id={user_id}&'
                        'extended=1&'
                        'v=5.61&'
                        'access_token=644987b239a8d99359202a0c7e2e2561542d61d5bf0eaaea2c3f9894dcff3bec56cc8452b03b04ac55831')

if response.ok:
    json_data = json.loads(response.text)

    try:
        groups_count = json_data['response']['count']
    except KeyError:
        print(f'\n\tПользователь с id {user_id} не существует!')
    else:
        if groups_count:
            print('\nКол-во сообществ: ', groups_count)

            print('Список сообществ: ')
            for i in range(groups_count):
                print(f'\t\t\t\t\t\t\t\t{i+1}.', json_data['response']['items'][i]['name'])

            file_name = f'task_2_{user_id}.json'
            with open(file_name, 'w') as f:
                f.write(response.text)
            print(f'\n\tПодробная информация записана в файл "{file_name}"')
        else:
            print('\nПользователь не подписан ни на одно сообщество!')
else:
    print(f'\n\tОшибка выполнения запроса! ({response.status_code})')
