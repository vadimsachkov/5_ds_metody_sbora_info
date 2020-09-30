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
        print (f"Всего подписок {len(user_data['subscriptions'])}")
        for subs_id in user_data['subscriptions']:
            # выводим список id пользоватлей подписок
            #print (subs_id)
            pass

        # выводим подписчиков
        user_id=user_data['user_id']
        users_doc = col.find({"subscriptions": user_id})
        print(f'Всего подписчиков {col.count_documents({"subscriptions": user_id})}')
        for subs_id in users_doc:
            # выводим список id пользоватлей подписок
           #print (subs_id['user_id'])
            pass
    else:
        print(f'Пользоватли с логином {username} не найдены')





