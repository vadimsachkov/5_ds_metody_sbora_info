# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

# Список публичных API
# https://github.com/public-apis/public-apis
# выберем из вышеуказанного списка API у котороой авторизация по APIKEY


# например https://linguarobot.docs.apiary.io/#introduction/authentication
# Чтобы получить ключ нужно зарегистрироваться на https://rapidapi.com/

# Authentication
# To use the API you need to retrieve an API Key that is used to authenticate requests.
# We use RapidAPI as a platform for access management.
# Please register at Rapid API (or log in if you already have an account)
# and subscribe to the API on the following page (https://rapidapi.com/rokish/api/lingua-robot/pricing)
# to get your API key.
# The API key has to be specified in X-RapidAPI-Key header in every request:
# сгенерироан  тестовый ключ :

import json
# pip install requests
import requests
import pprint

url = "https://lingua-robot.p.rapidapi.com/language/v1/entries/en/example"

headers = {
    'x-rapidapi-host': "lingua-robot.p.rapidapi.com",
    'x-rapidapi-key': "ebfa3b1012msha6bfcba1ccfc601p12b858jsne75ca25ad4d7"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

# к сожалению требуют кредитную карту даже за бесплатный аккаунт. обойдутся

# пробуем https://dictionaryapi.com/
# зарегиитрировался на сайте https://dictionaryapi.com
# и получил ключи
# Key (Elementary Dictionary):
# 8c36ebe9-2ff1-4adc-97c4-6e34e35c19ba
# Key (School Dictionary):
# 32cb8926-62a5-4737-b442-09b5c9f766b5

# Request URL
# https://www.dictionaryapi.com/api/v3/references/sd2/json/school?key=your-api-key

# будем например  использовать  https://dictionaryapi.com/products/api-elementary-dictionary

url = "https://www.dictionaryapi.com/api/v3/references/sd2/json/"
key = '8c36ebe9-2ff1-4adc-97c4-6e34e35c19ba'

myword = 'python'
fulllink = url + myword + '?key=' + key

# запрос на сайт
response = requests.get(fulllink)
# преобразовываем ответ в формат json
rjson = response.json()

pprint.pprint(rjson)

# получили жедаемый ответ
# преобразуем полученный json в объект python
# изучаем полученные данные
# тип данных
print(f'type = {type(rjson)} , длина = {len(rjson)}')
# это список из одного элемента в котором словарь. Интересует элемент 'shortdef' (кстати он тоже список)
print (rjson[0]['shortdef'][0])

# отлично мы получили описание что такое python
# это a large nonpoisonous snake of Africa, Asia, and Australia that squeezes and suffocates its prey

