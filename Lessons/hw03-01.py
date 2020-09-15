# добавить в переменную PATH  путь до bin mongo
# C:\Program Files\MongoDB\Server\4.4\bin
# создать папку c:/data/db


'''1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
функцию, записывающую собранные вакансии в созданную БД.'''

# pip install pymongo
# Все базы данных MongoDB создает по умолчанию в каталоге C:\data\db\.
#Сервер запускается и привязывается к адресу localhost (127.0.0.1) на порту 27017
# добавить в Path C:\Program Files\MongoDB\Server\4.4\bin
# запустить службу net start mongodb
from pymongo import MongoClient
import json
from pprint import pprint

# читаем записанные ранее данные вакансий в файле  vacancies.json
data = json.load(open("vacancies.json"))
#print(data)

# приведем переменные   salary_min и salary_max к float (вдруг они в строковые)
for vac in (data['hh'] +  data['superjob']):
    try:
        vac['salary_min']=float(vac['salary_min'])
    except:
        vac['salary_min']=None
    try:
        vac['salary_max']=float(vac['salary_max'])
    except:
        vac['salary_max']=None



client = MongoClient( 'localhost' , 27017 )
db = client[ 'vacancies_db' ]

# создаем коллекцию  db.vacancies
vacancies = db.vacancies

# очищаем  коллекцию пока тестируем
vacancies.drop()
# добавляем вакансии из hh
#vacancies.insert_many(data['hh'])
# добавляем вакансии из superjob
#vacancies.insert_many(data['superjob'])

'''
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с
сайта.'''

# добавляем из файла только новвые вакансии
# для определения уникальности используем url  вакансии

# вариант добавления через insert_one
def add_vacancy(curvacancy, col):
    #col.replaceOne({'link': curvacancy['link']}, curvacancy, {'upsert': True})
    if not col.count_documents({'link': curvacancy['link']}):
        # таких вакансий нет- добавляем
        col.insert_one(curvacancy)

# вариант добавления через replace_one
def add_vacancy1(curvacancy, col):
    try:
        col.replace_one({'link': curvacancy['link']}, curvacancy, upsert=True)
    except ValueError:
        print(ValueError)




# добавляем новые вакансии
for vacancy in data['hh']+data['superjob']:
    add_vacancy1(vacancy, vacancies)


print(vacancies.count())



'''
Написать функцию, которая производит поиск и выводит на экран вакансии с заработной
платой больше введённой суммы.
'''

#  отбираем вакансии где ЗП явно больше введенной суммы
# если ЗП на сайте не указана - значит не выводим
def print_vacancy(vacancies):
    mysalary = input('Введите желаемую минимальную ЗП : ')
    # если ввели не число  -значит ничего не выводим (ЗП ноль)
    try:
        mysalary = float(mysalary)
    except:
        mysalary = 0
    for vacancy in vacancies.find({'$or':[{'salary_min':{'$gt':mysalary}}, {'salary_max':{'$lt':mysalary}}]}):
         pprint(vacancy)

print_vacancy(vacancies)