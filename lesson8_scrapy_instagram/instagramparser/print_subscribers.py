from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
mongo_base = client.instagram

col = mongo_base['instagram']

# ищем все подписки избранного пользователя с логином

username = input('Введите логин пользователя , чьи подписки и подписчики вас интересуют (для выхода ничего не вводите):  ')

if username:
    #ищем такого пользователя в базе
    if col.count_documents({"username":username}):
        # найден ищем его пидписки
        user_data=col.find_one({"username":username})

        for user_id in user_data['subscriptions']:
            # выводим список логинов пользоватлей подписок по его user_id
            try:
                if col.count_documents({"user_id":user_id}):
                    # раскомментировать чтобы вывести все подписки
                    #print (col.find_one({"user_id":user_id})['username'])
                    pass
                else:
                    print(f"Не найден {user_id}")
            except:
                print(f"Ошибка {user_id}")

        print (f"Всего подписок {len(user_data['subscriptions'])}")

        # выводим подписчиков
        user_id=user_data['user_id']
        # находим всех пользоватлей у кого в подписках стоит наш пользователь
        users_doc = col.find({"subscriptions": user_id})
        for subs in users_doc:

           pass
           # выводим список id пользоватлей подписок
           # раскомментировать чтобы вывести все подписчиков
           #print (subs['username'])

        print(f'Всего подписчиков {col.count_documents({"subscriptions": user_id})}')

    else:
        print(f'Пользоватли с логином {username} не найдены')





