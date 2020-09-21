# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from urllib.parse import urlparse
import re


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongobase = client.vacancy210920
#        self.mongobase.drop()

    def process_item(self, item, spider):
        salary = item['salary']

        item['min_salary'],item['max_salary'],item['currency'] = self.process_salary(salary)
        item['site'] = self.process_site(item['link'])

        vacansy = dict(item)

        collection = self.mongobase[spider.name]
        collection.insert_one(vacansy)




        return item

    def process_salary(self,salary:list):
        # анализируем строку с описанием ЗП _ она ввиде сприска и представлена может быть в виде:
        # ["з/п не указана"]
        # ["от ","100 000"," до ","130 000"," ","руб."," на руки"
        # ["от ","80 000"," до ","120 000"," ","руб."," до вычета налогов"]
        # ["до ","150 000"," ","руб."," до вычета налогов"]
        # ["от ","50 000"," ","руб."," на руки"]
        # []

        salary0=[i.strip().replace(u'\xa0', '') for i in salary]
        # ищем "от "

        try:
            imin = salary0.index("от") if ("от" in salary0) else None   # позиция в листе минимума
            # #удаляем между разрядами чисел пробельный символ  , в частности  символ  \xa0 и превращаем в число
            min_salary= float(re.sub(r'(\d)\s*(\d)', r'\1\2', salary0[imin+1]))
        except:
            min_salary=None
        # ищем "до "
        try:
            imax = salary0.index("до") if ("до" in salary0) else None # позиция в листе макса
            #удаляем между разрядами чисел пробельный символ  , в частности  символ  \xa0 и превращаем в число
            max_salary= float(re.sub(r'(\d)\s*(\d)', r'\1\2', salary0[imax+1]))
        except:
            max_salary=None

        # ищем валюту (она либо после суммы imax либо если ее нет до после суммы imin), причем там послу суммы есть еще один пустой элемент
        try:
            icur= imax if max_salary else (imin if min_salary else None)  # позиция в листе валюты
            cur_salary= salary0[icur+3] if icur is not None else None

        except:
            cur_salary=None

        return min_salary,max_salary,cur_salary

    # возвращает имя домена из ссылки вакансии
    def process_site(self,link):
        parsed_uri = urlparse(link)
        #result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri
        # возвращаем домен источника из ссылки



        return parsed_uri.netloc